from scipy.io.wavfile import read,write
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fftfreq, fftshift
from scipy.interpolate import interp1d
from scipy.signal import resample
from scipy import signal
from scipy import integrate
import matplotlib.animation as animation


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
    tiempo2 = np.linspace(0,len(data)/rate,len(data)*8)
    y = interp(tiempo2)
    #print (tiempo[-1])
    #print(len(data)/rate)
    return y

def modulacionAM(data,rate,mod_index):
    senal_interp = interpolacion(data,rate)
    largo=len(senal_interp)
    tiempo= np.linspace(0,len(data)/(rate), num=largo)
    frecuencuencia_portadora=20000
    portadora = np.cos(2*np.pi*frecuencuencia_portadora*tiempo)*mod_index
    y = senal_interp * portadora
    #graficar("Señal modulada","Tiempo","Amplitud",tiempo,y)
    
    return y

def demodulacionAM(signal,time,freq_demod):
    t=time
    portadora = np.cos(2*np.pi*freq_demod*t)
    data = signal * portadora
    return data

def modulacionFM(data,rate,mod_index):
    k=mod_index
    senal_interp = interpolacion(data,rate)
    largo = len(senal_interp)
    tiempo = np.linspace(0,len(data)/(rate), num=largo)
    
    frecuencia_portadora=20000
    
    #wct = 2*np.pi*frecuencia_portadora*tiempo
    wct = 2*np.pi*frecuencia_portadora*tiempo

    audio_integrate = integrate.cumtrapz(senal_interp, tiempo, initial=0)
    
    portadora = np.cos(wct+k*audio_integrate)
    
    return portadora

def fourier(data,rate):
	timp=len(data)/rate
	Tdata = np.fft.fft(data)
	k = np.arange(-len(Tdata)/2,len(Tdata)/2)
	frq = k/timp
	frq=fftshift(frq)
	return Tdata,frq

def graficar(title,xlabel,ylabel,X,Y):
    print("Mostrando grafico")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(X, Y, "-")
    plt.show()

def lowpass_filter(data,rate):
    numtaps=1001
    nyq_rate=rate/2
    cutoff_hz=nyq_rate*0.09
    fircoef1_low = signal.firwin(numtaps,cutoff_hz/nyq_rate, window = "hamming")
    filtered_x = signal.lfilter(fircoef1_low,1.0,data)
    return filtered_x

def init():
    line.set_data([], [])
    return line,

def init2():
    line2.set_data([], [])
    return line2,

def init3():
    line2.set_data([], [])
    return line3,

# animation function.  This is called sequentially
def animateSenal(i):
    x = np.linspace(0, 1, 1000)
    y = np.cos(2 * np.pi * (x - 0.01* i)*5)
    line.set_data(x, y)
    return line,

def animatePortadora(i):
    x = np.linspace(0, 1, 1000)
    y = np.cos(2 * np.pi * (x - 0.01* i)*20)
    line2.set_data(x, y)
    return line2,

def animateModulada(i):
    x = np.linspace(0, 1, 1000)
    y = np.cos(2 * np.pi * (x - 0.01* i)*5)*np.cos(2 * np.pi * (x - 0.01* i)*20)
    line3.set_data(x, y)
    return line3,

data,rate = abrirArchivo()
timp = len(data)/rate
t=np.linspace(0,timp,len(data))

mod_index=1

#Tdata,frq=fourier(data,rate)
#graficar("Transformada de Fourier orig sin resample","Frecuencia [hz]","Amplitud [dB]",frq,Tdata)
new_rate=rate*8


timp = len(data)/rate
time=np.linspace(0,timp,len(data)*8)
'''
rate=2500
time = np.linspace(0,1,num=rate)
data = np.cos(2*np.pi*100*time)
new_rate=rate*
'''

#graficar("Señal original","Tiempo","Amplitud",time,data)

time_resample = np.linspace(0,len(data)/rate,num=len(data)*8)
senalModulada = modulacionAM(data,rate,mod_index)
senalDemodulada = demodulacionAM(senalModulada,time_resample,20000)
senal_demod_filtrada = lowpass_filter(senalDemodulada,new_rate)
data_resample=interpolacion(data,rate)

frecuencuencia_portadora=20000
senalPortadora=portadora = np.cos(2*np.pi*frecuencuencia_portadora*time_resample)*mod_index

#Tdata,frq=fourier(data_resample,new_rate)
#graficar("Transformada de Fourier orig resampleada","Frecuencia [hz]","Amplitud [dB]",frq,Tdata)

#Tdata,frq=fourier(senal_demod_filtrada,new_rate)
#graficar("Transformada de Fourier demodulada y filtrada","Frecuencia [hz]","Amplitud [dB]",frq,Tdata)
senalModuladaFM = modulacionFM(data,rate, mod_index)
senalModuladaFM15 = modulacionFM(data,rate, 0.15)
senalModuladaFM125 = modulacionFM(data,rate, 1.25)


