
'''
Simple script to handle
GEDI L4A files
'''

######################################

import h5py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt


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
    self.sar=np.empty((jFilt.shape[0],2),dtype=float)
    self.sar[:,0]=hh[jFilt,iFilt]

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
    self.sar[:,1]=hv[jFilt,iFilt]
    return

  ####################################

  def plotHH(self):
    '''Plot the HH dataset'''

    plt.plot(self.sar[:,0],self.agbd,'.')
    plt.xlabel('PALSAR-2 HH bakscatter')
    plt.ylabel('GEDI L4A AGBD (Mg/ha)')
    plt.show()
    return

  ####################################

  def plotHV(self):
    '''Plot the HH dataset'''

    plt.plot(self.sar[:,1],self.agbd,'.')
    plt.xlabel('PALSAR-2 HV bakscatter')
    plt.ylabel('GEDI L4A AGBD (Mg/ha)')
    plt.show()
    return

  ####################################

  def correlHH(self):
    '''Return the linear correlation of HH to AGBD'''
    correl=np.corrcoef(self.agbd,self.sar[:,0])[0][-1]
    print('Correlation between AGBD and HH is',round(correl,3))
    return

  ####################################

  def correlHV(self):
    '''Return the linear correlation of HV to AGBD'''
    correl=np.corrcoef(self.agbd,self.sar[:,1])[0][-1]
    print('Correlation between AGBD and HV is',round(correl,3))
    return

  ##################

  def splitData(self,trainFrac=0.7):
    '''Split into training and validation data'''

    self.x_train,self.x_test,self.y_train,self.y_test=train_test_split(self.sar,self.agbd,test_size=1-trainFrac,random_state=0)
    return

  ##################

  def splitSpatially(self,trainFrac=0.7):
    '''Split into training and validation data by latitude'''

    # find percentile latitude
    splitLat=np.percentile(self.lat,trainFrac*100)

    # split the data
    useInd=np.where(self.lat<=splitLat)[0]
    self.x_train=self.sar[useInd,:]
    self.y_train=self.agbd[useInd]

    useInd=np.where(self.lat>splitLat)[0]
    self.x_test=self.sar[useInd,:]
    self.y_test=self.agbd[useInd]
    return


  ##################

  def buildRF(self,n_estimators,max_depth):
    '''Build a random forest model'''

    # initlise the class
    self.regressor=RandomForestRegressor(n_estimators=n_estimators,max_depth=max_depth,random_state=0)  # initialise the class

    # fit the model to the training data
    self.regressor.fit(self.x_train,self.y_train)

    return

  ##################

  def predict(self):
    '''Predict the model on all the data'''

    self.y_pred=self.regressor.predict(self.sar)

    return

  ##################

  def scatterAll(self):
    '''Make a scatterplot of predicted and observed'''

    plt.plot(self.agbd,self.y_pred,'.')
    plt.xlabel('GEDI L4A AGBD (Mg/ha)')
    plt.ylabel('PALSAR-2 RF estimated AGBD (Mg/ha)')
    plt.show()
    return

  ##################

  def validateRF(self):
    '''Validate against the validation data'''

    # predict the validation data
    valid_pred=self.regressor.predict(self.x_test)

    # error metrics
    bias=np.mean(valid_pred-self.y_test)
    correl=np.corrcoef(self.y_test,valid_pred)[0][-1]
    rmse=sqrt(np.sum((valid_pred-self.y_test)**2)/valid_pred.shape[0])
    meanAGBD=np.mean(self.y_test)

    print('Bias',round(bias,3),'Mg/ha')
    print('RMSE',round(rmse,2),'Mg/ha')
    print('Correlation',round(correl,3))
    print('For a mean AGBD of',round(meanAGBD,2),'Mg/ha')


    return

