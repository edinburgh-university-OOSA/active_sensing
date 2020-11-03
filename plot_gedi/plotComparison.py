


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

# import a GEDI object
import sys,os
sys.path.append(os.environ["GEDIRAT_ROOT"])
from gediHandler import gediData


###########################################
# read the command line

if __name__ == '__main__':
  def readCommands():
    '''
    Read commandline arguments
    '''
    p = argparse.ArgumentParser(description=("Writes out properties of GEDI waveform files"))
    p.add_argument("--real",dest="realName",type=str,help=("Input GEDI HDF5 filename"))
    p.add_argument("--sim", dest ="simname", type=str,help=("Input simulated GEDI HDF5 filename"))
    p.add_argument("--outRoot",dest="outRoot",type=str,default='test',help=("Output graph filename root"))
    p.add_argument("--metric",dest="metName", type=str, default=" ", help=("Optional: Metric filename, for ground esoimates"))
    p.add_argument("--datumDiff",dest="datum", type=float, default=0.0, help=("Optional: Datum difference"))
    cmdargs = p.parse_args()
    return cmdargs


###########################################

class gediMetrics():
  '''Class to hold GEDI metrics'''
  def __init__(self,filename):
    '''Initialiser'''
    if(filename!=" "):
      self.waveID=np.genfromtxt(filename,usecols=(0,), unpack=True, dtype=str,comments='#')
      self.ZG,self.cov,self.slope,self.sense=np.loadtxt(filename,usecols=(1,4,3,112), unpack=True, dtype=float,comments='#')
      self.shotN=np.empty(self.waveID.shape,dtype=int)
      for i in range(0,self.waveID.shape[0]):
        self.shotN[i]=int(self.waveID[i].split('.')[2])
    else:
      self.useMet=0   # file is empty. Don't use

###########################################

def plotComparison(gedi,sim,met,outRoot,datum=0):
  '''Function to plot graph comparisons'''

  # loop over waveforms
  for i in range(0,gedi.nWaves):
    # find corresponding etric
    shotN=gedi.waveID[i]
    beam=gedi.waveID[i]
    simInd=np.where((sim.shotN==shotN)) #*(sim.beamID==gedi.beamID[i]))

    # do we have any?
    if(len(simInd)>0):
      if(len(simInd[0])>0):
        simInd=simInd[0][0]
      else:
        continue
    else:
      continue

    if(met.useMet==1):
      metInd=np.where(met.shotN==shotN)[0][0]

    # make a graph
    output=outRoot+".beam."+str(shotN)+".png"

    # set z arrays
    gedi.nBins=gedi.lenInds[i]
    gedi.res=(gedi.Z0[i]-gedi.ZN[i])/gedi.nBins
    gedi.setOneZ(i)
    sim.setOneZ(simInd)

    # set scalars and bounds
    reflScale,meanN,stdev=gedi.meanNoise(i)
    minX,maxX=gedi.findBounds(meanN,stdev,i)
    #temp=np.sort(np.copy(gedi.wave[i][0:gedi.nBins]))
    #minY=temp[int(temp.shape[0]*0.01)]-5  # to avoid artefacts
    maxY=1.2*np.max(gedi.wave[i][0:gedi.nBins])
    minY=meanN-0.1*(maxY-meanN)

    # arrange the plot
    plt.xlim(minY,maxY)
    plt.ylim((minX+datum,maxX+datum))
    plt.ylabel('Elevation (m)')
    plt.ylabel('DN')
    plt.plot(gedi.wave[i][0:gedi.nBins],gedi.z+datum,label='GEDI')
    plt.plot(sim.wave[simInd][0:sim.nBins]*reflScale+meanN,sim.z,label='Sim')
    plt.plot(sim.gWave[simInd][0:sim.nBins]*reflScale+meanN,sim.z,label='ALS ground')
    plt.legend()
    plt.savefig(output)
    plt.close()
    plt.clf()
    print("Written to",output)

  return

###########################################
# the main block

if __name__ == '__main__':
  # read the command line
  cmd=readCommands()

  realName='/Users/dill/data/teaching/nerc_cdt/space/gedi/subset.GEDI01_B_2019223180803_O03756_T03613_02_003_01.h5'
  simName='/Users/dill/data/teaching/nerc_cdt/space/gedi/sim.GEDI01_B_2019223180803_O03756_T03613_02_003_01.h5'

  # read real GEDI data
  gedi=gediData(filename=realName)

  # read simulated GEDI data
  sim=gediData(filename=simName)

  # read metrics, if needed
  met=gediMetrics(cmd.metName)

  # plot them up
  plotComparison(gedi,sim,met,cmd.outRoot,datum=cmd.datum)

