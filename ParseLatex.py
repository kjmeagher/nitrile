import sys
from copy import deepcopy ,copy
import string
import logging as log

from pprint import pprint

import plugin_manager

import latex2e

tabbing_commands = {
    "'" : (0,{}), #moves current columnto the right of the previous column
    "-" : (0,{}), #moves left margin tothe left by one tab stop
    "<" : (0,{}), #puts text to left oflocal left margin.
    "=" : (0,{}), #sets a tab stop
    ">" : (0,{}), #forward tab
    "`" : (0,{}), #environment moves all text which follows (up to \\) to the right margin.

    "cline"           : (1,{}),
    "kill" : (0,{},None),

    "multicolumn" : {'args':3},
    "pushtabs" : {'args':1},
    "tabbingsep" : None,
    "tabcolsep"  : None,

    
    #not sure how to handle theses
    #"a'" accute
    #"a`" grave
    #"a=" macron   
    }



environments = {
    "abstract"   : (0,{}), 
    "array"      : (1,{}), #start array enviorement
    "center"     : (0,{}), #lines are centered, end lines with '\\'
    "description": (0,{}), #labeled list
    "displaymath": (0,{}),
    "document"   : {'args':0,'level' : 1000},
    "enumerate"  : (0,{}),
    "eqnarray"   : (0,{}),
    "eqnarray*"  : (0,{}),
    "equation"   : (0,{}),
    "figure"     : (1,{1:""}),
    "figure*"    : (1,{1:""}),
    "flushleft"  : (0,{}),
    "flushright" : (0,{}),
    "itemize"    : (0,{}),
    "list"       : (2,{}),
    "math"       : (0,{}),
    "minipage"   : (2,{1:""}),
    #"picture" this one uses () for options not supporting for now
    "quotation"  : (0,{}),
    "quote"      : (0,{}),
    "tabbing"    : (0,{}),
    "table"      : (1,{1:""}),
    "table*"     : (1,{1:""}),
    "tabular"    : (1,{}),
    "theorem"    : (0,{}),
    "titlepage"  : (0,{}),
    "verbatim"   : (0,{}),
    "verse"      : (0,{}),



    #Not in the list but needed for intro.tex
    "comment"    : (0,{},None),
    "align"    : (0,{},None),
    "subequations"   : (0,{},None),
    "cases"    : (0,{},None),
    "pmatrix"    : (0,{},None),
    "thebibliography"    : (0,{},None),


    
    
    }
    


picture_commands = {
    "circle" : (1,{}),
    "circle*" : (1,{}),
    "dashbox" : (4,{3:""}),
    "framebox" : (3,{2:""}),
    "line" : (2,{},None),
    "linethickness":(1,{},None),
    "makebox" : (3,{1:"",2:""},None),
    "multiput" : {'args':4, 'paren_args':[1,2]},
    "oval"     : {'args':1, 'paren_args':[1],},
    "put"      : {'args':2, 'paren_args':[1],},
    "thicklines"           : None,
    "vector"      : {'args':2, 'paren_args':[1],},
    }



verbatim_rules = {
    "end_tolkens":set([]),
    "start_tolkens":[],
}


class LatexElement(object):

    """
    This is the base class for all output of the latex parser.
    The output contains a hierarchical DOM
    The DOM is composed of elements, each element contains 0 or more children
    Each element is represented by this class or something that inherits from it
    """
    
    def __init__(self,tag,attr={},info={}):
        self.tag = tag
        self.attr = attr
        self.info = info
        self.children = []

    def append(self,child):
        self.children.append(child)


    def __str__(self):
        
        if len(self.children)==0:
            return "<{}>".format(self.tag)
        else:
            s = "<{}>".format(self.tag)
            for child in self.children:
                s+=str(child)
            s+="</{}>".format(self.tag)
            return s


    
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

            


def eq(node1,node2):

    if node1==node2:
        return True

    if  node1.__class__.__name__ == node2.__class__.__name__:
        if hasattr(node1, "children") and hasattr(node2,"children") and len(node1.children)==len(node2.children):
            for i, child in enumerate (node1.children):
                if not eq(child,node2.children[0]):
                    return False
            return True
        else:
            return False
    else:
        
        return False
        
        

