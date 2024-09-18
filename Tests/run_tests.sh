#!/bin/bash

# Compile the test files along with SensorUtils.cpp and define UNIT_TEST for testing
echo "Compiling test files..."
g++ -DUNIT_TEST -I./lib/unity -I./lib -I./ESP32 -I./tests -o tests/testRunner Tests/Tests.cpp ESP32/SensorUtils.cpp lib/unity/unity.c lib/ArduinoMock.cpp

# Check if compilation succeeded
if [ $? -ne 0 ]; then
  echo "Compilation failed!"
  exit 1
fi

# Run the tests
echo "Running tests..."
./tests/testRunner

# Check if tests succeeded
if [ $? -eq 0 ]; then
  echo "All tests passed!"
else
  echo "Some tests failed."
  exit 1
fi

# Clean up the test runner executable
echo "Cleaning up..."
rm -rf Tests/testRunner

echo "Done."
