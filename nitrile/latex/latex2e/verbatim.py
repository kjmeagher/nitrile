from ..parsers import *
from package import Package

class verbatim(Package):
    envs = {
        "verbatim"  : VerbatimParser("\end{verbatim}",CommentParser),#,env="verbatim"),
        "verbatim*" : None,
        "comment"   : VerbatimParser("\end{comment}",CommentParser),
    }

    text_cmds = {
        "verbatiminput" : None,
    }
