

'''
Make illustrations of range resolution
'''


import numpy as np
import matplotlib.pyplot as plt


#####################################

class pulse():
  '''Class to hold a pulse'''

  ################################

  def __init__(self,filename):
    '''Read data from a file'''
    self.x,self.y=np.loadtxt(filename,usecols=(0,1),unpack=True,dtype=float)
    self.x0=self.x[self.y.argmax()]
    return

  ################################

  def addOffset(self,offset):
    '''Add a distance offset'''
    self.x+=offset
    self.x0+=offset
    return


#####################################

def addPulses(p1,p2):
  '''Function to add two pulses'''

  # determine bounds
  xS=np.min((p1.x,p2.x))
  xE=np.max((p1.x,p2.x))
  res=(p1.x[-1]-p1.x[0])/(p1.x.shape[0]-1)
  numb=int((xE-xS)/res+1)

  # allocate space
  x=np.linspace(xS,xE,numb)
  y=np.zeros(numb,dtype=float)


  # determine each start
  sIndP1=np.abs(x-p1.x[0]).argmin()
  sIndP2=np.abs(x-p2.x[0]).argmin()


  # add up intensities
  y[sIndP1:sIndP1+p1.y.shape[0]]+=p1.y
  y[sIndP2:sIndP2+p2.y.shape[0]]+=p2.y

  return(x,y)


#####################################

if __name__ == "__main__":
  '''Main block'''

  filename='/Users/dougal/data/gedi/pulses/meanPulse.BEAM0010.filt'
  offList=[10,2]

  # loop over a list of offsets
  for offset in offList:
    p1=pulse(filename)
    p2=pulse(filename)
    p2.addOffset(offset)
  
    # add two pulses
    x,y=addPulses(p1,p2)

    # plot it
    outName='rangeRes.offset.'+str(offset)+'.png'
    plt.plot(x,y)
    plt.xlabel('Range (m)')
    plt.ylabel('Intensity')
    # add lines
    maxY=np.max(y)
    plt.arrow(p1.x0,maxY,0,-maxY,width=0.2,head_length=0)
    plt.arrow(p2.x0,maxY,0,-maxY,width=0.2,head_length=0)

    plt.savefig(outName)
    plt.cla()
    print("Written to",outName)

