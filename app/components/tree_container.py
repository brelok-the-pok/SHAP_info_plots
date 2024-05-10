from PyQt5 import QtWidgets, uic
from app.components.plot_container import PlotContainer
from app.constants import (
    STYLESHEET,
)


class TreeContainer(QtWidgets.QDialog):
    def __init__(self, paths):
        super(TreeContainer, self).__init__()
        uic.loadUi("../ui/tree_plot.ui", self)
        self.setWindowTitle("Графики дерева решений")
        self.show()  # Show the GUI
        self.paths = paths

        name = next(iter(paths))
        self.set_image(name)

        self.comboBox.clear()
        self.comboBox.addItems(list(paths))
        self.comboBox.setCurrentIndex(0)
        self.comboBox.currentIndexChanged.connect(self.change_image)

    def change_image(self):
        text = self.comboBox.currentText()
        if text:
            self.verticalLayout.removeWidget(self.pixmap)
            self.set_image(text)

    def set_image(self, name):
        pixmap = PlotContainer(self.paths[name])
        pixmap.setStyleSheet(STYLESHEET)
        pixmap.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
        )
        self.verticalLayout.addWidget(pixmap)
        self.pixmap = pixmap

    def resizeEvent(self, event):
        if hasattr(self, "pixmap"):
            self.pixmap.resizeEvent(event)
