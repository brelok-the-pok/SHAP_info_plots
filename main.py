from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from pathlib import Path
from PlotData import PlotDataDialog
from funcLib import loadPickle, savePickle, getMinMax, plot_ice_plot, plot_top5_centered_importance, find_categorical

import sys
import os
import matplotlib.pyplot as plt
import tempfile
import shutil

stylesheet = 'border-bottom-width: 1px;border-bottom-style: solid;border-top-width: 1px;border-top-style: solid;border-left-width: 1px;border-left-style: solid;border-right-width: 1px;border-right-style: solid;border-radius: 0px;'


class Ui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('ui/main.ui', self)  # Load the .ui file

        self.show()  # Show the GUI

        # fileMenu
        # openFile
        self.openFile.setStatusTip('Открыть файл проекта')
        self.openFile.triggered.connect(self.OpenSavedFile)
        # saveFile
        self.saveFile.setStatusTip('Сохранить файл модели и выборки')
        self.saveFile.triggered.connect(self.SaveFile)
        # loadModel
        self.loadModel.setStatusTip('Открыть файл модели')
        self.loadModel.triggered.connect(self.OpenModel)
        # loadDataset
        self.loadDataset.setStatusTip('Открыть файл выборки')
        self.loadDataset.triggered.connect(self.OpenDataset)

        self.savePlot.triggered.connect(self.savePlots)

        self.pushButtonPlot.clicked.connect(self.plotGrath)

        self.comboBox.currentIndexChanged.connect(self.changeGrath)

        self.statusBar().showMessage('Ожидается загрузка модели и датасета')

        self.modelLoaded = False
        self.dataLoaded = False

        self.temp = tempfile.TemporaryDirectory()

        self.setWindowState(QtCore.Qt.WindowMaximized)
        # self.debug_start()

    def closeEvent(self, event):
        self.temp.cleanup()

    def debug_start(self):
        fname = 'D:\\Study\\diplom\\App\\Data\\obj'
        modelNdata = loadPickle(fname)
        self.model = modelNdata[0]
        self.data = modelNdata[1]

        self.CreateColumns(self.data)
        self.CreateRows(self.data)

        self.modelLoaded = True
        self.dataLoaded = True

        self.statusBar().showMessage('Загрузка датасета и модели произведена')

    def OpenSavedFile(self):
        home_dir = str(Path.cwd())
        fname = QFileDialog.getOpenFileName(self, 'Открыть файл', home_dir)
        if fname[0]:
            modelNdata = loadPickle(fname[0])

            if modelNdata is not None:

                try:
                    modelNdata[1].columns
                except:
                    self.statusBar().showMessage('Загруженный объект не является сохранённым')
                    return

                try:
                    modelNdata[0].classes_
                except:
                    self.statusBar().showMessage('Загруженный объект не является сохранённым')
                    return

                self.model = modelNdata[0]
                self.data = modelNdata[1]

                self.CreateColumns(self.data)
                self.CreateRows(self.data)

                self.modelLoaded = True
                self.dataLoaded = True

                self.statusBar().showMessage('Загрузка датасета и модели произведена')
            else:
                self.statusBar().showMessage('Ошибка загрузки, неверный файл')

    def SaveFile(self):
        if self.modelLoaded and self.dataLoaded:
            home_dir = str(Path.cwd())
            fname = QFileDialog.getSaveFileName(self, 'Сохранить файл', home_dir)

            if fname[0]:
                toSave = [self.model, self.data]
                savePickle(toSave, fname[0])
                self.statusBar().showMessage('Сохранение модели и датасета произведено')
        else:
            self.statusBar().showMessage('Не загружена модель или датасет')

    def OpenDataset(self):
        home_dir = str(Path.cwd())
        fname = QFileDialog.getOpenFileName(self, 'Открыть файл', home_dir)
        if fname[0]:
            data = loadPickle(fname[0])

            if data is not None:

                try:
                    data.columns
                except:
                    self.statusBar().showMessage('Загруженный объект не является выборкой')
                    return

                self.data = data
                self.CreateColumns(self.data)
                self.CreateRows(self.data)

                self.dataLoaded = True

                if self.modelLoaded:
                    self.statusBar().showMessage('Загрузка выборки произведена.')
                else:
                    self.statusBar().showMessage('Загрузка выборки произведена. Ожидается загрузка модели')
            else:
                self.statusBar().showMessage('Ошибка загрузки, неверный файл')

    def CreateColumns(self, data):
        vertLayout = QtWidgets.QVBoxLayout()
        groupBox = QtWidgets.QGroupBox()
        # groupBox.setStyleSheet(stylesheet)
        shape = data.shape

        temp = tempfile.TemporaryDirectory()

        for i in range(0, shape[1]):
            groupBox1 = QtWidgets.QGroupBox()
            groupBox1.setStyleSheet(stylesheet)

            minLabel = QtWidgets.QLabel(f'min: {round(data[data.columns[i]].min(), 2)}')
            meanLabel = QtWidgets.QLabel(f'mean: {round(data[data.columns[i]].mean(), 2)}')
            maxLabel = QtWidgets.QLabel(f'max: {round(data[data.columns[i]].max(), 2)}')

            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(minLabel)
            vbox.addWidget(meanLabel)
            vbox.addWidget(maxLabel)

            label = QtWidgets.QLabel()
            plt.clf()
            plot = plt.axes()
            plot.hist(x=data[data.columns[i]], label=data.columns[i])
            # plot.set_title(data.columns[i])
            plot.get_xaxis().set_ticklabels([])
            plot.get_yaxis().set_ticklabels([])
            plot.get_figure().savefig(temp.name + f"/img{i}.svg")

            pixmap = QtGui.QPixmap(temp.name + f"/img{i}.svg")
            pixmap = pixmap.scaledToHeight(200).scaledToWidth(200)
            label.setPixmap(pixmap)

            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(label)
            hbox.addLayout(vbox)

            # vertLayout.addLayout(hbox)
            hbox.setContentsMargins(0, 12, 0, 0)
            hbox.setStretch(0, 4)
            hbox.setStretch(1, 1)
            groupBox1.setLayout(hbox)
            groupBox1.setTitle(data.columns[i])
            vertLayout.addWidget(groupBox1)

        groupBox.setLayout(vertLayout)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(scroll)

        vvlayout = QtWidgets.QVBoxLayout()
        vvlayout.addLayout(layout)

        self.tabCollumns.setLayout(vvlayout)

    def CreateRows(self, data):
        vLayout = QtWidgets.QVBoxLayout()

        tableWidget = QtWidgets.QTableWidget()
        tableWidget.setSortingEnabled(True)

        shape = data.shape

        tableWidget.setColumnCount(shape[1])
        tableWidget.setRowCount(shape[0])

        columns = list(data.columns)
        tableWidget.setHorizontalHeaderLabels(columns)

        color_white = QtGui.QColor(255, 255, 255)
        color_beige = QtGui.QColor(235, 204, 153)
        cur_color = color_white

        for i in range(0, shape[0]):
            if cur_color == color_beige:
                cur_color = color_white
            else:
                cur_color = color_beige

            for j in range(0, shape[1]):
                item = QtWidgets.QTableWidgetItem(f'{data.loc[i][j]}')
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                tableWidget.setItem(i, j, item)
                tableWidget.item(i, j).setBackground(cur_color)

        tableWidget.setFont(QtGui.QFont('Arial', 12))
        tableWidget.resizeColumnsToContents()

        vLayout.addWidget(tableWidget)
        self.tabData.setLayout(vLayout)

    def OpenModel(self):
        home_dir = str(Path.cwd())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        if fname[0]:
            model = loadPickle(fname[0])

            if model is not None:

                try:
                    model.classes_
                except:
                    self.statusBar().showMessage('Загруженный объект не является моделью')
                    return

                self.model = model
                self.modelLoaded = True
                self.statusBar().showMessage('Загрузка модели произведена')

                if self.dataLoaded:
                    self.statusBar().showMessage('Загрузка модели произведена.')
                else:
                    self.statusBar().showMessage('Загрузка модели произведена. Ожидается загрузка выборки')
            else:
                self.statusBar().showMessage('Ошибка загрузки, неверный файл')

    def savePlots(self):
        if self.comboBox.count() != 0:
            home_dir = str(Path.cwd())
            dir_name = QFileDialog.getExistingDirectory(self, 'Сохранить файл', home_dir)
            if dir_name:
                files = os.listdir(self.temp.name)
                for file in files:
                    if '.png' in file:
                        shutil.copy2(f'{self.temp.name}\\{file}', f'{dir_name}\\{file}')
        else:
            self.statusBar().showMessage('Сохранение графиков невозможно, графики не были построены')

    def changeGrath(self):
        if not self.creating_grath:
            text = self.comboBox.currentText()
            print(text)

            self.show_grath(text.replace(':', ''))

    def plotGrath(self):
        if self.dataLoaded and self.modelLoaded:
            self.dialog = QtWidgets.QDialog()
            self.ui = PlotDataDialog()
            minMax = getMinMax(self.data)
            categorical = find_categorical(self.data)
            self.ui.setupUi(self.dialog, list(self.data.columns), categorical, minMax, self)
            self.dialog.show()
        else:
            self.statusBar().showMessage('Для постройки графиков загрузите модель и выборку')

    def createPlots(self, colName, minVal, maxVal, categorcal_col=''):
        categorical = categorcal_col != ''

        cond1 = self.data[colName] >= minVal
        cond2 = self.data[colName] <= maxVal

        cur_data = self.data[cond1 & cond2].reset_index(drop=True)

        h = 6
        w = 12
        plt.figure(1, figsize=(1000, 1000), dpi=1)

        temp = self.temp

        self.creating_grath = True

        if categorical:
            categories = sorted(list(self.data[categorcal_col].unique()))
            categories_items = [f'{colName}:{categorcal_col}:{x}' for x in categories]
            self.comboBox.addItems(categories_items)
            self.comboBox.setEnabled(True)
            self.comboBox.setCurrentIndex(self.comboBox.count() - len(categories))

            for i in range(len(categories)):
                plt.clf()

                cond3 = self.data[categorcal_col] == categories[i]

                cur_data = self.data[cond1 & cond2 & cond3].reset_index(drop=True)

                name = categories_items[i].replace(':', '')

                plot_lt = plot_top5_centered_importance(self.model, cur_data, colName, True)
                fig_lt = plot_lt.get_figure()
                fig_lt.set_size_inches(w, h)
                fig_lt.savefig(temp.name + f"\\img1{name}.svg", bbox_inches='tight')
                fig_lt.savefig(temp.name + f"\\img1{name}.png", bbox_inches='tight', format='png')
                plt.clf()
                #
                if colName == categorcal_col:
                    plot_lb = plot_ice_plot(self.model, self.data[cond1 & cond2].reset_index(drop=True), colName, True)
                else:
                    plot_lb = plot_ice_plot(self.model, cur_data, colName, True)
                fig_lb = plot_lb.get_figure()
                fig_lb.set_size_inches(w, h)
                fig_lb.savefig(temp.name + f"\\img2{name}.svg", bbox_inches='tight')
                fig_lb.savefig(temp.name + f"\\img2{name}.png", bbox_inches='tight', format='png')
                plt.clf()

                plot_rt = plot_top5_centered_importance(self.model, cur_data, colName)
                fig_rt = plot_rt.get_figure().figure
                fig_rt.set_size_inches(w, h)
                fig_rt.savefig(temp.name + f"\\img0{name}.svg", bbox_inches='tight')
                fig_rt.savefig(temp.name + f"\\img0{name}.png", bbox_inches='tight', format='png')
                plt.clf()
                #
                if colName == categorcal_col:
                    plot_rb = plot_ice_plot(self.model, self.data[cond1 & cond2].reset_index(drop=True), colName)
                else:
                    plot_rb = plot_ice_plot(self.model, cur_data, colName)
                fig_rb = plot_rb.get_figure().figure
                fig_rb.set_size_inches(w, h)
                fig_rb.savefig(temp.name + f"\\img3{name}.svg", bbox_inches='tight')
                fig_rb.savefig(temp.name + f"\\img3{name}.png", bbox_inches='tight', format='png')
                plt.clf()

            self.show_grath(self.comboBox.itemText(self.comboBox.count() - len(categories)).replace(':', ''))


        else:
            self.comboBox.addItems([colName])
            self.comboBox.setEnabled(True)
            self.comboBox.setCurrentIndex(self.comboBox.count() - 1)

            plt.clf()
            plot_lt = plot_top5_centered_importance(self.model, cur_data, colName, True)
            fig_lt = plot_lt.get_figure()
            fig_lt.set_size_inches(w, h)
            fig_lt.savefig(temp.name + f"\\img1{colName}.svg", bbox_inches='tight')
            fig_lt.savefig(temp.name + f"\\img1{colName}.png", bbox_inches='tight', format='png')
            plt.clf()

            self.statusBar().showMessage('1')
            print('1')

            plot_lb = plot_ice_plot(self.model, cur_data, colName, True)
            fig_lb = plot_lb.get_figure()
            fig_lb.set_size_inches(w, h)
            fig_lb.savefig(temp.name + f"\\img2{colName}.svg", bbox_inches='tight')
            fig_lb.savefig(temp.name + f"\\img2{colName}.png", bbox_inches='tight', format='png')
            plt.clf()
            self.statusBar().showMessage('2')
            print('2')

            plot_rt = plot_top5_centered_importance(self.model, cur_data, colName)
            fig_rt = plot_rt.get_figure().figure
            fig_rt.set_size_inches(w, h)
            fig_rt.savefig(temp.name + f"\\img0{colName}.svg", bbox_inches='tight')
            fig_rt.savefig(temp.name + f"\\img0{colName}.png", bbox_inches='tight', format='png')
            plt.clf()
            self.statusBar().showMessage('3')
            print('3')

            plot_rb = plot_ice_plot(self.model, cur_data, colName)
            fig_rb = plot_rb.get_figure().figure
            fig_rb.set_size_inches(w, h)
            fig_rb.savefig(temp.name + f"\\img3{colName}.svg", bbox_inches='tight')
            fig_rb.savefig(temp.name + f"\\img3{colName}.png", bbox_inches='tight', format='png')
            plt.clf()
            self.statusBar().showMessage('5')
            print('4')

            self.show_grath(colName)

        self.creating_grath = False

    def show_grath_by_name(self, i, j, name):
        temp = self.temp
        pixmap = PixmapContainer(temp.name + f"/img{2 * i + j}{name}.svg")
        pixmap.setMaximumSize(800, 600)
        pixmap.setStyleSheet(stylesheet)
        pixmap.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        widget_to_replace = self.gridLayout.itemAtPosition(i, j)
        widget_to_replace.widget().setParent(None)
        self.gridLayout.addWidget(pixmap, i, j)

    def show_grath(self, name):
        temp = self.temp
        for i in range(0, 2):
            for j in range(0, 2):
                pixmap = PixmapContainer(temp.name + f"/img{2 * i + j}{name}.svg")
                pixmap.setMaximumSize(800, 600)
                pixmap.setStyleSheet(stylesheet)
                pixmap.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                widget_to_replace = self.gridLayout.itemAtPosition(i, j)
                widget_to_replace.widget().setParent(None)
                self.gridLayout.addWidget(pixmap, i, j)


class PixmapContainer(QtWidgets.QLabel):
    def __init__(self, pixmap, parent=None):
        super(PixmapContainer, self).__init__(parent)
        self._pixmap = QtGui.QPixmap(pixmap)
        self.setMinimumSize(1, 1)  # needed to be able to scale down the image

    def resizeEvent(self, event):
        w = min(self.width(), self._pixmap.width())
        h = min(self.height(), self._pixmap.height())
        self.setPixmap(self._pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))


def main():
    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    ui = Ui()  # Create an instance of our class
    app.exec_()  # Start the application


if __name__ == '__main__':
    main()
