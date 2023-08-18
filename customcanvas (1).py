import numpy as np
import queue
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.pyplot import subplots
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from  concurrent.futures import ThreadPoolExecutor


class CustomFigCanvas(FigureCanvas, TimedAnimation):
    def __init__(self):
        
        # The data
        self.scale = 5
        self.xlim = 200
        self.amplitude = 0.5
        self.addedData = queue.Queue()
        self.addedLabel = queue.Queue()

        self.n = np.linspace(0, 299, 500)
        self.cue_line = np.zeros(500)#, np.linspace(0, self.amplitude, 100), np.ones(200) * self.amplitude,np.linspace( self.amplitude, 0,100),np.zeros(150) ])
        self.extra = np.arange(0,self.scale*9,self.scale)
        print(self.cue_line.shape)
        self.y = np.zeros([500,9]) - self.extra
        #self.labels = (self.n * 0.0) + 50
        
        # The window
        self.fig, self.axes  = subplots(2,1, figsize=(10, 8), gridspec_kw={'height_ratios': [4, 1]})

        for i in range(1):

            setattr(self, f'line{i}',Line2D([], [], color='blue')) 
            self.axes[1].add_line(getattr(self,f'line{i}')) 
        for i in range(1,9):

            setattr(self, f'line{i}',Line2D([], [], color='blue')) 
            self.axes[0].add_line(getattr(self,f'line{i}')) 
        
        self.line9 = Line2D([], [], color='red', alpha=0.3)
        self.axes[1].add_line(self.line9) 
        self.labels = [f'Channel {chan}' for chan in range (1,9)]
        self.axes[0].set_xlim(0, 500)
        
        self.axes[0].set_ylim(-self.scale*9, -0)
        self.axes[0].set_yticks(-self.extra[1:])
        self.axes[0].set_yticklabels(self.labels)

        self.axes[1].set_xlim(0, 500)
        self.axes[1].set_ylim(0,1.5)
        self.axes[1].set_yticks([])
        self.axes[1].set_yticks([], minor=True)
        
        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50,repeat=True, blit = True)
        

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        #lines = [self.line1, self.line2, self.line3, self.line4]#, self.line1_tail]#, self.line1_head]
        for l in range(10):
            getattr(self,f'line{l}').set_data([], [])
        #[self.axes.plot(self.extra[i-1])[0] for i in range(1,9)]

    def addData(self, value):
        self.addedData.put(value)
        #self.addedLabel.put(value[1])
        
    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            print(str(self.abc))
            TimedAnimation._stop(self)
            pass
    def update_amp(self, new_val):
        self.amplitude = new_val
        print(self.amplitude)
        self.cue_line = np.hstack([np.zeros(700), np.linspace(0, new_val, 100), np.ones(200) * new_val,np.linspace( new_val, 0,100)  ])
        

    def set_line(self, idx):
        getattr(self, f"line{idx}").set_data( self.n, range(2000))
    def _draw_frame(self, framedata):
        try:
            new_data = self.addedData.get_nowait()
            self.y = np.roll(self.y,-1,0)
            self.cue_line = np.roll(self.cue_line,-1)
            self.y[-1,:] = new_data# np.random.randint(100,150,8) #self.addedData.get_nowait()
            self.y[-1,:] -= self.extra
            #self.n = np.roll(self.n, -1)
            #self.n[-1] = self.n[-2] + 1
            
        #self.labels = np.roll(self.labels, -1)
        except Exception as e:
            print("Error:", type(e),e)
        
       
                #p.map(self.set_line, range(1,9))
        try:
            for i in range (9): 
            #return [self.axes.plot(self.y[i-1,:])[0] for i in range(1,9)]#
                getattr(self, f"line{i}").set_data(range(500),self.y[:,i])
            self.line9.set_data(range(500), self.cue_line[:500])
            self.axes[1].set_ylim(-0.01, self.amplitude * 2)
            self.axes[1].set_yticks([], minor=True)
            self._drawn_artists = [getattr(self, f"line{i}") for i in range(10)]#, self.line2, self.line3, self.line4, self.line5, self.line6, self.line7, self.line8]#, self.line1_tail]#, self.line1_head]
        except Exception as e:
            print("Error after get data",e)