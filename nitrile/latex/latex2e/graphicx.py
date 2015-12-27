from package_defs import *

from package import Package

class graphicx(Package):

    text_cmds = {
        "rotatebox"   : null(3,{0:""}),
        "scalebox"    : null(3,{1:""}),
        "reflectbox"  : null(1),
        "resizebox"   : null(3),
        "resizebox*"  : null(3),
        "includegraphics" : null(3,{0:"",1:""}),
        "includegraphics*" : null(3,{0:"",1:""}),
        "graphicspath" : null(1),
        "DeclareGraphicsExtensions" :null(1),
        "DeclareGraphicsRule" : null(4),
        }
        

        
