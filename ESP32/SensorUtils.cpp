#include "SensorUtils.h"
#include "Constants.h"

float calculateTemperature(bool buttonStatus, int temp) {
    if (buttonStatus) {
      if (temp < MIN_TEMP) {
        temp = MIN_TEMP;
      }
      else if (temp > MAX_TEMP) {
        temp = MAX_TEMP;
      }
    }
    else {
      temp = -274; // Absolute zero to say that it is off
    }
    return temp;
}

float getTemperature(DallasTemperature sensor, String unit, bool sensorState) {
  float temperature;
  // if off
  if (!sensorState) {
    return SENSOR_OFF_TEMP;
  }
  else {
    sensor.requestTemperatures();
    // check unit
    if (unit == "F") {
      temperature = sensor.getTempFByIndex(0);

      // if disconnected
      if (temperature == DEVICE_DISCONNECTED_F) {
        temperature = SENSOR_DISCONNECT_TEMP;
      }
    }
    else {
      temperature = sensor.getTempCByIndex(0);

      // if disconnected
      if (temperature == DEVICE_DISCONNECTED_C) {
        temperature = SENSOR_DISCONNECT_TEMP;
      }
    }
  }
  return temperature;
}

float convertTemperature(float temperature, String oldUnit, String newUnit) {

    // if no unit change or fail condition
    if (oldUnit == newUnit || temperature == SENSOR_OFF_TEMP || temperature == SENSOR_DISCONNECT_TEMP) {
        return temperature;
    }
    else if (oldUnit == "C") {
        return 32 + (temperature * 1.8);
    } 
    else {
        return (temperature - 32) / 1.8;
    }
}