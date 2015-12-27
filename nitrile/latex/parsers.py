import sys
import string
from copy import copy
import logging
import difflib


log = logging.getLogger(__name__)


class ParseError(Exception):
    def __init__(self, message, start=None, stop=None, node=None):

        # Call the base class constructor with the parameters it needs
        super(ParseError, self).__init__(message)

        if node:
            self.start = node.start
            self.stop = node.stop
        else:
            self.start = start
            self.stop = stop


#     """
#     This is the base class of the latex parser intermediate representation
#     The output of the latex parser is a document represented by a heirarchial tree of elements
#     Since documents are not represtened heirarcally in latex they must be
#     each node represents a latex node: string, command, enviroment, etc
#     latex contains tolkens which are non-heirarcical
#     the intermediate representation is then transformed from non-heirarcial nodes
#     into a heiracarcial representation of elements
#
#     all nodes in the intermediate representation derive from the base class
#     for now the code does not distiguish between a parser and a node
#     as the paradigm is to call a parser object witch contains the code to parse
#     and then it assembles itself into an node object which contians the data
#     """



def strip_group(node):
    #if isinstance(node, Group):
    #    if len(node.children) == 1:
    #        return node.children[0]

    if isinstance(node, GroupParser) or isinstance(node, OptionalGroupParser):
        if len(node.children) == 1:
            return node.children[0]
    return node

def get_latex(node):
    if isinstance(node,basestring):
        return node
    else:
        return node.get_latex()


class Reader(object):
    def __init__(self, buffer, filename="<string>"):
        self.line = 0
        self.column = 0
        self.index = 0
        self.startlines = [0]
        self.eof = False
        self.filename = filename
        self.encoding = 'ascii'
        self.buffer = buffer

    def get_char(self):
        """
        This function reads from the file and pops the next character
        The encoding can be changed on the fly
        I think this is the right way to do it given latex's variable encoding abilities
        """
        """
        for i in range(1,5):
            c = self.buffer[self.index:self.index+i]            
            try:
                u = c.decode(self.encoding)
                break
            except UnicodeDecodeError:
                if i==4:
                    raise          
        """

        if self.eof :
            return None

        c = self.buffer[self.index]
        self.index += 1

        if self.index >= len(self.buffer):
            self.eof = True

        if c == '\n':
            self.line += 1
            self.column = 0
            self.startlines.append(self.index)
        else:
            self.column += 1

        return c


    def peak(self, size=1):
        if self.eof:
            return None
        else:
            return self.buffer[self.index:self.index + size]

    def get_pos(self):
        return (self, self.index, self.line, self.column)

    def get_line(self, lineno):
        start = self.startlines[lineno]

        try:
            end = self.startlines[lineno + 1]
        except:
            end = string.find(self.buffer, '\n', start)
            if end ==-1:
                end = None

        return self.buffer[start:end]

    @staticmethod
    def get_pos_string(pos):
        return "{}:{}:{}".format(pos[0].filename, pos[2], pos[3])


class FileReader(Reader):
    def __init__(self, filename):
        buffer = open(filename, 'r').read()
        log.info("Opening file {!r} for reading, file is {}b"
                 .format(filename, len(buffer)))
        super(FileReader, self).__init__(buffer, filename)


