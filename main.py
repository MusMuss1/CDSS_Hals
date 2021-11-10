print("HI")
import random
import lxml.etree as et
import xml.dom.minidom
import sys

from PyQt6.QtCore import pyqtSlot
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
#from PyQt6.QtCharts import*
import matplotlib.pyplot as plt
import numpy as np


#def createxml(answerage):
    #if ans


#Frm Main
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("FrmMain.ui",self)
        self.setWindowTitle("CDSS")


        #button = QPushButton('PyQt5 button', self)
        #button.setToolTip('This is an example button')
        #button.move(100, 70)
        #button.clicked.connect(self.createxml)
        #t=QTextBrowser(self)
        #t.setText("TEST")


        #btnok
        self.btnok.clicked.connect(self.work)
        #self.btnok.clicked.connect(self.createchart)

        # ComboBoxPain
        listanswer = ["Nein", "Ja"]
        for answer in listanswer:
            self.cmbpain.addItem(answer)

        # ComboBoxPain
        listanswer = ["Nein", "Ja"]
        for answer in listanswer:
            self.cmbsmoke.addItem(answer)

        # ComboBoxFieber
        listanswer=["Nein", "Ja"]
        for answer in listanswer:
            self.cmbfever.addItem(answer)
            self.cmbfever.setEnabled(False)

        # ComboBoxTonsillen
        listanswer = ["Nein", "Ja"]
        for answer in listanswer:
            self.cmbtonsill.addItem(answer)

        # ComboBoxGender
        listgender = ["M", "W", "D"]
        for answer in listgender:
            self.cmbgender.addItem(answer)

        # ComboBoxGender
        listanswer = ["Nein", "Ja"]
        for answer in listanswer:
            self.cmbhusten.addItem(answer)
        # ComboBoxLymph
        listanswer = ["Nein", "Ja"]
        for answer in listanswer:
            self.cmblymph.addItem(answer)

        #Text
        self.txtresult.setText("LOL")

        # SpinnBoxAge
        self.spinboxage.setMinimum(1)
        self.spinboxage.setMaximum(120)

        # SpinnBoxFieber
        self.spinboxtemp.setMinimum(30)
        self.spinboxtemp.setMaximum(44)
        self.spinboxtemp.setValue(36)
        self.spinboxtemp.setSuffix(" °C")
        self.spinboxtemp.setSingleStep(0.1)
        self.cmbfever.setCurrentIndex(0)
        self.spinboxtemp.valueChanged.connect(self.updatecmbfever)

        # SpinnBoxTime
        self.spinboxtime.setMinimum(1)
        self.spinboxtime.setMaximum(365)


