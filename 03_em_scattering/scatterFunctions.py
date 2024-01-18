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


#################################################

class scatterDemo():
  '''Class to hold scatter demonstration
     data and functions'''

  ############################

  def __init__(self):
    # do nothing
    return

  ###########################

  def makeSurface(self,rough=0.1,length=20.0,res=0.01):
    '''Make a surface'''

    # make sure that the roughness is well sampled
    if(res>(rough/10.0)):
      res=rough/10.0

    # save variables
    self.length=length
    self.rough=rough
    self.res=res

    # allocate array
    self.nBins=int(self.length/self.res)
    self.x=np.linspace(0,self.length,num=self.nBins)
    self.y=np.random.normal(loc=0.0,scale=self.rough,size=self.nBins) # make the random heights
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

