#!/bin/bash -e 

esptool.py --chip esp32 --port "/dev/cu.usbserial-0001" run || true
esptool.py --chip esp32 --port "/dev/cu.usbserial-0001" erase_flash
esptool.py --chip esp32 --port "/dev/cu.usbserial-0001" write_flash 0x1000 firmware.bin

# Set baud rate or perform any other configurations needed
./set_esp_baud.sh
