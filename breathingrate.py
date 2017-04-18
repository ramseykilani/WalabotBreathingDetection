import numpy as np
import pylab as plt
import matplotlib as mpl
from peakdetect import peakdetect
import time

def breathingrate(Data):

    timestep=0.083 # 0.083s for Walabot
    n=np.size(Data)
    Time=np.arange(0,n*timestep,timestep)

    peaks = peakdetect(Data,Time,lookahead=10) # average breathing rarly goes above 1breath/2second, set lookahead as half of that for 1 peak/second
    maxpeaks = np.array(peaks)[0]
    minpeaks =np.array(peaks)[1] 

    maxX = [0 for k in range(np.size(maxpeaks))]
    maxY=[0 for k in range(np.size(maxpeaks))]
    for i in range(0,np.size(maxpeaks,0)):
        peakP=maxpeaks[i]
        maxX[i]=peakP[0]
        maxY[i]=peakP[1]

    minX = [0 for k in range(np.size(minpeaks))]
    minY=[0 for k in range(np.size(minpeaks))]
    for i in range(0,np.size(minpeaks,0)):
        peakP=minpeaks[i]
        minX[i]=peakP[0]
        minY[i]=peakP[1]


    bpm=((np.size(maxX)+np.size(minX))/2) / ((Time[-1]-Time[0])/60) # turn peaks into breaths/minute


    print(bpm)
    #plt.gcf().clear()
    #plt.plot(Time,Data,maxX,maxY,'bo',minX,minY,'ro')
    #plt.show()

    return bpm, maxX, maxY, minX, minY
