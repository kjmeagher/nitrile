import codecs
import logging

try:
    import chardet
except ImportError:
    chardet=None

import Elements
import plugin_manager

class TextElement(object):
    def __init__(self,tag,attr={},info={}):
        self.tag = tag
        self.attr = attr
        self.children = []

    def append(self,child):
        self.children.append(child)

        """
    def __str__(self):        
        if len(self.children)==0:
            return "<{}>".format(self.tag)
        else:
            s = "<{}>".format(self.tag)
            for child in self.children:
                s+=str(child)
            s+="</{}>".format(self.tag)
            return s
        """

           
    def pprint(self,level=0):
        if self.attr:
            attr_str = ''.join([ ' '+a+'='+repr(b) for a,b in self.attr.iteritems()])
        else:
            attr_str = ""
            
        
        if len(self.children)==0:
            print  level*" "+"<"+self.tag+attr_str+"/>"
        else:

            if len(self.children)==1 and isinstance(self.children[0], basestring):
                print  level*" "+"<"+self.tag+attr_str+">"+ repr(self.children[0])+"</"+self.tag+">"

            else:
                print  level*" "+"<"+self.tag+attr_str+">"
                for child in self.children:
                    if isinstance(child, basestring):
                        print ( (level+1)*" "+repr(child))
                    else:
                        child.pprint(level+1)
                print  level*" "+"</"+self.tag+">"

class TextReader(object):
    def __init__(self,filename,options):

        enc = options.get("encoding","utf-8")

        #if the user selects automatic detection of character encoding
        if enc == "detect":
            if not chardet:            
                raise Exception("module chardet not available: auto detecting text file encoding disabled")

            with open(filename,'rt') as text_file:
                detection = chardet.detect(text_file.read())
                enc = detection['encoding']
                confidence = detection['confidence']*100
                confidence_threshold  = float(options.get("confidence",0))
                if confidence < confidence_threshold:
                    raise Exception("Detected encoding %s for file %s with %2.0f%% confidence."
                                    "This is below the threshold set at %2.0f: Exiting"%(repr(enc),repr(filename),
                                                                                         confidence,confidence_threshold )
                                )              
                logging.info("Detected encoding %s for file %s with %2.0f%% confidence"%(repr(enc),repr(filename),confidence))

            
                
        with codecs.open(filename,'r',enc) as text_file:

            #self.paragraphs = []

            self.root_element=TextElement("Text",{},{"filename":filename})
            for line in text_file.readlines():

                if len(line)>=2 and line[-2:]=='\r\n':
                    line = line[:-2]
                elif line[-1]=='\n':
                    line = line[:-1]

                #paragraph = Elements.Paragraph(line,{})
                paragraph = TextElement("para",{},{})
                paragraph.append(line)

                self.root_element.append(paragraph)
            
                    #self.paragraphs.append(paragraph)

    def get_style(self):
        return {}
                
    @classmethod
    def GetExtensions(cls):
        return ["txt"]

    def get_elements(self):
        return self.root_element


plugin_manager.input_plugins.append(TextReader)
