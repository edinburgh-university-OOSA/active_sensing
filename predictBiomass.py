
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
    self.RH60,self.RH95,self.lon,self.lat=np.loadtxt=np.loadtxt(filename,usecols=(25,32,106,107),unpack=True, dtype=float,comments='#')


  ###########################################

  def predictBiomass(self,outName):
    '''Predict biomass using a hard wired model'''
    # filter usable data
    useInd=np.where((self.RH60>-100)&(self.RH60<1000)&(self.RH95>-100)&(self.RH95<1000))

    if(len(useInd)>0):
      useInd=useInd[0]
      # parametric values
      rh69rh90=np.log(self.rh60[useInd]*self.rh95[useInd])
      # log transform
      rh60=np.log(self.RH60)
      rh95=np.log(self.RH95)
      biomass=np.exp(-19.12512+rh60*0.73074+rh95*0.47493-0.00787*rh60rh90)

      # write to output
      f=open(outNamen,'w')
      j=0
      for i in useInd:
        line=str(self.lon[i])+" "+str(self.lat[i])+" "+str(biomass[j])+"\n"
        f.write(line)
        j=j+1
      f.close()
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
  p.add_argument("--output",dest="output",type=str,default='test.txt',help=("Output filename"))
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
  data=gediMetrics(inName)

  # plot it
  data.predictBiomass(output)

