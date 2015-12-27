import sys
#from parsers import *
from nitrile.latex.latex import latex


import logging
log = logging.getLogger()
verbosity =2
ch = logging.StreamHandler(sys.stdout)
if verbosity==1:
    log.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)
elif verbosity==2:
    log.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
elif verbosity>=3:
    log.setLevel(logging.NOTSET)
    ch.setLevel(logging.NOTSET)
formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
ch.setFormatter(formatter)
logging.getLogger('nitrile').addHandler(ch)

errout = logging.StreamHandler(sys.stdout)
errout.setLevel(logging.WARN)
errout.setFormatter(logging.Formatter('%(message)s'))
logging.getLogger('errout').addHandler(errout)
                    

#r = RootParser('symbols.tex')
#r = RootParser('intro.tex')

#input = latex('intro.tex',{})
input = latex('symbols.tex',{})



#print r._Parser__tolkens


#r.GetNode().pprint()