class Parser(object):
    def __init__(self, parent):
        self.__rules = parent.__rules
        self.__modified = {}
        for r in self.__rules:
            self.__modified[r] = False
        self.source = parent.source
        self.parent = parent
        self.root = parent.root
        self.trace = parent.trace

        if getattr(self, 'mode', None):
            pass
        else:
            self.mode = parent.mode

        self.children = []
        self.start = None
        self.stop = None
        self.info = {}


    def add_child(self, n):
        # if adding a string to a node whose last child is already a string
        #append the string to the last child
        #otherwise just add it to the list of children
        if isinstance(n, basestring) and self.children and isinstance(self.children[-1], basestring):
            self.children[-1] += n
        else:
            self.children.append(n)


    def get_node_name(self):
        c = self.__class__.__name__
        while c.endswith('_'):
            c=c[:-1]
        if c.endswith("Parser"):
            return c[:-6]
        else:
            return c

    def pprint_node(self, level=0):

        if len(self.children) == 0:
            print  level * " " + "[" + self.get_node_name() + "/]"

        elif len(self.children) == 1 and isinstance(self.children[0], basestring):
            print  level * " " + "[" + self.get_node_name() + "/]", repr(self.children[0])

        else:
            print  level * " " + "[" + self.get_node_name()+ "]"
            for child in self.children:
                if isinstance(child, basestring):
                    print ( (level + 1) * " " + repr(child))
                else:
                    if child is None:
                        print "NONE"
                    else:
                        child.pprint_node(level + 1)


            print level * " " + "[/" + self.get_node_name() + "]"


    def get_tag(self):
        return self.__class__.__name__

    def InitRules(self):
        self.__rules = dict(verb_codes={},
                            text_codes={},
                            math_codes={},
                            all_cmds={},
                            text_cmds={},
                            math_cmds={},
                            envs={},
                            )
        self.__modified = {}
        for r in self.__rules:
            self.__modified[r] = False

    def CopyOnModify(self, name):
        if not self.__modified[name]:
            self.__rules[name] = copy(self.__rules[name])
            self.__modified[name] = True

    def UpdateRules(self, name, new_rules):
        if new_rules:
            self.CopyOnModify(name)
            self.__rules[name].update(new_rules)

    def AddPackage(self, package):
        for r in self.__rules:
            self.UpdateRules(r, getattr(package, r, None))

    def AddCode(self, char, code):
        self.CopyOnModify("text_codes")
        self.__rules['text_codes'][char] = code

    def GetCode(self, char):
        if self.mode == 'text':
            return self.__rules['text_codes'].get(
                char, self.__rules['verb_codes'].get(char, None))
        elif self.mode == 'math':
            return self.__rules['math_codes'].get(
                char, self.__rules['text_codes'].get(
                    char, self.__rules['verb_codes'].get(
                        char, None)))

    def AddCommand(self, cmd, cmd_info):
        self.CopyOnModify("all_cmds")
        self.__rules['all_cmds'][cmd] = cmd_info

    def GetCommand(self, cmd):
        if self.mode == 'text':
            return self.__rules['all_cmds'].get(cmd, self.__rules['text_cmds'].get(cmd, None))
        if self.mode == 'math':
            return self.__rules['all_cmds'].get(cmd, self.__rules['math_cmds'].get(cmd, None))

    def GetEnvironment(self, env):
        return self.__rules['envs'].get(env, None)

    def SetMode(self, mode):
        self.mode = mode

    def GetNode(self):

        pos = self.source.get_pos()
        char = self.source.get_char()

        # if eof
        #if char is None:
        #    if self.eof_ok:
        #        return ""
        #    else:
        #        raise Exception("Encountered End of file")




        catcode = self.GetCode(char)

        if catcode is None:
            #None signifies no operation
            #so just return the char that the parser got
            return char
        elif isinstance(catcode, basestring):
            #simple string substitution
            return catcode
        elif isinstance(catcode, type) and issubclass(catcode, Parser):
            parser = catcode(self)
            parser.start_tolken = char
            parser.start = pos

            return parser.GetNode()

        elif isinstance(catcode, BaseException):

            self.PrintMessage(pos, logging.ERROR, catcode)

        else:
            Exception("Got code {!r} from character {!r} and have no idea what to do with it!"
                      .format(catcode, char))

    def ParseArguments(self, info, node):
        for i in range(info.args):
            # the hasattr here should go at some point in the future
            if hasattr(info, "arg_parsers") and i in info.arg_parsers:
                subparser = info.arg_parsers[i](self)
            elif i in info.defaults:
                #transitional code info.defaults should go at some point in the future
                subparser = OptionalArgumentParser()(self)
            else:
                subparser = Parser(self)
            t = subparser.GetNode()

            node.add_child(t)

    def AddTrace(self,parser,node,priority,message):

        self.trace.append((parser,node,priority,message))

    def PrintMessage(self, node, priority, message, print_trace = True):

        if print_trace:
            for t in self.trace:

                t[0].PrintMessage(t[1],t[2],t[3],print_trace=False)

        errlog = logging.getLogger("errout")

        if hasattr(node, "start"):
            start = node.start
            if hasattr(node, "stop"):
                stop = node.stop
            else:
                stop = (node.start[0],
                        node.start[1] + 1,
                        node.start[2],
                        node.start[3] + 1,
                        )
            posstr = FileReader.get_pos_string(node.start)
        elif node:
            start = node
            stop = (start[0],
                    start[1] + 1,
                    start[2],
                    start[3] + 1,
                    )
            posstr = FileReader.get_pos_string(start)

        else:
            posstr = "nitirle"
            start = None

        p = {logging.CRITICAL: "fatal error",
             logging.ERROR: "error",
             logging.WARN: "warning", }[priority]
        msg = posstr + ": " + p + ": " + str(message)

        if start:
            assert start[2] == stop[2]
            line = self.source.get_line(start[2])
            node_len = stop[3] - start[3]
            console_width = 80
            elipsis = "..."

            if len(line) <= console_width:
                printline = line
                pointer = start[3] * " " + node_len * "^"
            else:
                padding = (console_width - node_len) / 2 - len(elipsis)
                assert padding >= 0
                if start[3] < padding:
                    printline = line[0:console_width - len(elipsis)] + elipsis
                    pointer = start[3] * " " + node_len * "^"

                elif stop[3] + padding > len(line):
                    assert console_width > len(elipsis)
                    printline = elipsis + line[-console_width + len(elipsis):]
                    pointer = (console_width - len(line) + start[3]) * " " + node_len * "^"
                else:
                    printline = elipsis + line[start[3] - padding:stop[3] + padding] + elipsis
                    pointer = (len(elipsis) + padding) * " " + node_len * "^"

        errlog.log(priority, msg)
        if start:
            errlog.log(priority, printline)
            errlog.log(priority, pointer)

    def warn(self, node, msg):
        self.root.warnings += 1
        self.PrintMessage(node, logging.WARN, msg)

    def error(self, node, msg):
        self.root.errors += 1
        self.PrintMessage(node, logging.ERROR, msg)

    def fatal(self, node, msg):
        self.root.errors += 1
        self.PrintMessage(node, logging.CRITICAL, msg)
        raise Exception(msg)


