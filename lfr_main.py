import sys
import re
from PySide2.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem, QHeaderView)
from ui_lfr import Ui_MainWindow
import psycopg2 as pg

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

        self.afficheCentres("""SELECT * FROM centre ORDER BY id_c;""")

        listPays = reqOnePostgresql("""SELECT DISTINCT pays FROM centre ORDER BY pays;""")
        qt.cbPays.addItems(listPays)

        listRegion = reqOnePostgresql("""SELECT DISTINCT region FROM centre ORDER BY region;""")
        qt.cbRegion.addItems(listRegion)

        listNom = reqOnePostgresql("""SELECT nom FROM centre ORDER BY nom;""")
        qt.cbNom.addItems(listNom)

        qt.leRech.textChanged.connect(self.entreeRech)
        qt.cbPays.currentIndexChanged.connect(self.cbpaysChanged)
        qt.cbRegion.currentIndexChanged.connect(self.cbregionChanged)
        qt.cbNom.currentIndexChanged.connect(self.cbnomChanged)

    def afficheCentres(self, req):
        qt = self.ui
        qt.tableWidget.setRowCount(0)
        listCentres = reqPostgresql(req)
        nbCol = reqPostgresql("""SELECT count(*) FROM information_schema.columns WHERE table_name = 'centre';""")
        namesCol = reqPostgresql("""SELECT column_name FROM information_schema.columns WHERE table_schema = 'lafriterose' AND table_name = 'centre';""")

        namesColList = []
        for name in namesCol:
            if re.match(r'id_*', name[0]):
                namesColList.append("")
            else:
                namesColList.append(name[0])

        cpt_centre = 0
        qt.tableWidget.setColumnCount(nbCol[0][0])
        qt.tableWidget.verticalHeader().hide()
        qt.tableWidget.setHorizontalHeaderLabels(namesColList)

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
        self.afficheCentres(f"""SELECT * FROM centre WHERE pays like '%{textRech}%' OR
        adresse ILIKE '%{textRech}%' OR
        region ILIKE '%{textRech}%' OR
        nom ILIKE '%{textRech}%' OR
        ville ILIKE '%{textRech}%'
         ORDER BY id_c;""")

    def cbpaysChanged(self):
        self.cbChanged('pays')
    def cbregionChanged(self):
        self.cbChanged('region')
    def cbnomChanged(self):
        self.cbChanged('nom')

    def cbChanged(self,col):
        qt = self.ui
        qt.leRech.setText("")
        if col == 'pays':
            rech = qt.cbPays.currentText()
        if col == 'region':
            rech = qt.cbRegion.currentText()
        if col == 'nom':
            rech = qt.cbNom.currentText()
        self.afficheCentres(f"""SELECT * FROM centre WHERE {col} = '{rech}'""")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mces = MainWindow()
    mces.show()

    sys.exit(app.exec_())