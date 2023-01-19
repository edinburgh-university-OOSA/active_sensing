
'''
A sript to plot histograms 
of ground finding error
'''

###########################################
import numpy as np
import argparse
import matplotlib.pyplot as plt


###########################################
# class to hold GEDI metrics

class gediMetrics(object):

  ###########################################

  def __init__(self,filename):
    '''Read the file'''
    self.tG,self.eG=np.loadtxt=np.loadtxt(filename,usecols=(1,5),unpack=True, dtype=float,comments='#')


  ###########################################

  def groundErrHist(self,outName,nBins=10):
    '''make an error histogram'''
    # filter out missing data
    useInd=np.where((self.tG>-100)&(self.eG>-100)&(self.eG<10000)&(self.eG<10000))
    if(len(useInd)>0):
      useInd=useInd[0]
      # calculate differences
      err=self.eG[useInd]-self.tG[useInd]
      # make histogram
      hist=np.histogram(err,bins=nBins)
      x=np.empty(len(hist[0]),dtype=float)
      for i in range(1,len(hist[1])):
        x[i-1]=(hist[1][i]+hist[1][i-1])/2.0
      # plot it
      plt.plot(x,hist[0])
      plt.xlabel('Ground elevation error (m)')
      plt.ylabel('Frequency')
      plt.ylim(bottom=0)
      plt.savefig(outName)
      plt.close()
      plt.clf()
      print("Written to",outName)
    else:
      printf("No usable data in file")


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
  p.add_argument("--nBins",dest="nBins",type=int,default=10,help=("Number of histogram bins to use"))
  cmdargs = p.parse_args()
  return cmdargs


###########################################
# the main block

if __name__ == '__main__':
  # read the command line
  cmdargs=gediCommands()
  inName=cmdargs.inName
  output=cmdargs.output
  nBins=cmdargs.nBins

  # read data
  data=gediMetrics(inName)

  # plot it
  data.groundErrHist(output,nBins=nBins)

