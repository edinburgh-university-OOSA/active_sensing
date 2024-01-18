#!/bin/csh -f

set inList="gedi/l1b/subset.GEDI01_B_2019135115649_O02386_T01720_02_003_01.h5 gedi/l1b/subset.GEDI01_B_2019183100636_O03130_T05189_02_003_01.h5 gedi/l1b/subset.GEDI01_B_2019223180803_O03756_T03613_02_003_01.h5 gedi/l1b/subset.GEDI01_B_2019242104318_O04046_T02343_02_003_01.h5 gedi/l1b/subset.GEDI01_B_2019256115713_O04264_T03143_02_003_01.h5"


foreach file( $inList )
  set root=`echo $file:r|gawk -F/ '{print $NF}'`
  set output="correl.$root.txt"

  if( ! -e $output )then
    touch $output 
    collocateWaves -listAls alsList.txt -gedi $file -lEPSG 4326 -aEPSG 32611 -solveCofG -readHDFgedi -step 2 -maxShift 20 -vStep 0.5 -maxVshift 3 -output $output -minSense 0.8
  endif
end

