TARGET=mpitest
CC=mpicxx
#CC=g++ -I$(MPI_ROOT)/include -I$(SCOREP_DIR)/include -DSCOREP_USER_ENABLE
LD=mpicxx
#LD=scorep --user --nocompiler --noopenmp --nopomp --nocuda --noopenacc --noopencl --nomemory $(CC)

all: $(TARGET)

$(TARGET): $(TARGET).o
	$(LD) -o $@ $^

$(TARGET).o: $(TARGET).cpp
	$(CC) -c $<

clean:
	rm -rf $(TARGET) *.o
