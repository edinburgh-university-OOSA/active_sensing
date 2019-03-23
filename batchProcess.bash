#!/bin/bash -f


#################
# Batch process #
# GEDI data     #
#################


# defaults
bounds=" "
readDir=1
inDir="/geos/netdata/avtrain/data/3d/active_sensing/week10/gedi_sonoma"
outRoot="test"

# Read the command line
while [[ $# -gt 0 ]]
do
key="$1"
  case $key in
    -input)
      input="$2"
      readDir=0
      shift;shift
      ;;
    -inDir)
      inDir="$2"
      readDir=1
      shift;shift 
      ;;
    -bounds)
      bounds="-bounds $2 $3 $4 $5"
      shift;shift;shift;shift;shift
      ;;
    -varScale)
      varScale="-varScale $2"
      shift;shift 
      ;;
    -statsLen)
      statsLen="-statsLen $2"
      shift;shift
      ;;
    -noiseTrack)
      noiseTrack="-noiseTrack"
      shift
      ;;
    -sWidth)
      sWidth="-sWidth $2"
      shift;shift
      ;;
    -psWidth)
      psWidth="-psWidth $2"
      shift;shift
      ;;
    -msWidth)
      msWidth="-msWidth $2"
      shift;shift
      ;;
    -gWidth)
      gWidth="-gWidth $2"
      shift;shift
      ;;
    -minGsig)
      minGsig="-minGsig $2"
      shift;shift
      ;;
   -minWidth)
      minWidth="-minWidth $2"
      shift;shift
      ;;
    -help)
      echo " "
      echo "Batch processing of GEDI data"
      echo " "
      echo "### I/0 ###" 
      echo "-inDir name;                  directory name to process all HDF5 files within"
      echo "-input name;                  input filename for single file"
      echo "-outRoot name;                output filename root"
      echo "-bounds minX minY maxX maxY;  define bounds"
      echo " "
      echo "### Denoising options ###" 
      echo "-varScale nStdev;             number of standard deviations to use for noise threshold"
      echo "-minWidth N;                  minimum number of bins above threshold to accept"
      echo "-statsLen len;                length to calculate waveform stats over (20 m by default)"
      echo "-noiseTrack;                  track back to mean noise level"
      echo "-sWidth sigma;                smoothing width (after mean background removal)"
      echo "-psWidth sigma;               smoothing width (before noise statistics calculation)"
      echo "-msWidth sigma;               smoothing width (after statistics, before background removal)"
      echo "-gWidth sigma;                smoothing width for Gaussian fitting initial estimates"
      echo "-minGsig sigma;               minimum width of Gaussians to allow"
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
if [ $readDir == 1 ]; then
  pushd $inDir/
  ls -l|grep ".h5"|gawk '{printf("%s/%s\n",dir,$NF)}' dir="$inDir" > $list
  popd
else   # otherwise write input to list
  echo "$input" > $list
fi


# loop over input files
while read inName; do
  root=`echo $inName|gawk -F/ '{print $NF}'`
  output="$outRoot.$root"
  gediMetric -input $inName -readHDFgedi $bounds -ground $varScale $statsLen $noiseTrack $sWidth $psWidth $msWidth $gWidth $minGsig $minWidth -outRoot $output -varNoise -rhRes 5
done  < $list

if [ -e $list ];then
  rm $list
fi

