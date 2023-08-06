from base64 import b64encode

from .core import BaseString


class OneLanguageSongString(BaseString):

    DEFAULT_FONT = 'HelveticaNeueLTStd-BlkEx'

    # Specific RTF properties
    formatted_text = ('\\f0\\b\\fs160 \\cf1 \\outl0\\strokewidth-80 '
                      '\\strokec2 \\uc0\\u8232 '
                      '{text}')

    def __init__(self, attributes={}, text=None):
        super(OneLanguageSongString, self).__init__(attributes)

        if text:
            self.add_text(text)

    def prepare_rtf(self, text):
        base = self.base_rtf()

        text = '\\\n'.join(text)

        return base.format(text=text)

    def add_text(self, text):
        text = [self.rtf_encode(text) for text in text]

        text = self.prepare_rtf(text)
        text = b64encode(text.encode('utf-8'))
        self.add_text_to_root(text)


class TwoLanguagesSongString(BaseString):

    DEFAULT_FONT = 'HelveticaNeueLTStd-BlkEx'

    # Specific RTF properties
    formatted_text = ('\\f0\\b\\fs160 \\cf1 \\outl0\\strokewidth-80 '
                      '\\strokec2 \\uc0\\u8232 '
                      '{main_language}'
                      '\\uc0\\u8232 \\u8232 \n\\fs130 \\strokec2 '
                      '{other_language}')

    def __init__(self, attributes={}, main_language=None, other_language=None):
        super(TwoLanguagesSongString, self).__init__(attributes)

        if main_language and other_language:
            self.add_text(main_language, other_language)

    def prepare_rtf(self, main_language, other_language):
        base = self.base_rtf()

        main_language = '\\\n'.join(main_language)
        other_language = '\\\n'.join(other_language)

        return base.format(
            main_language=main_language,
            other_language=other_language
        )

    def add_text(self, main_language, other_language):
        main_language = [self.rtf_encode(text) for text in main_language]
        other_language = [self.rtf_encode(text) for text in other_language]

        text = self.prepare_rtf(main_language, other_language)
        text = b64encode(text.encode('utf-8'))
        self.add_text_to_root(text)
