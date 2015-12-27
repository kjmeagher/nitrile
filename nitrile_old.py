#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys,os
from copy import deepcopy 
#import pangocairo
#import ast
#import magic

import argparse
parser = argparse.ArgumentParser(description="Nitrile Description")
parser.add_argument("infile", help="The input file")
parser.add_argument("outfile", help="The output file")
group = parser.add_mutually_exclusive_group()
group.add_argument("-q", "--quiet", action="store_true")
group.add_argument("-v", "--verbosity", action="count",default=0,
                    help="increase output verbosity")
parser.add_argument("-i","--input-options",default=None,
                    help="options to pass to input plugin")
parser.add_argument("-E","--evince",action='store_true',
                    help="open evince to view the file after successfule completion")

args = parser.parse_args()



import logging
log = logging.getLogger()


ch = logging.StreamHandler(sys.stdout)
if args.verbosity==1:
    log.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)
elif args.verbosity==2:
    log.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
elif args.verbosity>=3:
    log.setLevel(logging.NOTSET)
    ch.setLevel(logging.NOTSET)
formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)







import plugin_manager
import Elements



import collections

def deep_update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = deep_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d




default_style = {   

    "page-width"    : 72*8.5,
    "page-height"   : 72*11,
    "margin-top"    : 72*1,
    "margin-bottom" : 72*1,
    "margin-left"   : 72*1,
    "margin-right"  : 72*1,

    "background-color" :(1,1,1),

    "margin-box": True,
    "margin-box-color": (1,0,0),
    "margin-box-width": 1,

    "pixels-per-inch" : 144,

    #"font-family":'DejaVu Sans',
    #"font-family":'DejaVu Serif',
    #"font-family" : "default",
    "font-family" : 'CMU Serif',


    "font-size":11,
    "font-style":"normal", #italic, oblique
    "font-variant":"normal",# small-caps
    "font-weight" : "normal", #bold, bolder, lighter,900

    "text-justify": False,
    "text-color":(0,0,0),
}


if args.input_options:
    input_options = dict( [ a.split('=') for a in args.input_options.split(',')])
else:
    input_options = {}

log.info("got input options %s"%repr(input_options))


input_filename = args.infile
input = plugin_manager.get_input_plugin(input_filename)(input_filename,input_options)
input_style = input.get_style()

output_filename = args.outfile
output = plugin_manager.get_output_plugin(output_filename)(output_filename)



root_style = deep_update(default_style,input_style)

#output = PangoCairoRaster("out.cbz")
#output = PangoCairoRaster("out.cbz")

def newpage(style):

    output.NewPage(style)

    if style["margin-box"]:
        output.FillRectangle(0,0,
                             style["page-width"], 
                             style["page-height"],
                             style["background-color"],
                         )

    if style["margin-box"]:
        output.LineRectangle(style["margin-left"],
                             style["margin-top"],
                             style["page-width"]-style["margin-right"]-style["margin-left"],
                             style["page-height"]-style["margin-bottom"]-style["margin-top"],
                             style["margin-box-color"],
                             style["margin-box-width"]
                         )


    return style["margin-left"],style["margin-top"] 

current_position = newpage(root_style)


#    string = fontname + "".join(symbols)
#   style["font-family"]=fontname

#lines = open("command.txt",'rt').readlines()

#lines = [ line.replace("<","&lt;").replace(">","&gt;").strip() for line in lines]
#lines = [ line.strip() for line in lines]

#lines.reverse()

#print lines

#print pango.parse_markup("<i>LATEX</i>")


#fonts.reverse()


root_element = input.get_elements()

#root_element.pprint()
#paragraphs .reverse()

#print paragraphs
#lines = fonts



        
def markup_safe(string):
    return string.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    
    
def get_element_text(element,style):


    if isinstance(element, basestring):
        return  markup_safe(element)



    text = ""
    attributes = {}

    if hasattr(element,"tag"):
        style_updates = style.get(element.tag,{})
    else:
        style_updates = {}

    #print element.tag,style_updates
    
    if style_updates:
        new_style = deep_update(deepcopy(style),style.get(element.tag,{}))
    else:
        new_style = style

    for attr in  ["font-family","size","style","weight","variant",
                   "stretch","foreground","background","underline",
                   "rise","strikethrough","lang"]:
        if new_style.get(attr,"") != style.get(attr,""):
            attributes[attr.replace("-","_")]=new_style[attr]


    if element.tag == 'symbol':
        assert len(element.children)==1      
        text +=  markup_safe(new_style.get('symbol',{}).get(element.children[0],u"\N{replacement character}"))


    elif element.tag == 'combining':
        for child in element.children:
            text += get_element_text(child,new_style)

            
        text += new_style.get('combining-char',{}).get(element.attr['char'],u"\N{replacement character}")


    else:      
        for child in element.children:           
            text += get_element_text(child,new_style)


    if attributes:
        text = "<span {}>{}</span>".format(" ".join( [ a+"='"+b+"'" for a,b in attributes.items()]),
                                           text)

    #print element.tag, repr(text)
        
    return text
    


def layout_element(element,style):
    global current_position


    print element.tag, style

    if getattr(element,"tag","")=="para":

        text = ""
        for child in element.children:
            text += get_element_text(child,style)

        


        allowed_box = (current_position[0],
                       current_position[1],
                       style["page-width"]-current_position[0]-style["margin-right"],
                       style["page-height"]-current_position[1]-style["margin-bottom"]
                   )
    


        print "PARA", repr(text)
        x,y,residule = output.Text(allowed_box,text,style)

        #output.LineRectangle(current_position[0],current_position[1],x,y,(0,1,0),1)

        if residule:
            current_position = newpage(style)

        
        #paragraphs.append( Elements.Paragraph( Elements.InlineText(residule,{}),paragraph.info))


        else:
            current_position = current_position[0],current_position[1]+y

    else:
        
        for child in element.children:
            
            if isinstance(child, basestring):
                print "STRING!", repr(child)
            else:
                layout_element(child,style)

layout_element(root_element,root_style)

    
"""

while paragraphs:



    paragraph = paragraphs.pop(0)

    style = default_style.copy()
    style.update(paragraph.get_info())

    #print repr(line)

    box = (current_position[0],
           current_position[1],
           style["page-width"]-current_position[0]-style["margin-right"],
           style["page-height"]-current_position[1]-style["margin-bottom"]
           )

    x,y,residule = output.Text(box,paragraph.get_text(),style)


    output.LineRectangle(current_position[0],current_position[1],x,y,(0,1,0),1)

    if residule:
        current_position = newpage(style)
        
        #paragraphs.append( Elements.Paragraph( Elements.InlineText(residule,{}),paragraph.info))


    else:
        current_position = current_position[0],current_position[1]+y




output.LastPage()
"""


if args.evince:
    s= "evince {}".format(output_filename)
    print s
    os.system(s)
