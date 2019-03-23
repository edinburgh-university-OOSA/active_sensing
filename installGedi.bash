#!/bin/bash -f


######################
# Scripts to install #
# GEDI software and  #
# set up environemnt #
######################

# set up environment variables
envFile="$HOME/.bashrc"
export ARCH=`uname -m`
echo "export ARCH=`uname -m`" >> $envFile
echo "export PATH=$PATH:./:$HOME/bin/$ARCH:$HOME/bin/csh" >> $envFile
echo "export GEDIRAT_ROOT=$HOME/src/gedisimulator" >> $envFile
echo "export CMPFIT_ROOT=$HOME/src/minpack" >> $envFile
echo "export GSL_ROOT=/usr/local/lib" >> $envFile
echo "export LIBCLIDAR_ROOT=$HOME/src/libclidar" >> $envFile
echo "export HANCOCKTOOLS_ROOT=$HOME/src/tools" >> $envFile
echo "export HDF5_LIB=/apps/hdf5/1.8.15/patch1" >> $envFile


# set up directory structure
if [ ! -e $HOME/src ];then
  mkdir $HOME/src
fi
if [ ! -e $HOME/src/$ARCH ];then
  mkdir $HOME/src/$ARCH
fi
if [ ! -e $HOME/src/csh ];then
  mkdir $HOME/src/csh
fi
if [ ! -e $CMPFIT_ROOT ]; then
  mkdir $CMPFIT_ROOT
fi

pushd $CMPFIT_ROOT
wget https://www.physics.wisc.edu/~craigm/idl/down/cmpfit-1.2.tar.gz
tar -xvf cmpfit-1.2.tar.gz
mv cmpfit-1.2/* $CMPFIT_ROOT/
popd

pushd $HOME/src
hg clone https://bitbucket.org/StevenHancock/libclidar
hg clone https://bitbucket.org/StevenHancock/tools
git clone https://bitbucket.org/StevenHancock/gedisimulator


programList="gediRat gediMetric mapLidar lvisBullseye"
cd $GEDIRAT_ROOT/
make clean

for program in $programList;do
  make THIS=$program
  make THIS=$program install
done

cp *.csh $HOME/src/csh/
cp *.bash $HOME/src/csh/

popd

