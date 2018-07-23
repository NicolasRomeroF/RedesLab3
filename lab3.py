from scipy.io.wavfile import read,write
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fftfreq, fftshift


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

def modulacionAM(data,rate,mod_index):
    timp = len(data)/rate
    t=np.linspace(0,timp,len(data))
    frecuencuencia_portadora=88100000
    portadora = np.cos(2*np.pi*frecuencuencia_portadora*t)*mod_index
    y = data * portadora
    return y

def demodulacionAM(signal,rate,freq_demod):
    timp = len(signal)/rate
    t=np.linspace(0,timp,len(signal))
    portadora = np.cos(2*np.pi*freq_demod*t)
    data = signal * portadora
    return data

def modulacionFM(data,rate,mod_index):
    timp = len(data)/rate
    t=np.linspace(0,timp,len(data))
    frecuencuencia_portadora=3000
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
    plt.plot(X, Y)
    print("Mostrando grafico")
    plt.show()

data,rate = abrirArchivo()
timp = len(data)/rate
t=np.linspace(0,timp,len(data))


senalModulada = modulacionAM(data,rate,0.15)
senalDemodulada = demodulacionAM(senalModulada,rate,3000)


graficar("Señal original","Tiempo","Amplitud",t,data)

Tdata,frq=fourier(senalModulada,rate)
graficar("Transformada de Fourier modulada","Frecuencia [hz]","Amplitud [dB]",frq,Tdata)

Tdata,frq=fourier(data,rate)
graficar("Transformada de Fourier orig","Frecuencia [hz]","Amplitud [dB]",frq,Tdata)

Tdata,frq=fourier(senalDemodulada,rate)
graficar("Transformada de Fourier demodulada","Frecuencia [hz]","Amplitud [dB]",frq,Tdata)

graficar("Señal modulada","Tiempo","Amplitud",t,senalModulada)

graficar("Señal demodulada","Tiempo","Amplitud",t,senalModulada)
