begin_size = 8
end_size = 4194304
iters = 10

size = begin_size
while size <= end_size:
  input_file = str(size) + "b.out"
  input_handle = open(input_file, "r")

  comp_time_sum = {}
  comm_time_sum = {}
  total_time_sum = {}

  for line in input_handle:
    if not line.startswith("Iter"):
      tokens = line.split(' ')
      rank = int((tokens[1])[0])
      comp_time = float(tokens[4])
      comm_time = float(tokens[8])
      total_time = float(tokens[12])
      if rank not in comp_time_sum:
        comp_time_sum[rank] = 0
      comp_time_sum[rank] += comp_time
      if rank not in comm_time_sum:
        comm_time_sum[rank] = 0
      comm_time_sum[rank] += comm_time
      if rank not in total_time_sum:
        total_time_sum[rank] = 0
      total_time_sum[rank] += total_time

  print("Size", size)
  for rank in comp_time_sum.keys():
    print("[Rank", str(rank) + "]", "comp:", comp_time_sum[rank] / iters, "comm:", comm_time_sum[rank] / iters)

  size *= 2
