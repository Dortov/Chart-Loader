# файл Charts c графиками

import sys

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from collections import OrderedDict

import datetime
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

from PyQt5.QtWidgets import QSizePolicy

import random


      
class PlotCanvas(FigureCanvas):   # определяем бумагу, на которой ниже будем рисовать график и которую будем помещать в виджет в окне

    def __init__(self, parent=None, width=6, height=4, dpi=100, chart_type = 'Zero'):   # в качестве одного из аргументов принимаем выбраннный тип графика, который будет нарисован в виджете
        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)   # последний аргумент не дает обрезать названия графиков внутри figure

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.plot(chart_type)

        self.file_loaded = False
        # переменная для определения факта загрузки файла, используется для разветвления действий внутри функции listview_clicked в файле DataLoader;
        # значение меняется внутри функции calculation при загрузке


    def plot(self, chart_type):   # функция рисует выбранный пользователем в списке в левой части окна график по данным, полученным в ходе вычислений в функции calculation
        
        
        self.fig.clear()   # очищаем figure на случай, если ранее уже был выстроен график. Использовать axes.clear() не получается, так как при прорисовке pie объект теряет какие-то параметры (при последующей прорисовке графиков с рамками, рамок и осей не видно...)
        self.fig.set_facecolor('seashell')

        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('seashell')

        

        if chart_type == 'Zero':   # по умолчанию помещаем в виджет инструкции по загрузке файла с данными или подключению к БД

            self.axes.spines['right'].set_color('none')  # убираем границы рамки
            self.axes.spines['top'].set_color('none')
            self.axes.spines['left'].set_color('none')
            self.axes.spines['bottom'].set_color('none')

            self.axes.get_xaxis().set_visible(False)  # делаем оси невидимыми
            self.axes.get_yaxis().set_visible(False)
            
            self.axes.text(0,0.4,'To START please import the data file (csv): \n\nMenu – Import Data File \n\nor connect to data base:  \n\nMenu – Connect to DB \n\n\n\nThank U for using DataLoader!', fontsize=8)
            self.draw()

        elif chart_type == '1. Loan Issue Values per Month (9 months)':
            self.prepare_chart_1(self.axes)
            self.draw()
        elif chart_type == '2. Loan Issue Values per Year':
            self.prepare_chart_2(self.axes)
            self.draw()
        elif chart_type == '3. Loan Issue Values in Cities per Month (9 months)':
            self.prepare_chart_3(self.axes)
            self.draw()
        elif chart_type == '4. Loan Quantity Values per Year':
            self.prepare_chart_4(self.axes)
            self.draw()
        elif chart_type == '5. Loan Issue Values Currency per Month (9 months)':
            self.prepare_chart_5(self.axes)
            self.draw()
        elif chart_type == '6. Current Portfolio, Sum per Product':
            self.prepare_chart_6(self.axes)
            self.draw()
        elif chart_type == '7. Current Portfolio, Loans Quantity per City':
            self.prepare_chart_7(self.axes)
            self.draw()
        elif chart_type == '8. Current Portfolio, Moscow':
            self.prepare_chart_8(self.axes)
            self.draw()
        elif chart_type == '9. Current Portfolio, Sankt-Petersburg':
            self.prepare_chart_9(self.axes)
            self.draw()
        elif chart_type == '10. Current Portfolio, Ekaterinburg':
            self.prepare_chart_10(self.axes)
            self.draw()
        elif chart_type == '11. Current Portfolio, Novosibirsk':
            self.prepare_chart_11(self.axes)
            self.draw()
        elif chart_type == '12. Current Portfolio, Sum per City':
            self.prepare_chart_12(self.axes)
            self.draw()
        elif chart_type == '13. Current Portfolio, Currency':
            self.prepare_chart_13(self.axes)
            self.draw()
        elif chart_type == 'All charts':
            self.prepare_all_charts()
            self.draw()

