import sys
import json
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar
from graph import CircuitView
from menu import SidebarMenu

with open("settings.json", "r", encoding="utf-8") as f:
    SETTINGS = json.load(f)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{SETTINGS['app'].get('title', 'ArdVisualizer')} {SETTINGS['file']['title']}")

        self.circuit_view = CircuitView()
        self.setCentralWidget(self.circuit_view)

        self.toolbar = QToolBar("Główny pasek")
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Wczytanie panelu z pliku menu.py
        self.sidebar = SidebarMenu("Komponenty", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar)
        self.sidebar.hide()
        self.sidebar.setMinimumWidth(400)
        self.sidebar.setStyleSheet("font-size: 16px;")

        toggle_action = self.toolbar.addAction("☰ Menu")
        self.toolbar.setStyleSheet("font-size: 16px;")
        toggle_action.triggered.connect(self.toggle_sidebar)

    def toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())

def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    if SETTINGS["app"].get("fullscreen", False):
        window.showMaximized()
    else:
        width, height = SETTINGS["app"].get("window_size", [800, 600])
        window.resize(width, height)
        window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()