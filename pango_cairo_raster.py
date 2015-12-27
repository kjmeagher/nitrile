# -*- coding: utf-8 -*-
import math
import cairo,pangocairo
from cStringIO import StringIO
import zipfile,tarfile
#from PIL import Image

import pango_cairo
import plugin_manager

class PangoCairoRaster(pango_cairo.PangoCairo):
    

    zip_extensions = ["cbz"]
    tar_extensions = ["cbt"]

    def __init__(self,filename):
        super(PangoCairoRaster,self).__init__()
        self.filename = filename

        self.outfiles =[]


    def __write_file(self):
        image_file = StringIO()
        self.surf.write_to_png(image_file)
        self.outfiles.append(image_file.getvalue())

    @classmethod
    def GetExtensions(cls):
        return cls.tar_extensions + cls.zip_extensions

    def NewPage(self,style):
        if self.pagenumber >= 0:
            self.__write_file()

        self.pagenumber+=1

        self.scale = style["pixels-per-inch"]/72.

        self.surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 
                                       int(style["page-width"] * self.scale),
                                       int(style["page-height"] * self.scale))
        self.context = cairo.Context(self.surf)
        self.context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        self.pangocairo_context = pangocairo.CairoContext(self.context)


    def LastPage(self):
        self.__write_file()

        digits = int(math.log10(len(self.outfiles)))+1

        extension  = self.filename.split('.')[-1].lower()
        

        if extension in self.zip_extensions:
            cbz_file = zipfile.ZipFile(self.filename,'w')     
            for n,f in enumerate(self.outfiles):
                cbz_file.writestr("%0*d.png"%(digits,n),f)
            cbz_file.close()
                        
        elif extension in self.tar_extensions:
            tar = tarfile.open(self.filename, 'w')        
            for n,data in enumerate(self.outfiles):
                tarinfo = tarfile.TarInfo("%0*d.png"%(digits,n))
                tarinfo.size = len(data)
                tar.addfile(tarinfo, StringIO(data))                    
            tar.close()                

        else:
            raise Exception("Unknown File extention! %s", repr(extension))


plugin_manager.output_plugins.append(PangoCairoRaster)
