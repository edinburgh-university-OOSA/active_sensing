
'''
Functions used by the 
signal_processing notebook

For the Active Remote Sensing course
At the University of Edinburgh

Steven Hancock   2024
svenhancock@gmail.com
'''


import numpy as np
from matplotlib import pyplot as plt
from math import pi,sqrt
from scipy.signal import convolve,correlate



class setPulse():
    '''Class to hold and manipulate pulses'''
    
    def __init__(self,sigma,mode,res=0.1,E=1,sFreq=100000,eFreq=1000000000):
        '''Initialiser'''
        
        # save pulse properties within object
        self.sigma=sigma
        self.E=E
        self.res=res
        self.sFreq=sFreq
        self.eFreq=eFreq
        
        # behaviour depends upon pulse
        if(mode=="gauss"):
            self.A=self.E/(sigma*sqrt(2*pi))
            self.pX=np.arange(-sigma*8,sigma*8,res)
            self.pY=self.A*np.exp(-1*self.pX**2/(2*sigma**2))/(sigma*sqrt(2*pi))
        elif(mode=="chirp"):
            self.makeChirp()
        else:
            print(mode,"pulse shape mode not recognised.")
            print("mode must be gauss or chirp")

        return
            
    def makeChirp(self):
        '''Make a chirped pulse. Written by J Hansen for GLAMIS project'''
        self.pX = np.arange(0, self.sigma, self.res)
        t = self.pX / 2.998e8
        
        stime = self.sigma / (2.998e8)
        c = (self.eFreq - self.sFreq) / stime  # sweep scaling constant
        self.pY = np.sin(2.0 * pi * (t**2 * (c/2.0) + self.sFreq * t))
        
        # set energy to be correct total
        totE=np.sum(self.pY)*self.res
        self.pY=self.pY*self.E/totE

        return

    def setTarget(self,N,sep):
        '''Make a target profile'''
        self.tY=np.zeros((self.pX.shape),dtype=float)
        centX=np.mean(self.pX)
        for i in range(0,N):
            x=centX+i*sep
            minInd=np.abs(self.pX-x).argmin()
            self.tY[minInd]=1.0
        return
        
    def correlate(self):
        '''Compute cross-correlation of pulse and target'''
        self.correl=correlate(self.pY,self.conv,mode='full',method='auto')
        self.corX=np.linspace(self.cX[0],self.cX[0]+self.correl.shape[0]*self.res,num=self.correl.shape[0])
        return
    
    def convolve(self):
        """Compute convolution of target and pulse"""
        #N = max(self.pY.shape[0],self.tY.shape[0])
        #X = np.fft.fft(self.pY, n=N)
        #Y = np.fft.fft(self.tY, n=N)
        #self.conv = np.real(np.fft.ifft(X * Y))
        self.conv=convolve(self.pY,self.tY,mode='full')
        sX=self.pX[0]-(np.mean(self.pX)/2.0-self.pX[0])
        eX=sX+self.res*self.conv.shape[0]
        self.cX=np.linspace(sX,eX,num=self.conv.shape[0])
        return
        
    def plotPulse(self):
        '''Plot the pulse'''
        plt.xlabel('Range (m)')
        plt.ylabel('Intensity (unitless)')
        plt.plot(self.pX,self.pY-np.min(self.pY))
        plt.show()
        
    def plotConv(self):
        '''Plot the target and convolution'''
        plt.xlabel('Range (m)')
        plt.ylabel('Intensity (unitless)')
        plt.plot(self.pX,self.tY-np.min(self.tY),label="Target")
        plt.plot(self.cX,self.conv-np.min(self.conv),label="Convolution")
        plt.show()
        
    def plotCorrel(self):
        '''Plot the target and correlation'''
        plt.xlabel('Range (m)')
        plt.ylabel('Intensity (unitless)')
        plt.plot(self.corX,self.correl-np.min(self.correl),label="Correlation")
        plt.show()


