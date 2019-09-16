#!/bin/bash

iters=10
size=1
end_size=524288

while [ $size -le $end_size ]
do
  bytes=8*$size
  echo "Running $size ($bytes bytes)"
  iter=1
  while [ $iter -le $iters ]
  do
    echo "Iter $iter" >> "$bytes"b.out
    jsrun -n2 -a1 -c1 -g1 -K1 -r1 ./mpitest -s $size >> "$bytes"b.out
    ((iter = iter + 1))
  done
  ((size = size * 2))
done
