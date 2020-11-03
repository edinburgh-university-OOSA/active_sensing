

import h5py
import numpy as np
import argparse

##########################################

def getCmdArgs():
  '''
  Get commandline arguments
  '''
  p = argparse.ArgumentParser(description=("An illustration of a command line parser"))
  p.add_argument("--inList",dest="inList",type=str,help=("Input filename"))
  p.add_argument("--output",dest="outName",type=str,help=("Output filename"))
  p.add_argument("--minX", dest ="minX",type=float,help=("Min longitude in degrees"))
  p.add_argument("--maxX", dest ="maxX",type=float,help=("Max longitude in degrees"))
  p.add_argument("--minY", dest ="minY",type=float,help=("Min latitude in degrees"))
  p.add_argument("--maxY", dest ="maxY",type=float,help=("Max latitude in degrees"))
  cmdargs = p.parse_args()
  return cmdargs



##########################################

class gediData():
  '''Class to hold GEDI data'''

  def __init__(self,filename):
    '''Initialiser'''

    # create blank arrays
    self.x=np.array(())
    self.y=np.array(())
    self.id=np.array(())

    self.filename=filename
    # read the data
    try:
      f=h5py.File(filename,'r')
    except:
      return

    # loop over beams
    beamList=list(f)
    for beam in beamList:
      if(beam=='METADATA'):
        continue

      # does this file have data?
      if 'geolocation' in list(f[beam]):
        if(('longitude_bin0' in list(f[beam]['geolocation']))&('latitude_bin0' in list(f[beam]['geolocation']))&('shot_number' in list(f[beam]['geolocation']))):
          print(beam)
          self.x=np.append(self.x,np.array(f[beam]['geolocation']['longitude_bin0']))
          self.y=np.append(self.y,np.array(f[beam]['geolocation']['latitude_bin0']))
          self.id=np.append(self.id,np.array(f[beam]['geolocation']['shot_number']))

    f.close()


  def extractBounds(self,minX,maxX,minY,maxY,outName,filename):
    '''Select bounds and write to file'''

    # find usable footprints
    useInd=np.where((self.x>=minX)&(self.x<=maxX)&(self.y>=minY)&(self.y<=maxY))

    # are there any?
    if(len(useInd)>0):
      useInd=useInd[0]

      f=open(outName,'a+')

      for i in useInd:
        line=str(self.x[i])+" "+str(self.y[i])+" "+str(self.id[i])+" "+filename+"\n"
        f.write(line)

      f.close()


##########################################
# main

if __name__ == '__main__':
  # read the command line
  c=getCmdArgs()

  # loop over files
  listFile=open(c.inList)
  for filename in listFile:
    namen=filename.strip()
    print("Reading",namen)
    # read data
    d=gediData(namen)
    # find bounds and write to file
    d.extractBounds(c.minX,c.maxX,c.minY,c.maxY,c.outName,namen)

  listFile.close()

  print("Written to",c.outName)

