#!/bin/csh -f

set bin="$HOME/src/gediRat"
set list=`ls GEDI04_A*.h5|gawk '{for(i=1;i<=NF;i++)print $1}'`

set minX=-120
set minY=36
set maxX=-118
set maxY=39


foreach file( $list )
  set output="small.$file"

  if( ! -e $output )then
    touch $output
    python3 $bin/subsetGEDI.py --input $file --bounds $minX $minY $maxX $maxY --output $output
  endif
end

