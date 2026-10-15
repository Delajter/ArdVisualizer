import json
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPathItem
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath
from PySide6.QtCore import Qt

with open("settings.json", "r", encoding="utf-8") as f:
    SETTINGS = json.load(f)


class Wire(QGraphicsPathItem):
    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item

        self.setPen(QPen(QColor(SETTINGS["scene"]["wire_color"]), 3))
        self.setZValue(-1)
        self.update_path()

    def update_path(self):
        p1 = self.start_item.sceneBoundingRect().center()
        p2 = self.end_item.sceneBoundingRect().center()

        path = QPainterPath()
        path.moveTo(p1)
        mid_x = (p1.x() + p2.x()) / 2
        path.lineTo(mid_x, p1.y())
        path.lineTo(mid_x, p2.y())
        path.lineTo(p2)
        self.setPath(path)


class Component(QGraphicsRectItem):
    def __init__(self, x, y):
        super().__init__(0, 0, 80, 40)
        self.setPos(x, y)
        self.setBrush(QColor(SETTINGS["scene"]["component_color"]))
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)
        self.wire = None

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionHasChanged and self.wire:
            self.wire.update_path()
        return super().itemChange(change, value)


class CircuitScene(QGraphicsScene):
    def drawBackground(self, painter, rect):
        cfg = SETTINGS["scene"]
        grid = cfg["grid"]

        painter.fillRect(rect, QColor(cfg["background_color"]))

        left, right = int(rect.left()), int(rect.right())
        top, bottom = int(rect.top()), int(rect.bottom())

        minor_step = grid["minor_step"]
        painter.setPen(QPen(QColor(grid["minor_color"]), 1))
        for x in range(left - (left % minor_step), right, minor_step):
            painter.drawLine(x, top, x, bottom)
        for y in range(top - (top % minor_step), bottom, minor_step):
            painter.drawLine(left, y, right, y)

        major_step = grid["major_step"]
        painter.setPen(QPen(QColor(grid["major_color"]), 2))
        for x in range(left - (left % major_step), right, major_step):
            painter.drawLine(x, top, x, bottom)
        for y in range(top - (top % major_step), bottom, major_step):
            painter.drawLine(left, y, right, y)


from PySide6.QtGui import QCursor  # Dodaj to na górze pliku w importach z QtGui


class CircuitView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = CircuitScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

        # Wczytanie wymiarów sceny z settings.json
        scene_width, scene_height = SETTINGS["scene"]["size"]
        self.setSceneRect(0, 0, scene_width, scene_height)

        self._is_panning = False
        self._pan_start_pos = None

        self.comp1 = Component(100, 100)
        self.comp2 = Component(400, 300)
        self.wire = Wire(self.comp1, self.comp2)

        self.comp1.wire = self.wire
        self.comp2.wire = self.wire

        self.scene.addItem(self.comp1)
        self.scene.addItem(self.comp2)
        self.scene.addItem(self.wire)

    # --- Obsługa przesuwania siatki środkowym przyciskiem myszy ---

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self._is_panning = True
            self._pan_start_pos = event.position().toPoint()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self._is_panning = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self._is_panning:
            delta = event.position().toPoint() - self._pan_start_pos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self._pan_start_pos = event.position().toPoint()
            event.accept()
            return
        super().mouseMoveEvent(event)