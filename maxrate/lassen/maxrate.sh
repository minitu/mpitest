#!/bin/bash

iters=3
p=1
p_end=10
size=1
end_size=524288

while [ $p -le $p_end ]
do
  echo "Running $p process pairs"
  size=1
  while [ $size -le $end_size ]
  do
    bytes=$((8*$size))
    echo "Running $size ($bytes bytes)"
    iter=1
    vector_size=1024
    if [ $size -gt 1024 ]
    then
      vector_size=$size
    fi
    while [ $iter -le $iters ]
    do
      echo "Iter $iter" >> p"$p"-"$bytes"b.out
      jsrun --erf_input maxrate-maps/lassen/map-inter-node-"$p".txt ./mpitest -s $size -v $vector_size -i 1000 >> p"$p"-"$bytes"b.out
      ((iter = iter + 1))
    done
    ((size = size * 2))
  done
  ((p = p + 1))
done
