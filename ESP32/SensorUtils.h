#ifndef SENSOR_UTILS_H
#define SENSOR_UTILS_H

#include <DallasTemperature.h>
#include <OneWire.h>
#include <string>

#ifdef UNIT_TEST
  #include "../lib/ArduinoMock.h"  // For testing
#else
  #include <Arduino.h>
#endif

void checkButtonStatus(int buttonRead, bool& buttonOn, int& buttonState, int& lastButtonState, int debounceDelay, unsigned long& lastDebounceTime);
float calculateTemperature(bool buttonStatus, int temp);
float getTemperature(DallasTemperature sensor, String unit);
float convertTemperature(float temperature, String oldUnit, String newUnit);
#endif