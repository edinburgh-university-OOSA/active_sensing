
'''
Simple script to handle
GEDI L4A files
'''

######################################

import h5py
import numpy as np
import matplotlib.pyplot as plt

######################################

class gediL4A():
  '''Class to hold GEDI L4A data'''

  ####################################

  def __init__(self,filename):
    '''Class initialiser'''

    # read the data
    f=h5py.File(filename,'r')
    self.nWaves=0

    # loop over beams
    beamList=['BEAM0000','BEAM0001','BEAM0010','BEAM0011','BEAM0101','BEAM0110','BEAM1000','BEAM1011']
    for b in beamList:
      if((b in list(f))==False): # does this exist?
        continue                 # if not, skip it
      elif(('geolocation' in list(f[b]))==False):  # no data in bea,
        continue

      # read data from file
      agbd=np.array(f[b]['agbd'])
      quality=np.array(f[b]['l4_quality_flag'])
      lat=np.array(f[b]['lat_lowestmode'])
      lon=np.array(f[b]['lon_lowestmode'])
      sensitivity=np.array(f[b]['sensitivity'])

      # save data into structure
      if(self.nWaves>0):
        self.agbd=np.append(self.agbd,agbd)
        self.quality=np.append(self.quality,quality)
        self.lat=np.append(self.lat,lat)
        self.lon=np.append(self.lon,lon)
        self.sensitivity=np.append(self.sensitivity,sensitivity)
      else:
        self.agbd=agbd
        self.quality=quality
        self.lat=lat
        self.lon=lon
        self.sensitivity=sensitivity

      self.nWaves+=agbd.shape[0]

    print('Found',self.nWaves,"footprints")
    self.f=f
    return

  ####################################

  def filterQuality(self):
    '''Filter out quality==0'''

    # temporary arrays
    agbd=self.agbd[self.quality==1]
    quality=self.quality[self.quality==1]
    lat=self.lat[self.quality==1]
    lon=self.lon[self.quality==1]
    sensitivity=self.sensitivity[self.quality==1]

    # overwrite old arrays
    self.agbd=agbd
    self.quality=quality
    self.lat=lat
    self.lon=lon
    self.sensitivity=sensitivity

    print('Filtered',self.nWaves-self.agbd.shape[0],'from',self.nWaves)
    self.nWaves=self.agbd.shape[0]
    return

  ####################################

  def printHeaders(self):
    '''Prints out the top level structure'''
    print(list(self.f))
    return

  ####################################

  def plotCoords(self):
    '''Plot footprint coordinates'''
    plt.plot(self.lon,self.lat,'.')
    plt.xlabel("Longitude (degrees)")
    plt.ylabel("Latitude (degrees)")
    plt.show()
    return

  ####################################

  def plotHistogram(self):
    '''Plot a histogram of the biomass and the beam sensitivity'''

    # agdb
    hist=np.histogram(self.agbd,bins=1000)
    plt.plot(hist[1][0:-1],hist[0])
    plt.xlabel('AGBD (Mg/ha)')
    plt.ylabel('Frequency')
    plt.xlim(left=0,right=500)
    plt.show()

    # sensitivity
    hist=np.histogram(self.sensitivity,bins=100)
    plt.plot(hist[1][0:-1]*100,hist[0])
    plt.xlabel('Beam Sensitivity (%)')
    plt.ylabel('Frequency')
    #plt.xlim(right=100)
    plt.show()
    return

