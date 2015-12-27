class Element(object):
    def get_info(self):
        return {}


class Paragraph(Element):
    def __init__(self,inline,info):
        self.inline = inline
        self.info =info

    def get_inlines(self):
        return self.inline

    def get_text(self):
        return  self.inline

    def get_info(self):
        return self.info

class Inline(Element):
    pass

class InlineComposite(Element):
    def __init__(self,inlines,info):
        self.inlines = inlines
        self.info =info

    def get_inlines(self):
        return self.inlines

    def get_text(self):
        print repr(self.inlines)
        return  "".join([ s. get_text() for s in self.inlines])
            

    def get_info(self):
        return self.info

class InlineText(Element):
    def __init__(self,text,info):
        self.text =text
        self.info =info

    def get_text(self):
        return self.text

class InlineMath(Element):
    def __init__(self,math,info):
        self.math =math
        self.info =info

    def get_text(self):
        return self.text
