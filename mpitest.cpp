#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <time.h>
#include <float.h>

#define USE_BARRIER 1
#define USE_SCOREP 0

#if USE_SCOREP
#include <scorep/SCOREP_User.h>
#endif

int main(int argc, char** argv) {
  // Command line arguments
  int c;
  int comm_size = 1024;
  int vector_size = 1024;
  int n_iters = 100;
  bool coll = false;
  bool nonblocking = false;

  while ((c = getopt(argc, argv, "s:v:i:cn")) != -1) {
    switch (c) {
      case 's':
        comm_size = atoi(optarg);
        break;
      case 'v':
        vector_size = atoi(optarg);
        break;
      case 'i':
        n_iters = atoi(optarg);
        break;
      case 'c':
        coll = true;
        break;
      case 'n':
        nonblocking = true;
        break;
      default:
        abort();
    }
  }

  MPI_Init(NULL, NULL);

#if USE_SCOREP
  SCOREP_RECORDING_OFF();
#endif

  int rank, world_size;
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);

  // Check if world size is even
  if (world_size % 2 != 0) {
    if (rank == 0) printf("World size should be an even number!\n");
    MPI_Abort(MPI_COMM_WORLD, MPI_ERR_OTHER);
  }

  // Check if comm size is smaller than vector size
  if (vector_size < comm_size) {
    if (rank == 0) printf("Comm size should be smaller than vector size!\n");
    MPI_Abort(MPI_COMM_WORLD, MPI_ERR_OTHER);
  }

  double* a = (double*)malloc(sizeof(double) * vector_size);
  double* b = (double*)malloc(sizeof(double) * vector_size);

  srand(time(NULL));
  for (int i = 0; i < vector_size; i++) {
    a[i] = rand() % 100;
    b[i] = rand() % 100;
  }

  double comp_time_start = 0.0;
  double comm_time_start = 0.0;
  double comp_time = 0.0;
  double comm_time = 0.0;
  double comp_time_sum = 0.0;
  double comm_time_sum = 0.0;
  double comp_time_min = DBL_MAX;
  double comm_time_min = DBL_MAX;

#if USE_SCOREP
  SCOREP_RECORDING_ON();
  SCOREP_USER_REGION_BY_NAME_BEGIN("TRACER_Loop", SCOREP_USER_REGION_TYPE_COMMON);
  if (rank == 0) {
    SCOREP_USER_REGION_BY_NAME_BEGIN("TRACER_WallTime_Total", SCOREP_USER_REGION_TYPE_COMMON);
  }
#endif

  double total_time_start = MPI_Wtime();

  for (int i = 0; i < n_iters; i++) {
    comp_time_start = MPI_Wtime();
#if USE_SCOREP
    SCOREP_USER_REGION_BY_NAME_BEGIN("TRACER_WallTime_Comp", SCOREP_USER_REGION_TYPE_COMMON);
#endif

    // Some local computation
    for (int j = 0; j < vector_size; j++) {
      a[j] = sqrt(a[j] * b[j]);
      b[j] = a[j] / 2;
    }

    comp_time = MPI_Wtime() - comp_time_start;
    comp_time_sum += comp_time;
    if (comp_time < comp_time_min) comp_time_min = comp_time;
#if USE_SCOREP
    SCOREP_USER_REGION_BY_NAME_END("TRACER_WallTime_Comp");
#endif

#if USE_BARRIER
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);
#endif

    comm_time_start = MPI_Wtime();
#if USE_SCOREP
    SCOREP_USER_REGION_BY_NAME_BEGIN("TRACER_WallTime_Comm", SCOREP_USER_REGION_TYPE_COMMON);
#endif

    // MPI communication
    int peer;
    MPI_Request reqs[2];
    if (rank < world_size / 2) {
      peer = rank + (world_size / 2);
      if (!nonblocking) {
        MPI_Recv(a, comm_size, MPI_DOUBLE, peer, 9, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Send(b, comm_size, MPI_DOUBLE, peer, 9, MPI_COMM_WORLD);
      }
      else {
        MPI_Irecv(a, comm_size, MPI_DOUBLE, peer, 9, MPI_COMM_WORLD, &reqs[0]);
        MPI_Isend(b, comm_size, MPI_DOUBLE, peer, 9, MPI_COMM_WORLD, &reqs[1]);
        MPI_Waitall(2, reqs, MPI_STATUSES_IGNORE);
      }
    }
    else {
      peer = rank - (world_size / 2);
      if (!nonblocking) {
        MPI_Send(b, comm_size, MPI_DOUBLE, peer, 9, MPI_COMM_WORLD);
        MPI_Recv(a, comm_size, MPI_DOUBLE, peer, 9, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      }
      else {
        MPI_Isend(b, comm_size, MPI_DOUBLE, peer, 9, MPI_COMM_WORLD, &reqs[0]);
        MPI_Irecv(a, comm_size, MPI_DOUBLE, peer, 9, MPI_COMM_WORLD, &reqs[1]);
        MPI_Waitall(2, reqs, MPI_STATUSES_IGNORE);
      }
    }

    comm_time = MPI_Wtime() - comm_time_start;
    comm_time_sum += comm_time;
    if (comm_time < comm_time_min) comm_time_min = comm_time;
#if USE_SCOREP
    SCOREP_USER_REGION_BY_NAME_END("TRACER_WallTime_Comm");
#endif

    /*
    printf("[%03d][rank %d] comp time: %.3lf us, comm time: %.3lf us, iter time: %.3lf\n",
        i, rank, comp_time * 1000000, comm_time * 1000000, (comp_time + comm_time) * 1000000);
        */
  }

#if USE_SCOREP
  if (rank == 0) {
    SCOREP_USER_REGION_BY_NAME_END("TRACER_WallTime_Total");
  }
  SCOREP_USER_REGION_BY_NAME_END("TRACER_Loop");
  SCOREP_RECORDING_OFF();
#endif

  printf("[Rank %d] comp time: %.3lf us, comm time: %.3lf us, total time: %.3lf us\n",
      rank, comp_time_sum / n_iters * 1000000, comm_time_sum / n_iters * 1000000,
      (MPI_Wtime() - total_time_start) * 1000000);
  /*
  printf("[Rank %d, Minimum] comp time: %.3lf us, comm time: %.3lf us, iter time: %.3lf us\n",
      rank, comp_time_min * 1000000, comm_time_min * 1000000, (comp_time_min + comm_time_min) * 1000000);
      */

  MPI_Finalize();

  return 0;
}
