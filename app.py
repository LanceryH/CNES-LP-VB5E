from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
from datetime import date
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from data_mix import *
import webbrowser

dir_path = os.path.dirname(os.path.realpath(__file__))

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(dir_path + '\\ui\\window.ui', self)
        
        self.setWindowIcon(QIcon(dir_path + '\\logo\\logo.png'))
        self.setFixedSize(1120,760)
        self.setWindowTitle("LP_PY_5E")
        self.path = None
        self.temp_total_simu = []
        self.statusBar.showMessage("Cnes 2024")
        self.statusBar.addPermanentWidget(QLabel(str(date.today())))
        self.tab_6.setEnabled(False)
        self.treeWidget.expandAll()
        self.treeWidget.show()
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget_2.hide()
        self.treeWidget_2.setAlternatingRowColors(True)
        self.tableWidget.hide()
        self.tableWidget_on = False
        self.tabWidget.currentChanged.connect(self.tabWidget_fonction)
        self.figure_2D, self.axs_2D= plt.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [2,1]})#, figsize=(10, 4))
        self.figure_2D.tight_layout(rect=[0.015, 0, 0.95, 0.985])
        self.axs_2D[1].grid()
        self.axs_2D[1].set_xlabel("Temps [minutes]")
        self.axs_2D[0].set_ylabel("Perte de masse [%]")
        self.axs_2D[0].set_title("Prédiction du dégazage au cours du temps / ID: XXXX")
        self.axs_2D[0].patch.set_alpha(0)
        self.axs_2D[0].grid()
        self.twin_2D = self.axs_2D[0].twinx()
        self.twin_2D.set_ylabel("Température [°C]")
        self.twin_2D.set_ylim((0,140))
        self.canvas_2D = FigureCanvas(self.figure_2D)
        self.toolbar_2D = NavigationToolbar(self.canvas_2D,self)
        self.layout_of_2D = QtWidgets.QVBoxLayout()
        self.layout_of_2D.addWidget(self.toolbar_2D)
        self.layout_of_2D.addWidget(self.canvas_2D)
        self.twin_2D.set_zorder(self.twin_2D .get_zorder() - 1)
        self.groupBox_11.setLayout(self.layout_of_2D)
        self.figure_2D_sim, self.axs_2D_sim = plt.subplots(1, 1)#, figsize=(10, 4))
        self.figure_2D_sim.tight_layout(rect=[0.02, 0, 0.95, 0.985])
        self.axs_2D_sim.grid()
        self.axs_2D_sim.set_xlabel("Temps [minutes]")
        self.axs_2D_sim.set_ylabel("Perte de masse [%]")
        self.axs_2D_sim.patch.set_alpha(0)
        self.twin_2D_sim = self.axs_2D_sim.twinx()
        self.twin_2D_sim.set_ylabel("Température [°C]")
        self.twin_2D_sim.set_title("Simulation du dégazage au cours du temps / ID: XXXX")
        self.twin_2D_sim.set_ylim((0,140))
        self.twin_2D_sim.set_zorder(self.twin_2D .get_zorder() - 1)
        self.canvas_2D_sim = FigureCanvas(self.figure_2D_sim)
        self.toolbar_2D_sim = NavigationToolbar(self.canvas_2D_sim,self)
        self.layout_of_2D_sim = QtWidgets.QVBoxLayout()
        self.layout_of_2D_sim.addWidget(self.toolbar_2D_sim)
        self.layout_of_2D_sim.addWidget(self.canvas_2D_sim)
        self.groupBox_14.setLayout(self.layout_of_2D_sim)
        self.figure_3D = plt.figure(3)
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
        self.figure_3D_sim = plt.figure(4)
        self.ax_3D_sim = self.figure_3D_sim.add_subplot(projection='3d')
        self.figure_3D_sim.tight_layout()
        self.ax_3D_sim.view_init(elev=13, azim=-127)
        self.ax_3D_sim.grid()
        self.ax_3D_sim.set_xlabel("Temps [minutes]")
        self.ax_3D_sim.set_ylabel("ISO [°C]")
        self.ax_3D_sim.set_zlabel("Perte de masse [%]")
        self.canvas_3D_sim = FigureCanvas(self.figure_3D_sim)
        self.toolbar_3D_sim = NavigationToolbar(self.canvas_3D_sim,self)
        self.layout_of_3D_sim = QtWidgets.QVBoxLayout()
        self.layout_of_3D_sim.addWidget(self.toolbar_3D_sim)
        self.layout_of_3D_sim.addWidget(self.canvas_3D_sim)
        self.groupBox_15.setLayout(self.layout_of_3D_sim)
        self.actionOpen.triggered.connect(self.actionOpen_fonction)
        self.actionRafraichir.triggered.connect(self.actionRafraichir_fonction)
        self.actionRead_me.triggered.connect(self.actionRead_me_fonction)
        self.pushButton_2.clicked.connect(self.pushButton_2_fonction)
        self.pushButton_3.clicked.connect(self.pushButton_3_fonction)
        self.pushButton_5.clicked.connect(self.pushButton_5_fonction)
        self.pushButton_6.clicked.connect(self.pushButton_6_fonction)
        self.comboBox_7.addItems(["CNES fast", "ESTEC", "CNES"])
        self.comboBox_8.addItems(["Reg. Poly.", ""])
        self.comboBox_9.addItems(["Classique", "RegressionPol"])
        self.comboBox_7.currentIndexChanged.connect(self.comboBox_7_fonction)
        self.spinBox_8.setValue(0)
        self.spinBox_8.valueChanged.connect(self.spinBox_8_fonction)
        self.show()

        self.msg = QMessageBox()
        self.msg.setWindowTitle("Aide")
        self.msg.setText("Merci de séléctionner un fichier \n -> menu 'Fichier' \n -> cliquer 'Ouvrir'")
        self.msg.setIcon(QMessageBox.Information)
        self.msg_2 = QMessageBox()
        self.msg_2.setWindowTitle("Aide")
        self.msg_2.setText("Merci de calculer la prédiction \n -> tab 'Paramètres' \n -> cliquer 'Calculer'")
        self.msg_2.setIcon(QMessageBox.Information)
        self.msg_3 = QMessageBox()
        self.msg_3.setWindowTitle("Aide")
        self.msg_3.setText("Cette méthode nécessite d'avoir les paliers constants \n en développement")
        self.msg_3.setIcon(QMessageBox.Information)

    def pushButton_2_fonction(self):
        """Fonction qui permet d'enregistrer les paramètres et résultats de la prédiction dans un fichier.xls"""

        list_params = []
        list_lab_params = []
        try:
            if self.comboBox_7.currentText() == "CNES" or self.comboBox_7.currentText() == "CNES fast":
                params = ["A","E","mu"]
                for ind_i, expo_param in enumerate(self.system.result_dic["parameter_exp"]):
                    for ind_j, val in enumerate(expo_param):
                        list_params.append(val)
                        list_lab_params.append(f"{params[ind_j]}{ind_i+1}")
            if self.comboBox_7.currentText() == "ESTEC":
                params = ["to","mu","K","A"]
                for ind_i in range(0,len(self.system.result_dic["parameter_exp"])-1):    
                    list_lab_params.append(f"{params[2]}{ind_i+1}->{ind_i+2}")
                    list_lab_params.append(f"{params[3]}{ind_i+1}->{ind_i+2}")
                    list_params.append(self.system.result_dic["coeff_transition"][ind_i][0])
                    list_params.append(self.system.result_dic["coeff_transition"][ind_i][1])
                for ind_i, expo_param in enumerate(self.system.result_dic["parameter_exp"]):
                    for ind_j, val in enumerate(expo_param):
                        list_params.append(val)
                        if ind_j<6:
                            list_lab_params.append(f"{params[0]}{ind_i+1}")
                        else:
                            list_lab_params.append(f"{params[1]}{ind_i+1}")
            df = pd.concat([pd.DataFrame({'Params_label': list_lab_params}),
                            pd.DataFrame({'Params': list_params}),
                            pd.DataFrame({'Time [min]': self.table_data["time_tot_tot"]}),
                            pd.DataFrame({'Température [°C]': self.table_data["temp_tot_tot"]}),
                            pd.DataFrame({'TML_pred [%]': self.system.result_dic["fitted data 5exp"]}),
                            pd.DataFrame({'pred expo1 [%]': self.system.result_dic["fitted data exp"][0]}),
                            pd.DataFrame({'pred expo2 [%]': self.system.result_dic["fitted data exp"][1]}),
                            pd.DataFrame({'pred expo3 [%]': self.system.result_dic["fitted data exp"][2]}),
                            pd.DataFrame({'pred expo4 [%]': self.system.result_dic["fitted data exp"][3]}),
                            pd.DataFrame({'pred expo5 [%]': self.system.result_dic["fitted data exp"][4]})], axis=1)
            df.to_excel(f"Pred_{self.path.split("/")[-1][:-4]}.xlsx", index=True, header=True)
        except:
            self.msg_2.exec_()

    def pushButton_3_fonction(self):
        """Fonction qui permet d'enregistrer les paramètres et résultats de la simu dans un fichier.xls"""

        if self.comboBox_9.currentText() == "Classique":
            df = pd.concat([pd.DataFrame({'Time [min]': np.linspace(0,self.t_tot,len(self.result_simu))}),
                            pd.DataFrame({'Température [°C]': self.temp_total_simu}),
                            pd.DataFrame({'TML_sim [%]': self.result_simu})], axis=1)
        if self.comboBox_9.currentText() == "RegressionPol":
            df = pd.concat([pd.DataFrame({'Time [min]': np.linspace(0,self.t_tot,self.t_tot)}),
                            pd.DataFrame({'Température [°C]': self.temp_total_simu}),
                            pd.DataFrame({'TML_sim [%]': self.list_z_glob_ext})], axis=1)
        df.to_excel(f"Simu_{self.path.split("/")[-1][:-4]}_{np.unique(self.temp_total_simu)}.xlsx", index=True, header=True)

    def pushButton_6_fonction(self):
        """Fonction de la simulation (Algo + Affichage)"""
        #   Elle n'est pas optimisée et prend beaucoup de ligne
        #   mais le processus pour chaque condition est similaire

        self.temp_total_simu = []
        self.axs_2D_sim.cla()
        self.ax_3D_sim.cla()
        self.twin_2D_sim.remove()
        self.twin_2D_sim = self.axs_2D_sim.twinx()
        try:
            if self.comboBox_7.currentText() == "CNES":
                self.result_simu = [0]
                self.t_tot = 0
                for ind_i in range(len(self.data)):
                    tf = int(self.tableWidget.item(ind_i,2).text())
                    time = np.linspace(0,tf,tf)
                    temp = np.linspace(int(self.tableWidget.item(ind_i,0).text()),int(self.tableWidget.item(ind_i,1).text()),tf)
                    self.t_tot += tf
                    self.temp_total_simu.extend(temp)
                    result_palier=[]
                    for ind_j in range(len(temp)):
                        result_expo=0
                        for ind_k in range(5):
                            result_expo+=self.system.function_TML_simmu(self.system.result_dic["parameter_exp"][ind_k],time=time[ind_j],temp=temp[ind_j])
                        if result_expo>self.result_simu[-1]:
                            result_palier.append(result_expo)
                        else:
                            result_palier.append(self.result_simu[-1])
                    self.result_simu.extend(result_palier)
                self.result_simu.pop(0)

                a = self.axs_2D_sim.plot(np.linspace(0,self.t_tot,len(self.result_simu)),self.result_simu,"black", label="simu",linewidth=1)
                b = self.twin_2D_sim.plot(np.linspace(0,self.t_tot,len(self.temp_total_simu)),self.temp_total_simu,"orange", label="Température",linewidth=1)
                self.ax_3D_sim.plot_wireframe(self.system.result_dic["X_3D_smooth"], 
                                        self.system.result_dic["Y_3D_smooth"], 
                                        self.system.result_dic["Z_3D_smooth"], 
                                        color="black", 
                                        linewidth=1,
                                        antialiased=True)

            if self.comboBox_7.currentText() == "CNES fast":
                self.t_tot = 0
                self.result_simu = [0]
                if self.comboBox_9.currentText() == "Classique":
                    self.tab_6.setDisabled(True)
                    n_seg = len(self.data)
                    # Boucle par segment de l'User
                    for ind_k in range(n_seg):
                        tf = int(self.tableWidget.item(ind_k,2).text())
                        time_seg = np.linspace(0,tf,tf)
                        temp_seg = np.linspace(int(self.tableWidget.item(ind_k,0).text()),int(self.tableWidget.item(ind_k,1).text()),tf)
                        temp_pal = []
                        time_pal = []
                        list_pal = []
                        self.t_tot += tf
                        self.temp_total_simu.extend(temp_seg)
                        for ind_l in range(1,6):
                            pal_i_temp=[]
                            pal_i_time=[]
                            for ind_i, temp in enumerate(temp_seg):
                                if temp>=ind_l*25 and temp<(ind_l+1)*25: 
                                    list_pal.append(ind_l)
                                    pal_i_temp.append(temp)
                                    pal_i_time.append(time_seg[ind_i])
                            if len(pal_i_temp)!=0:
                                time_pal.append(np.array(pal_i_time)-pal_i_time[0])
                                temp_pal.append(pal_i_temp)
                        list_pal = np.unique(list_pal)
                        # Boucle par parlier atteint
                        result_seg = [0]
                        for ind_i in range(len(list_pal)):
                            # Boucle parcourant tout les 't' du palier
                            result_pal = [0]
                            for ind_j in range(len(time_pal[ind_i])):
                                # Boucle des paramètres fittés
                                expo = self.system.function_TML_simmu(self.system.result_dic["parameter_exp"][list_pal[ind_i]-1],time=time_pal[ind_i][ind_j],temp=temp_pal[ind_i][ind_j])
                                result_pal.append(expo)
                            result_pal.pop(0)
                            add_me = np.max(result_seg)
                            result_seg.extend(np.array(result_pal)+add_me)
                        result_seg.pop(0)
                        add_me = np.max(self.result_simu)
                        self.result_simu.extend(np.array(result_seg)+add_me)     
                    self.result_simu.pop(0)

                    a = self.axs_2D_sim.plot(np.linspace(0,self.t_tot,self.t_tot),self.result_simu[:self.t_tot],"black", label="simu",linewidth=1)
                    b = self.twin_2D_sim.plot(np.linspace(0,self.t_tot,self.t_tot),self.temp_total_simu,"orange", label="Température",linewidth=1)

                if self.comboBox_9.currentText() == "RegressionPol": 
                    try :
                        n_seg = len(self.data)   
                        self.tab_6.setEnabled(True)
                        list_z_glob = []
                        self.list_z_glob_ext = []
                        for ind_k in range(n_seg):
                            tf = int(self.tableWidget.item(ind_k,2).text())
                            time_seg = np.linspace(0,tf,tf)
                            temp_seg = np.linspace(int(self.tableWidget.item(ind_k,0).text()),int(self.tableWidget.item(ind_k,1).text()),tf)
                            self.t_tot += tf
                            list_x = []
                            list_y = []
                            list_z = []
                            self.temp_total_simu.extend(temp_seg)
                            for ind_d,time in enumerate(np.linspace(0,tf,tf)):
                                list_x.append(time)
                                list_y.append(temp_seg[ind_d])
                                list_z.append(self.system.result_dic["Z_3D_smooth"][int(100*(temp_seg[ind_d]-25.01)/100),int(180*time/7200)])
                            expo_encour = np.array(list_z)
                            if len(list_z_glob)>0:
                                self.list_z_glob_ext.extend(expo_encour-list_z_glob[-1][:len(expo_encour)]+self.list_z_glob_ext[-1])
                                list_z_glob.append(expo_encour)
                            else:
                                list_z_glob.append(expo_encour)
                                self.list_z_glob_ext.extend(expo_encour)
                            self.ax_3D_sim.plot(list_x,list_y,list_z,"red")
                            self.ax_3D_sim.plot(np.array(list_x)+self.t_tot-tf,list_y,list_z_glob[-1],"red")

                        a = self.axs_2D_sim.plot(np.linspace(0,self.t_tot,self.t_tot),self.list_z_glob_ext,"black", label="simu",linewidth=1)
                        b = self.twin_2D_sim.plot(np.linspace(0,self.t_tot,self.t_tot),self.temp_total_simu,"orange", label="Température",linewidth=1)
                        self.ax_3D_sim.plot_wireframe(self.system.result_dic["X_3D_smooth"], 
                                                    self.system.result_dic["Y_3D_smooth"], 
                                                    self.system.result_dic["Z_3D_smooth"], 
                                                    color="black", 
                                                    linewidth=1,
                                                    antialiased=True,
                                                    alpha=0.3)
                        self.ax_3D_sim.plot(np.linspace(0,self.t_tot,self.t_tot)[::100],self.temp_total_simu[::100],np.zeros(self.t_tot)[::100],"orange")
                    except:
                        self.msg_3.exec_()
                        pass

            if self.comboBox_7.currentText() == "ESTEC":
                n_seg = len(self.data)
                self.t_tot = 0
                # Boucle par segment de l'User
                self.result_simu = [0]
                for ind_k in range(n_seg):
                    tf = int(self.tableWidget.item(ind_k,2).text())
                    time_seg = np.linspace(0,tf,tf)
                    temp_seg = np.linspace(int(self.tableWidget.item(ind_k,0).text()),int(self.tableWidget.item(ind_k,1).text()),tf)
                    temp_pal = []
                    time_pal = []
                    list_pal = []
                    self.t_tot += tf
                    self.temp_total_simu.extend(temp_seg)
                    for ind_l in range(1,6):
                        pal_i_temp=[]
                        pal_i_time=[]
                        for ind_i, temp in enumerate(temp_seg):
                            if temp>=ind_l*25 and temp<(ind_l+1)*25: 
                                list_pal.append(ind_l)
                                pal_i_temp.append(temp)
                                pal_i_time.append(time_seg[ind_i])
                        if len(pal_i_temp)!=0:
                            time_pal.append(np.array(pal_i_time)-pal_i_time[0])
                            temp_pal.append(pal_i_temp)
                    list_pal = np.unique(list_pal)
                    # Boucle par parlier atteint
                    result_seg = [0]
                    for ind_i in range(len(list_pal)):
                        # Boucle parcourant tout les 't' du palier
                        result_pal = [0]
                        for ind_j in range(len(time_pal[ind_i])):
                            # Boucle des paramètres fittés
                            expo = self.system.function_TML_simmu(self.system.result_dic["parameter_exp"][list_pal[ind_i]-1],time=time_pal[ind_i][ind_j],temp=temp_pal[ind_i][ind_j], Tref=temp_pal[ind_i][0])
                            result_pal.append(expo)
                        result_pal.pop(0)
                        add_me = np.max(result_seg)
                        result_seg.extend(np.array(result_pal)+add_me)
                    result_seg.pop(0)
                    add_me = np.max(self.result_simu)
                    self.result_simu.extend(np.array(result_seg)+add_me)           
                self.result_simu.pop(0)

                a = self.axs_2D_sim.plot(np.linspace(0,self.t_tot,self.t_tot),self.result_simu[:self.t_tot],"black", label="simu",linewidth=1)
                b = self.twin_2D_sim.plot(np.linspace(0,self.t_tot,self.t_tot),self.temp_total_simu,"orange", label="Température",linewidth=1)
                self.ax_3D_sim.plot_wireframe(self.system.result_dic["X_3D_smooth"], 
                                        self.system.result_dic["Y_3D_smooth"], 
                                        self.system.result_dic["Z_3D_smooth"], 
                                        color="black", 
                                        linewidth=1,
                                        antialiased=True)

            lns = a + b
            labs = [l.get_label() for l in lns]
            self.twin_2D_sim.set_ylabel("Température [°C]")
            self.twin_2D_sim.set_zorder(self.twin_2D .get_zorder() - 1)
            self.axs_2D_sim.set_xlabel("Temps [minutes]")
            self.axs_2D_sim.set_ylabel("Perte de masse [%]")    
            self.axs_2D_sim.set_title("Simulation du dégazage au cours du temps / ID: "+self.path.split("/")[-1])
            self.axs_2D_sim.legend(lns, labs)
            self.axs_2D_sim.grid()
            self.axs_2D_sim.patch.set_alpha(0)
            self.twin_2D_sim.set_ylim((0,140))
            self.twin_2D.set_zorder(self.twin_2D .get_zorder() - 1)
            self.ax_3D_sim.grid()
            self.ax_3D_sim.set_xlabel("Temps [minutes]")
            self.ax_3D_sim.set_ylabel("ISO [°C]")
            self.ax_3D_sim.set_zlabel("Perte de masse [%]")
            self.canvas_3D_sim.draw()
            self.canvas_2D_sim.draw()
        except:
            self.msg_2.exec_()

    def spinBox_8_fonction(self):
        """Fonction affichage données dans la table"""
        try:
            self.temp_total_simu = []
            self.tableWidget.setRowCount(int(self.spinBox_8.value()))
            self.data = []
            for ind_i in range(1,int(self.spinBox_8.value())+1):
                self.data.append((str(25*ind_i),str(25*ind_i),str(1440)))
            for i, (T_init, T_fin, Duree) in enumerate(self.data):
                item_T_init = QTableWidgetItem(T_init)
                item_T_fin = QTableWidgetItem(T_fin)
                item_Duree = QTableWidgetItem(Duree)

                self.tableWidget.setItem(i, 0, item_T_init)
                self.tableWidget.setItem(i, 1, item_T_fin)
                self.tableWidget.setItem(i, 2, item_Duree)
        except:
            pass

    def tabWidget_fonction(self):
        """Fonction d'affichage"""
        try:
            if self.tableWidget_on:
                self.tableWidget_on = False
                self.tableWidget.hide()
                if self.comboBox_7.currentText() == "CNES":
                    self.treeWidget.show()

                if self.comboBox_7.currentText() == "CNES fast":
                    self.treeWidget.show()

                if self.comboBox_7.currentText() == "ESTEC":
                    self.treeWidget_2.show()

            else:
                self.tableWidget_on = True
                self.tableWidget.show()
                self.treeWidget_2.hide()
                self.treeWidget.hide()
        except:
            pass

    def comboBox_7_fonction(self):
        """Fonction d'affichage'"""

        if self.comboBox_7.currentText() == "CNES":
            self.treeWidget_2.hide()
            self.tableWidget.hide()
            self.treeWidget.show()

        if self.comboBox_7.currentText() == "CNES fast":
            self.treeWidget_2.hide()
            self.tableWidget.hide()
            self.treeWidget.show()

        if self.comboBox_7.currentText() == "ESTEC":
            self.treeWidget_2.show()
            self.tableWidget.hide()
            self.treeWidget.hide()
    
    def actionRafraichir_fonction(self):
        """Fonction permettant de rafraichir les plots"""

        self.axs_2D[0].cla()
        self.axs_2D[1].cla()
        self.axs_2D[0].grid()
        self.axs_2D[1].grid()
        self.axs_2D[0].patch.set_alpha(0)
        self.axs_2D[1].set_xlabel("Temps [minutes]")
        self.axs_2D[0].set_ylabel("Perte de masse [%]")
        self.canvas_2D.draw()

        self.axs_2D_sim.cla()
        self.axs_2D_sim.grid()
        self.axs_2D_sim.patch.set_alpha(0)
        self.axs_2D_sim.set_xlabel("Temps [minutes]")
        self.axs_2D_sim.set_ylabel("Perte de masse [%]")
        self.canvas_2D_sim.draw()

        self.ax_3D.cla()
        self.ax_3D.view_init(elev=13, azim=-127)
        self.ax_3D.grid()
        self.ax_3D.set_xlabel("Temps [minutes]")
        self.ax_3D.set_ylabel("ISO [°C]")
        self.ax_3D.set_zlabel("Perte de masse [%]")
        self.canvas_3D.draw()

        self.ax_3D_sim.cla()
        self.ax_3D_sim.view_init(elev=13, azim=-127)
        self.ax_3D_sim.grid()
        self.ax_3D_sim.set_xlabel("Temps [minutes]")
        self.ax_3D_sim.set_ylabel("ISO [°C]")
        self.ax_3D_sim.set_zlabel("Perte de masse [%]")
        self.canvas_3D_sim.draw()


    def actionRead_me_fonction(sef):
        """Fonction Aide du menubar"""
        webbrowser.open('https://github.com/LanceryH/Cnes_LP_VB5E/blob/main/README.md')

    def actionOpen_fonction(self):
        """Fonction Ouvrir du menubar + affichage des données"""
        msg = QMessageBox()
        msg.setWindowTitle("Aide")
        msg.setText("Merci de séléctionner un fichier \n -> menu 'Fichier' \n -> cliquer 'Ouvrir'")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        path, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file', '', '(*.xlsx *.xls)')
        if path:
            self.path = path
            self.table_data, self.data_expo = clear_data(self.path)
        try:
            self.axs_2D[0].cla()
            self.axs_2D[0].set_title("Prédiction du dégazage au cours du temps / ID: "+self.path.split("/")[-1])
            self.axs_2D[0].plot(self.table_data["time_tot"],self.table_data["mu_tot"],"b",label="data", linewidth=1)
            self.axs_2D[0].set_ylabel("Perte de masse [%]")
            self.axs_2D[0].grid()
            self.axs_2D[0].patch.set_alpha(0)
            self.axs_2D[0].legend()
            self.canvas_2D.draw() 
        except:
            pass

    def pushButton_5_fonction(self):
        """Fonction calcul de la prédiction suivant le choix + affichage paramètres dans la table + affichage des courbes"""
        import resolution_CNES as Res_CNES
        import resolution_ESA as Res_ESA
        import resolution_ONERA as Res_ONERA
        import resolution_CNES_M as Res_CNES_M

        try:
            self.axs_2D[0].cla()
            self.axs_2D[1].cla()
            self.ax_3D.cla()
            
            if self.comboBox_7.currentText() == "CNES":
                self.treeWidget_2.hide()
                self.tableWidget.hide()
                self.treeWidget.show()
                self.system = Res_CNES.Equations_CNES(self.table_data, self.data_expo, 5)
                self.system.Initialisation()
                self.system.function_TML_fit()  

                for ind_i in range(5):
                    self.treeWidget.topLevelItem(ind_i).child(0).setText(1, f'{np.round(self.system.result_dic["parameter_exp"][ind_i][2],3)}')
                    self.treeWidget.topLevelItem(ind_i).child(1).setText(1, f'{np.round(self.system.result_dic["parameter_exp"][ind_i][1],3)}')
                    self.treeWidget.topLevelItem(ind_i).child(2).setText(1, f'{np.round(self.system.result_dic["parameter_exp"][ind_i][0],3)}')

                a = self.axs_2D[0].plot(self.table_data["time_tot"],self.table_data["mu_tot"],"b", label="data", linewidth=1)
                b = self.axs_2D[0].plot(self.table_data["time_tot"],self.system.result_dic["fitted data 5exp"],"r--", label="prediction CNES", linewidth=1)

                for ind_i in range(len(self.system.result_dic["fitted data exp"])):
                    self.axs_2D[1].plot(self.table_data["time_tot"][::2],
                                    self.system.result_dic["fitted data exp"][ind_i][::2],
                                    "black",
                                    label=f"Expo {ind_i+1}",
                                    #marker=markers[ind_i],
                                    markersize=2,
                                    linewidth=1)
                
                self.ax_3D.plot_wireframe(self.system.result_dic["X_3D_smooth"], 
                                        self.system.result_dic["Y_3D_smooth"], 
                                        self.system.result_dic["Z_3D_smooth"], 
                                        color="black", 
                                        linewidth=1,
                                        antialiased=True)
                                
            if self.comboBox_7.currentText() == "ESTEC":
                self.treeWidget.hide()
                self.tableWidget.hide()
                self.treeWidget_2.show()
                self.system = Res_ESA.Equations_ESA(self.table_data, self.data_expo)
                self.system.Initialisation()
                self.system.function_TML_fit(n=6)

                for ind_i in range(5):
                    for ind_k in range(6):
                        self.treeWidget_2.topLevelItem(ind_i+ind_i*2).child(1).child(ind_k).setText(1, f'{np.round(self.system.result_dic["parameter_exp"][ind_i][ind_k],8)}')
                        self.treeWidget_2.topLevelItem(ind_i+ind_i*2).child(0).child(ind_k).setText(1, f'{np.round(self.system.result_dic["parameter_exp"][ind_i][ind_k+6],8)}')
                self.treeWidget_2.topLevelItem(1).setText(1, f'{np.round(self.system.result_dic["coeff_transition"][0][0],8)}')
                self.treeWidget_2.topLevelItem(2).setText(1, f'{np.round(self.system.result_dic["coeff_transition"][0][1],8)}')
                self.treeWidget_2.topLevelItem(4).setText(1, f'{np.round(self.system.result_dic["coeff_transition"][1][0],8)}')
                self.treeWidget_2.topLevelItem(5).setText(1, f'{np.round(self.system.result_dic["coeff_transition"][1][1],8)}')
                self.treeWidget_2.topLevelItem(7).setText(1, f'{np.round(self.system.result_dic["coeff_transition"][2][0],8)}')
                self.treeWidget_2.topLevelItem(8).setText(1, f'{np.round(self.system.result_dic["coeff_transition"][2][1],8)}')
                self.treeWidget_2.topLevelItem(10).setText(1, f'{np.round(self.system.result_dic["coeff_transition"][3][0],8)}')
                self.treeWidget_2.topLevelItem(11).setText(1, f'{np.round(self.system.result_dic["coeff_transition"][3][1],8)}')

                a = self.axs_2D[0].plot(self.table_data["time_tot"],self.table_data["mu_tot"],"b", label="data", linewidth=1)
                b = self.axs_2D[0].plot(self.table_data["time_tot_tot"],self.system.result_dic["fitted data 5exp"],"r--", label="prediction ESA", linewidth=1)
                
                for ind_i in range(len(self.system.result_dic["fitted data exp"])):
                    self.axs_2D[1].plot((np.array(self.table_data["time_tot_tot"])+(24*60*ind_i))[:24*60*(5-ind_i)][::100],
                                            self.system.result_dic["fitted data exp"][ind_i][:24*60*(5-ind_i)][::100],
                                                        "black",
                                                        label=f"Expo {ind_i+1}",
                                                        markersize=2,
                                                        #marker=markers[ind_i],
                                                        linewidth=1)
                    
                self.ax_3D.plot_wireframe(self.system.result_dic["X_3D_smooth"], 
                                        self.system.result_dic["Y_3D_smooth"], 
                                        self.system.result_dic["Z_3D_smooth"], 
                                        color="black", 
                                        linewidth=1,
                                        antialiased=True)
            
            if self.comboBox_7.currentText() == "CNES fast":
                self.treeWidget_2.hide()
                self.tableWidget.hide()
                self.treeWidget.show()
                self.system = Res_CNES_M.Equations_CNES_M(self.table_data, self.data_expo)
                self.system.Initialisation()
                self.system.function_TML_fit()  

                for ind_i in range(5):
                    self.treeWidget.topLevelItem(ind_i).child(0).setText(1, f'{np.round(self.system.result_dic["parameter_exp"][ind_i][2],3)}')
                    self.treeWidget.topLevelItem(ind_i).child(1).setText(1, f'{np.round(self.system.result_dic["parameter_exp"][ind_i][1],3)}')
                    self.treeWidget.topLevelItem(ind_i).child(2).setText(1, f'{np.round(self.system.result_dic["parameter_exp"][ind_i][0],3)}')

                a = self.axs_2D[0].plot(self.table_data["time_tot"],self.table_data["mu_tot"],"b", label="data", linewidth=1)
                b = self.axs_2D[0].plot(self.table_data["time_tot_tot"],self.system.result_dic["fitted data 5exp"],"r--", label="prediction CNES", linewidth=1)
                markers = ["s","D","o","x","v"]
                for ind_i in range(len(self.system.result_dic["fitted data exp"])):
                    self.axs_2D[1].plot((np.array(self.table_data["time_tot_tot"])+(24*60*ind_i))[:24*60*(5-ind_i)][::100],
                                            self.system.result_dic["fitted data exp"][ind_i][:24*60*(5-ind_i)][::100],
                                                        "black",
                                                        label=f"Expo {ind_i+1}",
                                                        markersize=2,
                                                        #marker=markers[ind_i],
                                                        linewidth=1)

                self.ax_3D.plot_wireframe(self.system.result_dic["X_3D_smooth"], 
                                        self.system.result_dic["Y_3D_smooth"], 
                                        self.system.result_dic["Z_3D_smooth"], 
                                        color="black", 
                                        linewidth=1,
                                        antialiased=True)
                
            self.ax_3D.set_xlabel("Temps [minutes]")
            self.ax_3D.set_ylabel("ISO [°C]")
            self.ax_3D.set_zlabel("Perte de masse [%]")
            self.axs_2D[1].set_xlabel("Temps [minutes]")
            self.axs_2D[0].set_ylabel("Perte de masse [%]")
            self.axs_2D[0].set_title("Prédiction du dégazage au cours du temps / ID: "+self.path.split("/")[-1])
            self.axs_2D[0].grid()
            self.axs_2D[1].grid()
            self.axs_2D[0].patch.set_alpha(0)
            self.twin_2D.set_zorder(self.twin_2D .get_zorder() - 1)
            c = self.twin_2D.plot(self.table_data["time_tot"],self.table_data["temp_tot"],"orange", label="Température", linewidth=1)  
            lns = a + b + c
            labs = [l.get_label() for l in lns] 
            self.axs_2D[0].legend(lns, labs)
            self.canvas_2D.draw() 
            self.canvas_3D.draw()

        except:
            self.msg.exec_()

    def array_2_table(self, array):
        for column in range(len(array)):
            self.tableWidget.setItem(0,column,QTableWidgetItem(str(array[column])))
