from communicate import Communicate
import numpy as np
import time

packet_cnt = 0
start_time = 0

def ondata(data):

    global STARTED, channels, file1

        # Data for EMG CH0~CHn repeatly.
        # Resolution set in setEmgRawDataConfig:
        #   8: one byte for one channel
        #   12: two bytes in LSB for one channel.
        # eg. 8bpp mode, data[1] = channel[0], data[2] = channel[1], ... data[8] = channel[7]
        #                data[9] = channel[0] and so on
        # eg. 12bpp mode, {data[2], data[1]} = channel[0], {data[4], data[3]} = channel[1] and so on

        # # end for
        
    extracted_data = data[1:]
    channels += extracted_data

    if STARTED:
        file1.write(' '.join(map(str, extracted_data)) +"\n")

def set_cmd_cb(resp):
    print('Command result: {}'.format(resp))

rms_formuula = lambda x: np.sqrt(np.mean(x ** 2, axis=1))
def dataSendLoop(addData_callbackFunc):
    # Setup the signal-slot mechanism.
    mySrc = Communicate()
    mySrc.data_signal.connect(addData_callbackFunc)
    #time.sleep(3)
    i = 0*500*8
    global PEAK, PEAK_MULTIPLIER, BASELINE, OFFSET, OFFSET_RMS, BASELINE_MULTIPLIER,ACTIONS, reg
    while(True):
        #channels[i:i+50*8]
        for j in range (8):
            try:
                datawindow = channels[i:i+50*8]
                if datawindow:
                    datastack = np.stack([np.array(datawindow[k::8]) for k in range (8)]).astype('float32') - OFFSET
                    mean_in_window = datastack.mean(1) # should have size (8,)
                    rms_ = rms_formuula(datastack/255)
                    rms = rms_.sum()- OFFSET_RMS
                    if reg:
                        pred_class = reg.predict(rms_.reshape(1,8))
                        print(ACTIONS[pred_class[0]+1][0])
                        mySrc.data_signal.emit([pred_class[0]/5+0.01] + list(mean_in_window))
                    elif OFFSET_RMS:
                        mySrc.data_signal.emit([rms] + list(mean_in_window))
                    else:
                        BASELINE = min(rms*BASELINE_MULTIPLIER, BASELINE)
                        PEAK = max(rms*PEAK_MULTIPLIER, PEAK)
                        mySrc.data_signal.emit([rms] + list(mean_in_window))
                    i += 25*8
                    #print(len(channels)-i)
                time.sleep(47/1000)

            except Exception as e:
                print("Error during plotting:", type(e),e) 