# прорисовку каждого графика прописываем отдельно в своей функции, чтобы помещать несколько графиков в одной figure

    def prepare_chart_1(self, axes):

        axes.axis([0,9,0,1.8])

        index = np.arange(len(self.x_issue_9m))

        axes.set(title = 'Loan Issue Values per Month',
                   xlabel = 'Issue Month',
                   ylabel = 'Sum, billion rub.',
                   xticks = index+0.8,
        #           xticklabels = self.x_issue_9m
                  )
        axes.set_xticklabels(self.x_issue_9m, fontsize = 7)

        axes.bar(index+0.4, self.mortgage_sum_9m, color='b', alpha = 0.8, label='Mortgage')
        axes.bar(index+0.4, self.car_sum_9m, color='g', alpha = 0.8, bottom = np.array(self.mortgage_sum_9m), label='Car lending')
        axes.bar(index+0.4, self.consumer_sum_9m, color='r', alpha = 0.7, bottom = (np.array(self.car_sum_9m) + np.array(self.mortgage_sum_9m)), label='Consumer lending')

        # далее проставляем значения столбцов по краям

        for x, y in zip(index, self.mortgage_sum_9m):   # zip объединяет несколько списков поочередно в кортежи
            axes.text(x + 0.4, y - 0.02, y, ha='center', va = 'top', color = 'white')

        # поскольку координата У текстовой метки car_sum_9m будет равна сумме (сумма ипотеки + сумма авто),
        # то создаем третью последовательность для zip объекта с координатами У
        car_sum_y = np.array(self.car_sum_9m) + np.array(self.mortgage_sum_9m)

        for x, y, s in zip(index, car_sum_y, self.car_sum_9m):
            axes.text(x + 0.4, y - 0.02, s, ha='center', va = 'top', color = 'white')

        consumer_sum_y = np.array(self.car_sum_9m) + np.array(self.mortgage_sum_9m) + np.array(self.consumer_sum_9m)
        for x, y, s in zip(index, consumer_sum_y, self.consumer_sum_9m):
            axes.text(x + 0.4, y, s, ha='center', va = 'bottom')

        # проставляем цвета
        for i,t in zip(self.x_issue_9m_colors,axes.xaxis.get_ticklabels()):
            t.set_color(i)

        axes.legend(loc=0)
        axes.grid(alpha = 0.3)


        
    def prepare_chart_2(self, axes):

        axes.axis([0,9,0,23])

        index = np.arange(len(self.x_issue_years))
        # index = list(range(len(x_issue_years))) вот так не канает... не тот тип получается.

        axes.set(title = 'Loan Issue Values per Year',
                   xlabel = 'Issue Year',
                   ylabel = 'Sum, billion rub.',
                   xticks = index+0.8,
                   xticklabels = self.x_issue_years
                  )

        axes.bar(index+0.4, self.mortgage_sum, color='b', alpha = 0.8, label='Mortgage')
        axes.bar(index+0.4, self.car_sum, color='g', alpha = 0.8, bottom = np.array(self.mortgage_sum), label='Car lending')
        axes.bar(index+0.4, self.consumer_sum, color='r', alpha = 0.7, bottom = (np.array(self.car_sum) + np.array(self.mortgage_sum)), label='Consumer lending')


        # далее проставляем значения столбцов по краям

        for x, y in zip(index, self.mortgage_sum):   # zip объединяет несколько списков поочередно в кортежи
            axes.text(x + 0.4, y - 0.02, y, ha='center', va = 'top', color = 'white')

        # поскольку координата У текстовой метки car_sum_9m будет равна сумме (сумма ипотеки + сумма авто),
        # то создаем третью последовательность для zip объекта с координатами У
        car_sum_y = np.array(self.car_sum) + np.array(self.mortgage_sum)

        for x, y, s in zip(index, car_sum_y, self.car_sum):
            axes.text(x + 0.4, y - 0.02, s, ha='center', va = 'top', color = 'white')

        consumer_sum_y = np.array(self.car_sum) + np.array(self.mortgage_sum) + np.array(self.consumer_sum)
        for x, y, s in zip(index, consumer_sum_y, self.consumer_sum):
            axes.text(x + 0.4, y, s, ha='center', va = 'bottom')

        axes.legend(loc = 3)

        axes.grid(alpha = 0.3)



    def prepare_chart_3(self, axes):

        axes.axis([0, 9, 0, 1])

        index = np.arange(len(self.x_issue_9m))

        axes.set(title='Loan Issue Values in Cities per Month',
                  xlabel='Issue Month',
                  ylabel='Sum, billion rub.',
                  xticks=index + 0.2,
        #          xticklabels=self.x_issue_9m
                  )
        axes.set_xticklabels(self.x_issue_9m, fontsize = 7)

        axes.plot(index + 0.2, self.moscow_sum_9m, 'b', alpha=0.8, label='Moscow')
        axes.plot(index + 0.2, self.piter_sum_9m, color='g', alpha=0.8, label='Sankt-Petersburg')
        axes.plot(index + 0.2, self.ekat_sum_9m, color='r', alpha=0.9, label='Ekaterinburg')
        axes.plot(index + 0.2, self.novosib_sum_9m, color='m', alpha=0.9, label='Novosibirsk')

        # далее проставляем значения столбцов по краям

        for x, y in zip(index, self.moscow_sum_9m):
            axes.text(x + 0.4, y + 0.02, y, ha='center', va='bottom', color='b')
        for x, y in zip(index, self.piter_sum_9m):
            axes.text(x + 0.4, y + 0.02, y, ha='center', va='bottom', color='g')
        for x, y in zip(index, self.ekat_sum_9m):
            axes.text(x + 0.4, y - 0.02, y, ha='left', va='top', color='r')
        for x, y in zip(index, self.novosib_sum_9m):
            axes.text(x + 0.4, y - 0.02, y, ha='right', va='top', color='m')

        # назначаем цвета лейблам оси Х, используя созданный во втором графике список x_issue_9m_colors
        for i, t in zip(self.x_issue_9m_colors, axes.xaxis.get_ticklabels()):
            t.set_color(i)

        axes.legend(loc=0)
        axes.grid(alpha=0.3)



    def prepare_chart_4(self, axes):

        axes.axis([0, 9, 0, 9])

        index = np.arange(len(self.x_issue_years))

        axes.set(title='Loan Quantity Values per Year',
                  xlabel='Issue Year',
                  ylabel='Quantity, thousand loans',
                  xticks=index + 0.8,
                  xticklabels=self.x_issue_years
                  )

        axes.bar(index + 0.4, self.mortgage_quantity_y, color='b', alpha=0.8, label='Mortgage')
        axes.bar(index + 0.4, self.car_quantity_y, color='g', alpha=0.8, bottom=np.array(self.mortgage_quantity_y),
                  label='Car lending')
        axes.bar(index + 0.4, self.consumer_quantity_y, color='r', alpha=0.7,
                  bottom=(np.array(self.car_quantity_y) + np.array(self.mortgage_quantity_y)), label='Consumer lending')

        # далее проставляем значения столбцов по краям

        for x, y in zip(index, self.mortgage_quantity_y):
            axes.text(x + 0.4, y - 0.02, y, ha='center', va='top', color='white')

        # поскольку координата У текстовой метки car_sum_9m будет равна сумме (сумма ипотеки + сумма авто),
        # то создаем третью последовательность для zip объекта с координатами У
        car_q_y = np.array(self.car_quantity_y) + np.array(self.mortgage_quantity_y)

        for x, y, s in zip(index, car_q_y, self.car_quantity_y):
            axes.text(x + 0.4, y - 0.02, s, ha='center', va='top', color='white')

        consumer_q_y = np.array(self.car_quantity_y) + np.array(self.mortgage_quantity_y) + np.array(self.consumer_quantity_y)
        for x, y, s in zip(index, consumer_q_y, self.consumer_quantity_y):
            axes.text(x + 0.4, y - 0.02, s, ha='center', va='top', color='white')

        axes.legend(loc=9)

        axes.grid(alpha=0.3)



    def prepare_chart_5(self, axes):

        axes.axis([0, 9, 0, 1.6])

        index = np.arange(len(self.x_issue_9m))

        axes.set(title='Loan Issue Values Currency per Month',
                  xlabel='Issue Month',
                  ylabel='Sum, billion rub.',
                  xticks=index + 0.2,
        #          xticklabels=self.x_issue_9m
                  )
        axes.set_xticklabels(self.x_issue_9m, fontsize = 7)

        axes.plot(index + 0.2, self.rub_sum_9m, 'b', alpha=0.8, label='RUB')
        axes.plot(index + 0.2, self.usd_sum_9m, color='g', alpha=0.8, label='USD')
        axes.plot(index + 0.2, self.eur_sum_9m, color='r', alpha=0.9, label='EUR')

        # далее проставляем значения столбцов по краям

        for x, y in zip(index, self.rub_sum_9m):
            axes.text(x + 0.4, y - 0.02, y, ha='center', va='top', color='b')
        for x, y in zip(index, self.usd_sum_9m):
            axes.text(x + 0.4, y + 0.1, y, ha='right', va='bottom', color='g')
        for x, y in zip(index, self.eur_sum_9m):
            axes.text(x + 0.4, y + 0.07, y, ha='left', va='bottom', color='r')

        # назначаем цвета лейблам оси Х, используя созданный во втором графике список x_issue_9m_colors
        for i, t in zip(self.x_issue_9m_colors, axes.xaxis.get_ticklabels()):
            t.set_color(i)

        axes.legend(loc=0)
        axes.grid(alpha=0.3)



    def prepare_chart_6(self, axes):

        explode_341 = [0, 0.05, 0.2]
        # добавляем список для аргумента explode, который отвечает за вырезанный "кусок пирога"

        # вычисляем 1% от общего размера портфеля в млрд.р. для указания на основной диаграмме
        one_percent_billion_341 = round((sum(self.current_common_products.values()) / 100 / 1000000000), 2)

        axes.set(title='Whole Portfolio, Current Sum',
                   ylabel='Sum, 1% = {} billion rub.'.format(one_percent_billion_341)
                   )

        axes.pie(list(self.current_common_products.values()),
                   labels=list(self.current_common_products.keys()),
                   colors=self.colors,
                   explode=explode_341,
                   shadow=True,
                   autopct='%1.1f%%',
                   startangle=55
                   )
        # startangle отвечает за поворот пирога на нужный угол - к примеру, чтобы не было наложения тайтла и лейбла...
        # autopct добавляет процентные значения на каждый кусок. Синтаксис не объяснен.
        # shadow добавляет тень на диаграмму

        axes.axis('equal')
        axes.legend(loc=0)



    def prepare_chart_7(self, axes):

        one_percent_add = round((sum(self.current_common_products_q.values()) / 100 / 1000), 2)

        axes.set(title='Current Quantity',
                   xlabel='Quantity, 1% = {} thousand loans'.format(one_percent_add)
                   )

        axes.pie(list(self.current_common_products_q.values()),
                   labels=list(self.current_common_products.keys()),
                   colors=self.colors,
                   shadow=True,
                   autopct='%1.1f%%',
                   startangle=190
                   )

        axes.axis('equal')
        axes.legend(loc=0)



    def prepare_chart_8(self, axes):

        explode_32 = [0, 0.05, 0.2]
        # вычисляем 1% от размера соответствующего портфеля в млрд.р. для указания на основной диаграмме
        one_percent_billion_32 = round((sum(self.current_moscow_products.values()) / 100 / 1000000000), 2)

        axes.set(title='MOSCOW, Current Sum',
                  #           xlabel = 'Issue Month',
                  ylabel='Sum, 1% = {} billion rub.'.format(one_percent_billion_32)
                  )

        axes.pie(list(self.current_moscow_products.values()),
                  labels=list(self.current_moscow_products.keys()),
                  colors=self.colors,
                  explode=explode_32,
                  shadow=True,
                  autopct='%1.1f%%',
                  startangle=55
                  )

        axes.axis('equal')
        axes.legend(loc=0)



    def prepare_chart_9(self, axes):

        explode_33 = [0, 0.05, 0.2]
        # вычисляем 1% от общего размера соответствующего портфеля в млрд.р. для указания на основной диаграмме
        one_percent_billion_33 = round((sum(self.current_piter_products.values()) / 100 / 1000000000), 2)

        axes.set(title='SANKT-PETERSBURG, Current Sum',
                  #           xlabel = 'Issue Month',
                  ylabel='Sum, 1% = {} billion rub.'.format(one_percent_billion_33)
                  )

        axes.pie(list(self.current_piter_products.values()),
                  labels=list(self.current_piter_products.keys()),
                  colors=self.colors,
                  explode=explode_33,
                  shadow=True,
                  autopct='%1.1f%%',
                  startangle=55
                  )

        axes.axis('equal')
        axes.legend(loc=0)



    def prepare_chart_10(self, axes):

        explode_42 = [0, 0.05, 0.2]
        # вычисляем 1% от размера соответствующего портфеля в млрд.р. для указания на основной диаграмме
        one_percent_billion_42 = round((sum(self.current_ekat_products.values()) / 100 / 1000000000), 2)

        axes.set(title='EKATERINBURG, Current Sum',
                  ylabel='Sum, 1% = {} billion rub.'.format(one_percent_billion_42)
                  )

        axes.pie(list(self.current_ekat_products.values()),
                  labels=list(self.current_ekat_products.keys()),
                  colors=self.colors,
                  explode=explode_42,
                  shadow=True,
                  autopct='%1.1f%%',
                  startangle=55
                  )

        axes.axis('equal')
        axes.legend(loc=0)



    def prepare_chart_11(self, axes):

        explode_43 = [0, 0.05, 0.2]
        # вычисляем 1% от общего размера соответствующего портфеля в млрд.р. для указания на основной диаграмме
        one_percent_billion_43 = round((sum(self.current_novosib_products.values()) / 100 / 1000000000), 2)

        axes.set(title='NOVOSIBIRSK, Current Sum',
                  #           xlabel = 'Issue Month',
                  ylabel='Sum, 1% = {} billion rub.'.format(one_percent_billion_43)
                  )

        axes.pie(list(self.current_novosib_products.values()),
                  labels=list(self.current_novosib_products.keys()),
                  colors=self.colors,
                  explode=explode_43,
                  shadow=True,
                  autopct='%1.1f%%',
                  startangle=55
                  )

        axes.axis('equal')
        axes.legend(loc=0)



    def prepare_chart_12(self, axes):

        explode_34 = [0, 0, 0, 0]
        # вычисляем 1% от размера соответствующего портфеля в млрд.р. для указания на основной диаграмме
        one_percent_billion_34 = round((sum(self.current_common_cities.values()) / 100 / 1000000000), 2)

        axes.set(title='Whole Portfolio, Current Sum in Cities',
                  #           xlabel = 'Issue Month',
                  ylabel='Sum, 1% = {} billion rub.'.format(one_percent_billion_34)
                  )

        axes.pie(list(self.current_common_cities.values()),
                  labels=list(self.current_common_cities.keys()),
                  colors=['lime', 'green', 'red', 'blue'],
                  explode=explode_34,
                  shadow=True,
                  autopct='%1.1f%%',
                  startangle=85
                  )

        axes.axis('equal')
        axes.legend(loc=0)



    def prepare_chart_13(self, axes):

        explode_44 = [0, 0.05, 0.3]
        # вычисляем 1% от общего размера соответствующего портфеля в млрд.р. для указания на основной диаграмме
        one_percent_billion_44 = round((sum(self.current_common_currency.values()) / 100 / 1000000000), 2)

        axes.set(title='Whole Portfolio, Currency',
                  ylabel='Sum, 1% = {} billion rub.'.format(one_percent_billion_44),
                  facecolor='white'
                  )

        axes.pie(list(self.current_common_currency.values()),
                  labels=list(self.current_common_currency.keys()),
                  colors=['green', 'lime', 'pink'],
                  explode=explode_44,
                  shadow=True,
                  autopct='%1.1f%%',
                  startangle=0
                  )

        axes.axis('equal')
        axes.legend(loc=0)



    def prepare_all_charts(self, PDF_file_name):

        fig_all_ch = plt.figure()
        fig_all_ch.set_figwidth(28)
        fig_all_ch.set_figheight(14)
        fig_all_ch.subplots_adjust(wspace=0.2, hspace=0.5, left=0.1, right=0.9, top=0.9, bottom=0.1)


        # первые две строки графиков
        ax_12 = fig_all_ch.add_subplot(4, 3, 2)  # 4 строки, 3 ряда, 2ое место сверху вниз слева направо
        ax_13 = fig_all_ch.add_subplot(4, 3, 3)
        ax_25 = fig_all_ch.add_subplot(4, 3, 5)
        ax_26 = fig_all_ch.add_subplot(4, 3, 6)

        # вторая пара строк графиков
        ax_32 = fig_all_ch.add_subplot(4, 4, 10)
        ax_33 = fig_all_ch.add_subplot(4, 4, 11)
        ax_34 = fig_all_ch.add_subplot(4, 4, 12)
        ax_42 = fig_all_ch.add_subplot(4, 4, 14)
        ax_43 = fig_all_ch.add_subplot(4, 4, 15)
        ax_44 = fig_all_ch.add_subplot(4, 4, 16)

        # отдельностоящие графики
        ax_431 = fig_all_ch.add_subplot(2, 3, 1)
        ax_445 = fig_all_ch.add_subplot(2, 4, 5)
        ax_add = fig_all_ch.add_subplot(6, 8, 42)

        # расскрашиваем axes
        ax_12.set_facecolor('seashell')
        ax_13.set_facecolor('seashell')
        ax_25.set_facecolor('seashell')
        ax_26.set_facecolor('seashell')
        ax_32.set_facecolor('seashell')
        ax_33.set_facecolor('seashell')
        ax_34.set_facecolor('seashell')
        ax_42.set_facecolor('seashell')
        ax_43.set_facecolor('seashell')
        ax_44.set_facecolor('seashell')
        ax_431.set_facecolor('seashell')
        ax_445.set_facecolor('seashell')
        ax_add.set_facecolor('seashell')

        # рисуем графики, обращаясь к соответствующим функциям
        self.prepare_chart_2(ax_12)
        self.prepare_chart_3(ax_13)
        self.prepare_chart_4(ax_25)
        self.prepare_chart_5(ax_26)
        self.prepare_chart_8(ax_32)
        self.prepare_chart_9(ax_33)
        self.prepare_chart_12(ax_34)
        self.prepare_chart_10(ax_42)
        self.prepare_chart_11(ax_43)
        self.prepare_chart_13(ax_44)
        self.prepare_chart_1(ax_431)
        self.prepare_chart_6(ax_445)
        self.prepare_chart_7(ax_add)

        fig_all_ch.savefig(PDF_file_name)   # выгружаем figure в файл по принятому адресу и названию файла. PDF_file_name прилетает из главного файла.


    def calculation(self, df):   # функция производит расчет данных их загруженного файла для последующего использования в графиках

        self.file_loaded = True   # переменная для определения факта загрузки файла, сообщаем, что файл загружен
        # проверка на корректность загруженного файла НЕ реализована

        usd = 77
        eur = 91   # внутренний курс валют для отчетов внутри банковской группы фиксируем здесь - меняться постоянно не будет
        
        def billion(x):   # готовим функции для расчетов: делим на миллиард и округляем до 2 цифр после запятой
            return round(x/1000000000, 2)
        
        def thousand(x):
            return round(x/1000, 2)
        
               
        df['sum_issue_RUB'] = 0   # создаем столбец для рублевого эквивалента суммы выданного кредита

        for i in range(len(df['ID'])):   # и заполняем его рублевыми суммами по курсу
            if df.loc[i, 'currency'] == 'EUR':
                df.loc[i, 'sum_issue_RUB'] = df.loc[i, 'sum_issue'] * eur
            elif df.loc[i, 'currency'] == 'USD':
                df.loc[i, 'sum_issue_RUB'] = df.loc[i, 'sum_issue'] * usd
            else:
                df.loc[i, 'sum_issue_RUB'] = df.loc[i, 'sum_issue']
                
        
        
        # 1. Рисуем первый график (разбивка сумм выдачи кредита по годам и по продуктам)

        # 1.1 Формируем данные для первого графика
        # создаем три словаря для лет выдачи под каждый тип кредита - каждая пара будет служить вместо переменной по году и типу кредита
        # объявлять переменные сразу не получится, если не знаем, какие годы включает период кредитования
        # словаря сразу три на случай, если разные типы выдавались в разные периоды времени
        self.mortgage_issue = {}
        self.car_issue = {}
        self.consumer_issue = {}

        # заполняем словари годами, когда выдавались кредиты разных типов
        for i in range(len(df['sum_issue_RUB'])):
            d = datetime.strptime(df.loc[i, 'date_issue'], "%Y-%m-%d").year
            # datetime.strptime("2018-01-31", "%Y-%m-%d") - конвертер строки в дату. 
            # Аргументы здесь https://www.delftstack.com/ru/howto/python/how-to-convert-string-to-datetime/

            if (df.loc[i,'type'] == 'mortgage' and d not in self.mortgage_issue):
                self.mortgage_issue.setdefault(d, 0)
            elif (df.loc[i,'type'] == 'consumer' and d not in self.consumer_issue):
                self.consumer_issue.setdefault(d, 0)
            elif (df.loc[i,'type'] == 'car loan' and d not in self.car_issue):
                self.car_issue.setdefault(d, 0)

        # Обходим sum_issue_RUB и заполняем словари значениями
        for i in range(len(df['sum_issue_RUB'])):
            d = datetime.strptime(df.loc[i, 'date_issue'], "%Y-%m-%d").year

            if df.loc[i,'type'] == 'mortgage':
                self.mortgage_issue[d] += df.loc[i,'sum_issue_RUB']
            elif df.loc[i,'type'] == 'car loan':
                self.car_issue[d] += df.loc[i,'sum_issue_RUB']
            elif df.loc[i,'type'] == 'consumer':
                self.consumer_issue[d] += df.loc[i,'sum_issue_RUB']


        # сортируем словари по возрастанию ключа. 
        #from collections import OrderedDict   Импортируем библиотеку (сделали ранее)

        self.mortgage_issue = dict(OrderedDict(sorted(self.mortgage_issue.items(), key=lambda t: t[0])))
        # выражение лямбды означает сортировку по ключу. Есть еще сортировка по значению и длине строки ключа:
        # https://docs.python.org/2/library/collections.html#collections.OrderedDict

        self.consumer_issue = dict(OrderedDict(sorted(self.consumer_issue.items(), key=lambda t: t[0])))
        self.car_issue = dict(OrderedDict(sorted(self.car_issue.items(), key=lambda t: t[0])))

        
        
        
        # 1.2 Обрабатываем данные для первого графика

        #  собираем все значения лет из трех словарей (ключи), скидываем в один список 
        # ...и убираем дубли для создания списка значений на общей оси х. Сразу сортируем по возрастанию.
        self.mortgage_years = list(self.mortgage_issue.keys())   # Возвращает все ключи словаря
        self.car_years = list(self.car_issue.keys())
        self.consumer_years = list(self.consumer_issue.keys())

        self.x_issue_years = sorted(list(set(self.mortgage_years + self.car_years + self.consumer_years)))

        # проверяем, все ли значения лет есть в трех словарях. 
        # Если нет, добавляем недостающие ключи со значением 0, тем самым унифицируя словари по годам
        for i in self.x_issue_years:
            if i not in self.mortgage_issue.keys():
                self.mortgage_issue.setdefault(i, 0)
            elif i not in self.car_issue.keys():
                self.car_issue.setdefault(i, 0)        
            elif i not in self.consumer_issue.keys():
                self.consumer_issue.setdefault(i, 0)        

        # готовим списки для оси Y, паралелльно округляя до миллиарда

        self.mortgage_sum = list(map(billion, self.mortgage_issue.values()))   # Возвращает все значения словаря
        self.car_sum = list(map(billion, self.car_issue.values()))
        self.consumer_sum = list(map(billion, self.consumer_issue.values()))
        
        
        
        
        # 2. Второй график (разбивка сумм выдачи кредита за последние 9 месяцев по продуктам)

        # 2.1 Формируем данные для второго графика
        # вычисляем последние 9 месяцев от текущей даты и создаем три словаря (под каждый продукт) для значений в формате дата месяца:0
        # по ключу (дате) будем сверять год и месяц и при соответствии прибавлять цифру в значение словаря
        # словаря сразу три на случай, если в какой-то месяц кредиты какого-то типа не выдавались...

        self.mortgage_issue_9m = {}
        self.car_issue_9m = {}
        self.consumer_issue_9m = {}

        day = date.today()

        for i in range(9):
            self.mortgage_issue_9m.setdefault(day, 0)
            self.car_issue_9m.setdefault(day, 0)
            self.consumer_issue_9m.setdefault(day, 0)
            day = day - relativedelta(months=1)

        # Обходим sum_issue_RUB и заполняем словари значениями
        for i in range(len(df['sum_issue_RUB'])):
            y = datetime.strptime(df.loc[i, 'date_issue'], "%Y-%m-%d").year
            m = datetime.strptime(df.loc[i, 'date_issue'], "%Y-%m-%d").month

            for j in self.mortgage_issue_9m:   #  поскольку ключи в трех словарях одинаковые, на входе сравниваем с ключами любого словаря, а рассортировываем по нужным
                if (j.month == m and j.year == y):

                    if df.loc[i,'type'] == 'mortgage':
                        self.mortgage_issue_9m[j] += df.loc[i,'sum_issue_RUB']

                    elif df.loc[i,'type'] == 'car loan':
                        self.car_issue_9m[j] += df.loc[i,'sum_issue_RUB']

                    elif df.loc[i,'type'] == 'consumer':
                        self.consumer_issue_9m[j] += df.loc[i,'sum_issue_RUB']


        # сортируем словари по возрастанию ключа. 
        #from collections import OrderedDict   Импортируем библиотеку (сделали ранее)

        self.mortgage_issue_9m = dict(OrderedDict(sorted(self.mortgage_issue_9m.items(), key=lambda t: t[0])))
        # выражение лямбды означает сортировку по ключу. Есть еще сортировка по значению и длине строки ключа:
        # https://docs.python.org/2/library/collections.html#collections.OrderedDict

        self.consumer_issue_9m = dict(OrderedDict(sorted(self.consumer_issue_9m.items(), key=lambda t: t[0])))
        self.car_issue_9m = dict(OrderedDict(sorted(self.car_issue_9m.items(), key=lambda t: t[0])))

        
        
        
        # 2.2 Обрабатываем данные для второго графика

        #  список текстовых меток для оси х формируем по ключам любого из наших трех словарей
        self.x_issue_9m = sorted(list(self.mortgage_issue_9m.keys()))

        for i in range(len(self.x_issue_9m)):   # ...и сразу же переписываем значения в нужном формате даты - месяц-год
            self.x_issue_9m[i] = datetime.strftime(self.x_issue_9m[i], "%b %Y")

        # создаем список для цветов сезонов
        self.x_issue_9m_colors = []

        for i in self.x_issue_9m:
            m = datetime.strptime(i, "%b %Y").month

            if m in [12,1,2]:
                self.x_issue_9m_colors.append('blue')
            elif m in [3,4,5]:
                self.x_issue_9m_colors.append('dimgrey')    
            elif m in [6,7,8]:
                self.x_issue_9m_colors.append('green')
            else:
                self.x_issue_9m_colors.append('darkorange')

        # готовим списки для оси Y, паралелльно округляя до миллиарда

        self.mortgage_sum_9m = list(map(billion, self.mortgage_issue_9m.values()))
        self.car_sum_9m = list(map(billion, self.car_issue_9m.values()))
        self.consumer_sum_9m = list(map(billion, self.consumer_issue_9m.values()))


        
        # 3. Рисуем третий график (количество кредитов по годам с разбивкой по продуктам)

        # 3.1 Формируем данные для третьего графика
        # как и в первом графике, создаем три словаря для лет выдачи под каждый тип кредита - каждая пара будет служить вместо переменной по году и типу кредита
        # для заполнения годами (ключами) используем ранее созданный словарь x_issue_years, годы заново уже не парсим
        self.mortgage_issue_quantity_y = {}
        self.consumer_issue_quantity_y = {}
        self.car_issue_quantity_y = {}

        for i in self.x_issue_years:
            self.mortgage_issue_quantity_y.setdefault(i, 0)
            self.car_issue_quantity_y.setdefault(i, 0)
            self.consumer_issue_quantity_y.setdefault(i, 0)

        # Обходим df и заполняем словари значениями
        for i in range(len(df['sum_issue_RUB'])):
            d = datetime.strptime(df.loc[i, 'date_issue'], "%Y-%m-%d").year

            if df.loc[i,'type'] == 'mortgage':
                self.mortgage_issue_quantity_y[d] += 1
            elif df.loc[i,'type'] == 'car loan':
                self.car_issue_quantity_y[d] += 1
            elif df.loc[i,'type'] == 'consumer':
                self.consumer_issue_quantity_y[d] += 1
        
        
        
        # 3.2 Обрабатываем данные для третьего графика
        # готовим списки для оси Y, паралелльно округляя до тысячи

        self.mortgage_quantity_y = list(map(thousand, self.mortgage_issue_quantity_y.values()))   # Возвращает все значения словаря
        self.car_quantity_y = list(map(thousand, self.car_issue_quantity_y.values()))
        self.consumer_quantity_y = list(map(thousand, self.consumer_issue_quantity_y.values()))
        
        
        
        
        # 4. Четвертый график (суммы выдачи за 9 месяцев с разбивкой по городам)

        # 4.1 Формируем данные для второго графика
        # вычисляем последние 9 месяцев от текущей даты и создаем 4 словаря (под каждый город) для значений в формате "город:0"
        # заполняем по аналогии с графиком 2
        self.moscow_issue_9m = {}
        self.piter_issue_9m = {}
        self.ekat_issue_9m = {}
        self.novosib_issue_9m = {}

        day = date.today()

        for i in range(9):
            self.moscow_issue_9m.setdefault(day, 0)
            self.piter_issue_9m.setdefault(day, 0)
            self.ekat_issue_9m.setdefault(day, 0)
            self.novosib_issue_9m.setdefault(day, 0)

            day = day - relativedelta(months=1)

        # Обходим df и заполняем словари значениями
        for i in range(len(df['sum_issue_RUB'])):
            y = datetime.strptime(df.loc[i, 'date_issue'], "%Y-%m-%d").year
            m = datetime.strptime(df.loc[i, 'date_issue'], "%Y-%m-%d").month

            for j in self.moscow_issue_9m:   #  поскольку ключи в трех словарях одинаковые, на входе сравниваем с ключами любого словаря, а рассортировываем по нужным
                if (j.month == m and j.year == y):

                    if df.loc[i,'city'] == 'Москва':
                        self.moscow_issue_9m[j] += df.loc[i,'sum_issue_RUB']

                    elif df.loc[i,'city'] == 'Санкт-Петербург':
                        self.piter_issue_9m[j] += df.loc[i,'sum_issue_RUB']

                    elif df.loc[i,'city'] == 'Новосибирск':
                        self.novosib_issue_9m[j] += df.loc[i,'sum_issue_RUB']

                    elif df.loc[i,'city'] == 'Екатеринбург':
                        self.ekat_issue_9m[j] += df.loc[i,'sum_issue_RUB']

        # сортируем словари по возрастанию ключа. 
        #from collections import OrderedDict   Импортируем библиотеку (сделали ранее)

        self.moscow_issue_9m = dict(OrderedDict(sorted(self.moscow_issue_9m.items(), key=lambda t: t[0])))
        # выражение лямбды означает сортировку по ключу. Есть еще сортировка по значению и длине строки ключа:
        # https://docs.python.org/2/library/collections.html#collections.OrderedDict

        self.piter_issue_9m = dict(OrderedDict(sorted(self.piter_issue_9m.items(), key=lambda t: t[0])))
        self.ekat_issue_9m = dict(OrderedDict(sorted(self.ekat_issue_9m.items(), key=lambda t: t[0])))
        self.novosib_issue_9m = dict(OrderedDict(sorted(self.novosib_issue_9m.items(), key=lambda t: t[0])))
        
        
        
        
        # 4.2 Обрабатываем данные для второго графика

        #  список текстовых меток (месяц-год) для оси х берем из второго графика: x_issue_9m
        # готовим списки для оси Y, паралелльно округляя до миллиарда

        self.moscow_sum_9m = list(map(billion, self.moscow_issue_9m.values()))
        self.piter_sum_9m = list(map(billion, self.piter_issue_9m.values()))
        self.ekat_sum_9m = list(map(billion, self.ekat_issue_9m.values()))
        self.novosib_sum_9m = list(map(billion, self.novosib_issue_9m.values()))



        
        
        # 5. Пятый график (суммы выдачи за 9 месяцев с разбивкой по валюте)

        # 5.1 Формируем данные для графика
        # создаем 3 словаря (под три валюты) для значений в формате "валюта:0" и заполняем их месяцами
        # заполняем по аналогии с графиком 2
        self.rub_issue_9m = {}
        self.usd_issue_9m = {}
        self.eur_issue_9m = {}

        day = date.today()

        for i in range(9):
            self.rub_issue_9m.setdefault(day, 0)
            self.usd_issue_9m.setdefault(day, 0)
            self.eur_issue_9m.setdefault(day, 0)

            day = day - relativedelta(months=1)


        # Обходим df и заполняем словари значениями
        for i in range(len(df['sum_issue_RUB'])):
            y = datetime.strptime(df.loc[i, 'date_issue'], "%Y-%m-%d").year
            m = datetime.strptime(df.loc[i, 'date_issue'], "%Y-%m-%d").month

            for j in self.rub_issue_9m:   #  поскольку ключи в трех словарях одинаковые, на входе сравниваем с ключами любого словаря, а рассортировываем по нужным
                if (j.month == m and j.year == y):

                    if df.loc[i,'currency'] == 'RUB':
                        self.rub_issue_9m[j] += df.loc[i,'sum_issue_RUB']

                    elif df.loc[i,'currency'] == 'USD':
                        self.usd_issue_9m[j] += df.loc[i,'sum_issue_RUB']

                    elif df.loc[i,'currency'] == 'EUR':
                        self.eur_issue_9m[j] += df.loc[i,'sum_issue_RUB']

        # сортируем словари по возрастанию ключа. 
        #from collections import OrderedDict   Импортируем библиотеку (сделали ранее)

        self.moscow_issue_9m = dict(OrderedDict(sorted(self.rub_issue_9m.items(), key=lambda t: t[0])))
        # выражение лямбды означает сортировку по ключу. Есть еще сортировка по значению и длине строки ключа:
        # https://docs.python.org/2/library/collections.html#collections.OrderedDict

        self.piter_issue_9m = dict(OrderedDict(sorted(self.usd_issue_9m.items(), key=lambda t: t[0])))
        self.ekat_issue_9m = dict(OrderedDict(sorted(self.eur_issue_9m.items(), key=lambda t: t[0])))






        # 5.2 Обрабатываем данные для графика

        #  список текстовых меток (месяц-год) для оси х берем из второго графика: x_issue_9m
        # готовим списки для оси Y, паралелльно округляя до миллиарда

        self.rub_sum_9m = list(map(billion, self.rub_issue_9m.values()))
        self.usd_sum_9m = list(map(billion, self.usd_issue_9m.values()))
        self.eur_sum_9m = list(map(billion, self.eur_issue_9m.values()))




        
        

        # Графики 6 - 13 (круговые диаграммы)

        # Готовим данные сразу для всех диаграмм
        # Создаем словари и руками заполняем известными ключами, которые не меняются
        self.current_common_products = {'mortgage':0, 'car loan':0, 'consumer':0}   # значения сумм текущего состояния кр.портф. общего в разбивке по продуктам
        self.current_common_products_q = {'mortgage':0, 'car loan':0, 'consumer':0}   # количественные значения текущего состояния кр.портф. общего в разбивке по продуктам
        self.current_moscow_products = {'mortgage':0, 'car loan':0, 'consumer':0}   # значения сумм текущего состояния кр.портф. Москвы в разбивке по продуктам
        self.current_piter_products = {'mortgage':0, 'car loan':0, 'consumer':0}   # значения сумм текущего состояния кр.портф. СПб в разбивке по продуктам
        self.current_ekat_products = {'mortgage':0, 'car loan':0, 'consumer':0}   # значения сумм текущего состояния кр.портф. Екб в разбивке по продуктам
        self.current_novosib_products = {'mortgage':0, 'car loan':0, 'consumer':0}   # значения сумм текущего состояния кр.портф. Новосиба в разбивке по продуктам
        self.current_common_cities = {'Москва':0,'Санкт-Петербург':0,'Новосибирск':0,'Екатеринбург':0}   # значения сумм текущего состояния кр.портф. в разбивке по городам
        self.current_common_currency = {'USD':0,'EUR':0,'RUB':0}   # значения сумм текущего состояния кр.портф. в разбивке по валюте

        self.colors = ['deepskyblue', 'lime', 'red']

        # Обходим df и заполняем словари текущими рублевыми значениями
        for i in range(len(df['sum_issue_RUB'])):

            self.current_common_products[df.loc[i,'type']] += int(df.loc[i,'sum_today_RUB'])
            self.current_common_products_q[df.loc[i,'type']] += 1
            self.current_common_cities[df.loc[i,'city']] += int(df.loc[i,'sum_today_RUB'])
            self.current_common_currency[df.loc[i,'currency']] += int(df.loc[i,'sum_today_RUB'])

            if df.loc[i,'city'] == 'Москва':
                self.current_moscow_products[df.loc[i,'type']] += int(df.loc[i,'sum_today_RUB'])

            if df.loc[i,'city'] == 'Санкт-Петербург':
                self.current_piter_products[df.loc[i,'type']] += int(df.loc[i,'sum_today_RUB'])

            if df.loc[i,'city'] == 'Новосибирск':
                self.current_novosib_products[df.loc[i,'type']] += int(df.loc[i,'sum_today_RUB'])

            if df.loc[i,'city'] == 'Екатеринбург':
                self.current_ekat_products[df.loc[i,'type']] += int(df.loc[i,'sum_today_RUB']) 


