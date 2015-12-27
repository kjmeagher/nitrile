from package_defs import *
from package import Package


class color(Package):
    text_cmds = {
        "definecolor" : null(3),
        "color"       : null(2,{0:""}),
        "textcolor"   : null(2,{0:""}),
        "pagecolor"   : null(2,{0:""}),
        "nopagecolor" : null(),
        "colorbox"    : null(3,{0:""}),
        "fcolorbox"   : null(4,{0:""}),
        }
        

        
