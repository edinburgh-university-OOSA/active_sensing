#!/bin/csh -f

set list="list.txt"

@ nFiles=`wc -l` < $list
@ i=1
while( $i <= $nFiles )
  set file=`gawk -v i=$i '{if(i==NR)print $1}'` < $list
  set root=`echo $file|gawk -F/ '{print $NF}'`

  if( ! -e $root )then
    wget --user stevenhancock --password $file
  endif

  @ i++
end

