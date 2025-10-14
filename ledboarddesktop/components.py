from pythonhelpers.singleton_metaclass import SingletonMetaclass

from ledboardlib.scan.detection_executor import DetectionExecutor
from ledboardlib.scan.detector_options import DetectorOptions

from ledboarddesktop.settings import Settings
from ledboarddesktop.threaded_board_communication.threaded_board_communicator import ThreadedBoardCommunicator


class Components(metaclass=SingletonMetaclass):
    def __init__(self):
        self.board_list_widget = None
        self.board_communicator = ThreadedBoardCommunicator()
        self.settings = Settings()
        # FIXME move DetectorOptions to Settings
        self.scan_detection = DetectionExecutor(options=DetectorOptions(
            average_frame_count=4,
            blur_radius=9,
            camera_height=480,
            camera_index=5,
            camera_width=640,
        ))
