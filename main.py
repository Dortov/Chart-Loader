import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from collections import OrderedDict

import datetime
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

from dl_charts import PlotCanvas   # импортируем графики
from dl_gui import Ui_MainWindow   # импортирем оболочку QT


class App(QMainWindow, Ui_MainWindow):  # соденияем классы нашего окна и оболочки

    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setupUi(self)  # какое-то обязательное техническое г., создающее экземпляр формы в компе
        self.setWindowTitle("Data Loader")
        self.item = 0  # переменная, отвечающая за выбранный в списке график. 0 = график не выбран

        self.chart = PlotCanvas(self.widget, width=6, height=4,
                                chart_type='Zero')  # Помещаем экземпляр Plotcanvas с графиком в виджет, self.widget - окно родитель
        self.toolbar = NavigationToolbar(self.chart, self)  # создаем тулбар, передавая аргментом экземпляр PlotCanvas
        self.v_box_chart.addWidget(self.chart)  # график и тулбар помещаем в QVBoxLayout, находящийся в Widget
        self.v_box_chart.addWidget(self.toolbar)

        # прописываем действие actionImport_data_file из верхнего менюбара при нажатии
        self.actionImport_data_file.triggered.connect(self.show_import_dialog)

        # прописываем действие actionConnect_to_DB из верхнего менюбара при нажатии. Через лямбду закидываем в исполняемую функцию аргумент (без лямбды не получится)
        self.actionConnect_to_DB.triggered.connect(lambda: self.show_msg("Unavailable in this version"))

        # прописываем действие actionCurrent_chart_to_PDF
        self.actionCurrent_chart_to_PDF.triggered.connect(self.show_current_file_export_dialog)

        # прописываем действие actionAll_charts_to_PDF
        self.actionAll_charts_to_PDF.triggered.connect(self.show_all_charts_export_dialog)

        # заполняем список QListWidget значениями (доступными графиками), при выборе которых в левой части окна будет выведен сам график
        self.list.insertItem(0, '1. Loan Issue Values per Month (9 months)')
        self.list.insertItem(1, '2. Loan Issue Values per Year')
        self.list.insertItem(2, '3. Loan Issue Values in Cities per Month (9 months)')
        self.list.insertItem(3, '4. Loan Quantity Values per Year')
        self.list.insertItem(4, '5. Loan Issue Values Currency per Month (9 months)')
        self.list.insertItem(5, '6. Current Portfolio, Sum per Product')
        self.list.insertItem(6, '7. Current Portfolio, Loans Quantity per City')
        self.list.insertItem(7, '8. Current Portfolio, Moscow')
        self.list.insertItem(8, '9. Current Portfolio, Sankt-Petersburg')
        self.list.insertItem(9, '10. Current Portfolio, Ekaterinburg')
        self.list.insertItem(10, '11. Current Portfolio, Novosibirsk')
        self.list.insertItem(11, '12. Current Portfolio, Sum per City')
        self.list.insertItem(12, '13. Current Portfolio, Currency')

        self.list.clicked.connect(self.listview_clicked)

        self.show()

    # функция выбора графика для демонстрации по выбору значения из списка справа
    def listview_clicked(self):

        if self.chart.file_loaded == True:  # проверка переменной, ответственной за факт загрузки файла с данными

            self.item = str(self.list.currentItem().text())
            self.chart.plot(chart_type=self.item)

        else:  # если файл не был загружен, значения списка в левой части кликаются вхолостую и всплывает подсказка

            self.show_msg("Please, import the data file or connect to DB")

    def show_import_dialog(self):  # функция загрузки данных из файла csv

        file_pass = QFileDialog.getOpenFileName(self, 'Open file', '/home', "*")[0]

        data = pd.read_csv(file_pass, delimiter='|')  # считываем данные из файла в датафрейм
        self.chart.calculation(df=data)  # запускаем расчеты для построения графиков в классе

    def show_current_file_export_dialog(self):  # функция экспорта текущего графика в PDF

        if self.item != 0:  # проверка переменной, содержащей выбранный график (если он был выбран)

            PDF_file_name = QFileDialog.getSaveFileName(self, "Save File", self.item + ".pdf", "PDF files (*.pdf)")[0]
            self.chart.fig.savefig(PDF_file_name)

        else:  # если график выбран не был (а также если не был загружен дата файл - без этого не выбрать график), всплывает подсказка

            self.show_msg("Please, choose the chart to PDF in the list")

    def show_all_charts_export_dialog(
            self):  # функция экспорта всех графиков на один лист PDF. Работает мимо PlotCanvas, так как через него сбивала настройки figure

        if self.chart.file_loaded == True:  # проверка переменной, ответственной за факт загрузки файла с данными

            PDF_file_name = \
            QFileDialog.getSaveFileName(self, "Save File", "All portfolio charts.pdf", "PDF files (*.pdf)")[
                0]  # выбираем путь и название для файла
            self.chart.prepare_all_charts(
                PDF_file_name)  # вызываем функцию для подготовки листа с чартами, выгрузка в файл прописана внутри той функции, путь для выгрузки передаем отсюда

        else:  # если файл не был загружен, значения списка в левой части кликаются вхолостую и всплывает подсказка

            self.show_msg("Please, import the data file or connect to DB")

    def show_msg(self, msg_text):  # всплывающее окно с подсказками, принимает текст из кнопки или экшна
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setWindowTitle("Information")

        msg.setText(msg_text)
        # msg.setInformativeText("InformativeText")
        # msg.setDetailedText("DetailedText")

        okButton = msg.addButton("Ок", QMessageBox.AcceptRole)
        #        msg.addButton("I don't care!", QMessageBox.RejectRole)

        msg.exec()


#        if msg.clickedButton() == okButton:
#            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())






