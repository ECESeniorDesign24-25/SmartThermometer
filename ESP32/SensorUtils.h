#ifndef SENSOR_UTILS_H
#define SENSOR_UTILS_H

#ifdef UNIT_TEST
  #include "../lib/ArduinoMock.h" 
  #include "../lib/DallasTemperatureMock.h" 
  #include "../lib/OneWireMock.h"
  #include <cstring>
#else
  #include <Arduino.h>
  #include <DallasTemperature.h>
  #include <OneWire.h>
#endif

float calculateTemperature(bool buttonStatus, int temp);
float getTemperature(DallasTemperature sensor, String unit, bool sensorState);
float convertTemperature(float temperature, String oldUnit, String newUnit);
#endif