class RootParser(Parser):

    level = sys.maxint
    def __init__(self, filename):
        self.InitRules()
        self.source = FileReader(filename)
        self.root = self
        self.mode = 'text'
        self.trace = []
        from latex2e import latex2e

        self.AddPackage(latex2e.latex2e)
        self.warnings = 0
        self.errors = 0

        self.children = []
        self.start = None
        self.stop = None
        self.info = {}


    def get_tag(self):
        return "Latex"

    def GetNode(self):


        try:
            while True:
                child = Parser.GetNode(self)
                if child:
                    self.add_child(child)
                if self.source.eof:
                    break

        except:
            raise
        finally:
            s = "Encountered {} errors and {} warnings".format(self.errors, self.warnings)
            if self.warnings or self.errors:
                self.warn(None, s)
            else:
                log.info(s)

        return self


class WhitespaceParser(Parser):
    mode = None
    level = 0

    def get_node_name(self):
        return "Paragraph"

    def get_tag(self):
        return "Paragraph"

    def GetNode(self):
        space = ' \t'
        newline = '\n'
        white = space + newline

        if self.start_tolken in newline:

            newline_count = 1
        else:
            newline_count = 0

        while self.source.peak() in white:
            c = self.source.get_char()
            if self.source.eof:
                break
            if c in newline:
                newline_count += 1

        if newline_count >= 2:
            return self
        else:
            return " "


