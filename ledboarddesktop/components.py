from pythonhelpers.singleton_metaclass import SingletonMetaclass

from ledboarddesktop.board_detection.board_detector import BoardDetector


class Components(metaclass=SingletonMetaclass):
    def __init__(self):
        self.board_detector = BoardDetector()
