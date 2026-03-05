'''Convert date output by GEE to that expected by BFAST'''

import numpy as np
from math import exp
import argparse


###############################################

def readCommands():
  '''
  Get commandline arguments
  '''
  # create an argparse object with a useful help comment
  p = argparse.ArgumentParser(description=("An illustration of a command line parser"))
  # read a string
  p.add_argument("--median",dest="median", action='store_true', default=False, help=("Use median filter"))
  cmdargs = p.parse_args()
  return cmdargs


###############################################

def convertNameMonth(m):
  '''Convert month name to number'''

  if(m=='Jan'):
    month=1
  elif(m=='Feb'):
    month=2
  elif(m=='Mar'):
    month=3
  elif(m=='Apr'):
    month=4
  elif(m=='May'):
    month=5
  elif(m=='Jun'):
    month=6
  elif(m=='Jul'):
    month=7
  elif(m=='Aug'):
    month=8
  elif(m=='Sep'):
    month=9
  elif(m=='Oct'):
    month=10
  elif(m=='Nov'):
    month=11
  elif(m=='Dec'):
    month=12
    
  return(month)


###############################################

def setDoy(day,month,year):

  mLength=[31,28,31,30,31,30,31,31,30,31,30,31]

  doy=0

  # add up years
  sYear=2014
  for y in range(sYear,year):
    # is it a leap year
    if(((y-2000)%4)==0):
      leap=1
    else:
      leap=0
    doy+=365+leap

  # add up months
  if(((year-2000)%4)==0):
    leap=1
  else:
    leap=0
  for m in range(0,month-1):
    doy+=mLength[m]
    if(m==1):
      doy+=leap

  # add day
  doy+=day

  return(doy)


###############################################

def smoothMedian(doy,vh,width=15):
  '''
  Smooth by a median filter
  It can deal with gappy data
  '''

  smoothed=np.zeros(y.shape,dtype=float)


  return(smoothed)


###############################################

def smoothGuass(doy,y,width):
  '''
  Smooth a function with a fixed window
  It is horrible in order to deal with gappy data
  '''

  smoothed=np.zeros(y.shape,dtype=float)
  contN=np.zeros(y.shape,dtype=float)

  for i in range(0,y.shape[0]):
    # step backwards
    for j in range(i,-1,-1):
      dx=doy[i]-doy[j]
      A=exp(-1*dx**2/width**2)
      if(A<=0.0001):
        break
      smoothed[i]+=y[j]*A
      contN[i]+=A
    # step forwardcs
    for j in range(i+1,y.shape[0],1):
      dx=doy[i]-doy[j]
      A=exp(-1*dx**2/width**2)
      if(A<=0.0001):
        break
      smoothed[i]+=y[j]*A
      contN[i]+=A

  # normalise
  smoothed=smoothed/contN

  return(smoothed)


###############################################

def writeData(outName,day,month,year,vh):
  '''Write output file'''

  # write header
  output=open(outName,'w')
  line="Date,VH\n"
  output.write(line)

  for i in range(0,vh.shape[0]):
    lineOut=str(year[i])+'-'+str(month[i])+'-'+str(day[i])+","+str(vh[i])+"\n"
    output.write(lineOut)

  # close files
  output.close()
  file.close()
  print('Written to',outName)


  return


###############################################

if(__name__=='__main__'):

  # filenames
  outName='bfastInput.csv'
  filename='ee-chart.csv'

  # read the command line
  cmd=readCommands()

  # read the VH backscatter and smooth
  vh=np.loadtxt(filename,usecols=(2),unpack=True,skiprows=1,delimiter=',')
  year=np.empty(vh.shape,dtype=int)
  month=np.empty(vh.shape,dtype=int)
  day=np.empty(vh.shape,dtype=int)
  doy=np.empty(vh.shape,dtype=int)

  # open data
  file=open(filename, 'r')

  # loop over lines
  inHead=True
  i=0
  for wholeLine in file.readlines():
    # skip first row
    if(inHead):
      inHead=False
      continue

    line=wholeLine.replace('"',"")

    # read parts of line
    m=line.split(',')[0].split(' ')[0].strip()
    day[i]=int(line.split(',')[0].split(' ')[1].strip())
    month[i]=convertNameMonth(m)
    year[i]=int(line.split(',')[1].strip())
    doy[i]=setDoy(day[i],month[i],year[i])
    i+=1

  # smooth it
  if(cmd.median):
    smoothed=smoothMedian(doy,vh,width=15)
  else:
    smoothed=smoothGauss(doy,vh,width=7)

  # write data
  writeData(outName,day,month,year,smoothed)