def MultiParser_GetNode(self):
    length = 0
    while self.source.peak() == self.start_tolken and length < len(self.values) - 1:
        self.source.get_char()
        length += 1

    return self.values[length]


def MultiParser(values):
    """
    Latex likes to have the same character repeated mean some other character 
    This parser will return the nth value of of values
    for example if values is ['-','endash','emdash']
    the parser will read '-' as '-', '--' as 'endash' and '---' as 'emdash'
    """
    return type("MultiParser__",
                (Parser,),
                dict(values=values,
                     GetNode=MultiParser_GetNode),
                )


class CommentParser(Parser):
    mode = None

    def GetNode(self):
        comment = ""
        while self.source.peak(1) != '\n':
            comment += self.source.get_char()
            if self.source.eof:
                break

        if self.source.peak(2)[-1] not in " \t\n":
            self.source.get_char()

        # node.end_pos = self.source.get_pos()
        #self.end_tolken=self.parser.peak(1)
        self.add_child(comment)
        return self

    def get_element(self):
        return ""


class EndTolkenParser(Parser):
    def GetNode(self):

        while True:
            if self.source.eof:
                self.Critical("Reached end of file while waiting for end tolken {!r}.".format(self.end_tolken))
            elif self.source.peak(len(self.end_tolken)) == self.end_tolken:
                for i in range(len(self.end_tolken)):
                    self.source.get_char()
                    # self.end = self.parser.get_pos()
                    return self
                    #else:
                    #for t in self.rules["end_tolkens"]:
                    #if self.parser.peak(len(self.end_tolken))==t:
                    #    raise Exception("Found end tolken {!r} while looking for end tolken {!r}".format(t,self.end_tolken))

            t = Parser.GetNode(self)
            self.add_child(t)
        self.end_node = self.end_tolken


class GroupParser(EndTolkenParser):
    end_tolken="}"

class OptionalGroupParser(EndTolkenParser):
    end_tolken="]"

class InlineMathParser(EndTolkenParser):
    end_tolken="$"
    mode = "math"

class BeginEnvironment(Parser):
    args = 1
    defaults = {}

    def GetNode(self):

        assert (isinstance(self.start_tolken, CommandParser))
        env = self.start_tolken.children[0].children[0]

        env_info = self.GetEnvironment(env)

        if env_info is None:
            # suggestion = difflib.get_close_matches(env,self.__rules['all_c.keys(),n=1)
            suggestion = None

            msg = "Unknown Environment: '{}'".format(env)
            if suggestion:
                msg += ", did you mean '{}'?".format(suggestion[0])
            self.error(self.start_tolken, msg)
            return self.start_tolken

        elif hasattr(env_info, "GetNode"):
            self.ParseArguments(env_info, self.start_tolken)
            self.start_tolken.stop = self.source.get_pos()

            parser = env_info(self)
            parser.start_tolken = self.start_tolken
            node = parser.GetNode()

            return node

        else:
            self.error(self.start_tolken,
                       "Got {!r} for environment {}, no idea what to do with that"
                       .format(env_info, env))


