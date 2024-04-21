from PyQt5.QtGui import QFontMetrics
from app.constants import (
    CHAT_USER_STYLESHEET,
    CHAT_LLM_STYLESHEET
)
from PyQt5 import QtCore, QtWidgets


class TextChatScrollArea(QtWidgets.QScrollArea):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self._widget = QtWidgets.QWidget()
        self._layout = QtWidgets.QVBoxLayout()
        self.setWidgetResizable(True)

    def add_text(self, text):
        text_widget = QtWidgets.QLabel(self)
        flags = QtCore.Qt.TextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
            |
            QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard
        )
        text_widget.setTextInteractionFlags(flags)

        if self.counter % 2:
            alignment = QtCore.Qt.AlignmentFlag.AlignLeft
            style = CHAT_LLM_STYLESHEET
        else:
            alignment = QtCore.Qt.AlignmentFlag.AlignRight
            style = CHAT_USER_STYLESHEET

        text_widget.setAlignment(alignment)

        self.counter += 1
        text_widget.setText(text)
        text_widget.setStyleSheet(style)


        fontMetrics = QFontMetrics(text_widget.font())
        textSize = fontMetrics.size(0, text)
        text_widget.setFixedHeight(textSize.height() + 10)

        self._layout.addWidget(text_widget)
        self._widget.setLayout(self._layout)
        self.setWidget(self._widget)
