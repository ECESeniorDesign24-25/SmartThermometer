#include "../lib/ArduinoMock.h"
#include "../lib/unity/unity.h"
#include "../ESP32/SensorUtils.h"
#include "ESPTests.h"

// Test temperature calculation
void testCalculateTemperature() {

    // check C -> C
    TEST_ASSERT_EQUAL_FLOAT(100.0, convertTemperature(100.0, "C", "C")); 

    // check F -> F
    TEST_ASSERT_EQUAL_FLOAT(100.0, convertTemperature(100.0, "F", "F"));

    // check C -> F
    TEST_ASSERT_EQUAL_FLOAT(212.0, convertTemperature(100.0, "C", "F"));

    // check F -> C
    TEST_ASSERT_EQUAL_FLOAT(37.777779, convertTemperature(100.0, "F", "C"));
}


void setUp(void) {}

void tearDown(void) {}

int main(int argc, char **argv) {
    UNITY_BEGIN();
    // RUN_TEST(testButtonTogglesOnOff);
    RUN_TEST(testCalculateTemperature);
    return UNITY_END();
}