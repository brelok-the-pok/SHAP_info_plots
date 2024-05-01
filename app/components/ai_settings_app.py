from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class AISettingDialog(QMainWindow):
    def setupUi(self, Dialog, callback_function):
        self.callback_function = callback_function
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(327, 235)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
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
        self.verticalLayout_2.addWidget(self.labelTop)
        self.comboBoxVar1 = QtWidgets.QComboBox(Dialog)
        self.comboBoxVar1.setObjectName("comboBoxVar1")
        self.comboBoxVar1.addItem("")
        self.comboBoxVar1.addItem("")
        self.comboBoxVar1.addItem("")
        self.verticalLayout_2.addWidget(self.comboBoxVar1)
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
        self.verticalLayout_2.addWidget(self.checkBoxCategorical)
        self.comboBoxCategoricalVar = QtWidgets.QComboBox(Dialog)
        self.comboBoxCategoricalVar.setEnabled(False)
        self.comboBoxCategoricalVar.setObjectName("comboBoxCategoricalVar")
        self.comboBoxCategoricalVar.addItem("")
        self.comboBoxCategoricalVar.addItem("")
        self.comboBoxCategoricalVar.addItem("")
        self.verticalLayout_2.addWidget(self.comboBoxCategoricalVar)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelMinValue = QtWidgets.QLabel(Dialog)
        self.labelMinValue.setObjectName("labelMinValue")
        self.verticalLayout.addWidget(self.labelMinValue)
        self.horizontalSlider = QtWidgets.QSlider(Dialog)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setValue(30)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout.addWidget(self.horizontalSlider)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelMaxValue = QtWidgets.QLabel(Dialog)
        self.labelMaxValue.setObjectName("labelMaxValue")
        self.horizontalLayout_3.addWidget(self.labelMaxValue)
        self.depth_spin_box = QtWidgets.QSpinBox(Dialog)
        self.depth_spin_box.setMinimum(1)
        self.depth_spin_box.setMaximum(5)
        self.depth_spin_box.setValue(3)
        self.depth_spin_box.setObjectName("depth_spin_box")
        self.horizontalLayout_3.addWidget(self.depth_spin_box)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
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
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.pushButtonAcceptPlot.clicked.connect(self.send_settings)
        self.pushButtonCancelPlot.clicked.connect(self.dialog.close)

        self.retranslateUi(Dialog)
        self.checkBoxCategorical.toggled["bool"].connect(self.comboBoxCategoricalVar.setEnabled)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def send_settings(self):
        temperature = self.horizontalSlider.value() / 100
        depth = self.depth_spin_box.value()
        self.dialog.hide()
        self.callback_function(temperature, depth)
        self.dialog.close()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Ввод параметров"))
        self.labelTop.setText(
            _translate(
                "Dialog",
                "Выберите по какой переменной строить график, границы изучения и числа отслеживаемых переменных",
            )
        )
        self.comboBoxVar1.setItemText(0, _translate("Dialog", "Переменная 1"))
        self.comboBoxVar1.setItemText(1, _translate("Dialog", "Переменная 2"))
        self.comboBoxVar1.setItemText(2, _translate("Dialog", "Переменная 3"))
        self.checkBoxCategorical.setText(_translate("Dialog", "По категориям"))
        self.comboBoxCategoricalVar.setItemText(0, _translate("Dialog", "Переменная 1"))
        self.comboBoxCategoricalVar.setItemText(1, _translate("Dialog", "Переменная 2"))
        self.comboBoxCategoricalVar.setItemText(2, _translate("Dialog", "Переменная 3"))
        self.labelMinValue.setText(
            _translate("Dialog", "Темперетура (Больше - креативнее)")
        )
        self.labelMaxValue.setText(_translate("Dialog", "Глубина"))
        self.pushButtonAcceptPlot.setText(_translate("Dialog", "Запустить"))
        self.pushButtonCancelPlot.setText(_translate("Dialog", "Отмена"))
