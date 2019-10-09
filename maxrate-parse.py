begin_size = 8
end_size = 4194304
iters = 3
p = 1

size = begin_size
while size <= end_size:
  input_file = "p" + str(p) + "-" + str(size) + "b.out"
  input_handle = open(input_file, "r")

  comp_time_sum = {}
  comm_time_sum = {}
  total_time_sum = {}

  for line in input_handle:
    if not line.startswith("Iter"):
      tokens = line.split(' ')
      rank = int(tokens[1].split(']')[0])
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

  max_comp_time = 0
  max_comm_time = 0

  for rank in comp_time_sum.keys():
    if (comp_time_sum[rank] / iters) > max_comp_time:
      max_comp_time = comp_time_sum[rank] / iters
    if (comm_time_sum[rank] / iters) > max_comm_time:
      max_comm_time = comm_time_sum[rank] / iters
  print("[Max, 1-way]", "comp:", round(max_comp_time, 2), "comm:", round(max_comm_time/2, 2))

  size *= 2
