import os
import json
import shlex
import subprocess
import hashlib
from .mlclient import MLClient
from threading import Timer
import os, getpass
from fnmatch import fnmatch

Global={
    'current_client':None,
    'container_rules':[]
}

def lariLogin(lari_id,lari_passcode=None):
    if (lari_passcode is None) and (lari_id):
        print('Enter processing passcode for lari node {}'.format(lari_id))
        lari_passcode=getpass.getpass()
    else:
        lari_passcode=''
    os.environ['LARI_ID']=lari_id
    os.environ['LARI_PASSCODE']=lari_passcode

class _MLPipeline():
    def __init__(self):
        self._client=MLClient()
        pass
    def client(self):
        return self._client
    def __enter__(self):
        self._client.clearJobs()
        Global['current_client']=self._client
    def __exit__(self, type, value, traceback):
        self._client.run()
        Global['current_client']=None


def initPipeline():
    P=_MLPipeline()
    P.client().displayJobMonitor()
    return P

def containerRules():
    return Global['container_rules']

def setContainerRules(rules):
    Global['container_rules']=rules

def addContainerRule(*,pattern,container):
    Global['container_rules'].append(dict(pattern=pattern,container=container))

#def clearJobs():
#    Global['current_client'].clearJobs()

def _get_container_for_processor_name(processor_name):
    rules=Global['container_rules']
    for rule in rules:
        if fnmatch(processor_name,rule['pattern']):
            return rule['container']
    
def addProcess(processor_name, inputs=None, outputs=None, parameters=None, opts=None):
    if not opts:
        opts=dict()

    if 'container' not in opts:
        container=_get_container_for_processor_name(processor_name)
        if container:
            opts['container']=container
    return Global['current_client'].addProcess(processor_name,inputs,outputs,parameters,opts)
    #if not Global['current_client']:
    #    return Global['current_client'].addProcess(processor_name,inputs,outputs,parameters,opts)
    #else:
    #   P=initPipeline()
    #   with P:
    #       return addProcess(processor_name,inputs,outputs,parameters,opts)
    

def runPipeline():
    client=Global['current_client']
    client.run()

class _MLProcessorPIO: #parameter, input, or output
    def __init__(self,obj):
        self._obj=obj
    def name(self):
        return self._obj.get('name','')
    def description(self):
        return self._obj.get('description','')
    def isOptional(self):
        return self._obj.get('optional',False)
    def defaultValue(self):
        return self._obj.get('default_value','')

