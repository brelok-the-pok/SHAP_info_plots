from PyQt5 import QtCore, QtGui, QtWidgets


class PlotContainer(QtWidgets.QLabel):
    def __init__(self, pixmap, parent=None):
        super(PlotContainer, self).__init__(parent)
        self._pixmap = QtGui.QPixmap(pixmap)
        self.setMinimumSize(1, 1)

    def resizeEvent(self, event):
        w = min(self.width(), self._pixmap.width())
        h = min(self.height(), self._pixmap.height())
        self.setPixmap(self._pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
