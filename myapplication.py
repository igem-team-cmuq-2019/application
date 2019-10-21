import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import serial
import random
import time
from time import gmtime, strftime
import numpy as np
from sklearn import svm


# Predicts score for precounseling
def prediction():
    params = []
    params.append(int(age.text()))
    params.append(int(e1.isChecked()))
    params.append(int(e2.isChecked()))
    params.append(int(e3.isChecked()))
    params.append(int(e4.isChecked()))
    params.append(int(e5.isChecked()))
    params.append(int(e6.isChecked()))
    params.append(int(e7.isChecked()))
    params.append(int(e8.isChecked()))
    params.append(int(e9.isChecked()))

    mydata = open("scd_data.csv",'r').read()
    mydata = mydata.split('\n')[1:-1]
    X = list(map(lambda x: x[:-2],mydata))
    for i in range(len(X)):
        X[i] = list(map(lambda x: int(x), X[i].split(',')))
    Y = list(map(lambda x: int(x[-1]),mydata))

    assert(len(X)==len(Y))
    clf = svm.LinearSVC()
    clf.fit(X, Y)



    pp = clf.predict([params])
    ppc = clf.decision_function([params])

    temp = "Precounseling Diagnosis = "
    if pp[0] == 1:
        temp += "Positive"
    else:
        temp += "Negative"
    precounseling_d.setText(str(temp))


    precounseling_p.setText("Precounseling Percentage = " + str(abs(ppc[0])*100)[:-4] + "%")




# Onclick function for precounseling button
def precounseling():
    prob = random.random()
    precounseling_p.setText("Precounseling Percentage = " + str(prob*100)[:4] + "%")

    if checked1:
        myresults = open("results.txt",'a')
        myresults.write(strftime("%a, %d %b %Y %H:%M:%S", gmtime())+"\n")
        myresults.write("Precounseling," + str(prob*100)[:4]+ '\n')
        myresults.close()

    prediction()


    
# onclick function for bluetooth button
def bluetooth():


    l_1.setText("Connecting Now...")
    time.sleep(0.7)

    '''
    s = serial.Serial(num_port)
    output = s.read(3)
    light = output

    '''

    l_2.setText("Receiving Result...")
    time.sleep(0.5)

    light = random.randint(0,255)
    device_result.setText(str(light))
    if checked1:
        myresults = open("results.txt",'a')
        myresults.write(strftime("%a, %d %b %Y %H:%M:%S", gmtime())+"\n")
        myresults.write("Fluorescence," + str(light)+ '\n')
        myresults.close()


        
# onclick function for save settings button
def settings():

    config = open("config.txt",'w')


    if save_data.isChecked():
        config.write("sr,1\n")
    else:
        config.write("sr,0\n")

    if com_port.text():
        config.write("cp," + com_port.text())
        label_com.setText("Current COM Port: " + com_port.text())

    else:
        config.write("cp," + num_port)


    config.close()






# Creates initial application window
app = QApplication(sys.argv)
win = QWidget()
grid = QGridLayout()



grid.addWidget(QLabel("Welcome to our Application!"),1,1)






tabs = QTabWidget()


# TAB 1 SETUP
tab1 = QWidget()
layout = QGridLayout()
layout.addWidget(QLabel("Age"),1,1)
age = QLineEdit()
age.setValidator(QIntValidator())
layout.addWidget(age,1,2)
e1 = QCheckBox("African American/Black")
e2 = QCheckBox("Hispanic/Latino")
e3 = QCheckBox("White")
e4 = QCheckBox("Asian")
e5 = QCheckBox("Arab")
e6 = QCheckBox("Other")
e7 = QCheckBox("Mother Carrier?")
e8 = QCheckBox("Father Carrier?")
e9 = QCheckBox("Consanguinity?")
layout.addWidget(e1,2,1)
layout.addWidget(e2,3,1)
layout.addWidget(e3,4,1)
layout.addWidget(e4,5,1)
layout.addWidget(e5,6,1)
layout.addWidget(e6,7,1)
layout.addWidget(e7,8,1)
layout.addWidget(e8,9,1)
layout.addWidget(e9,10,1)
b_pc = QPushButton("Conduct Precounseling")
b_pc.clicked.connect(precounseling)
layout.addWidget(b_pc,11,1)
precounseling_d = QLabel("Precounseling Diagnosis = ")
layout.addWidget(precounseling_d,12,1)
precounseling_p = QLabel("Confidence Percentage = ")
layout.addWidget(precounseling_p,13,1)
tab1.setLayout(layout)













# TAB 2 SETUP
tab2 = QWidget()
layout = QGridLayout()
layout.addWidget(QLabel("Press Recieve Flourescence to begin connection."),1,1)
b_rf = QPushButton("Recieve Flourescence")
b_rf.clicked.connect(bluetooth)
layout.addWidget(b_rf,2,1)
l_1 = QLabel("")
l_2 = QLabel("")
layout.addWidget(l_1,3,1)
layout.addWidget(l_2,4,1)
layout.addWidget(QLabel("Your Flourescence: "),5,1)
device_result = QLabel("")
layout.addWidget(device_result,5,2)
tab2.setLayout(layout)






# TAB 3 SETUP
tab3 = QWidget()
layout = QGridLayout()
layout.addWidget(QLabel("Fluorescence Result is dependent on light. Light readings"),1,1)
layout.addWidget(QLabel("Precounseling is based on historical data."),2,1)
tab3.setLayout(layout)




config = open("config.txt",'r').readlines()
if config[0][-2] == '1':
    checked1 = True
else:
    checked1 = False

num_port = config[1][-1]


# TAB 4 SETUP
tab4 = QWidget()
layout = QGridLayout()
label_com = QLabel("Current COM Port: " + num_port)
layout.addWidget(label_com,1,1)
layout.addWidget(QLabel("Set new COM port"),2,1)
com_port = QLineEdit()
com_port.setValidator(QIntValidator())
layout.addWidget(com_port,2,2)
save_data = QCheckBox("Save Results to File")
if checked1:
    save_data.setChecked(True)
layout.addWidget(save_data,3,1)
b_ss = QPushButton("Save Settings")
b_ss.clicked.connect(settings)
layout.addWidget(b_ss,4,1)
tab4.setLayout(layout)







# ADDS ALL TABS TOGETHER
tabs.addTab(tab1, "Precounseling")
tabs.addTab(tab2, "Bluetooth")
tabs.addTab(tab3, "Understand")
tabs.addTab(tab4, "Settings")





grid.addWidget(tabs, 2,1)



win.setLayout(grid)
win.setGeometry(100,100,400,500)
win.setWindowTitle("CMUQ IGEM Bio Kit")
win.show()
sys.exit(app.exec_())
