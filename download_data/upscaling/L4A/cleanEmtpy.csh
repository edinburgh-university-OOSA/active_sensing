#!/bin/csh -f

set list=`ls -l small.*.h5|gawk '{if($5<900)print $NF}'`
rm $list

