from PySide6.QtCore import QRect, QSize, QPoint, Qt
from PySide6.QtWidgets import QRubberBand

from ledboarddesktop.scan.viewport.interactors.abstract_graphicsview_interactor import AbstractGraphicsViewInteractor


class DetectionPointSelector(AbstractGraphicsViewInteractor):

    def __init__(self, view):
        super().__init__(view)

        self.is_enabled = True
        self._is_active = False
        self._temp_disable = False

        self._rubber_band = QRubberBand(QRubberBand.Rectangle, self._view)
        self._top_left = QPoint()
        self._bottom_right = QPoint()

    def mousePressEvent(self, event):
        if self._temp_disable:
            return

        self._top_left = event.pos()
        self._rubber_band.setGeometry(QRect(self._top_left, QSize()))
        self._rubber_band.show()

    def mouseMoveEvent(self, event):
        if self._temp_disable:
            return

        if event.buttons():
            self._is_active = True
        else:
            return

        self._bottom_right = event.pos()
        self._rubber_band.setGeometry(QRect(self._top_left, self._bottom_right).normalized())

    def mouseReleaseEvent(self, event):
        if self._temp_disable:
            return

        self._rubber_band.hide()

        if self._is_active:
            self._is_active = False

            top_left = self._view.mapToScene(self._top_left).toPoint()
            bottom_right = self._view.mapToScene(self._bottom_right).toPoint()
            rect = QRect(top_left, bottom_right)

            for item in self._view.scene().items():
                if not hasattr(item, "detection_point"):
                    continue

                if rect.contains(item.pos().toPoint()):
                    item.setSelected(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self._temp_disable = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self._temp_disable = False
