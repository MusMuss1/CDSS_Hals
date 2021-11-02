print("HI")
import os
import lxml.etree as et
import xml.dom.minidom
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QComboBox

#Frm Main
class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("FrmMain.ui",self)


        #button = QPushButton('PyQt5 button', self)
        #button.setToolTip('This is an example button')
        #button.move(100, 70)
        #button.clicked.connect(self.createxml)

        #btnok
        self.btnok.clicked.connect(self.createxml)

        #ComboBox
        listanswer=["Ja", "Nein"]
        for answer in listanswer:
            self.cmb1.addItem(answer)


#Button Clicked
    def createxml(self):
        m_encoding = 'UTF-8'

        root = et.Element("Halsschmerzen")
        doc = et.SubElement(root, "Tonsilitis", Bezeichnung="Tonsilitis Noninfektional")
        alter = et.SubElement(doc, "Alter", Bezeichnung="Alter")
        wert = et.SubElement(alter, "Wert").text = "3"
        dauer = et.SubElement(doc, "DauerTage", von="1", bis="14").text = "some vlaue2"
        risiko = et.SubElement(doc, "Risikofaktoren", Bezeichnung="Rauchen")
        wert = et.SubElement(risiko, "Wert").text = "Ja"
        wert = et.SubElement(risiko, "Wert").text = "Nein"
        symptom = et.SubElement(doc, "Symptopm", Bezeichnung="Fieber")
        wert = et.SubElement(symptom, "Wert").text = "Ja"
        wert = et.SubElement(symptom, "Wert").text = "Nein"

        dom = xml.dom.minidom.parseString(et.tostring(root))
        xml_string = dom.toprettyxml()
        part1, part2 = xml_string.split('?>')

        with open("krankheit.xml", 'w') as xfile:
            xfile.write(part1 + 'encoding=\"{}\"?>\n'.format(m_encoding) + part2)
            xfile.close()

        print("fertig")

app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1280)
widget.setFixedHeight(720)
widget.show()
try:
    sys.exit(app.exec())
except:
    print("Something went wromg")


#from tkinter import *
#window = Tk()
#window.title('Test')
#window.mainloop()



#f = open("krankheit" + ".xml", "w")
#f.write(str(t))
#f.write("TEST")
#f.close()
#os.system("start " + "krankheit" + ".xml")
