
'''
A sript to plot 
outputs of gediMetric
'''

###########################################
import numpy as np
import argparse




###########################################
# class to hold GEDI metrics

class gediMetrics(object):


###########################################
# read the command line

def gediCommands():
  '''
  Read commandline arguments
  '''
  p = argparse.ArgumentParser(description=("Writes out properties of GEDI waveform files"))
  p.add_argument("--input",dest="inName",type=str,help=("Input GEDI metric filename"))
  p.add_argument("--outRoot",dest="outRoot",type=str,default='test',help=("Output graph filename root"))
  p.add_argument("--writeCoords",dest="writeCoords", action='store_true', default=False, help=("Write out coordinates insteda of plotting waveforms"))
  cmdargs = p.parse_args()
  return cmdargs


###########################################
# the main block

if __name__ == '__main__':
  # read the command line
  cmdargs=gediCommands()

