'''Convert date output by GEE to that expected by BFAST'''

import numpy as np


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

def smooth(raw,width):
  '''Smooth a function with a fixed window'''

  x=np.arange(-10*width,10*width,1)
  pulse=np.exp(-1*x**2/width**2)
  y=np.convolve(raw,pulse)
  return(y)


###############################################

if(__name__=='__main__'):

  # filenames
  outName='bfastInput.csv'
  filename='ee-chart.csv'

  # read the VH backscatter and smooth
  vh=np.loadtxt(filename,usecols=(2),unpack=True,skiprows=1,delimiter=',')
  smoothed=smooth(vh,4)

  # open data
  file=open(filename, 'r')
  output=open(outName,'w')

  # write header
  line="Date,VH\n"
  output.write(line)

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
    day=line.split(',')[0].split(' ')[1].strip()
    year=line.split(',')[1].strip()

    month=convertNameMonth(m)

    lineOut=str(year)+'-'+str(month)+'-'+str(day)+","+str(smoothed[i])+"\n"
    output.write(lineOut)
    i+=1

  # close files
  output.close()
  file.close()
  print('Written to',outName)

