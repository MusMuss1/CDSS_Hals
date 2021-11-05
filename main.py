print("HI")
import random
import lxml.etree as et
import xml.dom.minidom
import sys

from PyQt6.QtCore import pyqtSlot
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCharts import *
from PyQt6.QtCore import *
import matplotlib.pyplot as plt
import numpy as np


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

        #btnok
        self.btnok.clicked.connect(self.createxml)
        #self.btnok.clicked.connect(self.createchart)

        #ComboBoxFieber
        listanswer=["Ja", "Nein"]
        for answer in listanswer:
            self.cmbfieber.addItem(answer)

        # ComboBoxGender
        listgender = ["M", "W", "D"]
        for answer in listgender:
            self.cmbgender.addItem(answer)

        # ComboBoxGender
        listanswer = ["Ja", "Nein"]
        for answer in listanswer:
            self.cmbhusten.addItem(answer)

        #SpinnBoxAge
        self.spinboxage.setMinimum(1)
        self.spinboxage.setMaximum(120)

        # SpinnBoxFieber
        self.spinboxtemp.setMinimum(30)
        self.spinboxtemp.setMaximum(44)
        self.spinboxtemp.setValue(36)
        self.spinboxtemp.setSuffix(" °C")
        self.spinboxtemp.setSingleStep(0.1)


#Button Clicked
    def createxml(self):

        #Declarations
        fever = bool
        centor = 0
        mcisaac = 0
        feverpain = 0

        m_encoding = 'UTF-8'

        answerage = str(self.spinboxage.value())
        #answerfieber = str(self.cmbgender.currentText())
        answerfieber = self.spinboxtemp.value()
        if answerfieber > 38:
            fever = True
            print(fever)
        else:
            fever = False
            print(fever)

        if fever == True:
            centor =+ 1
            print(centor)

        #Write parameter to XML
        root = et.Element("Halsschmerzen")
        doc = et.SubElement(root, "Tonsilitis", Bezeichnung="Tonsilitis Noninfektional")
        alter = et.SubElement(doc, "Alter", Bezeichnung="Alter")
        wert = et.SubElement(alter, "Wert").text = answerage
        dauer = et.SubElement(doc, "DauerTage", von="1", bis="14").text = "some vlaue2"
        risiko = et.SubElement(doc, "Risikofaktoren", Bezeichnung="Rauchen")
        wert = et.SubElement(risiko, "Wert").text = "Ja"
        wert = et.SubElement(risiko, "Wert").text = "Nein"
        symptom = et.SubElement(doc, "Symptopm", Bezeichnung="Fieber")
        wert = et.SubElement(symptom, "Wert").text = "answerfieber"
        wert = et.SubElement(symptom, "Wert").text = "Nein"

        dom = xml.dom.minidom.parseString(et.tostring(root))
        xml_string = dom.toprettyxml()
        part1, part2 = xml_string.split('?>')

        with open("krankheit.xml", 'w') as xfile:
            xfile.write(part1 + 'encoding=\"{}\"?>\n'.format(m_encoding) + part2)
            xfile.close()

        print("fertig")

        print(centor)

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
