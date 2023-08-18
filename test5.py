import time
import numpy as np
from scalene import scalene_profiler
from pyqtgraph import PlotWidget, mkPen,PlotCurveItem
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5 import  QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import sys 
import threading
from  concurrent.futures import ThreadPoolExecutor
#scalene_profiler.start()
listt = [0]*100000000
idx = 0
x = np.zeros((2000,8),dtype=float)

app = QtWidgets.QApplication(sys.argv)

win = QtWidgets.QMainWindow()
graphWidget1 = PlotWidget(background='w')
pen = mkPen(color = (255,0,0))
data_lines = [PlotCurveItem(x[:,1], pen=pen)]*8
def dataSendLoop(addData_callbackFunc):
    # Setup the signal-slot mechanism.
    mySrc = Communicate()
    mySrc.data_signal.connect(addData_callbackFunc)
    #time.sleep(1)
    i = 0*500*8
    while(i < 1000000):
        #channels[i:i+50*8]
        # datawindow = channels[i:i+50*8]
        # datastack = np.stack([np.array(datawindow[i::8]) for i in range (8)]).astype('float32')
        # print(datastack.shape)
        # #(datastack**2).mean(1)**0.5
        # rms = list((datastack**2).mean(1)**0.5)
        # for upsample in range (20):
        #     mySrc.data_signal.emit([rms, ACTION*10+100]) 
        #     time.sleep(1/500)
        # i += 25*8
        # print(i)
        #print("Channel has more data than i", len(actions)-i)
        #mySrc.data_signal.emit(channels[i]) 
        mySrc.data_signal.emit([listt[i:i+8],listt[i:i+8][0]]) 
        time.sleep(1/500)
        i += 1
        #print(i)
        #1s -- 500 samples => 500*8 elements
        #1window length 100ms --> 50 samples => 50*8 element
        #1 overlapping window 50ms --> 25 samples => 25*8 element

def addData_callbackFunc(value):
    return 
myDataLoop = threading.Thread(name = 'myDataLoop', target = dataSendLoop, daemon = True, args = (addData_callbackFunc,))
#print(type(data_line1))
class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(int)

start_time = time.time()
myDataLoop.start()
#scalene_profiler.stop()
print((time.time()-start_time)*1000/1000000)
