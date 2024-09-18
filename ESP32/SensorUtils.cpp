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