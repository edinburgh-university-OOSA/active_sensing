#!/bin/csh -f


set dir="/Users/dougal/data/teast/tellus/las"
set list="/Users/dougal/data/teast/tellus/alsRaw.tellus_sw.txt"

pushd $dir/
ls *las|gawk '{for(i=1;i<=NF;i++)printf("%s/%s\n",dir,$i)}' dir=$dir > $list
popd

echo "Written to $list"

