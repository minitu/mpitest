#!/bin/bash

machine="summit"
dir="$machine-replay"

size=8

#while [ $size -le 4194304 ]
while [ $size -le 8 ]
do
  echo "Running $size"
  jsrun -n1 -a1 -c1 -K1 -r1 $HPM_PATH/codes/build/src/network-workloads/model-net-mpi-replay --sync=1 --disable_compute=0 --workload_type="dumpi" --workload_file=$HPM_PATH/mpitest/dumpi/dumpi-"$size"b- --num_net_traces=2 --lp-io-dir="$dir"/"$size"b -- $HPM_PATH/conf/$machine/replay.conf &> "$dir"/"$size"b.out
  ((size = size * 2))
done
