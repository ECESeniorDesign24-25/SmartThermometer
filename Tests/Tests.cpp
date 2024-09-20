#include "../lib/ArduinoMock.h"
#include "../lib/unity/unity.h"
#include "../ESP32/SensorUtils.h"
#include "Tests.h"

// Test temperature calculation
void testCalculateTemperature() {

    // check C -> C
    TEST_ASSERT_EQUAL_FLOAT(100.0, convertTemperature(100.0, "c", "c")); 

    // check F -> F
    TEST_ASSERT_EQUAL_FLOAT(100.0, convertTemperature(100.0, "f", "f"));

    // check C -> F
    TEST_ASSERT_EQUAL_FLOAT(212.0, convertTemperature(100.0, "c", "f"));

    // check F -> C
    TEST_ASSERT_EQUAL_FLOAT(37.777779, convertTemperature(100.0, "f", "c"));
}


void setUp(void) {}

void tearDown(void) {}

int main(int argc, char **argv) {
    UNITY_BEGIN();
    // RUN_TEST(testButtonTogglesOnOff);
    RUN_TEST(testCalculateTemperature);
    return UNITY_END();
}