class InstanceMemory:
    def __init__(self):
        self.instances = list()

class MultipleInstanceError(Exception): pass

class UnknownAlignError(Exception): pass

class OutOfListBox(Exception): pass
