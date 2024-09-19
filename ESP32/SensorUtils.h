#ifndef SENSOR_UTILS_H
#define SENSOR_UTILS_H

#ifdef UNIT_TEST
  #include "../lib/ArduinoMock.h"  // For testing
#else
  #include <Arduino.h>
#endif

void checkButtonStatus(int buttonRead, bool& buttonOn, int& buttonState, int& lastButtonState, int debounceDelay, unsigned long& lastDebounceTime);
float calculateTemperature(bool buttonStatus, int temp);

#endif