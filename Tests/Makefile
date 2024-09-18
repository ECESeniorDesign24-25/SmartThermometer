CC=g++
CFLAGS=-I../lib/unity -I../lib -I../ESP32 -I../include
SRCS=tests.cpp ../lib/unity/unity.c
TARGET=testRunner

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRCS)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)