#Button Clicked
    def work(self):

        #Declarations
        fever = bool
        chronic = bool
        strchronic = ""
        centor = 0
        mcisaac = 0
        feverpain = 0

        m_encoding = 'UTF-8'

        answerage = self.spinboxage.value()
        answerdauer = self.spinboxtime.value()
        answertemp = self.spinboxtemp.value()
        fevers = str(self.cmbfever.currentText())
        answerhusten = self.cmbhusten.currentIndex()
        answerhustenstr = self.cmbhusten.currentText()
        answertonsill = self.cmbtonsill.currentIndex()
        answertonsillstr = self.cmbtonsill.currentText()
        answerlyph = self.cmblymph.currentIndex()
        answerlyphstr = self.cmblymph.currentText()
        answersmoke = self.cmbsmoke.currentIndex()
        answersmokestr = self.cmbsmoke.currentText()

        #changecmbfever(answerage)

        #Check Age
        if answerage < 15:
            mcisaac += 1
        if answerage >= 45:
            mcisaac -= 1
        else:
            mcisaac += 0

        #Check Temp
        if answertemp >= 38:
            fever = True
            print(fever)
        else:
            fever = False
            print(fever)

        #Check Fieber
        if fever == True:
            centor += 1
            mcisaac += 1
            print(centor)

        #Check Husten
        if answerhusten == 0:
            centor += 1
            mcisaac += 1

        #Check Dauer
        if answerdauer > 14:
            chronic = True
            strchronic = "Ja"
        else:
            chronic = False
            strchronic = "Nein"

        #Check Tonsill
        if answertonsill == 1:
            centor += 1
            mcisaac += 1

        #Check Lymph
        if answerlyph == 1:
            centor +=1
            mcisaac += 1
        print(centor)
        #Check Smoke
        if chronic & answersmoke == 1:
            self.txtresult.setText("Achtung !!! \nEs liegt evtl. eine Chronische Erkrankung vor. Das Prüfen auf weitere Anzeichen erforderlich")
        if chronic:
            self.txtresult.setText("Achtung !!! \nEs liegt evtl. eine Chronische Erkrankung vor. Das Prüfen auf weitere Anzeichen erforderlich")

        #Scoreboard
        if chronic == False:
            if centor <= 2 and mcisaac <= 2:
                self.txtresult.setText("Info:\nCentor und McIsaac score liegen unter 2.\nEs wird eine Symptomatische Behandlung empfohlen")
            if centor == 3 or mcisaac == 3:
                self.txtresult.setText("Info:\nUHLY.\nDU BIST HÄSSLICH")
            if centor == 4 or mcisaac >= 4:
                self.txtresult.setText("Info:\nCentor und McIsaac score liegen unter 2.\nBAKTERIEN")


        #Write parameter to XML
        root = et.Element("Halsschmerzen")
        doc = et.SubElement(root, "Tonsilitis", Bezeichnung="Erkrankung ?")
        alter = et.SubElement(doc, "Alter", Bezeichnung="Alter")
        wert = et.SubElement(alter, "Wert").text = str(answerage)
        dauer = et.SubElement(doc, "DauerTage", Wert=str(answerdauer))
        chchronic = et.SubElement(dauer, "Chronisch", Wert=strchronic)
        risiko = et.SubElement(doc, "Risikofaktoren", Bezeichnung="Rauchen", von="Ja", bis="Nein")
        wert = et.SubElement(risiko, "Wert").text = answersmokestr
        symptom = et.SubElement(doc, "Symptopm", Bezeichnung="Koerpertemperatur", Wert=str(answertemp))
        wert = et.SubElement(symptom, "Fieber").text = fevers
        symptom = et.SubElement(doc, "Symptom", Bezeichnung="Husten")
        wert = et.SubElement(symptom, "Wert").text = answerhustenstr
        symptom = et.SubElement(doc, "Symptom", Bezeichnung="Vergrößerte oder belegte Tonsillen")
        wert = et.SubElement(symptom, "Wert").text = answertonsillstr

        dom = xml.dom.minidom.parseString(et.tostring(root))
        xml_string = dom.toprettyxml()
        part1, part2 = xml_string.split('?>')

        with open("krankheit.xml", 'w') as xfile:
            xfile.write(part1 + 'encoding=\"{}\"?>\n'.format(m_encoding) + part2)
            xfile.close()


        #Create Charts
        height = [centor, mcisaac, feverpain]
        bars = ('Centor Score', 'McIssac', 'FeverPain')
        y_pos = np.arange(len(bars))

        # Create bars
        plt.bar(y_pos, height, color=['#ffca28', '#9ccc65', '#29b6f6'])
        #if centor <

        # Create names on the x-axis
        plt.xticks(y_pos, bars)

        # Show graphic
        plt.show()


    def updatecmbfever(self):
        answertemp = self.spinboxtemp.value()
        if answertemp >= 38:
            self.cmbfever.setCurrentIndex(1)
        else:
            self.cmbfever.setCurrentIndex(0)

app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1024)
widget.setFixedHeight(576)
widget.show()
try:
    sys.exit(app.exec())
except:
    print("Something went wromg")
