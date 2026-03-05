#!/bin/csh -f

set list="/tmp/emptyList.$$.dat"
ls -l *.laz|gawk '{if($5<500)print $NF}' > $list

@ nFiles=`wc -l` < $list
@ i=1
while( $i <= $nFiles )

  set file=`gawk -v i=$i '{if(i==NR)print $0}'` < $list

  echo $file
  rm $file

  @ i++
end

if( -e $list )rm $list