class Node(object):

    """
    This is the base class of the latex parser intermediate representation
    The output of the latex parser is a document represented by a heirarchial tree of elements
    Since documents are not represtened heirarcally in latex they must be 
    each node represents a latex node: string, command, enviroment, etc
    latex contains tolkens which are non-heirarcical
    the intermediate representation is then transformed from non-heirarcial nodes 
    into a heiracarcial representation of elements

    all nodes in the intermediate representation derive from the base class
    for now the code does not distiguish between a parser and a node
    as the paradigm is to call a parser object witch contains the code to parse
    and then it assembles itself into an node object which contians the data 
    """
    
    def __init__(self):
        self.children = []
        self.start = None
        self.stop = None
        self.info = {}


    def add_child(self,n):
        #if adding a string to a node whose last child is already a string
        #append the string to the last child
        #otherwise just add it to the list of children
        if isinstance(n, basestring) and self.children and isinstance(self.children[-1], basestring):
            self.children[-1]+=n
        else:
            self.children.append(n)

    def post(self):
        return self

    def pprint(self,level=0):
        print  level*" "+"<"+self.__class__.__name__+">", self.info
        for child in self.children:
            if isinstance(child, basestring):
                print ( (level+1)*" "+repr(child))
            else:
                try:
                    child.pprint(level+1)
                except:
                    print "FAIL", repr(child)

    """
    def __eq__(self,node):        
        if  self.__class__.__name__ == node.__class__.__name__:           
            if hasattr(node,"children"):
                return self.children == node.children
            else:
                return False
        else:
            return False
    """

class RootNode(Node):
    pass
        





class EndTolkenParser(Node):
    def __init__(self):
        super(EndTolkenParser,self).__init__()

    def parse(self,end_tolken,mode=None):    
        self.end_tolken=end_tolken
        self.rules = deepcopy(self.parent_rules)
        
        if mode:
            self.rules['mode'] = mode
        self.rules["end_tolkens"].add(self.end_tolken)
        #if end_tolken in self.rules["start_tolkens"]:
        #    del self.rules["start_tolkens"][end_tolken]

        while True:               


            """
            This is the old code which matches nodes instad of string to find the end tolken
            It is a lot slower
            
            t = self.parser.GetTolken(self.rules) 

            
            
            if self.parser.eof :
                log.error("Start tolken: {!r} start pos: {!r}".format(self.start_tolken,self.start_pos))
                raise Exception("Reached end of file while waiting for end tolken {!r}".format(self.end_tolken)) 
            elif t == self.end_tolken:
                self.end = self.parser.get_pos()
                return self
            elif t in self.rules["end_tolkens"]:
                raise Exception("Found end tolken {!r} while looking for end tolken {!r}".format(t,self.end_tolken))
            else:
                self.add_child(t)

            """

            #this code assumes that end_tolken is a string it is much faster!

            if self.parser.eof :
                log.error("Start tolken: {!r} start pos: {!r}".format(self.start_tolken,self.start_pos))
                raise Exception("Reached end of file while waiting for end tolken {!r}".format(self.end_tolken))

            elif self.parser.peak(len(self.end_tolken))==self.end_tolken:
                for i in range(len(self.end_tolken)):
                    self.parser.get_char()
                    self.end = self.parser.get_pos()
                return self
            else:
                for t in self.rules["end_tolkens"]:
                    if self.parser.peak(len(self.end_tolken))==t:
                        raise Exception("Found end tolken {!r} while looking for end tolken {!r}".format(t,self.end_tolken))
            
            t = self.parser.GetTolken(self.rules) 
            self.add_child(t)
                    
                
            

class VerbParser(EndTolkenParser):
    tag = 'verb'
    def __init__(self):
        super(VerbParser,self).__init__()

              
class GroupParser(EndTolkenParser):
    tag = 'group'
    def __init__(self):
        super(GroupParser,self).__init__()

class InlineMathParser(EndTolkenParser):
    tag="inlinemath"
    struct = "inline"
    def __init__(self):
        super(InlineMathParser,self).__init__()

