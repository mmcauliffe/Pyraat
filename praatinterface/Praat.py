'''
Created on 2012-11-09

@author: michael
'''

import subprocess
import os

from praatinterface.scripts import praatscripts


class PraatLoader:
    def __init__(self,praatpath=None,debug=False,additional_scripts = {}):
        self.debug=debug
        self.scripts = praatscripts
        self.scripts.update(additional_scripts)
        if praatpath:
            self.script_dir = os.path.join(os.path.dirname(praatpath),'praatScripts')
            self.praat = 'praat'
        else:
            self.script_dir = os.path.join(os.path.dirname(__file__),'praatScripts')
            self.praat = 'praat'
        self.init_scripts()
        if self.debug:
            self.initlog()
        self.window_size = 0.025
        self.preemphasis = 50

    def reinit_scripts(self):
        for s in self.scripts:
            if os.path.isfile(os.path.join(self.script_dir,s)):
                os.remove(os.path.join(self.script_dir,s))
        os.rmdir(self.script_dir)
        self.init_scripts()

    def init_scripts(self):
        if not os.path.isdir(self.script_dir):
            os.mkdir(self.script_dir)
        for s in self.scripts:
            if os.path.isfile(os.path.join(self.script_dir,s)):
                continue
            with open(os.path.join(self.script_dir,s),'w') as f:
                f.write(self.scripts[s])

    def initlog(self):
        with open(os.path.join(self.script_dir,'log.txt'),'w') as f:
            f.write("begin")

    def updatelog(self,line):
        with open(os.path.join(self.script_dir,'log.txt'),'a') as f:
            f.write(line+"\n")

    def extract_token(self,filename,begin,end,outname):
        out = self.run_script('extract.praat',[filename,begin,end,outname])

    def spectro_pic(self,filename,formantCheck,nformants,ceiling,boundaries):
        numbounds = boundaries.count(',')
        out = self.run_script('spectroPic.praat',[filename,formantCheck,nformants,ceiling,numbounds,boundaries])

    def waveform_pic(self,filename,boundaries):
        numbounds = boundaries.count(',')
        out = self.run_script('waveformPic.praat',[filename,numbounds,boundaries])

    def run_script(self,name,*args):
        if self.debug:
            self.updatelog('%s' % name)
        com = [self.praat, os.path.join(self.script_dir,name)] + list(map(str,args))
        if self.debug:
            self.updatelog('%s' % str(com))
        p = subprocess.Popen(com,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if self.debug:
            self.updatelog('stdout: %s' % str(stdout))
            self.updatelog('stderr: %s' % str(stderr))
        return stdout


    def convert_MP3(self,filename):
        com = 'lame --preset insane %s' % filename
        subprocess.call(com,shell=True)


    def read_praat_out(self,text):
        if not text:
            return None
        lines = text.splitlines()
        head = lines.pop(0)
        head = head.split("\t")[1:]
        output = {}
        for l in lines:
            if '\t' in l:
                line = l.split("\t")
                time = line.pop(0)
                values = {}
                for j in range(len(line)):
                    if line[j] != '--undefined--':
                        v = float(line[j])
                        if head[j].startswith('B'):
                            v = math.log(v)
                        values[head[j]] = v
                if values:
                    output[float(time)] = values
        return output




if __name__ == '__main__':
    #p = PraatLoader(praatpath='/home/michael/dev/Linguistics/Media/PraatScripts/')
    #p.reinit_scripts()
    p = PraatLoader()
    print(p.script_dir)


