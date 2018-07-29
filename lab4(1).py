# Import the plotting library
import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import read,write
from scipy import fft, arange, ifft
import scipy.integrate as integrate
from scipy.signal import lfilter, firwin

rate,info=read("handel.wav")
dimension = info[0].size
if dimension==1:
    data = info
else:
    data = info[:,dimension-1]

large = len(data)

T = large/rate 

t1 = np.linspace(0,T,large)    			#linspace(start,stop,number)

t2 = np.linspace(0,T,200000*T)

data1 = np.interp(t2, t1, data)

# Create the signals
carrier = np.cos(t2*np.pi);

am = carrier * data1 

plt.plot(t2[1000:2000], am[1000:2000])
plt.show()



#Modulacion FM,  4 veces mas 

t2_fm = np.linspace(0,T, 400000*T)

data_fm = np.interp(t2_fm, t1, data)

t3_fm = np.linspace(0, 400000, 400000*T)

A = 1
k = 0.15

# Create the signals
carrier_fm = np.sin(2*np.pi*t3_fm);

wct = rate * t2_fm

audio_integrate = integrate.cumtrapz(data_fm, t2_fm, initial=0)

fm = np.cos(np.pi*wct + audio_integrate*np.pi);

plt.plot(t2_fm[1000:4000], fm[1000:4000])
plt.show()