class _MLProcessor:
    def __init__(self,processor_name,package_uri=''):
        self._processor_name=processor_name
        self._package_uri=package_uri
        self._spec=None
        self._mlconfig=None
    def spec(self):

        if not self._spec:
            cmd='ml-spec {}'.format(self._processor_name)
            if self._package_uri:
                cmd='{} --package_uri={}'.format(cmd,self._package_uri)
            with os.popen(cmd) as pp:
                output=pp.read()
            #output=os.popen(cmd).read()
            try:
                obj=json.loads(output)
            except:
                print ('Unable to get spec for processor: {}'.format(self._processor_name))
                return None
            self._spec=obj
        return self._spec
    def name(self):
        return self._processor_name
    def packageUri(self):
        return self._package_uri
    def version(self):
        return self.spec().get('version','')
    def description(self):
        return self.spec().get('description','')
    def inputNames(self):
        inputs0=self.spec().get('inputs',[])
        ret=[]
        for input0 in inputs0:
            ret.append(input0['name'])
        return ret
    def input(self,name):
        inputs0=self.spec().get('inputs',[])
        for input0 in inputs0:
            if input0['name'] == name:
                return _MLProcessorPIO(input0)
        raise Exception('Input not found in spec: {}'.format(name))
    def outputNames(self):
        outputs0=self.spec().get('outputs',[])
        ret=[]
        for output0 in outputs0:
            ret.append(output0['name'])
        return ret
    def output(self,name):
        outputs0=self.spec().get('outputs',[])
        for output0 in outputs0:
            if output0['name'] == name:
                return _MLProcessorPIO(output0)
        raise Exception('Output not found in spec: {}'.format(name))
    def parameterNames(self):
        parameters0=self.spec().get('parameters',[])
        ret=[]
        for parameter0 in parameters0:
            ret.append(parameter0['name'])
        return ret
    def parameter(self,name):
        parameters0=self.spec().get('parameters',[])
        for parameter0 in parameters0:
            if parameter0['name'] == name:
                return _MLProcessorPIO(parameter0)
        raise Exception('Parameter not found in spec: {}'.format(name))

    def _print_color(self,col,txt):
        # terminal color codes
        ccc = {
            "Reset": "\x1b[0m",
            "Bright": "\x1b[1m",
            "Dim": "\x1b[2m",
            "Underscore": "\x1b[4m",
            "Blink": "\x1b[5m",
            "Reverse": "\x1b[7m",
            "Hidden": "\x1b[8m",
            "FgBlack": "\x1b[30m",
            "FgRed": "\x1b[31m",
            "FgGreen": "\x1b[32m",
            "FgYellow": "\x1b[33m",
            "FgBlue": "\x1b[34m",
            "FgMagenta": "\x1b[35m",
            "FgCyan": "\x1b[36m",
            "FgWhite": "\x1b[37m",
            "BgBlack": "\x1b[40m",
            "BgRed": "\x1b[41m",
            "BgGreen": "\x1b[42m",
            "BgYellow": "\x1b[43m",
            "BgBlue": "\x1b[44m",
            "BgMagenta": "\x1b[45m",
            "BgCyan": "\x1b[46m",
            "BgWhite": "\x1b[47m",
        };
        print (ccc[col]+txt+ccc['Reset'])

    def _run_command_and_print_output(self,command):
        with subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            while True:
                output_stdout= process.stdout.readline()
                output_stderr = process.stderr.readline()
                if (not output_stdout) and (not output_stderr) and (process.poll() is not None):
                    break
                if output_stdout:
                    self._print_color ('FgBlue',output_stdout.strip().decode())
                if output_stderr:
                    self._print_color ('FgRed',output_stderr.strip().decode())
            rc = process.poll()
            return rc

    def run(self,inputs,outputs,parameters,opts):
        inames=set(self.inputNames())
        for iname in inames:
            if not self.input(iname).isOptional():
                if not iname in inputs:
                    raise Exception('Missing input argument: {}'.format(iname))
        for iname in inputs:
            if not iname in inames:
                raise Exception('Unexpected input: {}'.format(iname))
        onames=set(self.outputNames())
        for oname in onames:
            if not self.output(oname).isOptional():
                if not oname in outputs:
                    raise Exception('Missing output argument: {}'.format(oname))
        for oname in outputs:
            if not oname in onames:
                raise Exception('Unexpected output: {}'.format(oname))
        pnames=set(self.parameterNames())
        for pname in pnames:
            if not self.parameter(pname).isOptional():
                if not pname in parameters:
                    raise Exception('Missing parameter argument: {}'.format(pname))
        for pname in parameters:
            if not pname in pnames:
                raise Exception('Unexpected parameter: {}'.format(pname))
        
        cmd='ml-run-process {}'.format(self.name())
        if self._package_uri:
            cmd='{} --package_uri={}'.format(cmd,self._package_uri)
        cmd=cmd+' --inputs'
        input_names=sorted(inputs.keys())
        for iname in input_names:
            val=inputs[iname]
            if isinstance(val,(list,tuple)):
                for val0 in val:
                    path0=self._get_path_for_input('',val0)
                    cmd=cmd+' {}:{}'.format(iname,path0)
            else:
                path0=self._get_path_for_input(iname,val)
                cmd=cmd+' {}:{}'.format(iname,path0)
        cmd=cmd+' --parameters'
        parameter_names=sorted(parameters.keys())
        for pname in parameter_names:
            val=parameters[pname]
            cmd=cmd+' {}:{}'.format(pname,val)
        process_signature=self._get_signature_from_cmd(cmd)

        cmd=cmd+' --outputs'
        output_paths={}
        output_names=sorted(outputs.keys())
        for oname in output_names:
            val=outputs[oname]
            path0=self._create_path_for_output(oname,val,process_signature)
            output_paths[oname]=path0
            cmd=cmd+' {}:{}'.format(oname,path0)
        opt_names=sorted(opts.keys())
        for optname in opt_names:
            val=opts[optname]
            if val is True:
                cmd=cmd+' --{}'.format(optname)
            elif val is False:
                cmd=cmd+''
            else:
                cmd=cmd+' --{}={}'.format(optname,val)
        if opts.get('verbose','') == 'jupyter':
            from IPython.core.display import display, HTML
            display(HTML('<span class=ml_job processor_name="{}">JOB({})</span>'.format(self.name,self.name)));
        else:
            print ('RUNNING: '+cmd)
        #process = Popen(shlex.split(cmd), stdout=PIPE)
        #process.communicate()
        #exit_code = process.wait()
        exit_code = self._run_command_and_print_output(cmd)
        if exit_code != 0:
            raise Exception('Non-zero exit code for {}'.format(self.name()))
        ret={}
        for oname in output_names:
            ret[oname]=output_paths[oname]
        return ret

    def _get_mlconfig(self):
        if not self._mlconfig:
            with os.popen('ml-config --format json') as pp:
                txt=pp.read()
                self._mlconfig=json.loads(txt)
        return self._mlconfig

    def _get_temp_path(self):
        return self._get_mlconfig()['temporary_directory']

    def _get_path_for_input(self,iname,val):
        if (type(val)==str):
            return val
        return locateFile(val)

    def _get_signature_from_cmd(self,cmd):
        return hashlib.sha1(cmd.encode()).hexdigest()

    def _create_path_for_output(self,oname,val,signature):
        if (type(val)==str):
            return val
        temporary_path=self._get_temp_path()
        if not os.path.exists(temporary_path+'/mountainlab'):
            os.makedirs(temporary_path+'/mountainlab')
        if not os.path.exists(temporary_path+'/mountainlab/tmp_short_term'):
            os.makedirs(temporary_path+'/mountainlab/tmp_short_term')
        return temporary_path+'/mountainlab/tmp_short_term/output_'+oname+'_'+signature+'.prv'

