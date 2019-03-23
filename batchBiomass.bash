#!/bin/bash -f


#################
# Batch process #
# GEDI data     #
#################


# defaults
bin="/geos/netdata/avtrain/data/3d/active_sensing/week10/active_sensing"
output="allBiomass.txt"

# Read the command line
while [[ $# -gt 0 ]]
do
key="$1"
  case $key in
    -inDir)
      inDir="$2"
      shift;shift 
      ;;
    -output)
      output="$2"
      shift;shift
      ;;
    -help)
      echo " "
      echo "Batch processing of GEDI biomass"
      echo " "
      echo "-inDir name;       directory name to process all HDF5 files within"
      echo "-output name;      output filename"
      echo " "
      exit
      ;;
    *)
      echo $"Unrecognised option: $key"
      exit 1
  esac
done  # command line reader


# if a directory specified, read directory
list="/tmp/gedoToProcess.$$.txt"
pushd $inDir/
ls -l|grep ".metric.txt"|gawk '{printf("%s/%s\n",dir,$NF)}' dir="$inDir" > $list
popd

# clear old output
if [ -e $output ];then
  rm $output
fi

# loop over input files
temp="/tmp/workSpace.biomass.$$.txt"
while read inName; do

  python3 $bin/predictBiomass.py --input $inName --outpout $temp
  cat $temp >> $output

  if [ -e $temp ];then
    rm $temp
  fi
done  < $list

if [ -e $list ];then
  rm $list
fi

