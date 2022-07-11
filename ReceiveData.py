from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    # Setup notch filter
    b_notch, a_notch = signal.iirnotch(60.0, 20, 250)
    # Setup bandpass filter
    nyq = (1/3) * 250
    low = 1/nyq
    high = 50/nyq
    b_butter, a_butter = signal.butter(2, [low, high], 'bandpass', analog=False)
    firstsample, firsttimestamp = inlet.pull_sample()

    # Overwrite session file with temporary data
    tmpsessiontext = str(firsttimestamp)+", "+str(firstsample[0])+", "+str(firstsample[1])+", "+str(firstsample[2])+", "+str(firstsample[3])+", "+str(firstsample[4])+", "+str(firstsample[5])+", "+str(firstsample[6])+", "+str(firstsample[7])+", 0\n"
    tmpsessiontext = tmpsessiontext*15
    session = open("sessionfile.txt", "w")
    session.write(tmpsessiontext)
    session.close()
    
    while True:
        sample, timestamp = inlet.pull_sample()
        # Uncomment for an int timestamp starting at 0
        #timestamp = round(timestamp)-round(firsttimestamp)
        print([timestamp]+sample+[0])

        # Transpose and limit to 300 samples
        orginalsessiondata = np.loadtxt(open("sessionfile.txt", "rb"), delimiter=", ")
        if np.shape(orginalsessiondata)[0] >= 300:
            orginalsessiondata = orginalsessiondata[1:]
        sessiondata = orginalsessiondata.transpose()
        sessiondata = sessiondata[:-1]
        sessiondata = sessiondata.transpose()
        sessiondata = np.append(sessiondata, [np.append(np.array([timestamp]), np.array(sample))], axis=0)
        tsessiondata = sessiondata.transpose()

        # Filter channel 1
        y = signal.filtfilt(b_notch, a_notch, tsessiondata[1], axis=0)
        y = signal.filtfilt(b_butter, a_butter, y, axis=0)
        #y = signal.sosfilt(sos, y)
        tsessiondata = np.append(tsessiondata, np.array([y]), axis=0)
        
        # Transpose again and write to file
        sessiondata = tsessiondata.transpose()
        sessionfiletext = ""
        
        # Save entire filtered chunk
        for sd in sessiondata:
            for d in sd:
                sessionfiletext += str(d)+", "
            sessionfiletext = sessionfiletext[:-2]+"\n"
        sessionfiletext = sessionfiletext[:-2]
        
        session = open("sessionfile.txt", "w")
        session.write(sessionfiletext)
        session.close()


if __name__ == '__main__':
    main()
