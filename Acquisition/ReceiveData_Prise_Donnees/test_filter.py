from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import math



samplingFreq = 20000; # sampled at 1 kHz = 1000 samples / second
tlims = [0,0.05]        # in seconds
signalFreq = [50,250,800,1150,1500,200,300,400]; # Cycles / second

signalMag = [1,0.2]; # magnitude of each sine
t = np.linspace(tlims[0],tlims[1],int((tlims[1]-tlims[0])*samplingFreq))
y = signalMag[0]*np.sin(2*math.pi*signalFreq[0]*t) + signalMag[1]*np.sin(2*math.pi*signalFreq[1]*t)+ signalMag[1]*np.sin(2*math.pi*signalFreq[2]*t) + signalMag[1]*np.sin(2*math.pi*signalFreq[3]*t)+ signalMag[1]*np.sin(2*math.pi*signalFreq[4]*t)+ signalMag[1]*np.sin(2*math.pi*signalFreq[5]*t)+ signalMag[1]*np.sin(2*math.pi*signalFreq[6]*t)+ signalMag[1]*np.sin(2*math.pi*signalFreq[7]*t)
#y= signalMag[1]*np.sin(2*math.pi*signalFreq[4]*t)+signalMag[1]*np.sin(2*math.pi*signalFreq[1]*t)
# noise = np.random.normal(0,1,len(y))

# for i in range(len(y)):
#     y[i]+=noise[i]




# Compute the Fourier transform
yhat = np.fft.fft(y)
fcycles = np.fft.fftfreq(len(t),d=1.0/samplingFreq); # the frequencies in cycles/s

# Plot the signal
plt.figure()
plt.plot(t,y)
plt.ylabel("$y(t)$")
plt.xlabel("$t$ (s)")
plt.xlim([min(t),max(t)])

# Plot the power spectrum
plt.figure()
plt.plot(fcycles,np.absolute(yhat))
plt.xlim([-2000,2000])
plt.xlabel("$\omega$ (cycles/s)")
plt.ylabel("$|\hat{y}|$")
plt.show()



#on va tester notre filtre ici 


filter_output=[0,0,0]
filter_input=[0,0]
filtered_signal=np.zeros(len(y))
values_to_filter=np.zeros(len(y))

def filter(input,output):
    #output[0]=1.56450399*output[1] -0.64366232*output[2]+0.01978958*input[0]+0.03957917*input[1]

    output[0]= 1.80097432*output[1]  - 0.81906179*output[2]+ 0.00904373*input[0]+ 0.00452187*input[1]

   
  
   
   
    output[2]=output[1]
    output[1]=output[0]
    input[1]=input[0]

for j in range (len(y)):
    filter_input[0]=y[j]
    filter(filter_input,filter_output)


    filtered_signal[j]=filter_output[0]


print(values_to_filter, filtered_signal)


# Compute the Fourier transform
yhat = np.fft.fft(filtered_signal)
fcycles = np.fft.fftfreq(len(t),d=1.0/samplingFreq); # the frequencies in cycles/s

# Plot the signal
plt.figure()
plt.plot(t,filtered_signal)
plt.ylabel("$y(t)$")
plt.xlabel("$t$ (s)")
plt.xlim([min(t),max(t)])

# Plot the power spectrum
plt.figure()
plt.plot(fcycles,np.absolute(yhat))
plt.xlim([-2000,2000])
plt.xlabel("$\omega$ (cycles/s)")
plt.ylabel("$|\hat{y}|$")
plt.show()




