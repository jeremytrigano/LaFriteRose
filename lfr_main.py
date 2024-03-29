import sys
import re

from PySide2.QtCore import QDate
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem, QDialog)
from ui_lfr import Ui_MainWindow
from ui_lfr_centre import Ui_Form
import psycopg2 as pg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

user = 'lafriterose'
password = 'lfr'
host = '127.0.0.1'
port = 5432
dbname = 'lafriterose'
dsn = f"host='{host}' port={port} dbname='{dbname}'"

# exécution rêquete
def reqPostgresql(requete):
    with pg.connect(dsn=dsn, user=user, password=password) as conn:
        conn.set_session(autocommit=True)
        with conn.cursor() as cursor:
            cursor.execute(requete)
            listRes = list(cursor)
    return listRes

# exécution rêquete qui ne renvoie qu'une colonne
def reqOnePostgresql(requete):
    with pg.connect(dsn=dsn, user=user, password=password) as conn:
        conn.set_session(autocommit=True)
        with conn.cursor() as cursor:
            cursor.execute(requete)
            listRes = list(cursor)

    listF = []
    for elem in listRes:
        listF.append(elem[0])
    return listF


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        qt = self.ui
        qt.setupUi(self)

        qt.deNaissance.setDate(QDate(np.random.randint(1950, 2001), np.random.randint(1, 13), np.random.randint(1, 29)))
        auj = QDate().currentDate()
        qt.deDebut.setDate(auj)
        qt.deFin.setDate(auj.addDays(7))

        self.afficheCentres("""SELECT * FROM centre ORDER BY id_c;""")

        listPays = reqOnePostgresql("""SELECT DISTINCT pays FROM centre ORDER BY pays;""")
        qt.cbPays.addItems(listPays)

        listRegion = reqOnePostgresql("""SELECT DISTINCT region FROM centre ORDER BY region;""")
        qt.cbRegion.addItems(listRegion)

        listNom = reqOnePostgresql("""SELECT nom FROM centre ORDER BY nom;""")
        qt.cbNom.addItems(listNom)
        qt.cbCentreRes.addItems(["Tous les noms"] + listNom)

        qt.leRech.textChanged.connect(self.entreeRech)
        qt.cbPays.currentIndexChanged.connect(self.cbpaysChanged)
        qt.cbRegion.currentIndexChanged.connect(self.cbregionChanged)
        qt.cbNom.currentIndexChanged.connect(self.cbnomChanged)
        qt.tableWidget.cellDoubleClicked.connect(self.selecCentre)
        qt.cbCentreRes.currentIndexChanged.connect(self.selecAffImage)
        qt.pbValidRes.clicked.connect(self.reservation)

    def afficheCentres(self, req):
        qt = self.ui
        qt.tableWidget.setRowCount(0)
        listCentres = reqPostgresql(req)
        nbCol = reqPostgresql("""SELECT count(*) FROM information_schema.columns WHERE table_name = 'centre';""")
        namesCol = reqPostgresql("""SELECT column_name FROM information_schema.columns WHERE table_schema = 'lafriterose' AND table_name = 'centre';""")
        namesCol.remove(('nom_image',))

        self.namesColList = []
        for name in namesCol:
            if re.match(r'id_*', name[0]):
                self.namesColList.append("")
            else:
                self.namesColList.append(name[0])

        cpt_centre = 0
        qt.tableWidget.setColumnCount(nbCol[0][0]-1)
        qt.tableWidget.verticalHeader().hide()
        qt.tableWidget.setHorizontalHeaderLabels(self.namesColList)

        for centre in listCentres:
            qt.tableWidget.setRowCount(cpt_centre + 1)
            cpt_elemCentre = 0
            for elemCentre in centre:
                qt.tableWidget.setItem(cpt_centre, cpt_elemCentre, QTableWidgetItem(str(elemCentre)))
                cpt_elemCentre += 1
            cpt_centre += 1

    def entreeRech(self):
        qt = self.ui
        textRech = qt.leRech.text()
        textRech = textRech.replace("'", "''")
        self.afficheCentres(f"""SELECT * FROM centre WHERE pays ILIKE '%{textRech}%' OR
        adresse ILIKE '%{textRech}%' OR
        region ILIKE '%{textRech}%' OR
        nom ILIKE '%{textRech}%' OR
        ville ILIKE '%{textRech}%'
         ORDER BY id_c;""")

    def cbpaysChanged(self):
        qt = self.ui
        qt.cbRegion.currentIndexChanged.disconnect(self.cbregionChanged)
        qt.cbRegion.setCurrentIndex(0)
        qt.cbRegion.currentIndexChanged.connect(self.cbregionChanged)
        qt.cbNom.currentIndexChanged.disconnect(self.cbnomChanged)
        qt.cbNom.setCurrentIndex(0)
        qt.cbNom.currentIndexChanged.connect(self.cbnomChanged)
        self.cbChanged('pays')

    def selecCentre(self):
        qt = self.ui

        wAffichCentre = QDialog()
        uiAffichCentre = Ui_Form()
        uiAffichCentre.setupUi(wAffichCentre)

        rowSelec = qt.tableWidget.currentItem().row()
        idSelec = int(qt.tableWidget.item(rowSelec, 0).text())
        listIdSelec = reqPostgresql(f"""SELECT * FROM centre WHERE id_c = {idSelec};""")
        listAnIdSelect = reqOnePostgresql(f"""SELECT intitule FROM animation a
                                            JOIN proposer p ON a.id_an = p.id_an
                                            JOIN centre c ON p.id_c = c.id_c
                                            WHERE c.id_c = {idSelec};""")

        textDescr = ""
        for i in range(len(self.namesColList)):
            if i != 0:
                textDescr += self.namesColList[i] + " : " + listIdSelec[0][i] + "\n"

        textAnim = "Animation(s) proposée(s) : \n"
        for elem in listAnIdSelect:
            textAnim += elem + "\n"

        uiAffichCentre.teDescr.setText(textDescr)
        uiAffichCentre.teAnim.setText(textAnim)

        freq = [np.random.randint(100, 200), np.random.randint(100, 200), np.random.randint(100, 200), np.random.randint(200, 300),
                np.random.randint(300, 400), np.random.randint(500, 600), np.random.randint(700, 800), np.random.randint(700, 800),
                np.random.randint(500, 600), np.random.randint(300, 400), np.random.randint(200, 300), np.random.randint(100, 200)]
        mois = range(1, 13)

        fig, ax = plt.subplots()
        ax.plot(mois, freq)

        plt.xticks(np.arange(min(mois), max(mois) + 1, 1.0))

        ax.set(xlabel='mois', ylabel='fréq.',
               title='Fréquentation du centre')
        ax.grid(True, linestyle='dotted')

        canvas = FigureCanvas(fig)
        uiAffichCentre.horizontalLayout_2.addWidget(canvas)
        self.setLayout(uiAffichCentre.horizontalLayout_2)

        wAffichCentre.exec_()

    def cbregionChanged(self):
        qt = self.ui
        qt.cbPays.currentIndexChanged.disconnect(self.cbpaysChanged)
        qt.cbPays.setCurrentIndex(0)
        qt.cbPays.currentIndexChanged.connect(self.cbpaysChanged)
        qt.cbNom.currentIndexChanged.disconnect(self.cbnomChanged)
        qt.cbNom.setCurrentIndex(0)
        qt.cbNom.currentIndexChanged.connect(self.cbnomChanged)
        self.cbChanged('region')
    def cbnomChanged(self):
        qt = self.ui
        qt.cbPays.currentIndexChanged.disconnect(self.cbpaysChanged)
        qt.cbPays.setCurrentIndex(0)
        qt.cbPays.currentIndexChanged.connect(self.cbpaysChanged)
        qt.cbRegion.currentIndexChanged.disconnect(self.cbregionChanged)
        qt.cbRegion.setCurrentIndex(0)
        qt.cbRegion.currentIndexChanged.connect(self.cbregionChanged)
        self.cbChanged('nom')

    def cbChanged(self, col):
        qt = self.ui
        qt.leRech.setText("")
        if col == 'pays':
            rech = qt.cbPays.currentText()
            rech = rech.replace("'", "''")
            if rech == "Tous les pays":
                rech = ""
        if col == 'region':
            rech = qt.cbRegion.currentText()
            rech = rech.replace("'", "''")
            if rech == "Toutes les régions":
                rech = ""
        if col == 'nom':
            rech = qt.cbNom.currentText()
            rech = rech.replace("'", "''")
            if rech == "Tous les noms":
                rech = ""
        if rech == "":
            self.afficheCentres("""SELECT * FROM centre ORDER BY id_c;""")
        else:
            self.afficheCentres(f"""SELECT * FROM centre WHERE {col} = '{rech}' ORDER BY id_c;""")

    def selecAffImage(self):
        qt = self.ui
        rech = qt.cbCentreRes.currentText()
        rech = rech.replace("'", "''")
        if rech != "Tous les noms":
            pixCentre = reqOnePostgresql(f"""SELECT nom_image FROM centre WHERE nom = '{rech}'""")
            if pixCentre[0] != None:
                self.ui.lImage.setPixmap(QPixmap(f"img/{pixCentre[0]}"))
            else:
                self.ui.lImage.setPixmap(QPixmap("img/lfr_small.jpg"))
        else:
            self.ui.lImage.setPixmap(QPixmap("img/lfr_small.jpg"))

    def reservation(self):
        qt = self.ui
        msgErr = ""
        if qt.leNom.text() == "":
            msgErr += "<font color='red'>Le nom n'est pas renseigné</font><br>"
        if qt.lePrenom.text() == "":
            msgErr += "<font color='red'>Le prénom n'est pas renseigné</font><br>"
        qt.lMsgErr.setText(msgErr)

        if msgErr == "":
            qt.lMsgErr.setText("<font color='green'>GOGOGO</font><br>")
            nom = qt.leNom.text().replace("'", "")
            prenom = qt.lePrenom.text().replace("'", "")
            date_de_naissance = f"{qt.deNaissance.date().day():02d}/{qt.deNaissance.date().month():02d}/{qt.deNaissance.date().year()}"
            requete = f"""INSERT INTO vacancier (nom, prenom, date_de_naissance, statut) VALUES ('{nom}', '{prenom}', '{date_de_naissance}', 'nouveau')"""
            with pg.connect(dsn=dsn, user=user, password=password) as conn:
                conn.set_session(autocommit=True)
                with conn.cursor() as cursor:
                    cursor.execute(requete)
                    qt.lMsgErr.setText("<font color='green'>Inscription validée</font><br>")




if __name__ == "__main__":
    app = QApplication(sys.argv)

    mces = MainWindow()
    mces.show()

    sys.exit(app.exec_())