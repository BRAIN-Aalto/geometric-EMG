# Python program to create a countdown timer using PyQt5  
# import all the required modules  
from PyQt5.QtWidgets import *  
from PyQt5 import QtCore, QtGui  
from PyQt5.QtGui import *  
from PyQt5.QtCore import *  
import sys  
    
    
class Window(QMainWindow):  
    
    def __init__(self):  
        super().__init__()  
    
        # set the window title  
        self.setWindowTitle("Python ")  
    
        # set the window geometry  
        self.setGeometry(100, 100, 400, 600)  
    
        # call the components method  
        self.UiComponents()  
    
        # displaying all the present widgets  
        self.show()  
    
    # function for the widgets  
    def UiComponents(self):  
    
        # introducing the variables  
        # create a count variable  
        self.count = 0  
    
        # starting value of flag  
        self.start = False  
    
        # create a push button for getting the time in seconds  
        btn = QPushButton("Set time(s)", self)  
    
        # set the geometry of the push button  
        btn.setGeometry(125, 100, 150, 50)  
    
        # add action to the push button for being clicked  
        btn.clicked.connect(self.get_scnds)  
    
        # create a new label to display the seconds  
        self.label = QLabel("//TIMER//", self)  
    
        # set the geometry for the label  
        self.label.setGeometry(100, 200, 200, 50)  
    
        # set the label's borders  
        self.label.setStyleSheet("border : 3px solid black")  
    
        # set the font for the label  
        self.label.setFont(QFont('Times', 15))  
    
        # set the alignment for the label  
        self.label.setAlignment(Qt.AlignCenter)  
    
        # create a new start button  
        start_btn = QPushButton("Start", self)  
    
        # set the geometry for the start button  
        start_btn.setGeometry(125, 350, 150, 40)  
    
        # add action to the start button  
        start_btn.clicked.connect(self.start_actn)  
    
        # create a new pause button  
        pause_btn = QPushButton("Pause", self)  
    
        # set the geometry for the pause button  
        pause_btn.setGeometry(125, 400, 150, 40)  
    
        # add action to the button  
        pause_btn.clicked.connect(self.pause_actn)  
    
        # create a new reset button  
        reset_btn = QPushButton("Reset", self)  
    
        # set the geometry for the reset button  
        reset_btn.setGeometry(125, 450, 150, 40)  
    
        # add action to the reset button  
        reset_btn.clicked.connect(self.reset_actn)  
    
        # create a new timer clock object  
        timerClock = QTimer(self)  
    
        # add action to the timer clock  
        timerClock.timeout.connect(self.displayTime)  
    
        # updating the timer clock after every tenth of a second  
        timerClock.start(100)  
    
    # function to be called by the timer clock  
    def displayTime(self):  
    
        # check if the flag value is true  
        if self.start:  
            # increasing the counter  
            self.count -= 1  
    
            # timer clock is completed  
            if self.count == 0:  
    
                # converting the flag value to false  
                self.start = False  
    
                # set the text for the label  
                self.label.setText("Completed !!!! ")  
    
        if self.start:  
            # get the text from the count  
            txt = str(self.count / 10) + " s"  
    
            # displaying the text  
            self.label.setText(txt)  
    
    
    # func to be called by the push button  
    def get_scnds(self):  
    
        # converting the flag value to false  
        self.start = False  
    
        # get the seconds and the flag value  
        second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:')  
    
        # if the flag value is true  
        if done:  
            # improvising the value of the count variable  
            self.count = second * 10  
    
            # set the text for the label  
            self.label.setText(str(second))  
    
    def start_actn(self):  
        # changing the flag value to true  
        self.start = True  
    
        # count = 0  
        if self.count == 0:  
            self.start = False  
    
    def pause_actn(self):  
    
        # changing the flag value to false  
        self.start = False  
    
    def reset_actn(self):  
    
        # change the flag value to false  
        self.start = False  
    
        # set the count value to 0  
        self.count = 0  
    
        # set the label's text  
        self.label.setText("//TIMER//")  
    
    
    
# creating the pyqt5 application  
Base = QApplication(sys.argv)  
    
# creating an instance of the of Window created  
window = Window()  
    
# starting the application  
sys.exit(Base.exec())  