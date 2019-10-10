#!/bin/bash

iters=5
size=1
end_size=524288

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
    echo "Iter $iter" >> "$bytes"b.out
    #export I_MPI_EAGER_THRESHOLD=65536
    mpiexec -n 2 -ppn 1 -host gpu017,gpu019 ../../mpitest -s $size -v $vector_size -i 100 >> "$bytes"b.out
    ((iter = iter + 1))
  done
  ((size = size * 2))
done
