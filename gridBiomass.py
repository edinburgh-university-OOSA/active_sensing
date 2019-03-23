
'''
Grids biomass estimates
'''

#############################################
import numpy as np
import argparse
import scipy.stats as stats


#############################################

class gediBiomass(object):
  '''Class to hold GEDI biomass estimates'''

  #################################

  def __init__(self,filename):
    '''Read footprint level file'''
    self.lon,self.lat,self.agbd=np.loadtxt=np.loadtxt(filename,usecols=(0,1,2),unpack=True, dtype=float,comments='#')


  #################################

  def gridAGBDmean(self,res,outName):
    '''Grid AGBD estimates by simple mean'''
    # determine number of cells
    minX=np.min(self.lon)
    maxX=np.max(self.lon)
    minY=np.min(self.lat)
    maxY=np.max(self.lat)
    nX=int((maxX-minX)/res+1)
    nY=int((maxY-minY)/res+1)
    # grid up
    meanAGBD,x0,y0,binnumber=stats.binned_statistic_2d(self.lon,self.lat,values=self.agbd,statistic='mean',bins=[np.arange(nX), np.arange(nY)])
    # write header
    f=open(outName,'w')
    noData=-9999
    header="NCOLS"+str(nX)+"\n"
    header=header+"NROWS"+str(nY)+"\n"
    header=header+"XLLCENTER"+str(minX)+"\n"
    header=header+"YLLCENTER"+str(minY)+"\n"
    header=header+"CELLSIZE"+str(res)+"\n"
    header=header+"NODATA_VALUE"+str(noData)+"\n"
    f.write(header)
    # remove nan
    meanAGBD[np.isnan(meanAGBD)]=noData
    # write data
    for j in range(nY-1,-1,-1):
      line=""
      for x in meanAGBD[j]:
        line=line+str(x)+" "
      line=line+"\n"
      f.write(line)
    f.close()
    print("Written to",outName)


# end of gediBiomass
#############################################


###########################################
# read the command line

def gediCommands():
  '''
  Read commandline arguments
  '''
  p = argparse.ArgumentParser(description=("Writes out properties of GEDI waveform files"))
  p.add_argument("--input",dest="inName",type=str,help=("Input GEDI metric filename"))
  p.add_argument("--output",dest="output",type=str,default='test.asc',help=("Output graph filename"))
  p.add_argument("--res",dest="res",type=float,default=100,help=("Output resolution"))
  cmdargs = p.parse_args()
  return cmdargs


###########################################
# the main block

if __name__ == '__main__':
  # read the command line
  cmdargs=gediCommands()
  inName=cmdargs.inName
  output=cmdargs.output
  res=cmdargs.res

  # read data
  agbd=gediBiomass(inName)

  # grid data and write output
  agbd.gridAGBDmean(res,output)

