import WalabotAPI as wlbt
import numpy as np
import pylab as plt
import time
import matplotlib as mpl
from matplotlib import animation
from datetime import datetime
from scipy.interpolate import spline

plt.ion()
wlbt.Init()  # load the WalabotSDK to the Python wrapper
wlbt.SetSettingsFolder()  # set the path to the essetial database files
wlbt.ConnectAny()  # establishes communication with the Walabot

wlbt.SetProfile(wlbt.PROF_SENSOR_NARROW)  # set scan profile out of the possibilities

R_MIN, R_MAX, R_RES = 80, 105, 0.2  # SetArenaR values
THETA_MIN, THETA_MAX, THETA_RES = -1, 1, 1  # SetArenaTheta values
PHI_MIN, PHI_MAX, PHI_RES = -1, 1, 1  # SetArenaPhi values

wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_NONE)  # use no filter, which will find distance from walabot

wlbt.Start()  # starts Walabot in preparation for scanning

num = 110 # number of points to plot
# each point is about 0.0932 secconds in v2+
# each point is about 0.0929 secconds in v4+

y_max = 0.01 # below 0.0005 is background for derivative mode
y_min = -0.01  # 0.01 for NONE filter mode works for about 50cm

fig = plt.figure() # initialize plot
ax = plt.axes(xlim=(0,10), ylim=(y_min,y_max))
#ax = plt.axes()
#ax.ticklabel_format(useOffset=False)
#ax.autoscale(enable=True,axis='y')
#plt.autoscale(True)
ax.margins(0.001)
line, = ax.plot([],[],lw=2)


y=np.zeros(num) # initalize y values
y_smooth = np.zeros(num) # initalize smoothed y values
x = np.linspace(0,10,num) # set up x values for plot
x_sm = np.array(x)
y_sm = np.zeros(num)
x_smooth = np.linspace(x_sm.min(), x_sm.max(), 330)

today = str(datetime.today())
f = open(today[5:7]+'.'+today[8:10]+'_01.csv','w') # open file to write data to

# initialize plot at each frame
def init():
    line.set_data([],[])
    return line,

def animate(i):
    wlbt.Trigger() # trigger walabot
    ener = wlbt.GetImageEnergy() # use image energy of walabot to detect breathing

    # array of actual energy values
    # stores the array of energy values to be used in averaging 
    global y
    y = np.asarray(y)
    y = np.roll(y,-1)
    y = y.tolist() # shift the y values down by one
    y[num-1] = -ener
    
    # array of averaged values
    global y_sm
    y_sm = np.asarray(y_sm)
    y_sm = np.roll(y_sm,-1)
    y_sm = y_sm.tolist() # shift the averaged y values down by one row
    en_smth = np.sum(np.insert(y[num-5:num],0,0)) / 5 # averages the current y value with the previous 5 values
    y_sm[num-1] = en_smth

    # better smoothing
    global x_smooth
    y_smooth = spline(x, y_sm, x_smooth)

    # autoscaling
    if i%10 == 1:
        y_max=max(y_smooth)
        y_min=min(y_smooth)
        global ax
        ax.set_ylim(y_min,y_max)
        print (y_smooth)
        #print ("Min ",y_min)p
    # write to data
    line.set_data(x_smooth,y_smooth) # write new y value averages to plot
    f.write(str(datetime.now())+ ',' + str(ener)+'\n') # write every value to a new line, with a timestamp

    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init,interval=1,blit=True)
plt.show()


