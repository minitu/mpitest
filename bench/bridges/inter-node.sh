#!/bin/bash
#SBATCH -p GPU
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=32
#SBATCH --gres=gpu:p100:2
#SBATCH --time=00:30:00
#SBATCH --job-name=maxrate

date

cd /home/jchoi157/mpitest

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
    export I_MPI_JOB_RESPECT_PROCESS_PLACEMENT=0
    mpiexec -print-rank-map -n 4 -ppn 2 -genv I_MPI_DEBUG=5 ./mpitest -s $size -v $vector_size -i 1000 >> "$bytes"b.out
    ((iter = iter + 1))
  done
  ((size = size * 2))
done
