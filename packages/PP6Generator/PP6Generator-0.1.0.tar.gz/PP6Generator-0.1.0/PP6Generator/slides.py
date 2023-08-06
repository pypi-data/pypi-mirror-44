from uuid import uuid4

from lxml import etree

from .core import BaseElement
from .text import OneLanguageSongString


class SlideGroup(BaseElement):

    root_name = 'RVSlideGrouping'
    attributes = {
        'color': '0 0 0 0',
        'name': '',
        'uuid': str(uuid4())
    }

    def __init__(self, attributes={}):
        super(SlideGroup, self).__init__(attributes)

        self.slides = self.add_slide_groups()

        self.root.append(self.slides)

    def add_slide_groups(self):
        return self.array('slides')

    def add_slide(self, slide):
        self.slides.append(slide.root)

    def add_slides(self, slides):
        for slide in slides:
            self.add_slide(slide)

    def set_name(self, name):
        self.update_attribute('name', name)

    def set_color(self, color):
        self.update_attribute('color', color)


class Slide(BaseElement):

    root_name = 'RVDisplaySlide'
    attributes = {
        'UUID': str(uuid4()),
        'backgroundColor': '0 0 0 1',
        'chordChartPath': '',
        'drawingBackgroundColor': 'false',
        'enabled': 'true',
        'highlightColor': '0 0 0 0',
        'hotKey': '',
        'label': '',
        'notes': '',
        'socialItemCount': '1',
    }

    def __init__(self, attributes={}, elements=[]):
        super(Slide, self).__init__(attributes)

        self.cues = self.add_cues()
        self.display_elements = self.add_display_elements_root()

        self.root.append(self.cues)
        self.root.append(self.display_elements)

        if len(elements) > 0:
            self.add_display_elements(elements)

    def add_cues(self):
        return self.array('cues')

    def add_display_elements_root(self):
        return self.array('displayElements')

    def add_display_element(self, display_element):
        self.display_elements.append(display_element.root)

    def add_display_elements(self, display_elements):
        for display_element in display_elements:
            self.display_elements.append(display_element.root)

    def set_label(self, label):
        self.update_attribute('label', label)

    def set_notes(self, notes):
        self.update_attribute('notes', notes)

    def set_hot_key(self, hot_key):
        self.update_attribute('hot_key', hot_key)


class DisplayElement(BaseElement):
    pass


class Text(DisplayElement):

    root_name = 'RVTextElement'
    attributes = {
        'UUID': str(uuid4()),
        'additionalLineFillHeight': '0.000000',
        'adjustsHeightToFit': 'false',
        'bezelRadius': '0.000000',
        'displayDelay': '0.000000',
        'displayName': 'TextElement',
        'drawLineBackground': 'false',
        'drawingFill': 'false',
        'drawingShadow': 'true',
        'drawingStroke': 'false',
        'fillColor': '0 0 0 0',
        'fromTemplate': 'false',
        'lineBackgroundType': '0',
        'lineFillVerticalOffset': '0.000000',
        'locked': 'false',
        'opacity': '1.000000',
        'persistent': 'false',
        'revealType': '0',
        'rotation': '0.000000',
        'source': '',
        'textSourceRemoveLineReturnsOption': 'false',
        'typeID': '0',
        'useAllCaps': 'false',
        'verticalAlignment': '1',
    }

    def __init__(self, attributes={}, StringType=OneLanguageSongString):
        super(Text, self).__init__(attributes)

        self.rect_3d = Rect3D()
        self.shadow = Shadow()
        self.stroke = Stroke()
        self.string = StringType()

        self.root.append(self.rect_3d.root)
        self.root.append(self.shadow.root)
        self.root.append(self.stroke.root)
        self.root.append(self.string.root)

    def add_text(self, *args, **kwargs):
        if self.string:
            self.string.add_text(*args, **kwargs)


class Rect3D(BaseElement):

    root_name = 'RVRect3D'
    attributes = {
        'rvXMLIvarName': 'position'
    }

    CENTERED = '{30 40 0 1860 1000}'

    def __init__(self, attributes={}):
        super(Rect3D, self).__init__(attributes)

        self.root.text = self.CENTERED


class Shadow(BaseElement):

    root_name = 'shadow'
    attributes = {
        'rvXMLIvarName': 'shadow'
    }

    BASIC_SHADOW = '0.000000|0 0 0 0.3333333432674408|{5, -5}'

    def __init__(self, attributes={}):
        super(Shadow, self).__init__(attributes)

        self.root.text = self.BASIC_SHADOW


class Stroke(BaseElement):

    root_name = 'dictionary'
    attributes = {
        'rvXMLIvarName': 'stroke'
    }

    def __init__(self, attributes={}):
        super(Stroke, self).__init__(attributes)

        self.color = self.add_color()
        self.width = self.add_width()

        self.root.append(self.color)
        self.root.append(self.width)

    def add_color(self, color=(0, 0, 0, 1)):
        # Maybe make class in the future
        color = etree.Element(
            'NSColor',
            rvXMLDictionaryKey='RVShapeElementStrokeColorKey',
        )
        color.text = ' '.join(map(lambda x: str(x), color))
        return color

    def add_width(self, _width=1):
        # Maybe make class in the future
        width = etree.Element(
            'NSNumber',
            rvXMLDictionaryKey='RVShapeElementStrokeWidthKey',
            hint='integer',
        )
        width.text = str(_width)
        return width
