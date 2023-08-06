from abc import ABCMeta, abstractmethod

from lxml import etree


class BaseElement:

    root_name = None
    attributes = {}

    def __init__(self, attributes={}):
        self.attributes.update(attributes)
        self.root = etree.Element(self.root_name, **self.attributes)

    def to_string(self):
        return etree.tostring(self.root).decode('utf-8')

    def array(self, name):
        return etree.Element('array', rvXMLIvarName=name)

    def update_attribute(self, attribute, value):
        self.attributes[attribute] = value
        self.root.set(attribute, value)


class BaseString(BaseElement, metaclass=ABCMeta):

    root_name = 'NSString'
    attributes = {
        'rvXMLIvarName': 'RTFData',
    }

    # Default RTF properties
    DEFAULT_FONT = ''
    base = ('{{{{'
            '{headers}\n'
            '{font_table}\n'
            '{color_table}\n'
            '{expanded_color_table}\n'
            '{pard}\n\n'
            '{formatted_text}'
            '}}}}')
    headers = '\\rtf1\\ansi\\ansicpg1252\\cocoartf1561\\cocoasubrtf600'
    font_table = '{{{{\\fonttbl\\f0\\fnil\\fcharset0 {font_name};}}}}'
    color_table = ('{{{{\\colortbl;'
                   '\\red255\\green255\\blue255;'
                   '\\red0\\green0\\blue0;}}}}')
    expanded_color_table = ('{{{{'
                            '\\*\\expandedcolortbl;;\\cssrgb\\c0\\c0\\c0;'
                            '}}}}')
    pard = ('\\pard\\tx560\\tx1120\\tx1680\\tx2240\\tx2800\\tx3360\\tx3920'
            '\\tx4480\\tx5040\\tx5600\\tx6160\\tx6720\\pardirnatural\\qc'
            '\\partightenfactor0')
    formatted_text = ('{formatted_text}')

    def __init__(self, attributes={}):
        super(BaseString, self).__init__(attributes)

    @abstractmethod
    def add_text(self, text):
        raise NotImplementedError('Define add_text to use this class')

    def add_text_to_root(self, text):
        self.root.text = text

    def rtf_encode(self, text):
        return ''.join([
            c if ord(c) < 128 else u'\\u' + str(ord(c)) for c in text
        ])

    def base_rtf(self):
        return self.base.format(
            headers=self.headers,
            font_table=self.font_table.format(font_name=self.DEFAULT_FONT),
            color_table=self.color_table,
            expanded_color_table=self.expanded_color_table,
            pard=self.pard,
            formatted_text=self.formatted_text,
        )

    def prepare_rtf(self, font_name, formatted_text):
        base = self.base_rtf()
        return base.format(font_name=font_name, formatted_text=formatted_text)
