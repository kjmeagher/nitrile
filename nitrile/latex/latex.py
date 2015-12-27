import sys
from pprint import pprint
from parsers import RootParser
import latexelements
import plugin_manager

class latex(object):
    """
    Input Reader for reading Latex Files
    """

    @classmethod
    def GetExtensions(cls):
        return ["tex"]

    @classmethod
    def GetMimeTypes(cls):
        return ["text/x-tex"]

    def __init__(self,filename,options):

        self.meta = []

        parser  = RootParser(filename).GetNode()


        print parser.pprint_node()

        self.base_element =self.convert(parser)
        print "Latex Intermediate Represendation:"
        self.base_element.pprint()
        print "Meta Data:"
        pprint(self.meta)

    def convert(self,node,level=0):
        if isinstance(node,basestring):
            return node

        #if hasattr(node,"element_info"):
        #    element_info = node.element_info
        #else:
        #    element_info = node

        element_info = node


        node_level = getattr(element_info,"level",-sys.maxint)
        #attrs['level']=node_level
        if node_level > -sys.maxint:
            print  node.get_tag(), node_level


        print node, hasattr(element_info,"get_element")

        if hasattr(element_info,"get_element"):
            element = element_info.get_element()
        else:

            tag = element_info.get_tag()
            element = latexelements.LatexElement(tag,dict())

            curr_level = -sys.maxint
            appending_elements = [ (node_level,element) ]

            for child_node in node.children:

                child_element = self.convert(child_node,level+1)
                child_level = getattr(child_node,"level",-sys.maxint)

                print level*' ' + "T", node_level, element.tag
                print level*' ' + "A", curr_level, appending_elements[-1][1].tag
                print level*' ' + "C", child_level, getattr(child_element,"tag",repr(child_element))

                if node_level > 0 and curr_level > 0 and child_level < 0 :


                    if child_element in [ '', ' ']:
                        continue

                    print level*' ' + "Adding Paragraph to {}".format(appending_elements[-1][1].tag)
                    para_element = latexelements.LatexElement("Paragraph",{},{})
                    appending_elements[-1][1].append(para_element)
                    curr_level = 0
                    appending_elements.append((0,para_element))

                    print level*' ' + "Appending {} to {}".format(getattr(child_element,"tag",repr(child_element)),
                                                                  appending_elements[-1][1].tag)
                    appending_elements[-1][1].append(child_element)

                elif node_level >= 0 and child_level >= 0 and child_level >= curr_level :
                    #print level*' ' + "comming up some levels"

                    #go through the list of elements an get rid of the ones whose levels are
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




            #for child_node in node.children:
            #    child_element = self.convert(child_node,level+1)
            #    element.append(child_element)


        if hasattr(element_info,"get_meta"):
            self.meta.append( element_info.get_meta())



        return element



    def old_convert(self,node,level=0):
        children = None
        attrs = {}

        node_info = getattr(node,"node_info",{})

        if isinstance(node, basestring):
                return node
        elif node.type=="CommandParser":




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
                    para_element = LatexElement("Paragraph",{},{})
                    appending_elements[-1][1].append(para_element)
                    curr_level = 0
                    appending_elements.append((0,para_element))

                    print level*' ' + "Appending {} to {}".format(getattr(child_element,"tag",repr(child_element)),
                                                                  appending_elements[-1][1].tag)
                    appending_elements[-1][1].append(child_element)

                elif node_level >= 0 and child_level >= 0 and child_level >= curr_level :
                    #print level*' ' + "comming up some levels"

                    #go through the list of elements an get rid of the ones whose levels are
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




plugin_manager.input_plugins.append(latex)

"""

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


