#include "SensorUtils.h"
#include "Constants.h"

void checkButtonStatus(int buttonRead, bool& buttonOn, int& buttonState, int& lastButtonState, int debounceDelay, unsigned long& lastDebounceTime) {
    // Check if the button state has changed
    if (buttonRead != lastButtonState) {
        lastDebounceTime = millis(); 
    }

    if ((millis() - lastDebounceTime) > debounceDelay) {
        if (buttonRead != buttonState) {
            buttonState = buttonRead;

            // If the new button state is high toggle the button on/off state
            if (buttonState == HIGH) {
                buttonOn = !buttonOn; 
            }
        }
  }

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
      temperature = -460.00; // Absolute zero to say that it is disconnected
    }
  }
  else {
    sensor.requestTemperatures();
    temperature = sensor.getTempCByIndex(0);
    if (temperature == DEVICE_DISCONNECTED_C) {
      temperature = -274.00; // Absolute zero to say that it is disconnected
    }
  }
  delay(50);
  return temperature;
}

float convertTemperature(float temperature, const char* oldUnit, const char* newUnit) {
    if (strcmp(oldUnit, newUnit) == 0) {
        return temperature;
    } else if (strcmp(oldUnit, "C") == 0) {
        return 32 + (temperature * 1.8);
    } else {
        return (temperature - 32) / 1.8;
    }
}