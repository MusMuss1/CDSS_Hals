import lxml.etree as et
import xml.dom.minidom
import sys


from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *

import matplotlib.pyplot as plt
import numpy as np

#encoding for XML File
m_encoding = 'UTF-8'

# Write parameter to XML
def createxmlbak(strchronic, answerage, answergender, answerdauer, answertemp, answersmokestr, fevers, answerhustenstr, answertonsillstr, answerlymphstr):

    # Write parameter to XML
    root = et.Element("Halsschmerzen")
    id = et.SubElement(root, "id", Wert="1234")
    coding = et.SubElement(root, "coding")
    code = et.SubElement(coding, "system", Wert = "https://www.icd-code.de/")
    code = et.SubElement(coding, "system", Wert = "J03.0")
    doc = et.SubElement(root, "Tonsilitis", Bezeichnung="bakteriell")
    alter = et.SubElement(doc, "Alter", Bezeichnung="Alter")
    wert = et.SubElement(alter, "Wert").text = str(answerage)
    gender = et.SubElement(doc, "Geschlcht")
    wert = et.SubElement(gender, "Wert").text = answergender
    dauer = et.SubElement(doc, "DauerTage", Wert=str(answerdauer))
    chchronic = et.SubElement(dauer, "Chronisch", Wert=strchronic)
    risiko = et.SubElement(doc, "Risikofaktoren", Bezeichnung="Rauchen", von="Ja", bis="Nein")
    wert = et.SubElement(risiko, "Wert").text = answersmokestr
    symptom = et.SubElement(doc, "Symptopm", Bezeichnung="Koerpertemperatur", Wert=str(answertemp))
    wert = et.SubElement(symptom, "Fieber").text = fevers
    symptom = et.SubElement(doc, "Symptom", Bezeichnung="Husten")
    wert = et.SubElement(symptom, "Wert").text = answerhustenstr
    symptom = et.SubElement(doc, "Symptom", Bezeichnung="Vergroesserte oder belegte Tonsillen")
    wert = et.SubElement(symptom, "Wert").text = answertonsillstr
    symptom = et.SubElement(doc, "Symptom", Bezeichnung="Geschwollene Halslypmhknoten")
    wert = et.SubElement(symptom, "Wert").text = answerlymphstr

    dom = xml.dom.minidom.parseString(et.tostring(root))
    xml_string = dom.toprettyxml()
    part1, part2 = xml_string.split('?>')

    with open("krankheit.xml", 'w') as xfile:
        xfile.write(part1 + 'encoding=\"{}\"?>\n'.format(m_encoding) + part2)
        xfile.close()


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
        redflag = bool
        fever = bool
        chronic = bool
        strchronic = ""
        centor = 0
        mcisaac = 0
        feverpain = 0

        #m_encoding = 'UTF-8'

        answerage = self.spinboxage.value()
        answergender = self.cmbgender.currentText()
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
            #print(fever)
        else:
            fever = False
            #print(fever)

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

        #Check RedFlag
        if self.chkred_1.isChecked() or self.chkred_2.isChecked() or self.chkred_3.isChecked() or self.chkred_4.isChecked() or self.chkred_5.isChecked() or self.chkred_6.isChecked() or self.chkred_7.isChecked():
            self.txtresult.setText("Achtung !!! \nEs ist mindestens eines der 'Red Flags' vorhanden.\nEine Anwendung der scores ist hier nicht möglich. Es wird eine individuelle Beratung zur Diagnostik und Therapie empfohlen.")
            redflag = True
        else:
            redflag = False

        #if Redflag is not given -> use scores
        if redflag == False:
            # Check Smoke
            if chronic & answersmoke == 1:
                self.txtresult.setText(
                    "Achtung !!! \nEs liegt evtl. eine Chronische Erkrankung vor. Das Prüfen auf weitere Anzeichen erforderlich")
            if chronic:
                self.txtresult.setText(
                    "Achtung !!! \nEs liegt evtl. eine Chronische Erkrankung vor. Das Prüfen auf weitere Anzeichen erforderlich")

            # Scoreboard
            if chronic == False:
                if centor <= 2 and mcisaac <= 2:
                    self.txtresult.setText(
                        "Info:\nCentor und McIsaac score liegen unter 2.\nEs wird eine Symptomatische Behandlung empfohlen")
                if centor == 3 or mcisaac == 3:
                    self.txtresult.setText(
                        "Info:\nCentor oder McIsaac scroe liegen bei min. 3.\nEs wird ein Delayed prescription empfohlen\nRezept über antibiotische Therapie ausstellen. Dieses ist einzulösen bei signifikanter Verschlechterung ODER wenn nach 3-5 Tagen keine Besserung")
                    createxmlbak(strchronic, answerage, answergender, answerdauer, answertemp, answersmokestr, fevers,
                                 answerhustenstr, answertonsillstr, answerlyphstr)
                if centor == 4 or mcisaac >= 4:
                    self.txtresult.setText(
                        "Info:\nCentor- oder McIsaac-score haben einen Wert von min. 4.\nDie Wahrscheinlichkeit einer bakteriellen Infektion durch z.B. Streptokokken ist sehr hoch.\nEs wird eine antibiotische Therapie empfohlen.")
                    createxmlbak(strchronic, answerage, answergender, answerdauer, answertemp, answersmokestr, fevers,
                                 answerhustenstr, answertonsillstr, answerlyphstr)



        #Create Charts
        height = [centor, mcisaac, feverpain]
        bars = ('Centor Score', 'McIssac', 'FeverPain')
        y_pos = np.arange(len(bars))

        # Create bars
        plt.bar(y_pos, height, color=['#ffca28', '#9ccc65', '#29b6f6'])

        # Create names on the x-axis
        plt.xticks(y_pos, bars)

        # Show graphic
        plt.show()

    # update cmbfever status if temperature changed
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
