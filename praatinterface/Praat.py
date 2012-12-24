'''
Created on 2012-11-09

@author: michael
'''

import subprocess
import os

from .scripts import praatscripts


class PraatLoader:
    def __init__(self,praatpath):
		self.scripts = praatscripts
        self.script_dir = os.path.join(os.path.dirname(praatpath),'praatScripts')
        self.praat = praatpath
        self.init_scripts()
        
    def init_scripts(self):
		for s in self.scripts:
			if os.path.isfile(os.path.join(self.script_dir,s)):
				continue
			with open(os.path.join(self.script_dir,s),'w') as f:
				f.write(self.scripts[s])

    def get_formants(self,filename,begin,end,nformants,ceiling):
        output = self.runScript("formants-all.praat",[filename,begin,end,nformants,ceiling])
        output = self.read_praat_out(output)
        return output

    def extract_token(self,filename,begin,end,outname):
        out = self.runScript('extract.praat',[filename,begin,end,outname])
    
    def spectro_pic(self,filename,formantCheck,nformants,ceiling,boundaries):
        numbounds = boundaries.count(',')
        out = self.runScript('spectroPic.praat',[filename,formantCheck,nformants,ceiling,numbounds,boundaries])
    
    def waveform_pic(self,filename,boundaries):
        numbounds = boundaries.count(',')
        out = self.runScript('waveformPic.praat',[filename,numbounds,boundaries])
        
    def run_script(self,name,args):
        com = [self.praat, os.path.join(self.script_dir,name)] + map(str,args)
        p = subprocess.Popen(com,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return stdout
        
    
    def convert_MP3(self,filename):
        com = 'lame --preset insane %s' % filename
        subprocess.call(com,shell=True)
    
    def read_praat_out(self,text):
        output = []
        lines = text.splitlines()
        head = lines.pop(0).split("\t")
        for l in lines:
            if '\t' in l:
                line = l.split("\t")
                newline = {}
                for j in range(len(line)):
                    newline[head[j]] = line[j]
                output.append(newline)
        return output
    
if __name__ == '__main__':
    p = PraatLoader('/home/michael/dev/LingToolsWebsite/Media/PraatScripts/',"/home/michael/dev/LingToolsWebsite/Media/Tools/praat")
    #out = p.getFormants('/home/michael/dev/LingToolsWebsite/Media/Temp/Buckeye-41.wav', 0.0, 0.1, 5, 5000)
    #print out
    #for x in out:
    #    print x
    #fones = [x['F1(Hz)'] for x in out if x['F1(Hz)'] != '--undefined--']
    #ftwos = [x['F2(Hz)'] for x in out if x['F2(Hz)'] != '--undefined--']
    #print fones
    
                