class EnvironmentParser(EndTolkenParser):
    def __init__(self,
                 env_name,
                 parser,
                 parent_rules,
                 start_pos,
                 start_tolken,
                 ):
        super(EnvironmentParser,self).__init__()
        self.env_name = env_name

        self.node_info = environments[env_name]
        
        self.parser = parser
        #self.parent_rules = deepcopy(parent_rules)
        self.parent_rules = parent_rules
        
        self.start_pos = start_pos
        self.start_tolken = start_tolken
        
        if self.env_name not in environments:
            log.warn("{}:Unknown EnviromentParser {}".format(self.parser.get_location_string(),
                                                       self.env_name,
                                                   ))

        if self.env_name =="verbatim":
            self.parent_rules=verbatim_rules
        elif  self.env_name in [ "equation", "pmatrix"]:
            self.parent_rules['mode']='math'


                 
                     

    def info(self):
        return self.env_name

class Comment(Node):
    def __init__(self):        
        super(Comment,self).__init__()


    def parse(self):
        assert self.start_tolken in self.parent_rules["comment"]
        comment = ""
        while self.parser.peak(1) not in self.parent_rules["newline"]:
            comment += self.parser.get_char()
            if self.parser.eof:
                break


        if self.parser.peak(2)[-1] not in self.parent_rules["space"]+self.parent_rules["newline"]:
            self.parser.get_char()
                
        self.end_pos = self.parser.get_pos()
        self.end_tolken=self.parser.peak(1)
        self.children = [comment]
        return self
    
class ParagraphParser(Node):
    struct = 'para'

    node_info = { 'tag' : 'para', 'level' : 0}
    def __init__(self):
        super(ParagraphParser,self).__init__()


    def parse(self):
        space = self.parent_rules["space"]
        newline = self.parent_rules["newline"]
        white = space+newline

        if self.start_tolken in newline:
            newline_count = 1
        else:
            newline_count = 0

        while self.parser.peak(1) in white:
            c = self.parser.get_char()
            if self.parser.eof:
                break
            if c in newline:
                newline_count += 1
    
        if newline_count >= 2:
            return self
        else:
            return " "


class Substitute(Node):
    def __init__(self):
        super(Substitute,self).__init__()

    def parse(self,substitution):
        return substitution

class InvalidChar(Node):
    def __init__(self):
        super(Substitute,self).__init__()

    def parse (self,msg):

        raise Error("Encountered Invalid Character {!r}. {}".format(self.c,msg))


    
class CommandParser(Node):
    tag = 'command'
    def __init__(self):
        super(CommandParser,self).__init__()



    def parse(self):
        assert self.start_tolken == self.parent_rules["escape"]       
        #self.rules = deepcopy(self.parent_rules)
        self.rules = self.parent_rules

        cmd = self.parser.get_char()
        if cmd in self.rules['letters']:
            while self.parser.peak(1) in self.rules['letters']:
                cmd +=  self.parser.get_char()
        self.command = cmd


        #commands = deepcopy( self.rules["commands"])
        #print "MODE:",self.rules['mode']
        
        if cmd in [ "begin" ] :



            begin_arg = self.parser.GetTolken(self.rules)
            assert len(begin_arg.children)==1
            env_name = begin_arg.children[0]
            assert isinstance(env_name, basestring)


            #end_tolken =  ParseString(r"\end{"+env_name+"}").children[0]
            
            end_tolken =  r"\end{"+env_name+"}"
            #print "E={!r} {!r}".format(end_tolken,r"\end{"+env_name+"}" )



            node = EnvironmentParser(env_name,self.parser,self.rules,self.start_pos,Node)
            #node.parser = self.parser
            #node.parent_rules = deepcopy(self.rules)
            #node.start_pos = self.start_pos
            #node.start_tolken = None
            
            
            return node.parse(end_tolken = end_tolken)
            
            #end_tolken = ParseString(r"\end{equation}")

        elif cmd in ["verb"]:
            
            verb_tolken = self.parser.get_char()

            node = VerbParser()
            node.parser = self.parser
            node.parent_rules = verbatim_rules
            node.start_pos = self.parser.get_pos()
            node.start_tolken = verb_tolken
            return node.parse(end_tolken=verb_tolken)
            
        else:

            command_info = self.parser.find_command(cmd, self.rules['mode'])
            
            if command_info:


                for i in range(command_info.args):                   
                    p = self.parser.peak(1) 
                    new_rules = deepcopy(self.rules)
                    
                    if i+1 in command_info.defaults:
                        if p == '[':
                            new_rules["start_tolkens"]['['] = (GroupParser,dict(end_tolken = "]"))
                            t = self.parser.GetTolken(new_rules)
                        else:
                            t = command_info.defaults[i+1]
                    else:
                        t = self.parser.GetTolken(new_rules)
                        if t==' ':
                            t = self.parser.GetTolken(new_rules)
                        
                    self.children.append(t)

                self.element = command_info.__class__.__name__

                #print "###", cmd, self.element
                
                self.node_info = command_info


            else:
                self.element = None
                #raise Exception("Unknown CommandParser {}".format(cmd))
                log.warn("{}:Unknown CommandParser {} in mode {}".format(self.parser.get_location_string(),
                                                                   cmd,
                                                                   self.rules['mode'],
                                                                   )

                )



        return self

    def info(self):
        return "c={!r} e={!r}".format(self.command,self.element)

    def tranlate(self):
        element_type = getattr(self,"element",None)
        if element_type == 'symbol':
            return 

    def __repr__(self):
        return "<CommandParser {}, {!r}, {!r}>".format(self.command,self.element,self.children)

    def __eq__(self,node):
        if super(CommandParser,self).__eq__(node):
            return self.command==node.command
        else:
            return False
        



