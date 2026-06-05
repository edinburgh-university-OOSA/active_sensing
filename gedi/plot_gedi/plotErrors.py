


'''
A script to plot a comparison 
between real and simulated GEDI 
data. Make sure to collocate first
2020
'''


##################################
import numpy as np
import h5py
from sys import exit
import matplotlib.pyplot as plt
if __name__ == '__main__':
  import argparse


###########################################
# read the command line

if __name__ == '__main__':
  def readCommands():
    '''
    Read commandline arguments
    '''
    p = argparse.ArgumentParser(description=("Writes out properties of GEDI waveform files"))
    p.add_argument("--real",dest="realName",type=str,help=("Input GEDI HDF5 filename"))
    p.add_argument("--output",dest="outnamen",type=str,default='test.png',help=("Output graph filename"))
    p.add_argument("--als",dest="metName", type=str, default=" ", help=("Metric filename from ALS data"))
    p.add_argument("--useSense",dest="xSense",default=False,action='store_true', help=("Plot sensitivity - cover on the x axis"))
    cmdargs = p.parse_args()
    return cmdargs


###########################################

class gediMetrics():
  '''Class to hold GEDI metrics'''
  def __init__(self,filename):
    '''Initialiser'''

    self.waveID=np.genfromtxt(filename,usecols=(0,), unpack=True, dtype=str,comments='#')
    self.ZG,self.sense,self.cov=np.loadtxt(filename,usecols=(5,112,4), unpack=True, dtype=float,comments='#')

    self.shotN=np.empty(self.waveID.shape,dtype=int)
    self.beam=np.empty(self.waveID.shape,dtype=str)

    for i in range(0,self.waveID.shape[0]):
      self.shotN[i]=int(self.waveID[i].split('.')[2])
      self.beam[i]=self.waveID[i].split('.')[1]



###########################################

class gediL2A():
  '''Class to hold GEDI L2A data'''

  def __init__(self,filename):
    '''Initialiser'''

    # open the file
    f=h5py.File(filename,'r')
    self.nWaves=0

    # loop over beams
    beamList=['BEAM0000', 'BEAM0001', 'BEAM0010', 'BEAM0011', 'BEAM0101', 'BEAM0110', 'BEAM1000', 'BEAM1011']
    for b in beamList:
      if((b in list(f))==False): # does this exist?
        continue                 # if not, skip it
      elif(('geolocation' in list(f[b]))==False):  # no data in bea,
        continue        

      ZG=np.array(f[b]['elev_lowestmode'])
      shotN=np.array(f[b]['shot_number'])
      sensitivity=np.array(f[b]['sensitivity'])
      nWaves=ZG.shape[0]

      if(self.nWaves==0):
        self.ZG=ZG
        self.shotN=shotN
        self.sensitivity=sensitivity
        self.beam=np.repeat(b,nWaves)
      else:
        self.ZG=np.append(self.ZG,ZG)
        self.shotN=np.append(self.shotN,shotN)
        self.sensitivity=np.append(self.sensitivity,sensitivity)
        self.beam=np.append(self.beam,np.repeat(b,nWaves))

      self.nWaves+=nWaves

    f.close()
    return



###########################################

def plotComparison(gedi,met,outnamen,xSense=False):
  '''Function to plot graph comparisons'''

  # create arrays
  x=np.zeros(gedi.nWaves,dtype=float)
  y=np.zeros(gedi.nWaves,dtype=float)


  # align the datasets
  # loop over waveforms
  contN=0
  for i in range(0,gedi.nWaves):
    # find corresponding etric
    shotN=gedi.shotN[i]
    beam=gedi.beam[i]

    metInd=np.where((met.shotN==shotN)) #&(met.beam==beam))

    if(len(metInd)>0):
      metInd=metInd[0]
      if(len(metInd)>0):
        metInd=metInd[0]
      else:
        continue
    else:
      continue

    if(xSense):  # scatter plot of elevatiosn
      x[contN]=gedi.sensitivity[i]-met.cov[metInd]
      y[contN]=gedi.ZG[i]-met.ZG[metInd]
    else:         # error against sense-cover
      x[contN]=met.ZG[metInd]
      y[contN]=gedi.ZG[i]

    contN+=1

  # plot the graph
  plt.plot(x[0:contN],y[0:contN],'.')
  if(xSense):
    plt.xlabel('Beam sensitivity - canopy cover (%)')
    plt.ylabel('GEDI L2A - ALS ground elevation (m)')
  else:
    plt.xlabel('ALS ground elevation (m)')
    plt.ylabel('GEDI L2A ground elevation (m)')

  plt.savefig(outnamen)
  print('Drawn to',outnamen)

  return


###########################################
# the main block

if __name__ == '__main__':
  # read the command line
  cmd=readCommands()

  # read real GEDI data
  gedi=gediL2A(filename=cmd.realName)

  # read metrics, if needed
  met=gediMetrics(cmd.metName)

  # plot them up
  plotComparison(gedi,met,cmd.outnamen,xSense=cmd.xSense)

