import sys

import importlib
from ..parsers import strip_group,CommandParser,VerbatimArgumentParser,OptionalArgumentParser,MacroParser,CommandBase,Parser
from ..latexelements import LatexElement

import logging
log = logging.getLogger(__name__)

Symbol = None

InvalidChar = Exception("Invalid Character")

class CommandInfo(object):

    @classmethod
    def get_tag(cls,node):
        return cls.__name__

# class symbol(CommandInfo):
#     def __init__(self,c = u"\N{REPLACEMENT CHARACTER}",**kwargs):
#         self.args = 0
#         self.char = c
#         self.kwargs = kwargs
#
#
#     def convert(self,node):
#         print "symbol.convert()"
#         print self.char, self.kwargs
#         print node

def symbol(c = u"\N{REPLACEMENT CHARACTER}"):
    return type(
        'Symbol',
        (CommandBase,),
        dict(args=0,
             c=c,
             get_element = lambda self: self.c),
        )

def combining(c = u"\N{REPLACEMENT CHARACTER}"):
    return type(
        "Combining",
        (CommandBase,),
        dict(args=1,
             defaults = {},
             c=c,
             ),
        )

class subscript(Parser):
    args=1

    def get_node_name(self):
        return "Subscript "+self.start_tolken

    def GetNode(self):
        return self

class superscript(Parser):
    args=1

    def get_node_name(self):
        return "Superscript"+str(dir(self))

    def GetNode(self):
        return self


class declaration(CommandBase):
    args = 0

class null:
    def __init__(self, args=0, defaults = {},arg_parsers = {}):
        self.args = args
        self.defaults = defaults
        self.arg_parsers = arg_parsers

    #@staticmethod
    #def get_element(node):
    #    return LatexElement(node.command)

    @staticmethod
    def get_tag(node):
        return "Command "+node.escape+node.command


# class Meta(CommandParser):
#     def __init__(self, args=0, defaults = None,arg_parsers = None):
#         self.args = args
#         self.defaults = {} if defaults is None else defaults
#         self.arg_parsers = {} if arg_parsers is None else arg_parsers
#
#
#     def get_element(self):
#         return ""
#
#
#     def get_meta(self):
#
#         return node.command,tuple([strip_group(n) for n in node.children])


class element:
    def __init__(self, args=0, defaults = {},element = None,level = -sys.maxint):
        self.args = args
        self.defaults = defaults
        self.element = element
        self.level = level



def tolken(args = 0, defaults =None, level = -sys.maxint):
    return type(
        "tolken__",
        (CommandBase,),
        dict(args = args,
             defaults = defaults if defaults is not None else {},
             level = level,
             get_element = lambda self: LatexElement(self.command),
             )
    )

def heading_get_element(self):
    assert len(self.children)==self.args
    element = LatexElement(self.command,dict(name=strip_group(self.children[0])),{})
    return element


def heading(args,defaults,level):

    return type(
        "Heading__",
        (CommandBase,),
        dict(
            args = args,
            defaults = defaults,
            level = level,
            #get_element = heading_get_element,
            )
        )

class NewCommand(CommandBase):
    args = 4
    arg_parsers = {
        0:VerbatimArgumentParser(),
        1:OptionalArgumentParser("0"),
        2:OptionalArgumentParser(),
        3:VerbatimArgumentParser(),
        }

    def ModifyParser(self,parser):
        assert len(self.children)==4

        cmdname = strip_group(self.children[0])
        numargs = int(strip_group(self.children[1]))
        default = strip_group(self.children[2])
        macrostr = strip_group(self.children[3])

        assert cmdname[0]=='\\'
        cmdname = cmdname[1:]

        arg_parsers = {}

        if default:
            arg_parsers[0] = OptionalArgumentParser(default)

        log.info("Adding command {!r} with {} arguments and default {!r} to Parser".format(cmdname,numargs,default))
        parser.AddCommand(cmdname,MacroParser(cmdname,macrostr,self,numargs,arg_parsers))

        





        
class UsePackage(CommandBase):
    args = 2
    defaults = { 0:""}

    def get_element(self):
        return ""

    def get_meta(self):
        return self.command,tuple([strip_group(n) for n in self.children])

    def ModifyParser(self,parser):
        assert len(self.children)==2
        options = strip_group(self.children[0])
        package = strip_group(self.children[1])

        try:
            module =  importlib.import_module("nitrile.latex.latex2e."+package)
        except ImportError,e:
            #this seems to be the only way to find out what module failed to import
            if e.message.split()[-1] ==package:
                parser.PrintMessage(self,logging.ERROR,
                                    "Cannot find package named {}".format(package))
                return
            else:
                #if the module actually exists but has import errors of its own raise
                raise
        package = getattr(module,package)(options)
        parser.AddPackage(package)




