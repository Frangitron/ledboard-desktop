from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QMouseEvent, QKeyEvent, QWheelEvent, QResizeEvent


class AbstractGraphicsViewInteractor:

    def __init__(self, view):
        self.is_enabled = False
        self._view: QGraphicsView = view

    def keyPressEvent(self, event: QKeyEvent) -> None:
        pass

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        pass

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pass

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pass

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pass

    def resizeEvent(self, event: QResizeEvent) -> None:
        pass

    def wheelEvent(self, event: QWheelEvent) -> None:
        pass
