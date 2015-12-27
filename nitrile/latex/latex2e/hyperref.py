from package_defs import *
from ..parsers import *
from package import Package

class URLParser(Parser):
    pass

#class hyperref:
#    def __init__(self):
#        self.args=2
#        self.arg_parsers = 

#    def convert(self,node):
#        return ""

class hyperref(Package):

    text_cmds = {
        "href" : null(3,{0:""}),
        "url" : null(1),
        "nolinkurl" : null(1),
        "hyperbaseurl" : null(1),
        "hyperimage" : null(2),
        "hyperdef" : null(3),
        "hyperref" : null(2,{0:""}),
        "hyperlink" : null(2),
        "hypertarget": null(2),
        "phantomsection": null(),
        "autoref" : null(),
        "autopageref" : null(1,),
        "autopageref*" : null(1),
        "ref" : null(1),
        "ref*" : null(1),
        "pageref" : null(1),
        "pageref*" : null(1),
        "autoref" : null(1),
        "autoref*" : null(1),

        "pdfstringdef" : null(2),
        "pdfbookmark" : null(3,{0:""}),
        "currentpdfbookmark" : null(2),
        "subpdfbookmark" : null(2),
        "belowpdfbookmark" : null(2),
        "texorpdfstring": null(2),
        "hypercalcbp" : null(1),
        "Acrobatmenu" : null(2),
        "TextField"  : null(2,{0:""}),
        "CheckBox" : null(2,{0:""}),
        "ChoiceMenu" : null(3,{0:""}),
        "PushButton"  : null(2,{0:""}),
        "Submit" :  null(2,{0:""}),
        "Reset" : null(2,{0:""}),

        "LayoutTextField" : null(2,{0:""}),
        "LayoutChoiceField" : null(2,{0:""}),
        "LayoutCheckField" : null(2,{0:""}),
        "MakeRadioField" : null(2,{0:""}),
        "MakeCheckField" : null(2,{0:""}),
        "MakeTextField" : null(2,{0:""}),
        "MakeChoiceField" : null(2,{0:""}),
        "MakeButtonField" : null(2,{0:""}),
        }
        

        
