#!/bin/bash -e

green='\033[0;32m'
red='\033[0;31m'
clear='\033[0m'

echo "Running Client tests..."
python3 Tests/ClientTests.py
if [ $? -eq 0 ]; then
  printf "${green}All Client tests passed!${clear}\n"
else
  printf "${red}Some Client tests failed.${clear}\n"
  exit 1
fi