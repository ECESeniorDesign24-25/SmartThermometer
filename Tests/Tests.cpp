#include "../lib/ArduinoMock.h"
#include "../lib/unity/unity.h"
#include "../ESP32/SensorUtils.h"
#include "Tests.h"

// Test button toggling on and off
void testButtonTogglesOnOff() {
    bool buttonOn = false;
    int buttonPin = 2;
    int lastButtonState = LOW;
    int buttonState = LOW;
    unsigned long lastDebounceTime = 0;
    unsigned long debounceDelay = 50;
    int buttonRead = HIGH;
    checkButtonStatus(buttonRead, buttonOn, buttonState, lastButtonState, debounceDelay, lastDebounceTime);
    TEST_ASSERT_EQUAL_INT(0, buttonOn);

    buttonRead = LOW;
    lastDebounceTime += 100;
    checkButtonStatus(buttonRead, buttonOn, buttonState, lastButtonState, debounceDelay, lastDebounceTime);
    TEST_ASSERT_EQUAL_INT(1, buttonOn);
}

// Test temperature calculation
void testCalculateTemperature() {

    // check C -> C
    TEST_ASSERT_EQUAL_FLOAT(100.0, convertTemperature(100.0, "c", "c")); 
}


void setUp(void) {}

void tearDown(void) {}

int main(int argc, char **argv) {
    UNITY_BEGIN();
    // RUN_TEST(testButtonTogglesOnOff);
    RUN_TEST(testCalculateTemperature);
    return UNITY_END();
}