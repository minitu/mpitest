#!/bin/bash

top_dir="summit-maxrate"
replay_dir="."
size=8
while [ $size -le 4194304 ]
#while [ $size -le 8 ]
do
  echo "Running $size"
  jsrun -n1 -a1 -c1 -g1 -K1 -r1 $HOME/work/codes-dumpi/build/src/network-workloads/model-net-mpi-replay --sync=1 --disable_compute=0 --workload_type="dumpi" --workload_file=/ccs/home/jchoi/work/mpitest/tracer/dumpi-"$size"b/dumpi-"$size"b- --num_net_traces=2 --lp-io-dir="$top_dir/$replay_dir/$size"b -- "$top_dir/$replay_dir"/summit-replay.conf &> "$top_dir/$replay_dir/$size"b.out
  ((size = size * 2))
done
