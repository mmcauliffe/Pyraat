
from subprocess import Popen, PIPE, call
import os

from praatinterface.scripts import praatscripts

class PraatLoader:
    def __init__(self, **kwargs):
        praatpath = kwargs.pop('praatpath', None)

        self.debug = kwargs.pop('debug',False)
        self.scripts = praatscripts
        self.scripts.update(kwargs)
        if praatpath:
            self.script_dir = os.path.join(os.path.dirname(praatpath),'praatScripts')
            self.praat = praatpath
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
            if not s.lower().endswith('.praat'):
                s += '.praat'
            if os.path.isfile(os.path.join(self.script_dir,s)):
                os.remove(os.path.join(self.script_dir,s))
        os.rmdir(self.script_dir)
        self.init_scripts()

    def init_scripts(self):
        if not os.path.isdir(self.script_dir):
            os.mkdir(self.script_dir)
        for s in self.scripts:
            sfilename = s
            if not sfilename.lower().endswith('.praat'):
                sfilename += '.praat'
            if os.path.isfile(os.path.join(self.script_dir, sfilename)):
                continue
            with open(os.path.join(self.script_dir, sfilename),'w') as f:
                f.write(self.scripts[s])

    def initlog(self):
        with open(os.path.join(self.script_dir,'log.txt'),'w') as f:
            f.write("begin")

    def updatelog(self,line):
        with open(os.path.join(self.script_dir,'log.txt'),'a') as f:
            f.write(line+"\n")

    def extract_token(self,filename,begin,end,outname):
        out = self.run_script('extract.praat',[filename, begin, end, outname])

    def spectro_pic(self,filename,formantCheck,nformants,ceiling,boundaries):
        numbounds = boundaries.count(',')
        out = self.run_script('spectroPic.praat',[filename, formantCheck,
                                                nformants, ceiling,
                                                numbounds, boundaries])

    def waveform_pic(self,filename, boundaries):
        numbounds = boundaries.count(',')
        out = self.run_script('waveformPic.praat',[filename, numbounds, boundaries])

    def run_script(self, name,*args):
        if self.debug:
            self.updatelog('%s' % name)
        if not name.lower().endswith('.praat'):
            name += '.praat'
        com = [self.praat]
        if self.praat.endswith('con.exe'):
            com += ['-a']
        com +=[os.path.join(self.script_dir,name)] + list(map(str,args))
        if self.debug:
            self.updatelog('%s' % str(com))
        p = Popen(com,stdout = PIPE,stderr = PIPE,stdin = PIPE)
        stdout, stderr = p.communicate()
        if self.debug:
            self.updatelog('stdout: %s' % str(stdout))
            self.updatelog('stderr: %s' % str(stderr))
        return stdout.decode().strip()

    #def convert_MP3(self, filename):
    #    com = 'lame --preset insane %s' % filename
    #    call(com,shell=True)

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
                    v = line[j]
                    if v != '--undefined--':
                        try:
                            v = float(v)
                        except ValueError:
                            print(text)
                            print(head)
                    else:
                        v = 0
                    values[head[j]] = v
                if values:
                    output[float(time)] = values
        return output


