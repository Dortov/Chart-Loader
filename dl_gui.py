# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dl_gui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(848, 436)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 0, 581, 391))
        self.widget.setObjectName("widget")
        
        
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 581, 391))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        
        self.v_box_chart = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.v_box_chart.setContentsMargins(0, 0, 0, 0)
        self.v_box_chart.setObjectName("v_box_chart")
        
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(600, 0, 241, 391))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        
        self.v_box = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.v_box.setContentsMargins(0, 0, 0, 0)
        self.v_box.setObjectName("v_box")
        
        
        self.list = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.list.setObjectName("list")
        self.v_box.addWidget(self.list)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 848, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuExport = QtWidgets.QMenu(self.menuMenu)
        self.menuExport.setObjectName("menuExport")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionImport_data_file = QtWidgets.QAction(MainWindow)
        self.actionImport_data_file.setObjectName("actionImport_data_file")
        self.actionConnect_to_DB = QtWidgets.QAction(MainWindow)
        self.actionConnect_to_DB.setObjectName("actionConnect_to_DB")
        self.actionCurrent_chart_to_PDF = QtWidgets.QAction(MainWindow)
        self.actionCurrent_chart_to_PDF.setObjectName("actionCurrent_chart_to_PDF")
        self.actionAll_charts_to_PDF = QtWidgets.QAction(MainWindow)
        self.actionAll_charts_to_PDF.setObjectName("actionAll_charts_to_PDF")
        self.menuExport.addAction(self.actionCurrent_chart_to_PDF)
        self.menuExport.addAction(self.actionAll_charts_to_PDF)
        self.menuMenu.addAction(self.actionImport_data_file)
        self.menuMenu.addAction(self.actionConnect_to_DB)
        self.menuMenu.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuExport.setTitle(_translate("MainWindow", "Export"))
        self.actionImport_data_file.setText(_translate("MainWindow", "Import data file"))
        self.actionConnect_to_DB.setText(_translate("MainWindow", "Connect to DB"))
        self.actionCurrent_chart_to_PDF.setText(_translate("MainWindow", "Current chart to PDF"))
        self.actionAll_charts_to_PDF.setText(_translate("MainWindow", "All charts to PDF"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
