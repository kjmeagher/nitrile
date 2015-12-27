import pprint
import unicodedata
import unicode_to_latex
import ParseLatex

"""
for s,info in ParseLatex.commands.iteritems():
    if 'char' in info:
        c = info['char']
        print s, c,  unicode_to_latex.unicode_to_latex.get(c,None)

"""
        
import xml.etree.ElementTree as ET


print 'aa' in ParseLatex.commands

root = ET.parse("unicode.xml")
for a in root.iter():
    
    if a.tag == 'character':
        char = a.attrib['dec']

    if a.tag in ['latex','mathlatex','varlatex','AMS','IEEE']:
        if a.text[0]=='\\':

            #print a.text, repr(a.text[1:].strip()), a.text[1:].strip() in ParseLatex.commands, a.text[1:].strip() in ParseLatex.math_commands
            symbol_name = a.text[1:].strip()
            for d,mode in [(ParseLatex.commands,"TEXT"),
                           (ParseLatex.math_commands,"MATH"),
                          ]:


                try:
                    out_char = d.get(symbol_name,{}).get('char',None)
                except AttributeError:
                    continue 
                if out_char is not None :
                    uni = "".join([ unichr(int(c)) for c in char.split('-')])
                    if uni!=out_char:
                        print mode, repr(a.text), char, repr(uni), uni, repr(out_char), out_char
                    del d[symbol_name]

                    
pprint.pprint( [ (k,i['char']) for k,i in ParseLatex.commands.iteritems() if 'char' in i])
pprint.pprint( [ (k,i['char']) for k,i in ParseLatex.math_commands.iteritems() if 'char' in i])

