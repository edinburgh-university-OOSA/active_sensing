
'''
A sript to plot
waveform fits 
'''

###########################################
import numpy as np
import argparse
import matplotlib.pyplot as plt


###########################################
# class to hold GEDI metrics

class gediFit(object):

  ###########################################

  def __init__(self,filename):
    '''Read the file'''
    self.z,self.raw,self.denoise=np.loadtxt=np.loadtxt(filename,usecols=(0,1,2),unpack=True, dtype=float,comments='#')


  ###########################################

  def plotFit(self,outName):
    '''Plot a fitted waveform'''
    plt.plot(self.denoise,self.z)
    plt.xlabel('DN')
    plt.ylabel('Elevation (m)')
    plt.ylim(bottom=0)
    plt.savefig(outName)
    plt.close()
    plt.clf()
    print("Written to",outName)


# end of gediMetrics class
###########################################


###########################################
# read the command line

def gediCommands():
  '''
  Read commandline arguments
  '''
  p = argparse.ArgumentParser(description=("Writes out properties of GEDI waveform files"))
  p.add_argument("--input",dest="inName",type=str,help=("Input GEDI metric filename"))
  p.add_argument("--output",dest="output",type=str,default='test.png',help=("Output graph filename"))
  cmdargs = p.parse_args()
  return cmdargs


###########################################
# the main block

if __name__ == '__main__':
  # read the command line
  cmdargs=gediCommands()
  inName=cmdargs.inName
  output=cmdargs.output

  # read data
  data=gediFit(inName)

  # plot it
  data.plotFit(output)

