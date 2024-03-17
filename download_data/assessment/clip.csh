#!/bin/csh -f

set inDir="/Users/dougal/data/teaching/active_sensing/assessment/laz"
set outDir="/Users/dougal/data/teaching/active_sensing/assessment/clipped"
set list="/tmp/alsRaw.tellus_sw.txt"

set minX=406000 
set minY=560000
set maxX=412000 
set maxY=5605000


pushd $inDir/
ls *laz|gawk '{for(i=1;i<=NF;i++)printf("%s/%s\n",dir,$i)}' dir=$inDir > $list
popd

if( ! -e $outDir )mkdir $outDir/

@ nFiles=`wc -l < $list`
@ i=1
while( $i <= $nFiles )
  set file=`gawk -v i=$i '{if(NR==i)print $1}'` < $list
  set output=`echo $file|sed -e s%$inDir%$outDir%`

  wine64 $LASTOOLS/laszip.exe -i $file -o $output -keep_xy $minX $minY $maxX $maxY

  @ i++
end

if( -e $list )rm $list