def EnvironmentParser(args=0, defaults={}, mode=None, level = None, **kwargs):
    class EnvironmentParser_(Parser):

        def get_node_name(self):

            return Parser.get_node_name(self) + " " + repr(self.env)

        def GetNode(self):

            assert (isinstance(self.start_tolken, CommandParser))
            assert self.start_tolken.command == 'begin'
            self.env = self.start_tolken.children[0].children[0]

            #node = Environment(self.env)
            #node.start_tolken = self.start_tolken
            #node.element_info = self


            while True:
                if self.source.eof:
                    self.fatal(self.start_tolken,
                               "Reached end of file while "
                               "waiting for end of environment {!r}"
                               .format(self.env))

                t = Parser.GetNode(self)

                if isinstance(t, CommandParser):
                    if t.command == 'end':
                        if t.children[0].children[0] == self.env:
                            self.end_tolken = t
                            break

                self.add_child(t)
            return self

        # def __repr__(self):
        #            return "<",self.__class__.__name__,' ',self.env,">"


        def get_tag(self):
            return self.env

    EnvironmentParser_.args = args
    EnvironmentParser_.defaults = defaults
    EnvironmentParser_.mode = mode

    EnvironmentParser_.kwargs = kwargs
    if level is not None:
        EnvironmentParser_.level=level

    return EnvironmentParser_


class VerbParser(Parser):
    args = 0
    defaults = {}

    def GetNode(self):

        stop = self.source.get_char()

        self.info["start_tolken"] = stop

        string = ""
        while True:
            c = self.source.get_char()
            if c == stop:
                break

            string += c

        self.add_child(string)
        return self


def VerbatimParser_GetNode(self):
    node = self.node_type(self,**self.kwargs)
    while True:
        if self.source.eof:
            self.Critical("Reached end of file while waiting for end tolken {!r}.".format(self.end_tolken))
        elif self.source.peak(len(self.end_tolken)) == self.end_tolken:
            for i in range(len(self.end_tolken)):
                self.source.get_char()
            return node
        c = self.source.get_char()
        node.add_child(c)


def VerbatimParser(end_tolken, node_type, **kwargs):
    return type("VerbatimParser__",
                (Parser,),
                dict(args=0,
                     defaults={},
                     mode='verb',
                     node_type=node_type,
                     end_tolken=end_tolken,
                     kwargs=kwargs,
                     GetNode=VerbatimParser_GetNode,

                     )
                )


class CommandParser(Parser):
    mode = None

    def get_node_name(self):
        return Parser.get_node_name(self) + " " + repr(self.escape + self.command) + ' '

    def get_tag(self):
        return self.__class__.__name__  + repr(self.escape + self.command) + ' '

    def get_latex(self):
        return self.escape + self.command + "".join([get_latex(c) for c in self.children])

    def GetNode(self):
        cmd = self.source.get_char()
        if cmd in string.ascii_letters:
            while 1:
                p = self.source.peak()
                if p and p in string.ascii_letters:
                    cmd += self.source.get_char()
                else:
                    break


        command_info = self.GetCommand(cmd)


        self.start = self.start
        self.stop = self.source.get_pos()
        self.command = cmd
        self.escape = self.start_tolken
        self.element_info = command_info

        if command_info:

            print self.command, command_info

            if isinstance(command_info,basestring):
                return command_info


            if not hasattr(command_info, 'args'):
                raise Exception("Invalid Command Info for {!r} :{!r}"
                                .format(cmd, command_info))

            self.ParseArguments(command_info, self)

            self.stop = self.source.get_pos()



            if isinstance(command_info, type) and issubclass(command_info, Parser):

                parser = command_info(self)
                parser.start_tolken = self
                parser.escape = self.escape
                parser.command = self.command
                parser.children = self.children


                node = parser.GetNode()

            else:
                node = self

            if hasattr(node, "ModifyParser"):

                node.ModifyParser(self.parent)


            print self.command,node
            print self.command,isinstance(command_info, type) and issubclass(command_info, Parser)

            return node

        else:
            # suggestion = difflib.get_close_matches(cmd,self._Parser__cmds.keys(),n=1)
            suggestion = None

            msg = "Unknown Command: '{}{}'".format(self.start_tolken, cmd)

            if suggestion:
                msg += ", did you mean '{}{}'?".format(self.start_tolken, suggestion[0])
            self.error(self, msg)

            return ""