class Latex(Node):
    struct = 'root'
    def __init__(self,parser,rules):
        super(Latex,self).__init__()

        self.dialect = latex2e.latex2e()
        
        if rules is None:
            self.rules = dict( 
                escape = '\\',
                space =  " \t",
                newline = "\n",
                comment = "%",
                letters = string.ascii_letters,
                #commands = self.dialect.text_commands,
                #math_commands =  self.dialect.math_commands,
                mode = "text",
                start_tolkens = { 
                    "{"  : (GroupParser,      dict(end_tolken = "}" )),
                    "%"  : (Comment,    dict()),
                    " "  : (ParagraphParser,  dict()),
                    "\t" : (ParagraphParser,  dict()),
                    "\n" : (ParagraphParser,  dict()),                              
                    "$"  : (InlineMathParser, dict(end_tolken = "$",
                                                   mode="math")),                              
                    "\\" : (CommandParser   , dict()),
                    "~"  : (Substitute, dict(substitution = "\N{NON BREAKING SPACE}")),
                    "#"  : (InvalidChar, dict(msg = "I don't even know what the hash/number sign is used for in LaTeX,"
                                              "but it causes an error so you get an error as well."
                                              "You might want to try escaping the the character as '\#'.")),
                    "&"  : (InvalidChar, dict(msg = "The ampersand character is only used in tabulated enivroments"
                                              "such as tables. If you want a literal ampersand try escaping it: '\&'.")),
                    "_"  : (InvalidChar, dict(msg = "The underscore can only be used in math mode. "
                                              "I would like to use subscripts and superscripts in text mode as well, "
                                              "but thats not now LaTeX works.")),
                    "^"  : (InvalidChar,  dict(msg = "The underscore can only be used in math mode. "
                                               "I would like to use subscripts and superscripts in text mode as well, "
                                               "but thats not now LaTeX works.")),
                
                    "\x7f" : (InvalidChar, dict(msg = "character 0x7f is an Invalid character in LaTeX" )),
                },
                end_tolkens = set(["}"]) 
            )
        else:
            self.rules = rules

        curr_string = ""
        
        while True:            
            t = parser.GetTolken(self.rules)

            if parser.eof:
                break
            self.add_child(t)



"""
For reference
escape  = '\\',
begin   = '{',
end     = '}',
math    = '$',
align   = '&',
eol     = '\r',    # ^^M
macro   = '#',
sup     = '^\v',   # ^^K
sub     = "_\x01", # ^^A
ignore  = "\0",    # ^^@
space   = " \t",   # ^^I
letters = string.ascii_letters,
active  = "~\f",   # ^^L
comment = "%",
invalid = "\x7f",  #^^?
%#&$^{}~
"""
       



