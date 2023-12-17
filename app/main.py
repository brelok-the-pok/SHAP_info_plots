import sys
from PyQt5 import QtWidgets

from app.components.main_app import MainApp


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    app.exec_()


if __name__ == "__main__":
    main()
