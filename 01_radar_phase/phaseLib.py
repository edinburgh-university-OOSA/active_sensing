
'''
Library of functions for the
Radar phase practical
'''


# python code below. Do not modify.
import numpy as np
from math import pi
from matplotlib import pyplot as plt


################################################

def makeWave(A,l,p):
  '''make arrays of data'''
  c=2.998*10**8
  x=np.arange(0,l*3,l/36)
  y=A*np.sin(x*2*pi/l+p*pi/180)
  return(x,y)


################################################

def plotOneWave(x,y):
  '''Plot a single wave'''
  plt.plot(x,y)
  plt.xlabel("Distance (m)")
  plt.ylabel("Electric field strength")
  plt.show()


################################################

def plotThreeWaves(x1,x2,x3,y1,y2,y3):
  '''Plot three waves'''
  plt.plot(x1,y1,label='Wave 1')
  plt.plot(x2,y2,label='Wave 2')
  plt.plot(x3,y3,label='Interference')
  plt.xlabel("Distance (m)")
  plt.ylabel("Electric field strength")
  plt.legend()
  plt.show()


################################################

def interfereWaves(x1,y1,x2,y2):
  '''Interfere two waves'''
  minLen=np.min(np.array((y1.shape[0],y2.shape[0])))
  yI=y1[:minLen]+y2[:minLen]
  xI=x1[:minLen]

  return(xI,yI)

################################################



###################################
# the section below gives the     #
# python code needed to add up    #
# EM waves from multiple emitters #
###################################

class emitter():
    '''class to hold emitters'''
    
    def __init__(self,A,l,tP,x,y):
        '''Class initialiser'''
        self.A=A
        self.l=l
        self.p=tP
        self.x=x
        self.y=y
        
    def calcDistance(self,nX,nY,imWidth,res):
        '''Calculate distance from emitter to all pixels'''
        x1d=np.linspace(-imWidth/2,imWidth/2,num=nX)
        self.xG,self.yG=np.meshgrid(x1d,x1d)
        self.dists=np.sqrt((self.xG-self.x)**2+(self.yG-self.y)**2)

    def calcField(self):
        '''Calculate field strength over area'''        
        self.fieldS=self.A*np.sin(self.dists*2*pi/self.l+self.p)

#################################
        
# this function places the emitters
def placeEmitters(N,D,imWidth,A,l,p):
    
    emitters=np.zeros(N,dtype=emitter)
    
    for i in range(0,N):
        if(N>1):
            y=i*D/(N-1)-D/2
            tP=i*p*pi/180
        else:
            y=0.0
            tP=0.0
        x=0.0

        emitters[i]=emitter(A,l,tP,x,y)
        
    return(emitters)
    
#################################

def plotInterference(N,D,A,l,p):
    '''Function to plot interference'''

    # set image size
    imWidth=l*30
    if(imWidth<50):
      imWidth=50.0
    if(imWidth<D*5):
      imWidth=D*5.0
    res=l/8
    nX=int(imWidth//res)
    nY=int(imWidth//res)
    
                
    # place the emitters
    emitters=placeEmitters(N,D,imWidth,A,l,p)

    # loop over emitters and add up field
    fieldS=np.zeros((nX,nY),dtype=float)
    xs=[]  # this still store the emitter positions
    ys=[]
    for i in range(0,N):
        emitters[i].calcDistance(nX,nY,imWidth,res)
        emitters[i].calcField()
        fieldS=fieldS+emitters[i].fieldS
        xs.append(emitters[i].x)   # save emitter positions
        ys.append(emitters[i].y)
    

    # plot
    plt.imshow(np.abs(fieldS),extent=(imWidth/2,-imWidth/2,imWidth/2,-imWidth/2))
    plt.scatter(x=xs, y=ys, c='r', s=40)
    plt.show()

#################################

