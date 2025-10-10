from typing import Any

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPolygonF, QPen, QBrush, QColor

from ledboarddesktop.scan.viewport.interactors.abstract_graphicsview_interactor import AbstractGraphicsViewInteractor


class MaskDrawer(AbstractGraphicsViewInteractor):
    def __init__(self, view):
        super().__init__(view)
        self.is_enabled = True

        self.is_active = False
        self._temp_disable = False
        self._is_drawing = False

        color = QColor(128, 128, 128)

        pen = QPen(color)
        pen.setWidth(2)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)

        color.setAlpha(64)
        brush = QBrush(color)
        # brush.setStyle(Qt.BDiagPattern)

        self._polygon = QPolygonF()
        self._polygon_item = self._view.scene().addPolygon(self._polygon, pen, brush)
        self.reset()

    @property
    def mask_item(self):
        return self._polygon_item

    @property
    def mask(self) -> Any:
        return None
        mask = ScanMask()
        mask.points = [
            [int(self._polygon.at(i).x()), int(self._polygon.at(i).y())]
            for i in range(self._polygon.count())
        ]
        return mask

    def set_mask(self, mask: Any) -> None:
        return
        self._polygon = QPolygonF()
        for point in mask.points:
            self._polygon.append(QPoint(*point))
        self._polygon_item.setPolygon(self._polygon)

    def reset(self):
        self._polygon = QPolygonF()
        self._polygon_item.setPolygon(self._polygon)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self._temp_disable = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self._temp_disable = False

    def mousePressEvent(self, event):
        if self._temp_disable or not self.is_active:
            return

        position = self._view.mapToScene(event.position().toPoint())
        self._polygon.append(position)
        self._polygon_item.setPolygon(self._polygon)

    def mouseMoveEvent(self, event):
        return
        """
        if self._temp_disable or not self.is_active:
            return

        position = self._view.mapToScene(event.position().toPoint())
        polygon = self._polygon_item.polygon()
        if polygon.isEmpty():
            return

        polygon.last().setX(position.x())
        polygon.last().setY(position.y())
        self._polygon_item.setPolygon(polygon)
        """
