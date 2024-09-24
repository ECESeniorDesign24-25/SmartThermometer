#!/bin/bash

echo "Compiling ESP test files..."
g++ -DUNIT_TEST -I./lib/unity -I./lib -I./ESP32 -I./tests -o Tests/testRunner Tests/ESPTests.cpp ESP32/SensorUtils.cpp lib/unity/unity.c lib/ArduinoMock.cpp


if [ $? -ne 0 ]; then
  echo "Compilation failed!"
  exit 1
fi

echo "Running ESP tests..."
./Tests/testRunner

if [ $? -eq 0 ]; then
  echo "All ESP tests passed!"
else
  echo "Some ESP tests failed."
  exit 1
fi

echo "Running Client tests..."
python3 Tests/ClientTests.py
if [ $? -eq 0 ]; then
  echo "All Client tests passed!"
else
  echo "Some Client tests failed."
  exit 1
fi

echo "Cleaning up..."
rm -rf Tests/testRunner

echo "Done."
