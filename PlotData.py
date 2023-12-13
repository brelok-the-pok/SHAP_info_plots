from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QGraphicsView,
                             QMainWindow, QTextEdit)


class PlotDataDialog(QMainWindow):
    def setupUi(self, Dialog, columns, categorical, minNmax, owner):
        self.dialog = Dialog
        self.minMax = minNmax
        self.columns = columns
        self.categorical = categorical
        self.owner = owner

        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 191)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTop = QtWidgets.QLabel(Dialog)
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
        self.comboBoxVar1 = QtWidgets.QComboBox(Dialog)
        self.comboBoxVar1.setObjectName("comboBoxVar1")
        self.comboBoxVar1.addItem("")
        self.comboBoxVar1.addItem("")
        self.comboBoxVar1.addItem("")
        self.verticalLayout.addWidget(self.comboBoxVar1)
        self.checkBoxCategorical = QtWidgets.QCheckBox(Dialog)
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
        self.comboBoxCategoricalVar = QtWidgets.QComboBox(Dialog)
        self.comboBoxCategoricalVar.setEnabled(False)
        self.comboBoxCategoricalVar.setObjectName("comboBoxCategoricalVar")
        self.comboBoxCategoricalVar.addItem("")
        self.comboBoxCategoricalVar.addItem("")
        self.comboBoxCategoricalVar.addItem("")
        self.verticalLayout.addWidget(self.comboBoxCategoricalVar)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelMinValue = QtWidgets.QLabel(Dialog)
        self.labelMinValue.setObjectName("labelMinValue")
        self.horizontalLayout_2.addWidget(self.labelMinValue)
        self.doubleSpinBoxMinValue = QtWidgets.QDoubleSpinBox(Dialog)
        self.doubleSpinBoxMinValue.setObjectName("doubleSpinBoxMinValue")
        self.horizontalLayout_2.addWidget(self.doubleSpinBoxMinValue)
        self.labelMaxValue = QtWidgets.QLabel(Dialog)
        self.labelMaxValue.setObjectName("labelMaxValue")
        self.horizontalLayout_2.addWidget(self.labelMaxValue)
        self.doubleSpinBoxMaxValue = QtWidgets.QDoubleSpinBox(Dialog)

        self.doubleSpinBoxMaxValue.setObjectName("doubleSpinBoxMaxValue")
        self.horizontalLayout_2.addWidget(self.doubleSpinBoxMaxValue)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonAcceptPlot = QtWidgets.QPushButton(Dialog)
        self.pushButtonAcceptPlot.setObjectName("pushButtonAcceptPlot")
        self.horizontalLayout.addWidget(self.pushButtonAcceptPlot)
        self.pushButtonCancelPlot = QtWidgets.QPushButton(Dialog)
        self.pushButtonCancelPlot.setObjectName("pushButtonCancelPlot")
        self.horizontalLayout.addWidget(self.pushButtonCancelPlot)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.comboBoxVar1.clear()
        self.comboBoxVar1.addItems(columns[0 : len(columns) - 1])

        self.comboBoxCategoricalVar.clear()
        self.comboBoxCategoricalVar.addItems(categorical[0 : len(categorical) - 1])

        self.comboBoxVar1.currentIndexChanged.connect(self.changeMinMax)

        print(self.comboBoxVar1.currentIndex())

        self.pushButtonCancelPlot.clicked.connect(self.closeButton)
        self.pushButtonAcceptPlot.clicked.connect(self.sendPlotData)

        self.doubleSpinBoxMinValue.valueChanged.connect(
            self.doubleSpinBoxMinValueValueChanged
        )
        self.doubleSpinBoxMaxValue.valueChanged.connect(
            self.doubleSpinBoxMaxValueValueChanged
        )

        self.changeSpinBoxes(minNmax[0][0], minNmax[1][0])

        self.retranslateUi(Dialog)
        self.checkBoxCategorical.toggled["bool"].connect(
            self.comboBoxCategoricalVar.setEnabled
        )

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def doubleSpinBoxMinValueValueChanged(self):
        print("A")
        pass

    def doubleSpinBoxMaxValueValueChanged(self):
        print("B")
        pass

    def changeSpinBoxes(self, min, max):
        self.doubleSpinBoxMinValue.setMinimum(min)
        self.doubleSpinBoxMinValue.setMaximum(max)
        self.doubleSpinBoxMinValue.setValue(min)

        self.doubleSpinBoxMaxValue.setMinimum(min)
        self.doubleSpinBoxMaxValue.setMaximum(max)
        self.doubleSpinBoxMaxValue.setValue(max)

    def changeMinMax(self):
        i = self.comboBoxVar1.currentIndex()
        min = self.minMax[0][i]
        max = self.minMax[1][i]
        self.changeSpinBoxes(min, max)

    def closeButton(self):
        self.dialog.close()

    def sendPlotData(self):
        colName = self.comboBoxVar1.currentText()
        minVal = self.doubleSpinBoxMinValue.value()
        maxVal = self.doubleSpinBoxMaxValue.value()
        categorical = self.checkBoxCategorical.isChecked()
        if categorical:
            categoricalColl = self.comboBoxCategoricalVar.currentText()
            if categoricalColl == colName:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Ошибка")
                msg.setText(
                    "Именна переменной варьирования и категориальной переменной не могут совпадать"
                )
                msg.show()
                msg.exec_()
                return
        else:
            categoricalColl = ""
        self.dialog.hide()
        self.owner.createPlots(colName, minVal, maxVal, categoricalColl)
        self.dialog.close()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelTop.setText(
            _translate(
                "Dialog",
                "Выберите по какой переменной строить график, границы изучения и числа отслеживаемых переменных",
            )
        )

        self.checkBoxCategorical.setText(_translate("Dialog", "По категориям"))
        self.labelMinValue.setText(_translate("Dialog", "Минимум"))
        self.labelMaxValue.setText(_translate("Dialog", "Максимум"))
        self.pushButtonAcceptPlot.setText(_translate("Dialog", "Построить"))
        self.pushButtonCancelPlot.setText(_translate("Dialog", "Отмена"))
