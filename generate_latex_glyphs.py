import os.path,time
import subprocess
from collections import deque
import base64

document = r"""\documentclass{article}
\pagestyle{empty}
\begin{document}
%s
\end{document}
"""
import package_defs
import latex2e
package = latex2e.latex2e()


class latex_queue:

    def __init__(self,size):
        self.size = size
        self.queue = deque([])
        self.running = {}
        self.completed = {}

    
    def add_item(self,key,doc,jobname):
        filename = self.encode(jobname)+".tex"
        assert not os.path.isfile(filename)

        with open(filename,'w') as f:
            f.write(doc)
        self.queue.append((key,doc,jobname))

    @staticmethod
    def encode(jobname):
        return jobname.replace('%','percent').replace('|','pipe')+'_'+base64.b64encode(jobname)

    def start_jobs(self):
        c = 0
        for key,proc in self.running.items():
            proc.poll()
            
            if proc.returncode is not None:
                c+=1
                self.completed[key] = proc.returncode
                del self.running[key]
                
        
        r=0
        while len(self.running)<self.size and self.queue:
            r +=1
            key,doc,jobname = self.queue.popleft()
            filename = self.encode(jobname)
            
            proc = subprocess.Popen(['pdflatex',
                                     #'-jobname='+jobname,
                                     '-interaction=batchmode',
                                     '-halt-on-error',
                                     filename,
            ],
                                    stdin=subprocess.PIPE,
                                    stdout=FNULL,
                                    stderr=FNULL,
            )
            proc.stdin.write(doc)
            self.running[key] = proc

        print "Queued {} Running {} Completed {} just completed {} just started {}".format(len(self.queue),len(self.running),len(self.completed),c,r)
            
    def wait(self):
        while len(self.queue) or len(self.running):
            self.start_jobs()
            if len(self.running)<10:
                print self.running
            time.sleep(.1)

print package.__class__.__name__

FNULL = open(os.devnull,'w')
os.chdir('glyphs')
os.chdir('latex2e')
mode = 'text'
procs=[]
queue = latex_queue(200)

groups = [
    "all",
    "text",
    "math",
    ]

for mode in ['text','math']:
    for cmd_group in groups:
        cmds = getattr(package,cmd_group+"_commands")
        for cmd,info in cmds.iteritems():
            if not isinstance(info,package_defs.symbol):
                continue
            #if cmd not in ["l","L"]:
            #    continue

            expected = None
            if mode =='text':
                d = document%('\\'+cmd)
                if cmd_group in ['all','text']:
                    expected = 0
                elif cmd_group in ['math']:
                    expected = 1
            elif mode =='math':
                d = document%('$\\'+cmd+'$')
                if cmd_group in ['all','math']:
                    expected = 0
                elif cmd_group in ['text']:
                    expected = 1
            else:
                assert False
        
            jobname = mode+"_"+cmd

            assert expected in [True,False]
            #print mode,cmd_group, cmd,expected

            key = (mode,cmd_group,cmd,expected)
            queue.add_item(key,d,jobname)
            #queue.start_jobs()


queue.wait()
for key,ret in queue.completed.iteritems():
    if key[3]!=ret:
        print key,ret
    if key[3]==0:
        filename = queue.encode(key[0]+"_"+key[2])+'.pdf'
        if not os.path.isfile(filename):
            print "Missing file: {}".format(filename)
        
