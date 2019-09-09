#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <time.h>

#define USE_SCOREP 1

#if USE_SCOREP
#include <scorep/SCOREP_User.h>
#endif

int main(int argc, char** argv) {
  // Command line arguments
  int c;
  int comm_size = 8;
  int vector_size = 4 * 1024; // 4K elements
  int n_iters = 100;
  bool coll = false;

  while ((c = getopt(argc, argv, "s:v:i:c")) != -1) {
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

#if USE_SCOREP
  SCOREP_RECORDING_ON();
  SCOREP_USER_REGION_BY_NAME_BEGIN("TRACER_Loop", SCOREP_USER_REGION_TYPE_COMMON);
  if (rank == 0) {
    SCOREP_USER_REGION_BY_NAME_BEGIN("TRACER_WallTime_Total", SCOREP_USER_REGION_TYPE_COMMON);
  }
#endif

  for (int i = 0; i < n_iters; i++) {
    comp_time_start = MPI_Wtime();

    // Some local computation
    for (int j = 0; j < vector_size; j++) {
      a[i] = sqrt(a[i] * b[i]);
      b[i] = a[i] / 2;
    }

    comp_time += MPI_Wtime() - comp_time_start;

    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);

    comm_time_start = MPI_Wtime();

    // MPI communication
    int peer;
    if (rank < world_size / 2) {
      peer = rank + (world_size / 2);
      MPI_Recv(a, comm_size, MPI_DOUBLE, peer, 9, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      MPI_Send(b, comm_size, MPI_DOUBLE, peer, 9, MPI_COMM_WORLD);
    }
    else {
      peer = rank - (world_size / 2);
      MPI_Send(b, comm_size, MPI_DOUBLE, peer, 9, MPI_COMM_WORLD);
      MPI_Recv(a, comm_size, MPI_DOUBLE, peer, 9, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }

    comm_time += MPI_Wtime() - comm_time_start;
  }

#if USE_SCOREP
  if (rank == 0) {
    SCOREP_USER_REGION_BY_NAME_END("TRACER_WallTime_Total");
  }
  SCOREP_USER_REGION_BY_NAME_END("TRACER_Loop");
  SCOREP_RECORDING_OFF();
#endif

  printf("[Rank %d] comp time: %.3lf us, comm time: %.3lf us\n", rank, comp_time / n_iters * 10e6, comm_time / n_iters * 10e6);

  MPI_Finalize();

  return 0;
}
