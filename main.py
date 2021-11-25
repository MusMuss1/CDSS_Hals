import lxml.etree as et
from lxml.etree import fromstring
import xml.dom.minidom
import sys

from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *

import matplotlib.pyplot as plt
import numpy as np

#encoding for XML File
m_encoding = 'UTF-8'

#Load XML Database
tree = et.parse('Leitlinie.xml')
root = tree.getroot()

#Values

#Age
minage = root[2][0].get("von")
minage = int(minage)
print(minage)
#Fever
tempfever = root[2][22].get("min")
tempfever = float(tempfever)

#Labels
age = root[2][0].get("Bezeichnung")
symptomhusten = root[2][23].get("Bezeichnung")
symptomtonsillex = root[2][20].get("Bezeichnung")
symptomlymph = root[2][21].get("Bezeichnung")
symptomroetung = root[2][25].get("Bezeichnung")



#load data from XML Database
def loadxml(self):
    #Path to XML Database
    tree = et.parse('Leitlinie.xml')
    root = tree.getroot()

    #search all RedFlags get the name and print to Combobox
    flags = root.getchildren()[2]
    flag_list = flags.findall('RedFlags')
    print(len(flag_list))
    for flag in flag_list:
        self.cmbredflag.addItem(flag.get("Bezeichnung"))

    # search all Other get the name and print to Combobox
    other = root.getchildren()[2]
    other_things = other.findall('andereUrsachen')

    for other in other_things:
        self.cmbother.addItem(other.get("Bezeichnung"))

    # search all dangers get the name and print to Combobox
    danger = root.getchildren()[2]
    dangers = danger.findall('GefaehrlicherVerlauf')

    for danger in dangers:
        self.cmbdanger.addItem(danger.get("Bezeichnung"))