opcion=1
while opcion != 0:
    print("""Menú:
    1.- Mostrar señal original y señal portadora
    2.- Mostrar transformada de Fourier de la modulación AM
    3.- Mostrar transformada de Fourier demodulación AM
    4.- Mostrar transformada de Fourier de la modulación FM
    5.- Ejemplo animado
    6.- Salir""")
    try:
        opcion = int(input("Ingrese una opción: "))
    except:
        opcion = 6
    if opcion == 1:
        print("Mostrando grafico")
        ax1 = plt.subplot(3, 1, 1)
        plt.title('Señal original')
        plt.ylabel('Amplitud')
        plt.xlabel('Tiempo [s]')
        plt.plot(time_resample,senalModulada, '-')


        ax2 = plt.subplot(3, 1, 2)
        ax2.set_title('Señal portadora')
        plt.axis([1,1.01,-1.2,1.2])
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud')
        plt.plot(time_resample,senalPortadora, '-')

        ax3 = plt.subplot(3, 1, 3)
        ax3.set_title('Señal modulada AM')
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud')
        plt.plot(time_resample,senalModulada, '-')

        plt.tight_layout()

        plt.show()
    elif opcion==2:
        print("--------------")
        print("Mostrando grafico")

        Tdata,frq=fourier(data_resample,new_rate)

        ax = plt.subplot(4, 1, 1)
        plt.title('Fourier señal original')
        plt.xlabel('Frecuancia [hz]')
        plt.ylabel('Amplitud')
        plt.plot(frq,Tdata, '-')

        Tdata15,frq15=fourier(senalModulada*0.15,new_rate)

        ax1 = plt.subplot(4, 1, 2)
        plt.title('Fourier AM al 15%')
        plt.xlabel('Frecuencia [hz]')
        plt.ylabel('Amplitud')
        plt.plot(frq15,Tdata15, '-')

        Tdata100,frq100=fourier(senalModulada,new_rate)

        ax2 = plt.subplot(4, 1, 3)
        ax2.set_title('Fourier AM al 100%')
        plt.xlabel('Frecuencia [hz]')
        plt.ylabel('Amplitud')
        plt.plot(frq100,Tdata100, '-')

        Tdata125,frq125=fourier(senalModulada*1.25,new_rate)

        ax3 = plt.subplot(4, 1, 4)
        ax3.set_title('Fourier AM al 125%')
        plt.xlabel('Frecuencia [hz]')
        plt.ylabel('Amplitud')
        plt.plot(frq125,Tdata125, '-')

        plt.tight_layout()

        plt.show()
        print("--------------")
    elif opcion==3:
        print("--------------")
        print("Mostrando grafico")
        Tdata,frq=fourier(senalDemodulada,new_rate)
        TdataFiltrada,frqFiltrada=fourier(senal_demod_filtrada,new_rate)

        
        ax1 = plt.subplot(2, 1, 1)
        plt.title('Fourier señal demodulada')
        plt.ylabel('Amplitud')
        plt.xlabel('Frecuencia [hz]')
        plt.plot(frq,Tdata, '-')


        ax2 = plt.subplot(2, 1, 2)
        plt.title('Fourier señal demodulada y filtrada')
        plt.ylabel('Amplitud')
        plt.xlabel('Frecuencia [hz]')
        plt.plot(frqFiltrada,TdataFiltrada, '-')

        plt.tight_layout()

        plt.show()

        print("--------------")
    elif opcion==4:
        print("--------------")
        print("Mostrando grafico") 
        Tdata,frq=fourier(data_resample,new_rate)

        ax = plt.subplot(4, 1, 1)
        plt.title('Fourier señal original')
        plt.xlabel('Frecuancia [hz]')
        plt.ylabel('Amplitud')
        plt.plot(frq,Tdata, '-')

        Tdata15,frq15 = fourier(senalModuladaFM15, new_rate)

        ax1 = plt.subplot(4, 1, 2)
        plt.title('Fourier FM al 15%')
        plt.xlabel('Frecuencia [hz]')
        plt.ylabel('Amplitud')
        plt.plot(frq15,Tdata15, '-')

        Tdata100,frq100 = fourier(senalModuladaFM, new_rate)

        ax2 = plt.subplot(4, 1, 3)
        ax2.set_title('Fourier FM al 100%')
        plt.xlabel('Frecuencia [hz]')
        plt.ylabel('Amplitud')
        plt.plot(frq100,Tdata100, '-')

        Tdata125,frq125=fourier(senalModuladaFM125,new_rate)

        ax3 = plt.subplot(4, 1, 4)
        ax3.set_title('Fourier FM al 125%')
        plt.xlabel('Frecuencia [hz]')
        plt.ylabel('Amplitud')
        plt.plot(frq125,Tdata125, '-')

        plt.tight_layout()

        plt.show()
        print("--------------") 
    elif opcion == 5:
        print("Mostrando grafico")
        fig = plt.figure()
        ax = plt.axes(xlim=(0, 1), ylim=(-1, 1))
        line, = ax.plot([], [], lw=2)
        plt.title('Señal original (coseno frecuencia 5)')
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud')

        anim = animation.FuncAnimation(fig, animateSenal, init_func=init,frames=360, interval=20, blit=True)
        plt.show()


        fig2 = plt.figure()
        ax2 = plt.axes(xlim=(0, 1), ylim=(-1, 1))
        line2, = ax2.plot([], [], lw=2)
        plt.title('Señal portadora (coseno frecuencia 20)')
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud')
        
        anim = animation.FuncAnimation(fig2, animatePortadora, init_func=init2,frames=360, interval=20, blit=True)
        plt.show()

        
        fig3 = plt.figure()
        ax3 = plt.axes(xlim=(0, 1), ylim=(-1, 1))
        line3, = ax3.plot([], [], lw=2)
        plt.title('Señal modulada')
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud')

        anim = animation.FuncAnimation(fig3, animateModulada, init_func=init3,frames=360, interval=20, blit=True)
        plt.show()
   
        
    elif opcion > 6 or opcion < 1:
        print("Opcion no valida, intente otra vez")
    elif opcion == 6:
        opcion = 0
        print("Salir")