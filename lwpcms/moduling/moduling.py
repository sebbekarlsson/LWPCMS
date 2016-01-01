class LWPCMSModule(object):
    def __init__(self):
        self.events = {}

    def register_event(self, event, func):
        try:
            self.events[str(event)] = func
        except KeyError:
            pass

    def event(self, event, data):
        if str(event) in self.events:
            return self.events[str(event)](data)
