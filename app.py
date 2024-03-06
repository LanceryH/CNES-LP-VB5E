from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
from datetime import date
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from data_mix import *
from resolution_CNES import *
from resolution_ESA import *
from resolution_ONERA import *

dir_path = os.path.dirname(os.path.realpath(__file__))

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        self.fig, self.ax1= plt.subplots(1, 1, sharey=True, figsize=(10, 4))
        #self.fig.tight_layout()
        super(MplCanvas, self).__init__(self.fig)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(dir_path + '\\ui\\window.ui', self)
        self.setWindowTitle("LP/VB5E")
        self.path = None
        
        self.sc = MplCanvas() 
        self.toolbar = NavigationToolbar(self.sc,self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.sc)
        self.groupBox_11.setLayout(layout)
        
            
        headerH = ['µ(1)', 'A(1)', 'E(1)', 'µ(2)', 'A(2)', 'E(2)', 'µ(3)', 'A(3)', 'E(3)','µ(4)' , 'A(4)', 'E(4)','µ(5)' , 'A(5)', 'E(5)',]
        headerV = ['C 1', 'C 2', 'C 3', 'C 4', 'Moy', 'ETy', 'Env']
        
        self.tableWidget.setColumnCount(len(headerH))
        self.tableWidget.setRowCount(len(headerV))
        for ind in range (len(headerH)):
            self.tableWidget.setColumnWidth(ind, 77)
        for ind in range (len(headerV)):
            self.tableWidget.setRowHeight(ind, 29)
        self.setStyleSheet("QHeaderView::section{"
            "border-top:0px solid #D8D8D8;"
            "border-left:0px solid #D8D8D8;"
            "border-right:1px solid #D8D8D8;"
            "border-bottom: 1px solid #D8D8D8;"
            "background-color:white;"
            "padding:4.4%;"
            "padding-top:4.8%;"
        "}"
        "QTableCornerButton::section{"
            "border-top:0px solid #D8D8D8;"
            "border-left:0px solid #D8D8D8;"
            "border-right:1px solid #D8D8D8;"
            "border-bottom: 1px solid #D8D8D8;"
            "background-color:white;"
        "}")
        self.tableWidget.setHorizontalHeaderLabels(headerH)
        self.tableWidget.setVerticalHeaderLabels(headerV)
        self.label_10.setText(str(date.today()))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.actionQuitter.triggered.connect(self.menuQuitter_fonction)
        self.actionAffichage_Temp_rature.triggered.connect(self.actionAffichage_Temp_rature_fonction)
        self.actionRafraichir.triggered.connect(self.actionRafraichir_fonction)
        self.actionImprimer.triggered.connect(self.actionImprimer_fonction)
        self.actionCopier_Coller.triggered.connect(self.actionCopier_Coller_fonction)
        self.pushButton.clicked.connect(self.pushButton_fonction)
        self.pushButton_2.clicked.connect(self.pushButton_2_fonction)
        self.pushButton_3.clicked.connect(self.pushButton_3_fonction)
        self.show()
        
        
    def menuQuitter_fonction(self):
        #self.close() 
        print("clicked")
        return

    def actionAffichage_Temp_rature_fonction(self):
        return
    
    def actionRafraichir_fonction(self):
        return
    
    def actionImprimer_fonction(self):
        return
    
    def actionCopier_Coller_fonction(self):
        return
    
    def pushButton_fonction(self):
        path, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file', '', 'All files (*)')
        if path:
            self.path = path
            
    def pushButton_2_fonction(self):
        if self.path:
            table_data, data_expo = clear_data(self.path)
            #system_ESA = Equations_ESA(table_data, data_expo)
            #system_ESA.Initialisation()
            #table_data, data_expo = clear_data("L:\Projet_stage\LP_VB5E_3\Données\\EC9323-2.xls")

            system_CNES = Equations_CNES(table_data, data_expo)
            system_CNES.Initialisation()

            result_dic_CNES = system_CNES.function_TML_fit()            #system_ONERA = Equations_ONERA(table_data, data_expo)
            #system_ONERA.Initialisation()
            
            #ESA method
            #mu_t_ESA = system_ESA.function_TML_fit(n=6)
            
            #CNES method
            #mu_t_CNES, params = system_CNES.function_TML_fit()
            
            #ONERA method
            #mu_t_ONERA = system_ONERA.function_TML_fit()
            #tau = int(system_ONERA.tau)
            
            self.sc.ax1.clear()
            self.sc.ax1.plot(table_data["time_tot"],table_data["mu_tot"],"b", label = "data",linewidth=2)
            #self.sc.ax1.plot(table_data["time"][0],mu_t_ESA,"r",linewidth=1, label = "prediction n=6 esa")
            self.sc.ax1.plot(table_data["time_tot"],result_dic_CNES["fitted data 5exp"],"c",linewidth=1, label = "prediction n=5 cnes")
            #self.sc.ax1.plot(table_data["time"][0][:tau],mu_t_ONERA[:tau],"fuchsia",linewidth=1, label = "prediction onera <τ")
            #self.sc.ax1.plot(table_data["time"][0][tau:],mu_t_ONERA[tau:],"green",linewidth=1, label = "prediction onera >τ")
            self.sc.ax1.legend()
            self.sc.ax1.grid()
            #plt.draw()
            
            #self.array_2_table(params)
        else:
            print("pls select a file first")
            
    def array_2_table(self, array):
        for column in range(len(array)):
            self.tableWidget.setItem(0,column,QTableWidgetItem(str(array[column])))
                    
    def pushButton_3_fonction(self):
        plt.draw()

        
        
