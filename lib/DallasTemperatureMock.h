#define DEVICE_DISCONNECTED_F -460.0
#define DEVICE_DISCONNECTED_C -274.0

typedef struct DallasTemperature {
    void requestTemperatures() {}
    float getTempFByIndex(int index) { return 0; }
    float getTempCByIndex(int index) { return 0; }
} DallasTemperature;