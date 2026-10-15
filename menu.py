from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLineEdit, QScrollArea
from uklad import Uklad

class SidebarMenu(QDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)

        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.content_widget = QWidget()

        self.tmp_layout = QVBoxLayout(self.content_widget)

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.scroll_area = QScrollArea()
        self.kontener = QWidget()
        self.kontener.setLayout(self.layout)
        self.scroll_area.setWidget(self.kontener)
        self.scroll_area.setWidgetResizable(True)

        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("Szukaj")
        self.search_line_edit.setStyleSheet("font-size:18px; padding:10px; border-radius:10px;")
        self.tmp_layout.addWidget(self.search_line_edit)
        self.tmp_layout.addWidget(self.scroll_area)






        self.layout.addWidget(Uklad("arduino nano", "elements/arduino_nano.svg"),0,0)
        self.layout.addWidget(Uklad("arduino uno", "elements/arduino_uno.svg"),0,1)

        self.layout.addWidget(Uklad("nRF52840", "elements/nRF52840.svg"),1,0)
        self.layout.addWidget(Uklad("esp32", "elements/esp32.svg"),1,1)

        self.setWidget(self.content_widget)