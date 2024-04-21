from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QGraphicsView,
    QMainWindow,
    QTextEdit,
)
from app.schemes.plot_settings_app import PlotSettings
from app.constants import PLOT_SETTINGS_ERROR_MESSAGE


class PlotDataDialog(QMainWindow):
    def setupUi(self, dialog, columns, categorical, min_max, callback_function):
        self.dialog = dialog
        self.minMax = min_max
        self.columns = columns
        self.categorical = categorical
        self.callback_function = callback_function

        dialog.resize(460, 200)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTop = QtWidgets.QLabel(dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTop.sizePolicy().hasHeightForWidth())
        self.labelTop.setSizePolicy(sizePolicy)
        self.labelTop.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.labelTop.setWordWrap(True)
        self.labelTop.setObjectName("labelTop")
        self.verticalLayout.addWidget(self.labelTop)
        self.comboBoxVar1 = QtWidgets.QComboBox(dialog)
        self.comboBoxVar1.setObjectName("comboBoxVar1")
        self.comboBoxVar1.addItem("")
        self.comboBoxVar1.addItem("")
        self.comboBoxVar1.addItem("")
        self.verticalLayout.addWidget(self.comboBoxVar1)
        self.checkBoxCategorical = QtWidgets.QCheckBox(dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.checkBoxCategorical.sizePolicy().hasHeightForWidth()
        )
        self.checkBoxCategorical.setSizePolicy(sizePolicy)
        self.checkBoxCategorical.setObjectName("checkBoxCategorical")
        self.verticalLayout.addWidget(self.checkBoxCategorical)
        self.comboBoxCategoricalVar = QtWidgets.QComboBox(dialog)
        self.comboBoxCategoricalVar.setEnabled(False)
        self.comboBoxCategoricalVar.setObjectName("comboBoxCategoricalVar")
        self.comboBoxCategoricalVar.addItem("")
        self.comboBoxCategoricalVar.addItem("")
        self.comboBoxCategoricalVar.addItem("")
        self.verticalLayout.addWidget(self.comboBoxCategoricalVar)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelMinValue = QtWidgets.QLabel(dialog)
        self.labelMinValue.setObjectName("labelMinValue")
        self.horizontalLayout_2.addWidget(self.labelMinValue)
        self.doubleSpinBoxMinValue = QtWidgets.QDoubleSpinBox(dialog)
        self.doubleSpinBoxMinValue.setObjectName("doubleSpinBoxMinValue")
        self.horizontalLayout_2.addWidget(self.doubleSpinBoxMinValue)
        self.labelMaxValue = QtWidgets.QLabel(dialog)
        self.labelMaxValue.setObjectName("labelMaxValue")
        self.horizontalLayout_2.addWidget(self.labelMaxValue)
        self.doubleSpinBoxMaxValue = QtWidgets.QDoubleSpinBox(dialog)

        self.doubleSpinBoxMaxValue.setObjectName("doubleSpinBoxMaxValue")
        self.horizontalLayout_2.addWidget(self.doubleSpinBoxMaxValue)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonAcceptPlot = QtWidgets.QPushButton(dialog)
        self.pushButtonAcceptPlot.setObjectName("pushButtonAcceptPlot")
        self.horizontalLayout.addWidget(self.pushButtonAcceptPlot)
        self.pushButtonCancelPlot = QtWidgets.QPushButton(dialog)
        self.pushButtonCancelPlot.setObjectName("pushButtonCancelPlot")
        self.horizontalLayout.addWidget(self.pushButtonCancelPlot)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.comboBoxVar1.clear()
        self.comboBoxVar1.addItems(columns[0 : len(columns) - 1])

        self.comboBoxCategoricalVar.clear()
        self.comboBoxCategoricalVar.addItems(categorical[0 : len(categorical) - 1])

        self.comboBoxVar1.currentIndexChanged.connect(self.change_boundaries)

        self.pushButtonCancelPlot.clicked.connect(self.close_button)
        self.pushButtonAcceptPlot.clicked.connect(self.send_plot_data)

        self.changeSpinBoxes(min_max[0][0], min_max[1][0])

        self.retranslateUi(dialog)
        self.checkBoxCategorical.toggled["bool"].connect(
            self.comboBoxCategoricalVar.setEnabled
        )

        QtCore.QMetaObject.connectSlotsByName(dialog)

    def changeSpinBoxes(self, min_value, max_value):
        self.doubleSpinBoxMinValue.setMinimum(min_value)
        self.doubleSpinBoxMinValue.setMaximum(max_value)
        self.doubleSpinBoxMinValue.setValue(min_value)

        self.doubleSpinBoxMaxValue.setMinimum(min_value)
        self.doubleSpinBoxMaxValue.setMaximum(max_value)
        self.doubleSpinBoxMaxValue.setValue(max_value)

    def change_boundaries(self):
        column_index = self.comboBoxVar1.currentIndex()
        min_value = self.minMax[0][column_index]
        max_value = self.minMax[1][column_index]
        self.changeSpinBoxes(min_value, max_value)

    def close_button(self):
        self.dialog.close()

    def send_plot_data(self):
        column = self.comboBoxVar1.currentText()
        min_value = self.doubleSpinBoxMinValue.value()
        max_value = self.doubleSpinBoxMaxValue.value()

        is_category_plot = self.checkBoxCategorical.isChecked()
        category_column = (
            self.comboBoxCategoricalVar.currentText() if is_category_plot else ""
        )
        if is_category_plot and category_column == column:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Ошибка")
            msg.setText(PLOT_SETTINGS_ERROR_MESSAGE)
            msg.show()
            msg.exec_()
            return

        self.dialog.hide()

        settings = PlotSettings(
            column=column,
            min_value=min_value,
            max_value=max_value,
            category_column=category_column,
        )
        self.callback_function(settings)

        self.dialog.close()

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle("Параметры графиков")
        self.labelTop.setText(
            "Выберите по какой переменной строить график, границы изучения и числа отслеживаемых переменных"
        )

        self.checkBoxCategorical.setText(_translate("Dialog", "По категориям"))
        self.labelMinValue.setText(_translate("Dialog", "Минимум"))
        self.labelMaxValue.setText(_translate("Dialog", "Максимум"))
        self.pushButtonAcceptPlot.setText(_translate("Dialog", "Построить"))
        self.pushButtonCancelPlot.setText(_translate("Dialog", "Отмена"))
