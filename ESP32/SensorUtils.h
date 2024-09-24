#ifndef SENSOR_UTILS_H
#define SENSOR_UTILS_H

#ifdef UNIT_TEST
  #include "../lib/ArduinoMock.h" 
  #include "../lib/DallasTemperatureMock.h" 
  #include "../lib/OneWireMock.h"
#else
  #include <Arduino.h>
  #include <DallasTemperature.h>
  #include <OneWire.h>
#endif

void updateSensorStatus(int buttonPin, int& buttonState, int& lastButtonState, unsigned long& lastDebounceTime, bool& sensorStatus);
float calculateTemperature(bool buttonStatus, int temp);
float getTemperature(DallasTemperature sensor, const char* unit);
float convertTemperature(float temperature, const char* oldUnit, const char* newUnit);
#endif