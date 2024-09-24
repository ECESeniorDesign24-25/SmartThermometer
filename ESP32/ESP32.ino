#include <WiFi.h>
#include <ESPmDNS.h>
#include <string>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <LiquidCrystal.h>
#include "SensorUtils.h"
#include "Constants.h"

const char* ssid = WIFI_USERNAME;
const char* password = WIFI_PASSWORD;

float temp1 = 0;
float temp2 = 0;

bool button1On = false;
bool button2On = false;

int button1State = LOW;
int button2State = LOW;

int lastButton1State = LOW;
int lastButton2State = LOW;

unsigned long lastButton1DebounceTime = 0;
unsigned long lastButton2DebounceTime = 0;

unsigned long debounceDelay = 50;

// setup temperature sensors
OneWire oneWire1(TEMP1_SENSOR_PIN);
OneWire oneWire2(TEMP2_SENSOR_PIN);

DallasTemperature sensor1(&oneWire1);
DallasTemperature sensor2(&oneWire2);

AsyncWebServer server(80);
LiquidCrystal lcd(RS, ENABLE, D4, D5, D6, D7);

std::string unit = "C";

void setup() {
  pinMode(TEMP1_BUTTON_PIN, INPUT);
  pinMode(TEMP2_BUTTON_PIN, INPUT);
  pinMode(TEMP1_SENSOR_PIN, INPUT);
  pinMode(TEMP2_SENSOR_PIN, INPUT);

  sensor1.begin();
  sensor1.setResolution(11);

  sensor2.begin();
  sensor2.setResolution(11);

  Serial.begin(115200);
  Serial.println("Initialized serial.");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.printf("Connected to WiFi with IP Address: %s\n", WiFi.localIP().toString().c_str());

  if (!MDNS.begin("esp32")) {
    Serial.println("Error setting up MDNS.");
    while (1) {
      delay(1000);
    }
  }
  Serial.println("mDNS started. Access with http://esp32.local");

  server.on("/temperature1", HTTP_GET, [](AsyncWebServerRequest* request) {
    Serial.println("Received request for temperature 1.");
    std::string newUnit = unit;
    if (request->hasParam("unit")) {
      newUnit = request->getParam("unit")->value().c_str();
    }
    temp1 = convertTemperature(temp1, unit, newUnit);
    unit = newUnit;
    request->send(200, "text/plain", String(temp1));
  });

  server.on("/temperature2", HTTP_GET, [](AsyncWebServerRequest* request) {
    Serial.println("Received request for temperature 2.");
    std::string newUnit = unit;
    if (request->hasParam("unit")) {
      newUnit = request->getParam("unit")->value().c_str();
    }
    temp2 = convertTemperature(temp2, unit, newUnit);
    unit = newUnit;
    request->send(200, "text/plain", String(temp2));
  });

  server.on("/toggle1", HTTP_POST, [](AsyncWebServerRequest* request) {
    button1On = !button1On;
    request->send(200, "text/plain", "Button 1 toggled.");
  });

  server.on("/toggle2", HTTP_POST, [](AsyncWebServerRequest* request) {
    button2On = !button2On;
    request->send(200, "text/plain", "Button 2 toggled.");
  });

  server.begin();
  Serial.println("Server started.");

  lcd.begin(16, 2);
  pinMode(TEMP1_BUTTON_PIN, INPUT);
  pinMode(TEMP2_BUTTON_PIN, INPUT);
  lcd.setCursor(1, 0);
  lcd.print("Sensor 1 OFF");
  lcd.setCursor(1, 1);
  lcd.print("Sensor 2 OFF");
}

void loop() {}