def MacroParser_get_node_name(self):
    return Parser.get_node_name(self) + " " + repr(self.command)

def MacroParser_GetNode(self):

    self.escape = self.parent.escape
    self.command = self.parent.command

    self.AddTrace(self.parent,self.macronode,logging.WARN,"From macro defined here")
    self.AddTrace(self.parent,self.start_tolken,logging.WARN,"From macro called here")


    self.info = self.start_tolken.info

    self.source = Reader(self.macrostring,"<MACRO>")

    while not self.source.eof:
        while True:
            child = Parser.GetNode(self)
            if child:
                self.add_child(child)
            if self.source.eof:
                break

    return self
    # node.start_tolken = self.start_tolken
    #node.start = self.start


def MacroParser(macroname, macrostring,macronode, args, arg_parsers):
    return type("MacroParser__",
                (CommandParser,),
                dict(GetNode=MacroParser_GetNode,
                     get_node_name = MacroParser_get_node_name,
                     command=macroname,
                     macrostring=macrostring,
                     macronode = macronode,
                     args=args,
                     arg_parsers=arg_parsers,
                     ))


def OptionalArgumentParser_GetNode(self):
    while 1:
        p = self.source.peak()
        if p not in [' \t']:
            break
    if p == '[':
        parser = OptionalGroupParser(self)
        parser.start_tolken = self.source.get_char()
        parser.start = self.source.get_pos()
        t = parser.GetNode()
    else:
        t = OptionalGroupParser(self)
        t.add_child(self.default)
    return t


def OptionalArgumentParser(default=""):
    return type(
        "OptionalArgumentParser__",
        (Parser,),
        dict(
            default=default,
            GetNode=OptionalArgumentParser_GetNode,
        )
    )


def ArgumentParser_GetNode(self):
    while 1:
        p = self.source.peak()
        if p not in [' \t']:
            break
    return Parser.GetNode(self)


def ArgumentParser(mode=None):
    return type(
        "OptionalArgumentParser__",
        (Parser,),
        dict(
            GetNode=ArgumentParser_GetNode,
            mode=mode,
        )
    )


def VerbatimArgumentParser_GetNode(self):
    while 1:
        p = self.source.peak()
        if p not in [' \t']:
            break
        self.source.get_char()

    count = 0
    s = ""
    while 1:
        c = self.source.get_char()

        s += c
        if c == '{':
            count += 1
        elif c == '}':
            count -= 1
        elif c == '\\':
            s += self.source.get_char()
        if count == 0:
            break
    assert s[0] == '{'
    assert s[-1] == '}'
    g = GroupParser(self)
    g.add_child(s[1:-1])
    return g


def VerbatimArgumentParser():
    return type(
        "VerbatimArgumentParser__",
        (Parser,),
        dict(
            GetNode=VerbatimArgumentParser_GetNode,
            mode='verb',
        )
    )


class CommandBase(Parser):

    def get_node_name(self):
        return "Command "+repr(self.command)+ " "

    def GetNode(self):
        return self

    def get_tag(self):
        return self.command

def Meta_init(self,parent):
    CommandParser.__init__(self,parent)
    self.command = parent.command
    self.escape = parent.escape


    self.children = parent.children



def Meta_get_meta(self):
        return self.command,tuple([get_latex(strip_group(n)) for n in self.children])


def Meta(args=0, defaults = None,arg_parsers = None):

    return type(
        "Meta__",
        (CommandBase,),
        dict(
            #__init__ = Meta_init,
            args = args,
            defaults = {} if defaults is None else defaults,
            arg_parsers = {} if arg_parsers is None else arg_parsers,
            GetNode = lambda self: self,
            get_meta = Meta_get_meta,
            get_element = lambda self: "",
            ),
        )

    #def get_element(self):
    #    return ""


    #def get_meta(self):

    #    return node.command,tuple([strip_group(n) for n in node.children])