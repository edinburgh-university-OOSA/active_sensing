#!/bin/csh -f

set bin="$HOME/src/gediRat"
set list=`ls GEDI04_A*.h5|gawk '{for(i=1;i<=NF;i++)print $1}'`

set minX=-123.77
set minY=33.16
set maxX=-117.96
set maxY=39.71


foreach file( $list )
  set output="subset.$file"

  if( ! -e $output )then
    touch $output
    python3 $bin/subsetGEDI.py --input $file --bounds $minX $minY $maxX $maxY --output $output
  endif
end

