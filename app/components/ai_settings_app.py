from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class AISettingDialog(QMainWindow):
    def setupUi(self, Dialog, columns, category_columns, callback_function):
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

        self.checkBoxType = QtWidgets.QCheckBox(Dialog)
        self.checkBoxType.setObjectName("checkBoxType")

        self.verticalLayout_2.addWidget(self.labelTop)
        self.verticalLayout_2.addWidget(self.checkBoxType)

        self.comboBoxVar1 = QtWidgets.QComboBox(Dialog)
        self.comboBoxVar1.setObjectName("comboBoxVar1")
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
        sizePolicy.setHeightForWidth(self.checkBoxType.sizePolicy().hasHeightForWidth())
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

        self.checkBoxType.toggled["bool"].connect(self.checkBoxCategorical.setEnabled)  # type: ignore
        self.checkBoxType.toggled["bool"].connect(self.comboBoxVar1.setEnabled)  # type: ignore
        self.comboBoxVar1.setDisabled(True)
        self.checkBoxCategorical.setDisabled(True)

        self.pushButtonAcceptPlot.clicked.connect(self.send_settings)
        self.pushButtonCancelPlot.clicked.connect(self.dialog.close)

        self.comboBoxVar1.clear()
        self.comboBoxVar1.addItems(columns)

        self.comboBoxCategoricalVar.clear()
        self.comboBoxCategoricalVar.addItems(category_columns)

        self.retranslateUi(Dialog)
        self.checkBoxCategorical.toggled["bool"].connect(self.comboBoxCategoricalVar.setEnabled)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def on_type_state_changed(self):
        self.checkBoxCategorical.setDisabled(True)

    def send_settings(self):
        temperature = self.horizontalSlider.value() / 100
        depth = self.depth_spin_box.value()
        self.dialog.hide()

        category_feature_name = None
        if self.checkBoxCategorical.isChecked():
            category_feature_name = self.comboBoxCategoricalVar.currentText()

        self.callback_function(
            temperature,
            depth,
            self.checkBoxType.isChecked(),
            self.comboBoxVar1.currentText(),
            category_feature_name,
        )
        self.dialog.close()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Ввод параметров"))
        self.labelTop.setText(
            _translate(
                "Dialog",
                "Выберите по какой параметры LLM модели и параметры деревьев решений",
            )
        )

        self.checkBoxCategorical.setText(_translate("Dialog", "По категориям"))
        self.checkBoxType.setText(_translate("Dialog", "Дерево важности"))

        self.labelMinValue.setText(
            _translate("Dialog", "Темперетура (Больше - креативнее)")
        )
        self.labelMaxValue.setText(_translate("Dialog", "Глубина"))
        self.pushButtonAcceptPlot.setText(_translate("Dialog", "Запустить"))
        self.pushButtonCancelPlot.setText(_translate("Dialog", "Отмена"))
