from PySide6.QtGui import QPixmap, QIcon, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class Uklad(QWidget):
    def __init__(self,name,path, parent=None):
        super().__init__(parent)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)

        self.setFixedSize(200,200)

        self.img_label = QLabel()
        # Generowanie pixmapy o wymiarach 200x200 bezpośrednio z SVG
        self.pixmap = QIcon(fr"{path}").pixmap(200, 200)
        self.img_label.setPixmap(self.pixmap)
        self.name_label = QLabel(f"{name}")
        self.name_label.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.img_label)
        self.mainLayout.addWidget(self.name_label)

