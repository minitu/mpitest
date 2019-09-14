import getopt, sys

arg_list = sys.argv[1:]
unix_options = "i:"
gnu_options = ["input="]

try:
  args, vals = getopt.getopt(arg_list, unix_options, gnu_options)
except getopt.error as err:
  print(str(err))
  sys.exit(2)

for arg, val in args:
  if arg in ("-i", "--input"):
    input_file = val

#output_file = input_file.split('.')[0] + ".avg"

comm_start_time = {}
comp_start_time = {}
comm_time_sum = {}
comm_time_count = {}
comp_time_sum = {}
comp_time_count = {}

input_handle = open(input_file, "r")
for line in input_handle:
  if line.startswith("[ 0 "):
    tokens = line.split(' ')
    rank = int(tokens[2])
    time = float(tokens[-2])
    which = tokens[4]
    if which == "Begin":
      walltime_type = tokens[5]
      if walltime_type.endswith("Comm"):
        comm_start_time[rank] = time
      elif walltime_type.endswith("Comp"):
        comp_start_time[rank] = time
    elif which == "End":
      walltime_type = tokens[5]
      if walltime_type.endswith("Comm"):
        if rank not in comm_time_sum:
          comm_time_sum[rank] = 0
        comm_time_sum[rank] += time - comm_start_time[rank]
        if rank not in comm_time_count:
          comm_time_count[rank] = 0
        comm_time_count[rank] += 1
      elif walltime_type.endswith("Comp"):
        if rank not in comp_time_sum:
          comp_time_sum[rank] = 0
        comp_time_sum[rank] += time - comp_start_time[rank]
        if rank not in comp_time_count:
          comp_time_count[rank] = 0
        comp_time_count[rank] += 1

for rank in comp_time_sum.keys():
  print("[Rank", str(rank) + "]", "comp:", round(comp_time_sum[rank] / comp_time_count[rank] * 1000000, 2), "comm:", round(comm_time_sum[rank] / comm_time_count[rank] * 1000000, 2))
