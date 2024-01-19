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

  def makeSurface(self,rough=0.2,fineRough=0.001,length=20.0,res=0.1,correl=1.0,rho=0.5):
    '''Make a surface'''

    # make sure that the roughness is well sampled
    if(res>(rough/3.0)):
      res=rough/3.0

    # save variables
    self.length=length
    self.res=res
    self.correl=correl
    self.rho=rho

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
    zStart=100.0  # some arbitrary start point

    # allocate the result arrays
    self.angRes=angRes
    self.nAng=int(2*pi/angRes)
    self.angRefl=np.zeros((self.nAng),dtype=float)
    self.angContN=np.zeros((self.nAng),dtype=int)
    self.refRes=wavel/4.0
    self.refZ0=np.min(self.y)
    self.refNx=int(self.length/self.refRes)
    self.refNy=int((self.length+self.refZ0)/self.refRes)
    self.refImage=np.zeros((self.refNx,self.refNy),dtype=float)
    self.refCont=np.zeros((self.refNx,self.refNy),dtype=int)

    # array of image coordinates
    x=np.empty((self.refNx,self.refNy),dtype=float)
    y=np.empty((self.refNx,self.refNy),dtype=float)
    for i in range(0,self.refNx):
      x[i,:]=np.full(self.refNy,i*self.refRes)
    for j in range(0,self.refNy):
      y[:,j]=np.full(self.refNx,j*self.refRes)


    # for progress tracking
    nMess=10
    spacing=int(self.x.shape[0]/nMess+1)

    # set out an emitted wave from every point on the object
    for k in range(0,self.x.shape[0]):
      if((k%spacing)==0):
        print("Progress",100*k/self.x.shape[0],"%")

      x0=self.x[k]
      y0=self.y[k]
      # determine start phase
      startDist=(zStart-y0)/dZ

      # distance to every point
      dists=np.sqrt((x-x0)**2+(y-y0)**2)+startDist
      angles=2*pi*(dists/wavel)%(2*pi)
      amp=self.rho*np.sin(angles)

      # set underground to zero
      for i in range(0,self.refNx):
        ind=int(i*self.refRes/self.res)
        yGr=self.y[ind]
        amp[i,y[i]<yGr]=0.0

      self.refImage+=amp
      self.refCont+=1

    # normalise image
    self.refImage[self.refCont>0]/=self.refCont[self.refCont>0]
    print("Ping")
    return


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

    plt.imshow(self.refImage)
    plt.show()


    return


#################################################

