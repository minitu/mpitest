#!/bin/bash

dir="summit-1"
size=8
while [ $size -le 4194304 ]
do
  echo "Running $size"
  jsrun -n6 -a1 -g1 -c1 -K3 -r6 -d packed ~/TraceR/tracer/traceR --sync=3 --nkp=16 --extramem=100000 --max-opt-lookahead=1000000 --timer-frequency=1000 --lp-io-dir="$dir/$size"b -- "$dir"/summit.conf tracer_config scorep-"$size"b/traces.otf2 > "$dir/$size"b.out
  ((size = size * 2))
done
