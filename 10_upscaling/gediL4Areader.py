
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


###################################################

class dataTable():
  '''Class to intersect GEDI and PALSAR data'''

  ####################################

  def __init__(self,gedi,palsarHH,hh,palsarHV,hv):
    '''Class initialiser'''


    # intersect the GEDI and PALSAR data
    # HH
    i=(gedi.lon-palsarHH.bounds[0])//palsarHH.res[0]
    j=(palsarHH.bounds[3]-gedi.lat)//palsarHH.res[0]

    # filter data outside of image and save backscatter
    iFilt=np.array(i[(i>=0)&(i<=palsarHH.width)&(j>=0)&(j<palsarHH.height)],dtype=int)
    jFilt=np.array(j[(i>=0)&(i<=palsarHH.width)&(j>=0)&(j<palsarHH.height)],dtype=int)
    self.hh=hh[jFilt,iFilt]

    # save GEDI data
    self.agbd=gedi.agbd[(i>=0)&(i<=palsarHH.width)&(j>=0)&(j<palsarHH.height)]
    self.quality=gedi.quality[(i>=0)&(i<=palsarHH.width)&(j>=0)&(j<palsarHH.height)]
    self.lat=gedi.lat[(i>=0)&(i<=palsarHH.width)&(j>=0)&(j<palsarHH.height)]
    self.lon=gedi.lon[(i>=0)&(i<=palsarHH.width)&(j>=0)&(j<palsarHH.height)]
    self.sensitivity=gedi.sensitivity[(i>=0)&(i<=palsarHH.width)&(j>=0)&(j<palsarHH.height)]

    # HV
    i=(gedi.lon-palsarHV.bounds[0])//palsarHV.res[0]
    j=(palsarHV.bounds[3]-gedi.lat)//palsarHV.res[0]
    
    # filter data outside of image and save backscatter
    iFilt=np.array(i[(i>=0)&(i<=palsarHV.width)&(j>=0)&(j<palsarHV.height)],dtype=int)
    jFilt=np.array(j[(i>=0)&(i<=palsarHV.width)&(j>=0)&(j<palsarHV.height)],dtype=int)
    self.hv=hv[jFilt,iFilt]
    return

  ####################################

  def plotHH(self):
    '''Plot the HH dataset'''

    plt.plot(self.hh,self.agbd,'.')
    plt.xlabel('PALSAR-2 HH bakscatter')
    plt.ylabel('GEDI L4A AGBD (Mg/ha)')
    plt.show()
    return

  ####################################

  def plotHV(self):
    '''Plot the HH dataset'''

    plt.plot(self.hv,self.agbd,'.')
    plt.xlabel('PALSAR-2 HV bakscatter')
    plt.ylabel('GEDI L4A AGBD (Mg/ha)')
    plt.show()
    return

