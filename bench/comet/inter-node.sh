#!/bin/bash
#SBATCH -p gpu
#SBATCH --gres=gpu:p100:4
#SBATCH --ntasks-per-node=28
#SBATCH --nodes=2
#SBATCH --job-name="mpitest-p100"
#SBATCH -t 00:00:30

date

cd /home/jchoi157/mpitest/bench/comet

iters=10
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
    mpiexec -N 1 ../../mpitest -s $size -v $vector_size -i 1000 >> "$bytes"b.out
    ((iter = iter + 1))
  done
  ((size = size * 2))
done
