#include "ArduinoMock.h"

unsigned long millis() {
    return 0;
}

void delay(unsigned long) {
    return;
}
