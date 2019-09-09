TARGET=mpitest
CC=g++ -I$(SCOREP_DIR)/include -DSCOREP_USER_ENABLE
LD=scorep --user --nocompiler --noopenmp --nopomp --nocuda --noopenacc --noopencl --nomemory $(CC)
#CC=xlc++_r

all: $(TARGET)

$(TARGET): $(TARGET).o
	$(LD) -pthread -o $@ $^ -L$(MPI_ROOT)/lib -lmpi_ibm

$(TARGET).o: $(TARGET).cpp
	$(CC) -pthread -c $<

clean:
	rm -rf $(TARGET) *.o
