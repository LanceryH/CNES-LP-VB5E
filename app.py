from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
from datetime import date
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from data_mix import *


dir_path = os.path.dirname(os.path.realpath(__file__))

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(dir_path + '\\ui\\window.ui', self)

        self.setWindowIcon(QIcon('.\logo\cnes.png'))
        #self.setFixedSize(1080,760)
        self.setWindowTitle("LP/VB5E")
        self.path = None
        
        self.treeWidget.expandAll()
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget_2.expandAll()
        self.treeWidget_2.setAlternatingRowColors(True)

        self.figure_2D, self.axs_2D= plt.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [2,1]})#, figsize=(10, 4))
        self.figure_2D.tight_layout()
        self.axs_2D[0].grid()
        self.axs_2D[1].grid()
        self.axs_2D[1].set_xlabel("Temps [minutes]")
        self.axs_2D[0].set_ylabel("Perte de masse [%]")
        self.canvas_2D = FigureCanvas(self.figure_2D)
        self.toolbar_2D = NavigationToolbar(self.canvas_2D,self)
        self.layout_of_2D = QtWidgets.QVBoxLayout()
        self.layout_of_2D.addWidget(self.toolbar_2D)
        self.layout_of_2D.addWidget(self.canvas_2D)
        self.groupBox_11.setLayout(self.layout_of_2D)

        self.figure_3D = plt.figure(2)
        self.ax_3D = self.figure_3D.add_subplot(projection='3d')
        self.figure_3D.tight_layout()
        self.ax_3D.view_init(elev=13, azim=-127)
        self.ax_3D.grid()
        self.ax_3D.set_xlabel("Temps [minutes]")
        self.ax_3D.set_ylabel("ISO [°C]")
        self.ax_3D.set_zlabel("Perte de masse [%]")
        self.canvas_3D = FigureCanvas(self.figure_3D)
        self.toolbar_3D = NavigationToolbar(self.canvas_3D,self)
        self.layout_of_3D = QtWidgets.QVBoxLayout()
        self.layout_of_3D.addWidget(self.toolbar_3D)
        self.layout_of_3D.addWidget(self.canvas_3D)
        self.groupBox_13.setLayout(self.layout_of_3D)

        self.label_10.setText(str(date.today()))

        self.actionNew.triggered.connect(self.menuNew_fonction)
        self.actionOpen.triggered.connect(self.actionOpen_fonction)
        self.actionRecent.triggered.connect(self.actionRecent_fonction)

        self.pushButton.clicked.connect(self.pushButton_fonction)
        self.pushButton_2.clicked.connect(self.pushButton_2_fonction)

        self.comboBox_7.addItems(["CNES", "ESTEC", "ONERA"])
        self.comboBox_8.addItems(["Reg. Poly.", ""])
        #self.comboBox_7.currentIndexChanged.connect(self.comboBox_7_fonction)

        self.show()
    
    def comboBox_7_fonction(self):
        self.lineEdit_26.setText("TEST")

    def menuNew_fonction(self):
        print("New")
        return

    def actionOpen_fonction(self):
        print("Open")
        path, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file', '', 'All files (*)')
        if path:
            self.path = path
        return

    def actionRecent_fonction(self):
        print("Recent")
        return
            
    def pushButton_fonction(self):
        import resolution_CNES as Res_CNES
        import resolution_ESA as Res_ESA
        import resolution_ONERA as Res_ONERA

        table_data, data_expo = clear_data(self.path)
        if self.path:
            if self.comboBox_7.currentText() == "CNES":
                self.treeWidget_2.hide()
                self.treeWidget_3.hide()
                self.treeWidget.show()
                system = Res_CNES.Equations_CNES(table_data, data_expo, 5)
                system.Initialisation()
                system.function_TML_fit()  

                self.treeWidget.topLevelItem(0).child(0).setText(1, f'{np.round(system.result_dic["parameter exp"][0][2],3)}')
                self.treeWidget.topLevelItem(0).child(1).setText(1, f'{np.round(system.result_dic["parameter exp"][0][1],3)}')
                self.treeWidget.topLevelItem(0).child(2).setText(1, f'{np.round(system.result_dic["parameter exp"][0][0],3)}')

                self.treeWidget.topLevelItem(1).child(0).setText(1, f'{np.round(system.result_dic["parameter exp"][1][2],3)}')
                self.treeWidget.topLevelItem(1).child(1).setText(1, f'{np.round(system.result_dic["parameter exp"][1][1],3)}')
                self.treeWidget.topLevelItem(1).child(2).setText(1, f'{np.round(system.result_dic["parameter exp"][1][0],3)}')

                self.treeWidget.topLevelItem(2).child(0).setText(1, f'{np.round(system.result_dic["parameter exp"][2][2],3)}')
                self.treeWidget.topLevelItem(2).child(1).setText(1, f'{np.round(system.result_dic["parameter exp"][2][1],3)}')
                self.treeWidget.topLevelItem(2).child(2).setText(1, f'{np.round(system.result_dic["parameter exp"][2][0],3)}')

                self.treeWidget.topLevelItem(3).child(0).setText(1, f'{np.round(system.result_dic["parameter exp"][3][2],3)}')
                self.treeWidget.topLevelItem(3).child(1).setText(1, f'{np.round(system.result_dic["parameter exp"][3][1],3)}')
                self.treeWidget.topLevelItem(3).child(2).setText(1, f'{np.round(system.result_dic["parameter exp"][3][0],3)}')

                self.treeWidget.topLevelItem(4).child(0).setText(1, f'{np.round(system.result_dic["parameter exp"][4][2],3)}')
                self.treeWidget.topLevelItem(4).child(1).setText(1, f'{np.round(system.result_dic["parameter exp"][4][1],3)}')
                self.treeWidget.topLevelItem(4).child(2).setText(1, f'{np.round(system.result_dic["parameter exp"][4][0],3)}')

                self.axs_2D[0].cla()
                self.axs_2D[1].cla()
                self.axs_2D[1].set_xlabel("Temps [minutes]")
                self.axs_2D[0].set_ylabel("Perte de masse [%]")
                self.axs_2D[0].plot(table_data["time_tot"],table_data["mu_tot"],"b", label="data")
                self.axs_2D[0].plot(table_data["time_tot"],system.result_dic["fitted data 5exp"],"r--", label="prediction n=5 cnes")
                markers = ["s","D","o","x","v"]
                for ind_i in range(len(system.result_dic["fitted data exp"])):
                    self.axs_2D[1].plot(table_data["time_tot"][::10],
                                    system.result_dic["fitted data exp"][ind_i][::10],
                                    "black",
                                    label=f"Expo {ind_i+1}",
                                    marker=markers[ind_i],
                                    markersize=3,
                                    linewidth=1)
                self.axs_2D[0].legend()
                self.axs_2D[1].legend()
                self.axs_2D[0].grid()
                self.axs_2D[1].grid()
                self.canvas_2D.draw()
                self.ax_3D.cla()
                self.ax_3D.set_xlabel("Temps [minutes]")
                self.ax_3D.set_ylabel("ISO [°C]")
                self.ax_3D.set_zlabel("Perte de masse [%]")
                for ind_i in range(5):
                    self.ax_3D.plot(system.result_dic["X_3D"], system.result_dic["Y_3D"][ind_i], system.result_dic["Z_3D"][ind_i,:],"black")
                self.ax_3D.plot_wireframe(system.result_dic["X_3D_smooth"], 
                                        system.result_dic["Y_3D_smooth"], 
                                        system.result_dic["Z_3D_smooth"], 
                                        color="b",
                                        alpha=0.5, 
                                        antialiased=True)
                self.canvas_3D.draw()
                
            if self.comboBox_7.currentText() == "ESTEC":
                self.treeWidget.hide()
                self.treeWidget_3.hide()
                self.treeWidget_2.show()
                system = Res_ESA.Equations_ESA(table_data, data_expo)
                system.Initialisation()
                system.function_TML_fit(n=6)
                self.axs_2D[0].cla()
                self.axs_2D[1].cla()
                self.axs_2D[1].set_xlabel("Temps [minutes]")
                self.axs_2D[0].set_ylabel("Perte de masse [%]")
                self.axs_2D[0].plot(table_data["time_tot"],table_data["mu_tot"],"b", label="data")
                self.axs_2D[0].plot(table_data["time_tot_tot"],system.result_dic["fitted data 5exp"],"r--", label="prediction n=5 cnes")
                markers = ["s","D","o","x","v"]
                for ind_i in range(len(system.result_dic["fitted data exp"])):
                    self.axs_2D[1].plot(table_data["time"][ind_i][::100],
                                    system.result_dic["fitted data exp"][ind_i][::100],
                                    "black",
                                    label=f"Expo {ind_i+1}",
                                    markersize=3,
                                    marker=markers[ind_i],
                                    linewidth=1)
                
                self.axs_2D[0].legend()
                self.axs_2D[1].legend()
                self.axs_2D[0].grid()
                self.axs_2D[1].grid()
                self.canvas_2D.draw()
                
            #table_data, data_expo = clear_data("L:\Projet_stage\LP_VB5E_3\Données\\EC9323-2.xls")

                      
            
            #system_ONERA = Equations_ONERA(table_data, data_expo)
            #system_ONERA.Initialisation()
            
            #ESA method
            #mu_t_ESA = system_ESA.function_TML_fit(n=6)
            
            #CNES method
            #mu_t_CNES, params = system_CNES.function_TML_fit()
            
            #ONERA method
            #mu_t_ONERA = system_ONERA.function_TML_fit()
            #tau = int(system_ONERA.tau)
                


        

        else:
            print("pls select a file first")
            
    def array_2_table(self, array):
        for column in range(len(array)):
            self.tableWidget.setItem(0,column,QTableWidgetItem(str(array[column])))
                    
    def pushButton_2_fonction(self):
        print("Refresh")

    

        
        
