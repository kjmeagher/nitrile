
import plugin_manager

class PangoCairoFontInputPlugin(object):
    def __init__(filename,options):


#get font families:
font_map = pangocairo.cairo_font_map_get_default()
families = font_map.list_families()

# to see family names:
fonts = sorted([f.get_name() for f in   font_map.list_families()])
#print fonts


paragraphs = [ (font,{"font-family":font}) for font in fonts]
