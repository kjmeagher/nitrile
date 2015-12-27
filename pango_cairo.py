# -*- coding: utf-8 -*-
import cairo,pango,pangocairo

#get font families:
#font_map = pangocairo.cairo_font_map_get_default()
#families = font_map.list_families()

# to see family names:
#fonts = sorted([f.get_name() for f in   font_map.list_families()])
#print fonts

class PangoCairo(object):
    def __init__(self):
        self.pagenumber = -1



    def NewPage(self,style):
        raise NotImplemented

    def LineRectangle(self,x,y,size_x,size_y,color,width):
        self.context.rectangle(x*self.scale,y*self.scale,size_x*self.scale,size_y*self.scale)
        self.context.set_source_rgb(*color)
        self.context.set_line_width(width*self.scale)
        self.context.stroke()

    def FillRectangle(self,x1,y1,x2,y2,color):
        self.context.rectangle(x1*self.scale,y1*self.scale,
                               (x2-x1)*self.scale,(y2-x1)*self.scale)
        self.context.set_source_rgb(*color)
        self.context.fill()


    def Text(self,box,text,style):      


        box_x,box_y,box_width,box_height = box

        #print box_width,box_height
        


        layout = self.pangocairo_context.create_layout()

        font = pango.FontDescription(style["font-family"] + " " + str(style["font-size"]*self.scale))

        layout.set_font_description(font)

        pango_width = int(box_width*self.scale*pango.SCALE)
        pango_height = int(box_height*self.scale*pango.SCALE)

        layout.set_width(pango_width)
    
        layout.set_justify(style["text-justify"])
        #print repr(text)
        #attr = pango.parse_markup(text)
        #print attr
        #layout.set_text(text)


        #print "PANGO: ",text
        attr_list, plain_text, accel = pango.parse_markup(text)

        #print        [a for a in  attr_list.get_iterator()], repr(plain_text), repr(accel)

        #itr = attr_list.get_iterator()
        #while 1:
        #    print itr.range(),itr.get_font(),itr.get_attrs()

        #if not itr.next():
        #        break
            
            

            
            
        
        
        #layout.set_markup(text)

        layout.set_attributes(attr_list)
        layout.set_text(plain_text)

        
        #_,( _,_,extent_x,extent_y)=  layout.get_extents()
        ink_rect,logical_rect = layout.get_extents()
        _,_,extent_x,extent_y = logical_rect

        #print self.scale

        """
        self.LineRectangle((box_x+ink_rect[0]/pango.SCALE)/self.scale,
                           (box_y+ink_rect[1]/pango.SCALE)/self.scale,
                           (ink_rect[2]/pango.SCALE)/self.scale,
                           (ink_rect[3]/pango.SCALE)/self.scale,
                           (0,0,0),2)


        self.LineRectangle((box_x+logical_rect[0]/pango.SCALE)/self.scale,
                           (box_y+logical_rect[1]/pango.SCALE)/self.scale,
                           (logical_rect[2]/pango.SCALE)/self.scale,
                           (logical_rect[3]/pango.SCALE)/self.scale,
                           (0,1,0),1)

        """
        print repr(text[:78])
        print "B", extent_x/pango.SCALE,extent_y/pango.SCALE
        
        boxes = []


        if text and extent_y > pango_height:



            for i in range(len(text)):
                char_box = layout.index_to_pos(i)

                boxes.append((text[i],char_box))

                #print i,text[i],char_box , char_box[1] + char_box[3]

                if char_box[1] + char_box[3]> pango_height:
                    break

            residule = text[i:]
            
            #layout.set_text(text[:i] +' '+ 80*u'\N{no-break space}')
            layout.set_text(text[:i])
            print "PAGE"

        else:
            residule = ""

        _,( _,_,extent_x,extent_y)=  layout.get_extents()

        print "A",extent_x/pango.SCALE,extent_y/pango.SCALE
        
        self.context.move_to(box_x*self.scale,box_y*self.scale)       
        self.context.set_source_rgb(*style["text-color"])
        self.pangocairo_context.update_layout(layout)
        self.pangocairo_context.show_layout(layout)
        return float(extent_x)/self.scale/pango.SCALE,float(extent_y)/self.scale/pango.SCALE,residule

    def LastPage(self):
        raise NotImplemented
