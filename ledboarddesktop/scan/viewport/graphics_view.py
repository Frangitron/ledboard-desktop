from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QFrame, QGraphicsView

from ledboarddesktop.scan.viewport.interactors.abstract_graphicsview_interactor import AbstractGraphicsViewInteractor


class GraphicsView(QGraphicsView):

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.setRenderHint(QPainter.Antialiasing, True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setMouseTracking(True)

        self.interactors: list[AbstractGraphicsViewInteractor] = list()

    def keyPressEvent(self, event):
        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.keyPressEvent(event)

        QGraphicsView.keyPressEvent(self, event)

    def keyReleaseEvent(self, event):
        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.keyReleaseEvent(event)

        QGraphicsView.keyReleaseEvent(self, event)

    def wheelEvent(self, event):
        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.wheelEvent(event)

        QGraphicsView.wheelEvent(self, event)

    def mousePressEvent(self, event):
        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.mousePressEvent(event)

        QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.setFocus()

        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.mouseMoveEvent(event)

        QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.mouseReleaseEvent(event)

        QGraphicsView.mouseReleaseEvent(self, event)

    def resizeEvent(self, event):
        for interactor in self.interactors:
            if interactor.is_enabled:
                interactor.resizeEvent(event)

        QGraphicsView.resizeEvent(self, event)
