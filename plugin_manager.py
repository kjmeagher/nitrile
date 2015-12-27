import logging

input_plugins = []
output_plugins = []

import nitrile.latex.latex
import TextReader
#import LatexReader
#import ParseLatex
import pango_cairo_pdf
import pango_cairo_raster
import magic

def __get_plugin(plugin_list,string,filename):


    extension = filename.split('.')[-1].lower()



    for plugin in plugin_list:
        plugin_exts = plugin.GetExtensions()
        logging.debug("plugin {} has extensions: {}".format(plugin.__name__,repr(plugin_exts)))
        if  extension in plugin_exts:
            logging.info("Based on %s file %r extension %r, selected %s plugin %r",
                         string,filename,extension,string,plugin.__name__)
            return plugin

    print plugin_list
    raise Exception("could not find %s with extension: %r"
                    %(string,extension))


def get_output_plugin(filename):
    return  __get_plugin(output_plugins,'output',filename)

def get_input_plugin(filename):
    p = __get_plugin(input_plugins,'input',filename)

    mime = magic.from_file(filename,mime=True)

    if mime in p.GetMimeTypes():
        logging.info("%s file %s has mimetype %r, which input plugin %r supports","input",filename, mime,p.__name__)
    else:
        logging.warn("%s file %s has mimetype %r, which input plugin %r does not support!","input",filename, mime,p.__name__)

    return p 




