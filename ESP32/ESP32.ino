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
  pinMode(TEMP1_BUTTON_PIN, INPUT_PULLUP);
  pinMode(TEMP2_BUTTON_PIN, INPUT_PULLUP);
  pinMode(TEMP1_SENSOR_PIN, INPUT);
  pinMode(TEMP2_SENSOR_PIN, INPUT);

  Serial.begin(115200);
  lcd.begin(16, 2);

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
      newUnit = request->getParam("unit")->value();
    }
    temp1 = convertTemperature(temp1, unit, newUnit);
    unit = newUnit;
    request->send(200, "text/plain", temp1);
  });

  server.on("/temperature2", HTTP_GET, [](AsyncWebServerRequest* request) {
    Serial.println("Received request for temperature 2.");
    std::string newUnit = unit;
    if (request->hasParam("unit")) {
      newUnit = request->getParam("unit")->value();
    }
    temp2 = convertTemperature(temp2, unit, newUnit);
    unit = newUnit;
    request->send(200, "text/plain", temp2);
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
}

void loop() {
  checkButtonStatus(digitalRead(TEMP1_BUTTON_PIN), button1On, button1State, lastButton1State, debounceDelay, lastButton1DebounceTime);
  if (button1On) {
      temp1 = getTemperature(sensor1, unit);
  }
  else {
    temp1 = -1000.00; // set to -1000 to indicate button is off
  }

  checkButtonStatus(digitalRead(TEMP2_BUTTON_PIN), button2On, button2State, lastButton2State, debounceDelay, lastButton2DebounceTime);
  if (button2On) {
      temp2 = getTemperature(sensor2, unit);
  }
  else {
    temp2 = -1000.00; // set to -1000 to indicate button is off
  }

  lcd.clear();
  lcd.setCursor(1, 0);
  if (temp1 != -1000.00) {
    lcd.print("Sensor 1: ");
    lcd.print(getTemperature(sensor1, unit));
    lcd.print(unit);
  }
  else {
    lcd.print("Sensor 1 OFF");
  }
  lcd.setCursor(1, 1);
  if (temp2 != -1000.00) {
    lcd.print("Sensor 2: ");
    lcd.print(getTemperature(sensor2, unit));
    lcd.print(unit);
  }
  else {
    lcd.print("Sensor 2 OFF");
  }
}
