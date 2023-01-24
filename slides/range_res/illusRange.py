

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
    return

  ################################

  def addOffset(self,offset):
    '''Add a distance offset'''
    self.x+=offset
    return


#####################################

def addPulses(p1,p2):
  '''Function to add two pulses'''

  # determine alignment

  # allocate space

  # add two arrays

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
    plt.savefig(outName)
    plt.cla()
    print("Written to",outName)