def execProcess(processor_name,inputs={},outputs={},parameters={},opts={}):
    opts['mode']='exec'
    return runProcess(processor_name,inputs,outputs,parameters,opts)

def queueProcess(processor_name,inputs={},outputs={},parameters={},opts={}):
    opts['mode']='queue'
    return runProcess(processor_name,inputs,outputs,parameters,opts)
    
def runProcess(processor_name,inputs={},outputs={},parameters={},opts={}):
    P=_MLProcessor(processor_name)
    if not P.spec():
        raise Exception('Unable to find processor:::: {}'.format(processor_name))
    return P.run(inputs,outputs,parameters,opts)

def spec(processor_name,package_uri='',**kwargs):
    P=_MLProcessor(processor_name,package_uri=package_uri)
    return P.spec()

def locateFile(X,download=False,remote_only=False):
    if type(X)==str:
        if os.path.exists(X):
            if not X.endswith('.prv'):
                return X
        opts=''
        if download:
            opts=opts+'--download '
        if remote_only:
            opts=opts+'--remote_only '
        cmd='ml-prv-locate {} {}'.format(X,opts)
        with os.popen(cmd) as pp:
            path=pp.read().strip()
        if not path:
            raise Exception('Unable to locate file: {}'.format(X))
        return path
    else:
        raise Exception('Unexpected type in locateFile.')

def readDir(path):
    with os.popen('ml-read-dir {}'.format(path)) as pp:
        txt=pp.read()
        return json.loads(txt)

def kbucketPath(path):
    if path.startswith('kbucket://'):
        return path
    if path.startswith('sha1://'):
        return path
    if path.endswith('.prv'):
        with open(path,'r') as f:
            obj=json.load(f)
            return 'sha1://'+obj['original_checksum']
    if (not os.path.exists(path)) and os.path.exists(path+'.prv'):
        return kbucketPath(path+'.prv')
    return None
        
def realizeFile(X):
    return locateFile(X,download=True)