# Write parameter to XML
def createxmlbak(strchronic, answerage, answergender, answerdauer, answertemp, fevers, answerhustenstr, answertonsillstr, answerlymphstr,answerredflag,answerother,symptomhusten, symptomlymph, symptomtonsillex, symptomroetung):

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
    symptom = et.SubElement(doc, "Symptopm", Bezeichnung="Koerpertemperatur", Wert=str(answertemp))
    wert = et.SubElement(symptom, "Fieber").text = fevers
    symptom = et.SubElement(doc, "Symptom", Bezeichnung=symptomhusten)
    wert = et.SubElement(symptom, "Wert").text = answerhustenstr
    symptom = et.SubElement(doc, "Symptom", Bezeichnung=symptomtonsillex)
    wert = et.SubElement(symptom, "Wert").text = answertonsillstr
    symptom = et.SubElement(doc, "Symptom", Bezeichnung=symptomlymph)
    wert = et.SubElement(symptom, "Wert").text = answerlymphstr
    symptom = et.SubElement(doc, "Symptom", Bezeichnung=symptomroetung)
    wert = et.SubElement(symptom, "Wert").text = answerlymphstr
    other = et.SubElement(doc, "andereUrsachen", Bezeichnung=answerother)
    redflag = et.SubElement(doc, "RedFlag", Bezeichnung = answerredflag)

    #create xml documentobjectmodel
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

        #ComboboxRedflags
        self.cmbredflag.addItem("Nein")
        self.cmbother.addItem("Nein")
        self.cmbdanger.addItem("Nein")

        # Get infos from XML Databasefile in Comboboxes
        loadxml(self)

        # GroupBoxes
        self.grpanamnese.setVisible(False)
        self.grpredflags.setVisible(False)
        self.grpother.setVisible(False)

        #set text for label form xml
        self.lblage.setText(age)
        self.lblsymptom1.setText(symptomhusten)
        self.lblsymptom2.setText(symptomtonsillex)
        self.lblsymptom3.setText(symptomlymph)
        self.lblsymptom4.setText(symptomroetung)

        #btnok
        self.btnok.clicked.connect(self.work)
        self.btnok_start.clicked.connect(self.start)

        self.btnload.clicked.connect(self.loadxml2)

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

        # ComboBoxRoetung
        listanswer = ["Nein", "Ja"]
        for answer in listanswer:
            self.cmbroet.addItem(answer)

        #Text
        self.txtresult.setText("Hallo")

        # SpinnBoxAge
        self.spinboxage.setMinimum(minage)
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
        self.spinboxtime.valueChanged.connect(self.updatetime)


    def start(self):
        if self.cmbdanger.currentIndex() == 0:
            print("FAMFKLMKL")
            self.grpdanger.setVisible(False)
            self.grpanamnese.setVisible(True)
            self.grpredflags.setVisible(True)
            self.grpother.setVisible(True)


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
        answerroet = self.cmbroet.currentIndex()
        answerroetstr =self.cmbroet.currentText()

        answerredflag = self.cmbredflag.currentText()
        answerother = self.cmbother.currentText()


        #Check Age
        if answerage < 15:
            mcisaac += 1
        if answerage >= 45:
            mcisaac -= 1
        else:
            mcisaac += 0

        #Check Temp
        if answertemp >= tempfever:
            fever = True
            #print(fever)
        else:
            fever = False
            #print(fever)

        #Check Fieber
        if fever == True:
            centor += 1
            mcisaac += 1
            feverpain += 1
            print(centor)

        #Check Husten
        if answerhusten == 0:
            centor += 1
            mcisaac += 1
            feverpain += 1

        #Check Dauer
        if answerdauer > 14:
            chronic = True
            strchronic = "Ja"
        if answerdauer <= 3:
            feverpain += 1
            chronic = False
        else:
            chronic = False
            strchronic = "Nein"

        #Check Tonsill
        if answertonsill == 1:
            centor += 1
            mcisaac += 1
            feverpain += 1

        #Check Lymph
        if answerlyph == 1:
            centor +=1
            mcisaac += 1

        # Check Roetng
        if answerroet == 1:
            feverpain += 1


        #List for all parameters need for create xml
        parameters = [strchronic, answerage, answergender, answerdauer, answertemp, fevers, answerhustenstr, answertonsillstr, answerlyphstr, answerredflag, answerother, symptomhusten, symptomlymph, symptomtonsillex, symptomroetung]

        #Check RedFlag
        if self.cmbredflag.currentIndex() != 0:
            createxmlbak(*parameters)
            redflag = True
        else:
            redflag = False

        #if Redflag is not given -> use scores
        if redflag == False:
            # Check Smoke
            if chronic :
                self.txtresult.setText(
                    "Achtung !!! \nEs liegt evtl. eine Chronische Erkrankung vor. Das Prüfen auf weitere Anzeichen erforderlich")

            # Scoreboard
            if chronic == False:
                if centor <= 2 and mcisaac <= 2 and feverpain <= 2:
                    self.txtresult.setText(
                        "Info:\nCentor und McIsaac score liegen unter 2.\nEs wird eine Symptomatische Behandlung empfohlen")
                if centor == 3 or mcisaac == 3 or feverpain == 3:
                    self.txtresult.setText(
                        "Info:\nCentor oder McIsaac scroe liegen bei min. 3.\nEs wird ein Delayed prescription empfohlen\nRezept über antibiotische Therapie ausstellen. Dieses ist einzulösen bei signifikanter Verschlechterung ODER wenn nach 3-5 Tagen keine Besserung")
                    createxmlbak(*parameters)
                if centor == 4 or mcisaac >= 4 or feverpain >= 4:
                    self.txtresult.setText(
                        "Info:\nCentor- oder McIsaac-score haben einen Wert von min. 4.\nDie Wahrscheinlichkeit einer bakteriellen Infektion durch z.B. Streptokokken ist sehr hoch.\nEs wird eine antibiotische Therapie empfohlen.\nAlternativ GAS-Schnelltest")
                    createxmlbak(*parameters)

        else:
            self.txtresult.setText("Achtung !!! \nEs ist mindestens eines der 'Red Flags' vorhanden.\nEine Anwendung der scores ist hier nicht möglich. Es wird eine individuelle Beratung zur Diagnostik und Therapie empfohlen.")



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

    # update cmbfever status if temperature changed if defined value is reached it shows fever or not
    def updatecmbfever(self):
        answertemp = self.spinboxtemp.value()
        if answertemp >= tempfever:
            self.cmbfever.setCurrentIndex(1)
        else:
            self.cmbfever.setCurrentIndex(0)

    def updatetime(self):
        answertime = self.spinboxtime.value()
        if answertime >= 14:
            self.grpother.setVisible(True)
        else:
            self.grpother.setVisible(False)


    def loadxml2(self):
        print("HI")
        ts = int
        tree = et.parse('Leitlinie.xml')
        root = tree.getroot()
        print(root[2][20].attrib)

        print(len(root[2].tag))

        flags = root.getchildren()[2]
        flag_list = flags.findall('RedFlags')
        print(len(flag_list))
        for flag in flag_list:
            self.cmbredflag.addItem(flag.get("Bezeichnung"))

        other = root.getchildren()[2]
        other_things = other.findall('andereUrsachen')

        for other in other_things:
            self.cmbother.addItem(other.get("Bezeichnung"))

        danger = root.getchildren()[2]
        dangers = danger.findall('GefaehrlicherVerlauf')

        for danger in dangers:
            self.cmbdanger.addItem(danger.get("Bezeichnung"))


        #print(root[2][3].attrib)
        #print(root[2][3].get("Bezeichnung"))
        #t = len(root.getchildren())
        #print(t)
        #r = tree.xpath('/Halsschmerzen/coding')
        #r = r[0].tag
        #rt = root[1].tag
        #print('r = '+r)
        #print('rt = '+rt)
        #print(root[2][3].tag)
        #print(root[2][1].get("bis"))
        #print("Alter "+root[2][0].get("min"))

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
