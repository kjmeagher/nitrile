class LatexElement(object):

    """
    This is the base class for all output of the latex parser.
    The output contains a hierarchical DOM
    The DOM is composed of elements, each element contains 0 or more children
    Each element is represented by this class or something that inherits from it
    """

    def __init__(self,tag,attr=None,info=None):
        self.tag = tag
        self.attr = {} if attr is None else attr
        self.info = {} if attr is None else info
        self.children = []

    def append(self,child):
        if isinstance(child, basestring) and self.children and isinstance(self.children[-1], basestring):
            self.children[-1] += child
        else:
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

