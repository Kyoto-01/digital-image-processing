CC = g++

OBJS = main.cpp

CFLAGS = -Wall `pkg-config --cflags opencv4`
LIBS = `pkg-config --libs opencv4`
OBJ_NAME = main.o

all: $(objs)
	$(CC) $(OBJS) $(FLAGS) -o $(OBJ_NAME) $(CFLAGS) $(LIBS)

clean:
	rm -f $(OBJ_NAME)
