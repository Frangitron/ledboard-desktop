from PySide6.QtCore import Qt, QRectF

from ledboarddesktop.scan.viewport.graphics_image_plane import GraphicsImagePlane
from ledboarddesktop.scan.viewport.interactors.abstract_graphicsview_interactor import AbstractGraphicsViewInteractor


class Navigator(AbstractGraphicsViewInteractor):
    def __init__(self, view, image_plane: GraphicsImagePlane):
        super().__init__(view)
        self.is_enabled = True

        self._image_plane = image_plane

        self._is_active = False
        self._zoom = 0
        self._drag_anchor = 0, 0
        self._frustum = QRectF(0, 0, self._view.size().width(), self._view.size().height())
        self._update_frustum()

    def _update_frustum(self):
        self._view.setSceneRect(self._frustum)
        self._view.fitInView(self._frustum, Qt.KeepAspectRatio)

    def fit(self):
        self._frustum = self._image_plane.boundingRect()
        self._update_frustum()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self._is_active = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self._is_active = False

    def mouseMoveEvent(self, event):
        if not self._is_active or not event.buttons() == Qt.MouseButton.LeftButton:
            return

        position = self._view.mapToScene(event.position().toPoint())
        delta = self._drag_anchor - position

        self._frustum.adjust(delta.x(), delta.y(), delta.x(), delta.y())
        self._update_frustum()

    def mousePressEvent(self, event):
        if not self._is_active:
            return

        self._drag_anchor = self._view.mapToScene(event.position().toPoint())

    def resizeEvent(self, event):
        # TODO
        """
        w, h = self.size().width(), self.size().height()
        if 0 in [w, h]:
            self.resize(self._last_size)
        delta = max(w / self._last_size.width(), h / self._last_size.height())
        self._set_viewer_zoom(delta)
        self._last_size = self.size()
        super(NodeViewer, self).resizeEvent(event)
        """

    def wheelEvent(self, event):
        if not self._is_active:
            return

        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 0.8

        position = self._view.mapToScene(event.position().toPoint())
        w = self._frustum.width() / factor
        h = self._frustum.height() / factor

        self._frustum = QRectF(
            position.x() - (position.x() - self._frustum.left()) / factor,
            position.y() - (position.y() - self._frustum.top()) / factor,
            w, h
        )
        self._update_frustum()
