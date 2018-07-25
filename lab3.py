from scipy.io.wavfile import read,write
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fftfreq, fftshift
from scipy.interpolate import interp1d
from scipy.signal import resample
from scipy import signal


def abrirArchivo():
    rate,info = read("handel.wav")
    print("El rate del archivo es: " + str(rate))
	#print(info)

    dimension = info[0].size
	#print(dimension)  

    if dimension == 1:
    	data = info
    	perfect = 1
    else:
    	data = info[:,dimension-1]
    	perfect = 0
    


    return data,rate
	

def interpolacion(data,rate):
    tiempo = np.linspace(0,len(data)/rate, num=len(data))
    interp = interp1d(tiempo,data)
    tiempo2 = np.linspace(0,len(data)/rate,len(data)*4)
    y = interp(tiempo2)
    return y

def modulacionAM(data,rate,mod_index):
    senal_interp = interpolacion(data,rate)
    largo=len(senal_interp)
    tiempo= np.linspace(0,len(data)/(rate), num=largo)
    frecuencuencia_portadora=400
    portadora = np.cos(2*np.pi*frecuencuencia_portadora*tiempo)*mod_index
    y = senal_interp * portadora
    graficar("Señal modulada","Tiempo","Amplitud",tiempo,y)
    
    return y

def demodulacionAM(signal,time,freq_demod):
    t=time
    portadora = np.cos(2*np.pi*freq_demod*t)
    data = signal * portadora
    return data

def modulacionFM(data,rate,mod_index):
    timp = len(data)/rate
    t=np.linspace(0,timp,len(data))
    frecuencuencia_portadora=400
    portadora=2*np.pi*frecuencuencia_portadora*t*mod_index
    y = np.cos(portadora+data)

def fourier(data,rate):
	timp=len(data)/rate
	Tdata = np.fft.fft(data)
	k = np.arange(-len(Tdata)/2,len(Tdata)/2)
	frq = k/timp
	frq=fftshift(frq)
	return Tdata,frq

def graficar(title,xlabel,ylabel,X,Y):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(X, Y, "-")
    print("Mostrando grafico")
    plt.show()

def lowpass_filter(data,rate):
    numtaps=1001
    nyq_rate=rate/2
    cutoff_hz=nyq_rate*0.09
    fircoef1_low = signal.firwin(numtaps,cutoff_hz/nyq_rate, window = "hamming")
    filtered_x = signal.lfilter(fircoef1_low,1.0,data)
    return filtered_x
'''
data,rate = abrirArchivo()
timp = len(data)/rate
t=np.linspace(0,timp,len(data))

Tdata,frq=fourier(data,rate)
graficar("Transformada de Fourier orig sin resample","Frecuencia [hz]","Amplitud [dB]",frq,Tdata)
new_rate=rate*8


timp = len(data)/rate
time=np.linspace(0,timp,len(data)*8)
'''
rate=2500
time = np.linspace(0,1,num=rate)
data = np.cos(2*np.pi*100*time)
new_rate=rate*4

graficar("Señal original","Tiempo","Amplitud",time,data)

time_resample = np.linspace(0,1,num=new_rate)
senalModulada = modulacionAM(data,rate,1)
senalDemodulada = demodulacionAM(senalModulada,time_resample,400)
senal_demod_filtrada = lowpass_filter(senalDemodulada,new_rate)
data_resample=interpolacion(data,rate)



Tdata,frq=fourier(data_resample,new_rate)
graficar("Transformada de Fourier orig resampleada","Frecuencia [hz]","Amplitud [dB]",frq,Tdata)

Tdata,frq=fourier(senalModulada,new_rate)
graficar("Transformada de Fourier modulada","Frecuencia [hz]","Amplitud [dB]",frq,Tdata)

Tdata,frq=fourier(senalDemodulada,new_rate)
graficar("Transformada de Fourier demodulada","Frecuencia [hz]","Amplitud [dB]",frq,Tdata)

Tdata,frq=fourier(senal_demod_filtrada,new_rate)
graficar("Transformada de Fourier demodulada y filtrada","Frecuencia [hz]","Amplitud [dB]",frq,Tdata)

