from uuid import uuid4

from .core import BaseElement
from .slides import SlideGroup


class Presentation(BaseElement):

    root_name = 'RVPresentationDocument'
    attributes = {
        'CCLIArtistCredits': '',
        'CCLIAuthor': '',
        'CCLICopyrightYear': '',
        'CCLIDisplay': 'false',
        'CCLIPublisher': '',
        'CCLISongNumber': '',
        'CCLISongTitle': '',
        'backgroundColor': '0 0 0 1',
        'buildNumber': '16229',
        'category': 'Song',
        'chordChartPath': '',
        'docType': '0',
        'drawingBackgroundColor': 'false',
        'height': '1080',
        'lastDateUsed': '',
        'notes': '',
        'os': '2',
        'resourcesDirectory': '',
        'selectedArrangementID': '',
        'usedCount': '',
        'uuid': str(uuid4()),
        'versionNumber': '600',
        'width': '1920',
    }
    FILE_EXTENSION = 'pro6'

    def __init__(self, attributes={}):
        super(Presentation, self).__init__(attributes)

        self.timeline = Timeline()
        self.bible_reference = BibleReference()
        self.groups = self.add_groups()

        self.root.append(self.timeline.root)
        self.root.append(self.bible_reference.root)
        self.root.append(self.groups)

    def add_groups(self):
        return self.array('groups')

    def add_slide_group(self, slide_group):
        self.groups.append(slide_group.root)

    def current_slide_group(self):
        if len(self.groups.getchildren()) == 0:
            slide_group = SlideGroup()
            self.add_slide_group(slide_group)
        else:
            slide_group = self.groups.getchildren()[-1]

        return slide_group

    def add_slide(self, slide):
        slide_group = self.current_slide_group()
        slide_group.add_slide(slide)

    def add_slides(self, slides):
        slide_group = self.current_slide_group()
        slide_group.add_slides(slides)

    def set_title(self, title):
        self.update_attribute('title', title)

    def generate_file(self):
        filename = '{}.{}'.format(
            self.attributes['title'],
            self.FILE_EXTENSION
        )
        f = open(filename, 'w')
        f.write(self.to_string())
        f.close()

        return f


class Timeline(BaseElement):

    root_name = 'RVTimeline'
    attributes = {
        'duration': '0.000000',
        'loop': 'false',
        'playBackRate': '1.000000',
        'rvXMLIvarName': 'timeline',
        'selectedMediaTrackIndex': '0',
        'timeOffset': '0.000000',
    }

    def __init__(self, attributes={}):
        super(Timeline, self).__init__(attributes)

        self.time_cues = self.add_time_cues()
        self.media_tracks = self.add_media_tracks()

        self.root.append(self.time_cues)
        self.root.append(self.media_tracks)

    def add_time_cues(self):
        # Not implemented since we are not using them
        return self.array('timeCues')

    def add_media_tracks(self):
        # Not implemented since we are not using them
        return self.array('mediaTracks')


class BibleReference(BaseElement):

    root_name = 'RVBibleReference'
    attributes = {
        'bookIndex': '0',
        'bookName': '',
        'chapterEnd': '0',
        'chapterStart': '0',
        'rvXMLIvarName': 'bibleReference',
        'translationAbbreviation': '',
        'translationName': '',
        'verseEnd': '0',
        'verseStart': '0',
    }
