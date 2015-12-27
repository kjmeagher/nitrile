# -*- coding: utf-8 -*-
import cairo, pangocairo
import plugin_manager

import pango_cairo

import logging as log


class PangoCairoPDF(pango_cairo.PangoCairo):
    def __init__(self, filename):
        super(PangoCairoPDF, self).__init__()
        self.filename = filename
        self.scale = 1.  # dummy for compatibility with raster format
        log.info("{}: Writing PDF file: {!r}".format(self.__class__.__name__, self.filename))

    @staticmethod
    def GetExtensions():
        return ["pdf"]

    def NewPage(self, style):
        if self.pagenumber == -1:
            self.surf = cairo.PDFSurface(self.filename, style["page-width"], style["page-height"])
            self.context = cairo.Context(self.surf)
            self.pangocairo_context = pangocairo.CairoContext(self.context)

        else:
            self.surf.show_page()
        log.debug("{}: Wrote page: {!r}".format(self.__class__.__name__, self.pagenumber))
        self.pagenumber += 1

    def LastPage(self):
        self.surf.show_page()
        log.debug("{}: Finished with last page: {!r}".format(self.__class__.__name__, self.pagenumber))
        del self.surf
        del self.context
        del self.pangocairo_context


plugin_manager.output_plugins.append(PangoCairoPDF)
