#!/bin/bash

echo "Compiling test files..."
g++ -DUNIT_TEST -I./lib/unity -I./lib -I./ESP32 -I./tests -o Tests/testRunner Tests/Tests.cpp ESP32/SensorUtils.cpp lib/unity/unity.c lib/ArduinoMock.cpp


if [ $? -ne 0 ]; then
  echo "Compilation failed!"
  exit 1
fi

echo "Running tests..."
./Tests/testRunner

if [ $? -eq 0 ]; then
  echo "All tests passed!"
else
  echo "Some tests failed."
  exit 1
fi

echo "Cleaning up..."
rm -rf Tests/testRunner

echo "Done."
