from PyQt5 import QtCore, QtGui, QtWidgets
from gforce import GForceProfile, NotifDataType, DataNotifFlags
import time

from  pagewindow import PageWindow

from window import *

if __name__ == "__main__":
    import sys
    

    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())