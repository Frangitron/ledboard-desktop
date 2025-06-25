from pythonhelpers.singleton_metaclass import SingletonMetaclass

from ledboarddesktop.settings import Settings
from ledboarddesktop.threaded_board_communication.threaded_board_communicator import ThreadedBoardCommunicator


class Components(metaclass=SingletonMetaclass):
    def __init__(self):
        self.board_communicator = ThreadedBoardCommunicator()
        self.settings = Settings()
