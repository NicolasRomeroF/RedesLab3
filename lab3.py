from scipy.io.wavfile import read,write
import numpy as np

def abrirArchivo():
	rate,info = read("beacon.wav")
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
    largo = len(data)
    tiempo = np.linspace(0, data/rate, num = largo)
    frecuencuencia_portadora=88100000
    portadora = np.cos(2*np.pi*frecuencuencia_portadora*tiempo)*mod_index
    y = data * portadora

    def modulacionFM(data,rate,mod_index):
    largo = len(data)
    tiempo = np.linspace(0, data/rate, num = largo)
    frecuencuencia_portadora=88100000
    portadora=2*np.pi*frecuencuencia_portadora*tiempo*mod_index
    y = np.cos(portadora+data)

