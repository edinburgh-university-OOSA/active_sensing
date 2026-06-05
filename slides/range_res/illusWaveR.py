

'''
Make illustrations of wavelength limit to range resolution
'''


import numpy as np
import matplotlib.pyplot as plt
from math import pi,sqrt


#####################################

class newPulse():
  '''Class to hold a pulse with extra methods'''


  ################################

  def __init__(self,sigma,res):

    self.x=np.arange(-10,10,res)
    self.y=np.exp(-1*self.x**2/(2*sigma**2))/(sigma*sqrt(pi))

    return


  ################################

  def addEM(self,wavel):
    '''Add in the Em radiation'''

    A=1
    self.carrier=A*np.sin(self.x*2*pi/wavel)
    self.carried=self.carrier*self.y

    return


#####################################

if __name__ == "__main__":
  '''Main block'''

  sigma=0.9
  waveList=[0.1*10**-3,1,5,0.2,10]

  # loop over a list of offsets
  for wavel in waveList:
    res=wavel/4.0
    if(res>0.1):
      res=0.1
    p=newPulse(sigma,res)
    p.addEM(wavel)
  
    # plot it
    outName='waveRes.carrier.lambda.'+str(wavel)+'.png'
    plt.plot(p.x,p.carrier)
    plt.xlabel('Range (m)')
    plt.ylabel('Intensity')
    plt.savefig(outName)
    plt.cla()
    print("Written to",outName)

    # plot it
    outName='waveRes.carried.lambda.'+str(wavel)+'.png'
    plt.plot(p.x,p.carried)
    plt.xlabel('Range (m)')
    plt.ylabel('Intensity')
    plt.savefig(outName)
    plt.cla()
    print("Written to",outName)

    # plot it
    outName='waveRes.pulse.lambda.'+str(wavel)+'.png'
    plt.plot(p.x,p.y)
    plt.xlabel('Range (m)')
    plt.ylabel('Intensity')
    plt.savefig(outName)
    plt.cla()
    print("Written to",outName)
