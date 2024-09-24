#include "SensorUtils.h"
#include "Constants.h"

void updateSensorStatus(int buttonPin, int& buttonState, int& lastButtonState, unsigned long& lastDebounceTime, bool& sensorStatus) {
  int buttonRead = digitalRead(buttonPin);

  if (buttonRead != lastButtonState) {
    lastDebounceTime = millis();
  }

  // debounce
  if ((millis() - lastDebounceTime) > DEBOUNCE_DELAY) {
    // update state
    if (buttonRead != buttonState) {
      buttonState = buttonRead;

      // toggle if high
      if (buttonState == HIGH) {
        sensorStatus = !sensorStatus;
      }
    }
  }
  
  // update state
  lastButtonState = buttonRead;
}

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

float getTemperature(DallasTemperature sensor, const char* unit) {
  sensor.requestTemperatures();
  float temperature;
  if (strcmp(unit, "F") == 0) {
    temperature = sensor.getTempFByIndex(0);
    if (temperature == DEVICE_DISCONNECTED_F) {
      temperature = -274.00;
    }
  }
  else {
    sensor.requestTemperatures();
    temperature = sensor.getTempCByIndex(0);
    if (temperature == DEVICE_DISCONNECTED_C) {
      temperature = -274.00;
    }
  }
  delay(50);
  return temperature;
}

float convertTemperature(float temperature, const char* oldUnit, const char* newUnit) {
    if (strcmp(oldUnit, newUnit) == 0) {
        return temperature;
    } else if ((temperature == -100000.0) || (temperature == -274.0)) {
      return temperature;
    } else if (strcmp(oldUnit, "C") == 0) {
        return 32 + (temperature * 1.8);
    } else {
        return (temperature - 32) / 1.8;
    }
}