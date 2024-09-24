#ifndef SENSOR_UTILS_H
#define SENSOR_UTILS_H
#include <cstring>

#ifdef UNIT_TEST
  #include "../lib/ArduinoMock.h" 
  #include "../lib/DallasTemperatureMock.h" 
  #include "../lib/OneWireMock.h"
#else
  #include <Arduino.h>
  #include <DallasTemperature.h>
  #include <OneWire.h>
#endif

void checkButtonStatus(int buttonRead, bool& buttonOn, int& buttonState, int& lastButtonState, int debounceDelay, unsigned long& lastDebounceTime);
float calculateTemperature(bool buttonStatus, int temp);
float getTemperature(DallasTemperature sensor, const char* unit);
float convertTemperature(float temperature, const char* oldUnit, const char* newUnit);
#endif