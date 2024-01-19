'''
A set of functions to demonstrate
EM radiation scattering.

University of Edinburgh
Active Remote Sensing course

Steven Hancock      2024
svenhancock@gmail.com
'''


#################################################
# import needed parts

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt,cos,sin,pi
from scipy.ndimage import gaussian_filter


#################################################

class scatterDemo():
  '''Class to hold scatter demonstration
     data and functions'''

  ############################

  def __init__(self):
    # do nothing on initialisation
    return


  ###########################

  def makeSurface(self,rough=0.1,fineRough=0.001,length=20.0,res=0.01,correl=1.0,rho=0.5):
    '''Make a surface'''

    # make sure that the roughness is well sampled
    if(res>(rough/10.0)):
      res=rough/10.0

    # save variables
    self.length=length
    self.res=res
    self.correl=correl

    # allocate array
    self.nBins=int(self.length/self.res)
    self.x=np.linspace(0,self.length,num=self.nBins)
    y=np.random.normal(loc=0.0,scale=sqrt(rough**2+self.correl**2),size=self.nBins) # make the random heights
    self.y=gaussian_filter(y,correl/res)+np.random.normal(loc=0.0,scale=fineRough,size=self.nBins) # add correlation and final roughness
    return


  ###########################

  def plotSurface(self):
    '''Plot a surface'''
    plt.xlabel("Distance (m)")
    plt.ylabel("Height (m)")
    plt.plot(self.x,self.y)
    plt.show()
    return


  ###########################

  def interfereWaves(self,zen=0.0,wavel=0.06,angRes=2*pi/360):
    '''Produce BRDF through wave interference'''

    # set the illumination height vector
    dZ=-1.0*cos(zen)
    z0=100.0  # some arbitrary start point

    # allocate the result arrays
    self.angRes=angRes
    self.nAng=int(2*pi/angRes)
    self.angRefl=np.zeros((self.nAng),dtype=float)
    self.angContN=np.zeros((self.nAng),dtype=int)
    self.refRes=wavel/4.0
    self.refNx=self.refNy=int(self.length/self.refRes)
    self.refImage=np.zeros((self.refNx,self.refNy),dtype=float)
    self.refCont=np.zeros((self.refNx,self.refNy),dtype=int)

    # set out an emitted wave from every point on the object
    for i in range(0,self.x.shape[0]):
      # determine start phase
      startPhase=(((z0-self.y[i])/dZ)/wavel)%(2*pi)






  ###########################

  def traceEnergy(self,zen=0.0,wavel=0.06):
    '''Trace energy and determine BRDF'''

    # set the illumination vector
    vectRay=np.array((sin(zen),-1.0*cos(zen)))

    # for every segment of the scene, trace to the sun and work out the reflected energy
    for i in range(0,self.x.shape[0]-1):
      # find ground vector here
      dX=self.x[i+1]-self.x[i]
      dY=self.y[i+1]-self.y[i]
      vectLen=sqrt(dX**2+dY**2)
      vectGr=np.array((dX/vectLen,dY/vectLen))

      # determine angle of reflection


    return


  ###########################

  def plotEnergy(self):
    '''Plot the returned energy'''
    return


#################################################