class ParseLatex(object):
    def __init__(self,file,filename,encoding='ascii',dialect='latex2e'):
        self.line = 0
        self.column = 0
        self.index = 0
        self.eof = False
        self.encoding = encoding
        self.file = file
        self.filename = filename
        self.dialect = dialect

        self.commands = []
        self.modes = []

        if self.dialect =='latex2e':
            self.add_package(latex2e.latex2e())        

    def add_package(self,package):
        d = { m:getattr(package,m+"_commands",{}) for m in ['all','text','math']}
        self.commands.append(d)
                   
    def find_command(self,cmd,mode):
        for d in reversed(self.commands):
            for m in [mode,'all']:
                dd = d[m]
                if cmd in dd:
                    return dd[cmd]
        return None

    def get_pos(self):
        return (self.index,self.line,self.column)

    def get_location_string(self):
        return "{}:{}:{}".format(self.filename,self.line,self.column)

    
    def get_char(self):
        """
        This function reads from the file and pops the next character
        The encoding can be changed on the fly
        I think this is the right way to do it given latex's variable encoding abilities
        """
        for i in range(1,5):
            c = self.file[self.index:self.index+i]            
            try:
                u = c.decode(self.encoding)
                break
            except UnicodeDecodeError:
                if i==4:
                    raise          

        self.index+=i

        if self.index > len(self.file):
            self.eof=True
            return None

        if u =='\n':
            self.line +=1
            self.column = 0
        else:
            self.column+=1

        return u


    def peak(self,size):
        return self.file[self.index:self.index+size]
            
    def GetTolken(self,rules):
        try:
            start_pos = self.get_pos()
            c = self.get_char()
            
            if self.eof:
                return None

            if c in rules["start_tolkens"]:
                node_type, args = rules["start_tolkens"][c]
                node = node_type()
                node.parser = self
                node.parent_rules = rules
                node.start_pos = start_pos
                node.start_tolken = c
                return node.parse(**args)
            else:
                return c
        except:
            log.error("{}:{}:{} Error while parsing".format(self.filename,self.line,self.column))
            raise

def ParseString(string,rules=None):
    parser = ParseLatex(string,"<string>")
    return Latex(parser,rules)

def ParseFile(filename,rules=None):
    file = open(filename,'rb').read()
    parser = ParseLatex(file,filename)
    return Latex(parser,rules)
  
def print_tree(node,level=0):
    print  level*" "+"<"+node.type+">", 
    if node.type =="CommandParser":
        print "c={!r}, e={!r}".format(node.command,node.element)
    elif node.type == "Comment":
        pass
    else:
        print 
    for child in node.children:
        if isinstance(child, basestring):
            print ( (level+1)*" "+repr(child))
        else:
            print_tree(child,level=level+1)      

