#import ParseLatex
import string
from nitrile.latex.latex2e.latex2e import latex2e
from nitrile.latex.latex2e.package_defs import Symbol


whitespace = string.whitespace+u'\xa0'+u"\N{THIN SPACE}"+ u"\N{soft hyphen}"

f=open("symbols.tex",'w')
f.write(r"\documentclass{article}"+"\n"+
        r"\begin{document}"+"\n" +
        r"\setlength{\columnsep}{1.5in}\twocolumn"+ "\n"+
        r"\setlength\parindent{0pt}"+"\n"
        )

chars = [ chr(i) for i in range(32,128)]

#print chars

verb = '+'

package = latex2e()

#codes = sorted({ k for c in dir(package) if c.endswith("_codes") for  k in getattr(package,c).keys()})
codes = [chr(c) for c in range(256)]

n = 0
for code in codes:
    text_code = package.text_codes.get(code,package.verb_codes.get(code,None))





    text_n = 1

    text_code = package.text_codes.get(code,package.verb_codes.get(code,None))
    if text_code is None:
        text_code = code
    if isinstance(text_code,basestring):
        if text_code in whitespace:
            text_n=0
        else:
            text_code = text_code
    elif isinstance(text_code,type) and text_code.__name__=="Symbol":
        text_code = text_code.c
    elif isinstance(text_code,type) and text_code.__name__ == "MultiParser__":
        text_n=len(text_code.values)
        text_code = code
    else:
        text_n =0
        text_code = " "

    math_n = 1
    math_code = package.math_codes.get(code,package.text_codes.get(code,package.verb_codes.get(code,None)))
    if math_code is None:
        math_code = code
    if isinstance(math_code,basestring):
        if math_code in whitespace:
            math_n=0
        else:
            math_code = math_code
    elif isinstance(math_code,type) and math_code.__name__=="Symbol":
        math_code = math_code.c
    elif isinstance(math_code,type) and math_code.__name__ == "MultiParser__":
        math_n= len(math_code.values)
        math_code = code
    else:
        math_n=0
        math_code = " "

    if code == verb:
        v = chr(ord(verb)+1)
    else:
        v = verb

    #if text_code not in whitespace or math_code not in whitespace:

    for i in range(1,max(text_n,math_n)+1):
        print repr(code),repr(i*code),repr(text_code),repr(math_code),i,text_n,math_n
        s = i*code+"\\hfill$" + i*code +"$\\hfill\\verb"+v+i*code+v
            #print c,d,repr(s)
        f.write(s+'\n\n')


    if math_n or text_n:
        n+=1
        if n >5:
            break



f.write('\pagebreak\n\n')


cmds = sorted({ k for c in dir(package) if c.endswith("_cmds") for  k in getattr(package,c).keys()})

n = 0

for cmd in cmds:
    text_info = package.all_cmds.get(cmd,package.text_cmds.get(cmd,None))

    if isinstance(text_info,basestring):
        text_cmd = cmd
    elif isinstance(text_info,type) and text_info.__name__=="Symbol" and text_info.c not in whitespace:
        print repr(text_info.c)
        text_cmd = cmd
    elif isinstance(text_info,type) and text_info.__name__ == "MultiParser__":
        text_cmd = cmd
    else:
        text_cmd = " "
    math_info = package.all_cmds.get(cmd,package.math_cmds.get(cmd,None))
    if isinstance(math_info,basestring):
        math_cmd = cmd
    elif isinstance(math_info,type) and math_info.__name__=="Symbol" and math_info.c not in whitespace:
        math_cmd = cmd
    elif isinstance(math_info,type) and math_info.__name__ == "MultiParser__":
        math_cmd = cmd
    else:
        math_cmd = " "

    if verb in cmd:
        v = chr(ord(verb)+1)
    else:
        v = verb

    if text_cmd not in whitespace or math_cmd not in whitespace:
        print repr(text_cmd),repr(math_cmd)
        s = "\\"+text_cmd+"\\hfill$\\" + math_cmd +"$\\hfill\\verb"+verb+"\\"+cmd+verb
            #print c,d,repr(s)
        f.write(s+'\n\n')

        n +=1
        if n > 5:
             break
    #else:
    #    print "ERROR", repr(cmd)

"""
print repr(string.whitespace)

for mode,a,b in [ ("all","",""),
                  #("all","$","$"),
                  #("text","",""),
                  #("math","$","$")
                ]:
    commands = getattr(latex2e(),mode+"_commands")


    f.write(r"\section{"+mode+" Symbols}"+'\n')
    n =0 
    for c,d in sorted(commands.items()):
        if type(d).__name__ == "instance" and d.__class__.__name__=="symbol":
            if c in chars:
                chars.remove(c)
            s = a+"\\"+c+b+"\\hfill\\verb"+verb+"\\"+c+verb
            print c,d,repr(s)
            f.write(s+'\n\n')
            n+=1
            if n > 5:
                break
        
    #f.write(r"\section{"+mode+" Accents}"+'\n')
    #for c,d in sorted(commands.items()):
    #    print c,d,type(d)
    #    if type(d).__name__ == "instance" and d.__class__.__name__=="combining":
    #        s=""
    #        for char in ['A','E','I','O','U','a','e','i','o','u','\i']:
    ##            s+= a+"\\"+c+"{"+char+"}"+b
    #        s+="\\hfill\\verb"+verb+"\\"+c+verb
    #        print repr(s)
    #        f.write(s+'\n\n')


        """
"""
f.write(r"\section{Math Accents}"+'\n')
for c,d in sorted(ParseLatex.math_commands.items()):
    if type(d) == dict and d.get('element',None)=="combining":
        s="$"
        for char in ['A','E','I','O','U','a','e','i','o','u','\imath']:
            s+=  "{\\"+c+' '+char+'}'
        s+="$\\hfill\\verb"+verb+"\\"+c+verb
        print repr(s)
        f.write(s+'\n\n')

f.write(r"\section{Text Symbols}"+'\n')
for c,d in sorted(ParseLatex.text_commands.items()):
    if type(d) == dict and d.get('element',None)=="symbol":
        if c in chars:
            chars.remove(c)
        s = "\\"+c+"\\hfill\\verb"+verb+"\\"+c+verb
        print repr(s)
        f.write(s+'\n\n')

f.write(r"\section{Math Symbols}"+'\n')
for c,d in sorted(ParseLatex.math_commands.items()):
    if type(d) == dict and d.get('element',None)=="symbol":
        if c in chars:
            chars.remove(c)
        s = "$\\"+c+"$\\hfill\\verb"+verb+"\\"+c+verb
        print repr(s)
        f.write(s+'\n\n')

"""
print verb in chars

f.write(r'\end{document}'+'\n\n')
f.close()
