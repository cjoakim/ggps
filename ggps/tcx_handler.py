
import xml.sax

from ggps.sax import BaseHandler
from ggps.trackpoint import Trackpoint


class TcxHandler(BaseHandler):

    root_tag = 'TrainingCenterDatabase'
    tkpt_path = root_tag + "|Activities|Activity|Lap|Track|Trackpoint"
    tkpt_path_len = len(tkpt_path)

    @classmethod
    def parse(cls, filename, augment=False):
        handler = TcxHandler(augment)
        xml.sax.parse(open(filename), handler)
        return handler

    def __init__(self, augment=False):
        BaseHandler.__init__(self, augment)

    def startElement(self, tag_name, attrs):
        self.heirarchy.append(tag_name)
        self.reset_curr_text()
        path = self.curr_path()

        if path == self.tkpt_path:
            self.curr_tkpt = Trackpoint()
            self.trackpoints.append(self.curr_tkpt)
            return

    def endElement(self, tag_name):
        path = self.curr_path()

        if self.tkpt_path in path:
            if len(path) > self.tkpt_path_len:
                retain = True
                if tag_name == 'Extensions':
                    retain = False
                elif tag_name == 'Position':
                    retain = False
                elif tag_name == 'TPX':
                    retain = False
                elif tag_name == 'HeartRateBpm':
                    retain = False
                elif tag_name == 'Value':
                    tag_name = 'HeartRateBpm'

                if retain:
                    self.curr_tkpt.set(tag_name, self.curr_text)

        self.heirarchy.pop()
        self.reset_curr_text()

    def endDocument(self):
        self.end_reached = True
        if self.augment:
            for idx, t in enumerate(self.trackpoints):
                if idx == 0:
                    self.set_first_trackpoint(t)
                self.augment_with_calculations(idx, t)

    def augment_with_calculations(self, idx, t):
        t.set('seq', "{0}".format(idx + 1))
        self.meters_to_feet(t, 'altitudemeters', 'altitudefeet')
        self.meters_to_miles(t, 'distancemeters', 'distancemiles')
        self.meters_to_km(t, 'distancemeters', 'distancekilometers')
        self.runcadence_x2(t)
        self.calculate_elapsed_time(t)
