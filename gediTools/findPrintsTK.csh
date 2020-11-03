#/bin/csh -f

set bin="$HOME/wordybits/auldreekie/20.03.01.davos/gedi_tracks/scripts/find_prints"
set dirRoot="/gpfs/data1/vclgp/data/iss_gedi/soc"
set yearList="2019 2020"

set list="/tmp/trackList.$$.dat"

set output="gediTracksTK.dat"
if( -e $output )rm $output

set minY=36.9488
set maxY=36.9871
set minX=-119.0967
set maxX=-119.0

foreach year( $yearList )
  # list dates
  set yDir="$dirRoot/$year"

  pushd $yDir/
  ls */GEDI01_B*01.h5|sed -e s%\*%""% |gawk '{for(i=1;i<=NF;i++)printf("%s/%s\n",dir,$i)}' dir="$yDir" > $list
  popd

  python3 $bin/findPrints.py --inList $list --output $output --minX $minX --maxX $maxX --minY $minY --maxY $maxY

  if( -e $list )rm $list
end



