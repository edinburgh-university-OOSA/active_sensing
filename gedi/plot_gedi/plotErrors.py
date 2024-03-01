


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
    p.add_argument("--outRoot",dest="outRoot",type=str,default='test',help=("Output graph filename root"))
    p.add_argument("--als",dest="metName", type=str, default=" ", help=("Metric filename from ALS data"))
    cmdargs = p.parse_args()
    return cmdargs


###########################################

class gediMetrics():
  '''Class to hold GEDI metrics'''
  def __init__(self,filename):
    '''Initialiser'''

    self.waveID=np.genfromtxt(filename,usecols=(0,), unpack=True, dtype=str,comments='#')
    self.ZG,self.sense=np.loadtxt(filename,usecols=(5,112), unpack=True, dtype=float,comments='#')

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

    # loop over beams
    beamList=['BEAM0000', 'BEAM0001', 'BEAM0010', 'BEAM0011', 'BEAM0101', 'BEAM0110', 'BEAM1000', 'BEAM1011']
    for b in beamList:
      if((b in list(f))==False): # does this exist?
        continue                 # if not, skip it
      elif(('geolocation' in list(f[b]))==False):  # no data in bea,
        continue        

      if(self.nWaves==0)
        self.ZG=np.array(f[b]['elev_lowestmode'])
        self.shotN=np.array(f[b]['shot_number'])
        self.sensitivity=np.array(f[b]['sensitivity'])
      else:
        self.ZG=np.append(self.ZG,np.array(f[b]['elev_lowestmode']))
        self.shotN=np.append(self.shotN,np.array(f[b]['shot_number']))
        self.sensitivity=np.append(self.sensitivity,f[b]['sensitivity'])

      self.nWaves=self.ZG.shape[0]

    f.close()
    return



###########################################

def plotComparison(gedi,met,outRoot,datum=0,mode=0):
  '''Function to plot graph comparisons'''

  # create arrays
  x=np.zeros(gedi.nWaves,dtype=float)
  y=np.zeros(gedi.nWaves,dtype=float)


  # align the datasets
  # loop over waveforms
  contN=0
  for i in range(0,gedi.nWaves):
    # find corresponding etric
    shotN=gedi.waveID[i]
    beam=gedi.beam[i]

    metInd=np.where((met.shotN==shotN)&(met.beam==beam))
    if(len(metInd)>0):
      metInd=metInd[0]
    else:
      continue

    if(mode==0):  # scatter plot of elevatiosn
      x[contN]=met.ZG
      y[contN]=gedi.ZG[i]
    else:         # error against sense-cover

    contN+=1


    if(met.useMet==1):
      plt.plot([minY,maxY], [met.ZG[metInd],met.ZG[metInd]], color='b', linestyle='-', linewidth=2)

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
  plotComparison(gedi,met,cmd.outRoot,datum=cmd.datum)

