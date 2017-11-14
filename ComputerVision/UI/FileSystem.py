import os

class Basefilepath(object):
    def __init__(self, *args):
        self.setSystempath()
        self.setFilepath()

    def setSystempath(self, path=None):
        if not path:
            self.systempath = os.path.abspath(".")
        else:
            pass

    def getSystempath(self):
        return self.systempath

    def setFilepath(self, path=None):
        if not path:
            self.filepath = os.path.abspath(".")
        else:
            pass

    def getFilepath(self):
        return self.filepath