class LatexReader(object):

    def convert(self,node,level=0):
        children = None
        attrs = {}

        node_info = getattr(node,"node_info",{})

        if isinstance(node, basestring):
                return node                   
        elif node.type=="CommandParser":

            
            

            print node_info
            #print dir(node_info)

            if hasattr(node_info,'convert'):
                print node_info.convert(node)

            
            

            
            if hasattr(node_info,'element'):
                tag = node_info.element
                print "Element", tag
                if tag=="symbol":
                    children = [node.command]                                        
                elif tag=="combining":
                    attrs = {"char":node.command}
                elif tag=="Section":
                    children =[]
                    attrs ={ "name" : "asdf"}
                else:
                    pass
            else:
                tag = "UNKNOWN COMMAND"
                children = []
                attrs = {'cmd' :node.command}
        elif node.type == "EnvironmentParser":
            tag = node.env_name                                                            
        else:
            tag = node_info.get("tag", getattr(node,"tag",node.type))
        
        element = LatexElement(tag,attrs,{})

        node_level = getattr(node_info,"level",-sys.maxint)        
        attrs['level']=node_level

        if children is None:
            curr_level = -sys.maxint
            appending_elements = [ (node_level,element) ]
            
            for child_node in node.children:

                child_element = self.convert(child_node,level+1)
                child_level = getattr(getattr(child_node,"node_info",None),"level",-sys.maxint)

                #print level*' ' + "T", node_level, element.tag
                #print level*' ' + "A", curr_level, appending_elements[-1][1].tag
                #print level*' ' + "C", child_level, getattr(child_element,"tag",repr(child_element))
               
                if node_level > 0 and curr_level > 0 and child_level < 0 :

                    
                    if child_element in [ '', ' ']:
                        continue
                    
                    print level*' ' + "Adding Paragraph to {}".format(appending_elements[-1][1].tag)
                    para_element = LatexElement("para",{},{})
                    appending_elements[-1][1].append(para_element)
                    curr_level = 0                    
                    appending_elements.append((0,para_element))

                    print level*' ' + "Appending {} to {}".format(getattr(child_element,"tag",repr(child_element)),
                                                                  appending_elements[-1][1].tag)
                    appending_elements[-1][1].append(child_element)

                elif node_level >= 0 and child_level >= 0 and child_level >= curr_level :
                    #print level*' ' + "comming up some levels"

                    #go throught the list of elements an get rid of the ones whose levels are
                    #less than the current level

                    copy_list = list(appending_elements)
                    copy_list.reverse()

                    #print  level*' ' + "*", len(copy_list)
                    
                    for l,e in copy_list:
                        #print level*' ' + '####', l, getattr(child_element,"tag",repr(e))                       
                        if l <= child_level:
                            poped_level , poped_element = appending_elements.pop()
                            ###print level*' ' + 'POPED', poped_element                            
                        else:
                            break
                    else:
                        Error("This Should Never Happen")
                        #appending_elements = [ (node_level,element) ]

                    #print level*' ' +  "Appending {} to {}".format(getattr(child_element,"tag",repr(child_element)),
                    #                                               appending_elements[-1][1].tag)
                    appending_elements[-1][1].append(child_element)
                    #print level*' ' + "Adding {} to appending_elements".format(child_element.tag)
                    curr_level = child_level
                    appending_elements.append((child_level,child_element))
                    

                else:
                    #print appending_elements
                    #print level*' ' +  "Appending {} to {}".format(getattr(child_element,"tag",repr(child_element)),
                    #                                                 appending_elements[-1][1].tag)
                    appending_elements[-1][1].append(child_element)
                    
        else:
            for child in children:                              
                element.append(child)
                
        return element
                

    
    def __init__(self,filename,options):
        node = ParseFile(filename,rules=None)

        print "Latex Intermediate Represendation:"
        print node.pprint()
        
        self.base_element =         self.convert(node)                       
    
    @classmethod
    def GetExtensions(cls):
        return ["tex"]

    @classmethod
    def GetMimeTypes(cls):
        return ["text/x-tex"]

    def get_elements(self):
        return self.base_element

    def get_style(self):

        """
        text_symbols = { c:d['char'] for c,d in self.dialect.text_commands.iteritems()
                         if type(d)==dict and d.get('element',"")=='symbol'}

        math_symbols  = { c:d['char'] for c,d in self.dialectmath_commands.iteritems()
                          if type(d)==dict and d.get('element',"")=='symbol'}

        text_combining = { c:d['char'] for c,d in self.dialect.commands.iteritems()
                           if type(d)==dict and d.get('element',"")=='combining'}

        math_combining = { c:d['char'] for c,d in self.dialect.math_commands.iteritems()
                           if type(d)==dict and d.get('element',"")=='combining'}
        """
        return { "inlinemath" : {"symbol": {},
                                 "combining-char": {}},
                 "symbol"     : {},
                 "combining-char" : {},
                 'verb'       : {"font-family" : "Courier",
                                 "weight"      : "bold",
                                 "background"  : "lightgrey",
                                 },
                 }
                

"""
plugin_manager.input_plugins.append(LatexReader)


            
if __name__=='__main__':

    #begin_equation = ParseString(r"\begin{equation}")

    #n = ParseLatex('hello2.tex',encoding='cp437').Parse()
    #n = ParseFile('intro.tex')
    #n = ParseFile('symbols.tex')
    #n = ParseFile('hello.tex')
    #print_tree(n)
    #n.pprint()


    #n = ParseString(r"\begin{equation}")
    #n = ParseString(r"\end{equation}")
    #print_tree(n)
    #n.pprint()

    #print eq(n,begin_equation)
    #print ParseLatex('rune.txt',encoding='utf-8').Parse()
    #print ParseLatex.catcodes


    r = RootParser('symbols.tex')
    print r._Parser__tolkens
    print r._Parser__cmds

    r.GetNode().pprint()

    #while 1:
    #    c = r.GetNode()
    #    if c is None:
    #        break
    #    else:
    #        print c
            
"""
