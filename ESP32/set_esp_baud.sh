#!/bin/bash

# Default values
PORT="/dev/cu.usbserial-0001"
DEFAULT_BAUD=115200

# Check if a baud rate argument was provided, otherwise use the default
BAUD=${1:-$DEFAULT_BAUD}

# Display the command being run
echo "Using port: $PORT"
echo "Using baud rate: $BAUD"

# Run the esptool.py command with the specified or default baud rate
esptool.py --port "$PORT" --baud "$BAUD" flash_id

