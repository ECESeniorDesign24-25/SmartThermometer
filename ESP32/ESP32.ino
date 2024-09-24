#include <WiFi.h>
#include <ESPmDNS.h>
#include <string>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <LiquidCrystal.h>
#include "SensorUtils.h"
#include "Constants.h"

const char* ssid PROGMEM = WIFI_USERNAME;
const char* password PROGMEM = WIFI_PASSWORD;

float temp1 = 0.0;
float temp2 = 0.0;
char unit[2] = "C"; // default to celsius, make length 2 so we can null terminate

bool temp1Enabled = true;
bool temp2Enabled = true;

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

void setup() {
  pinMode(TEMP1_BUTTON_PIN, INPUT);
  pinMode(TEMP2_BUTTON_PIN, INPUT);
  pinMode(TEMP1_SENSOR_PIN, INPUT);
  pinMode(TEMP2_SENSOR_PIN, INPUT);

  sensor1.begin();
  sensor1.setResolution(9); // use lowest precision for faster measurements

  sensor2.begin();
  sensor2.setResolution(9);

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
    if (request->hasParam("unit")) {
      String newUnit = request->getParam("unit")->value();

      // if we have a valid unit, convert temp
      if (newUnit == "C" || newUnit == "F") {
        temp1 = convertTemperature(temp1, unit, newUnit.c_str());
        strncpy(unit, newUnit.c_str(), sizeof(unit) - 1);
        unit[sizeof(unit) - 1] = '\0';
      }
      request->send(200, "text/plain", String(temp1));
    }
    else {
      request->send(400, "text/plain", "Invalid parameters.");
    }
  });

  server.on("/temperature2", HTTP_GET, [](AsyncWebServerRequest* request) {
    Serial.println("Received request for temperature 2.");
    if (request->hasParam("unit")) {
      String newUnit = request->getParam("unit")->value();

      // if we have a valid unit, convert temp
      if (newUnit == "C" || newUnit == "F") {
        temp2 = convertTemperature(temp2, unit, newUnit.c_str());
        strncpy(unit, newUnit.c_str(), sizeof(unit) - 1);
        unit[sizeof(unit) - 1] = '\0';  
      }
      request->send(200, "text/plain", String(temp2));
    }
    else {
      request->send(400, "text/plain", "Invalid parameters.");
    }
  });

  server.on("/toggle1", HTTP_GET, [](AsyncWebServerRequest* request) {
    Serial.println("Received request for toggle 1.");
    if (request->hasParam("toggle")) {
      String toggle = request->getParam("toggle")->value();

      if (toggle == "ON") {
        temp1Enabled = true;
      }
      else {
        temp1Enabled = false;
      }
      request->send(200, "text/plain", "Sensor 1 toggled: " + toggle);
    }
    else {
      request->send(400, "text/plain", "Invalid parameters.");
    }
  });

  server.on("/toggle2", HTTP_GET, [](AsyncWebServerRequest* request) {
    Serial.println("Received request for toggle 2.");
    if (request->hasParam("toggle")) {
      String toggle = request->getParam("toggle")->value();

      if (toggle == "ON") {
        temp2Enabled = true;
      }
      else {
        temp2Enabled = false;
      }
      request->send(200, "text/plain", "Sensor 2 toggled: " + toggle);
    }
    else {
      request->send(400, "text/plain", "Invalid parameters.");
    }
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

void loop() {

  updateSensorStatus(TEMP1_BUTTON_PIN, button1State, lastButton1State, lastButton1DebounceTime, temp1Enabled);
  updateSensorStatus(TEMP2_BUTTON_PIN, button2State, lastButton2State, lastButton2DebounceTime, temp2Enabled);

  if (temp1Enabled) {
    temp1 = getTemperature(sensor1, unit);
  }
  else {
    temp1 = -100000.0;
  }
  if (temp2Enabled) {
    temp2 = getTemperature(sensor2, unit);
  }
  else {
    temp2 = -100000.0;
  }
}
