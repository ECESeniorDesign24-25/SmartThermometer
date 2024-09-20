#!/bin/bash

PORT="/dev/cu.usbserial-0001"
DEFAULT_BAUD=115200
BAUD=${1:-$DEFAULT_BAUD}
echo "Using port: $PORT"
echo "Using baud rate: $BAUD"
esptool.py --port "$PORT" --baud "$BAUD" flash_id

