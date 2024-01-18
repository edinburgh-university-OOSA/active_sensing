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
from math import sqrt
from scipy.ndimage import gaussian_filter


#################################################

class scatterDemo():
  '''Class to hold scatter demonstration
     data and functions'''

  ############################

  def __init__(self):
    # do nothing
    return

  ###########################

  def makeSurface(self,rough=0.1,fineRough=0.001,length=20.0,res=0.01,correl=1.0):
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


#################################################

