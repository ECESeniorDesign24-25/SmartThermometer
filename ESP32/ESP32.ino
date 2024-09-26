#include <WiFi.h>
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

bool sensor1Enabled = true;
bool sensor2Enabled = true;

unsigned long debounceDelay = 75;
unsigned long lastButton1Press = 0;
unsigned long lastButton2Press = 0;

bool temp1ButtonPressed = false;
bool temp2ButtonPressed = false;

// setup temperature sensors
OneWire oneWire1(TEMP1_SENSOR_PIN);
OneWire oneWire2(TEMP2_SENSOR_PIN);

DallasTemperature sensor1(&oneWire1);
DallasTemperature sensor2(&oneWire2);

AsyncWebServer server(80);
LiquidCrystal lcd(RS, ENABLE, D4, D5, D6, D7);

// button 1 interrupt
void IRAM_ATTR handleTemp1Button() {
    unsigned long currentTime = millis();
    if (currentTime - lastButton1Press > debounceDelay) {
        temp1ButtonPressed = true;
        lastButton1Press = currentTime;
    }
}

// button 2 interrupt
void IRAM_ATTR handleTemp2Button() {
    unsigned long currentTime = millis();
    if (currentTime - lastButton2Press > debounceDelay) {
        temp2ButtonPressed = true;
        lastButton2Press = currentTime;
    }
}


void setup() {
  pinMode(TEMP1_BUTTON_PIN, INPUT);
  pinMode(TEMP2_BUTTON_PIN, INPUT);
  pinMode(TEMP1_SENSOR_PIN, INPUT);
  pinMode(TEMP2_SENSOR_PIN, INPUT);

  // set interrupts on falling edge high to low
  attachInterrupt(digitalPinToInterrupt(TEMP1_BUTTON_PIN), handleTemp1Button, FALLING);
  attachInterrupt(digitalPinToInterrupt(TEMP2_BUTTON_PIN), handleTemp2Button, FALLING);

  sensor1.begin();
  sensor1.setResolution(11); // high precision

  sensor2.begin();
  sensor2.setResolution(11);

  Serial.begin(115200);
  Serial.println("Initialized serial.");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }
  Serial.printf("\nConnected to WiFi with IP Address: %s\n", WiFi.localIP().toString().c_str());

  server.on("/temperature1", HTTP_GET, [](AsyncWebServerRequest* request) {
    if (request->hasParam("unit")) {
      String newUnit = request->getParam("unit")->value();

      // if we have a valid unit, convert temp
      if (newUnit == "C" || newUnit == "F") {

        // check enabled
        if (sensor1Enabled) {

          // if sensor was off but not disconnected, recompute
          if (temp1 == SENSOR_OFF_TEMP || temp1 != SENSOR_DISCONNECT_TEMP) {
            temp1 = getTemperature(sensor1, unit, sensor1Enabled);
          }
          temp1 = convertTemperature(temp1, unit, newUnit.c_str());
          strncpy(unit, newUnit.c_str(), sizeof(unit) - 1);
          unit[sizeof(unit) - 1] = '\0';
        }
        else {
          temp1 = SENSOR_OFF_TEMP;
        }
      }
      request->send(200, "text/plain", String(temp1));
    }
    else {
      request->send(400, "text/plain", "Invalid parameters.");
    }
  });

  server.on("/temperature2", HTTP_GET, [](AsyncWebServerRequest* request) {
    if (request->hasParam("unit")) {
      String newUnit = request->getParam("unit")->value();
      
      // if we have a valid unit, convert temp
      if (newUnit == "C" || newUnit == "F") {

        // check enabled
        if (sensor2Enabled) {
          if (temp2 == SENSOR_OFF_TEMP || temp2 != SENSOR_DISCONNECT_TEMP) {
            temp2 = getTemperature(sensor1, unit, sensor2Enabled);
          }

          temp2 = convertTemperature(temp2, unit, newUnit.c_str());
          strncpy(unit, newUnit.c_str(), sizeof(unit) - 1);
          unit[sizeof(unit) - 1] = '\0';  
        } 
        else {
          temp2 = SENSOR_OFF_TEMP;
        }
      }
      request->send(200, "text/plain", String(temp2));
    }
    else {
      request->send(400, "text/plain", "Invalid parameters.");
    }
  });

  server.on("/toggle1", HTTP_GET, [](AsyncWebServerRequest* request) {
    if (request->hasParam("toggle")) {
      String toggle = request->getParam("toggle")->value();

      if (toggle == "ON") {
        sensor1Enabled = true;
      }
      else {
        sensor1Enabled = false;
      }
      request->send(200, "text/plain", "Sensor 1 toggled: " + toggle);

      // recompute
      temp1 = getTemperature(sensor1, unit, sensor1Enabled);
    }
    else if (request->params() == 0) {
      String responseString = "OFF";
      if (sensor1Enabled) {
        responseString = "ON";
      }
      request->send(200, "text/plain", responseString);    
    }
    else {
      request->send(400, "text/plain", "Invalid parameters.");
    }
  });

  server.on("/toggle2", HTTP_GET, [](AsyncWebServerRequest* request) {
    if (request->hasParam("toggle")) {
      String toggle = request->getParam("toggle")->value();

      if (toggle == "ON") {
        sensor2Enabled = true;
      }
      else {
        sensor2Enabled = false;
      }
      request->send(200, "text/plain", "Sensor 2 toggled: " + toggle);

      // recompute 
      temp2 = getTemperature(sensor2, unit, sensor2Enabled);
    }
    else if (request->params() == 0) {
      String responseString = "OFF";
      if (sensor2Enabled) {
        responseString = "ON";
      }
      request->send(200, "text/plain", responseString);    
    }
    else {
      request->send(400, "text/plain", "Invalid parameters.");
    }
  });

  server.begin();
  Serial.println("Server started.");

  lcd.begin(16, 2);
  lcd.clear();
  pinMode(TEMP1_BUTTON_PIN, INPUT);
  pinMode(TEMP2_BUTTON_PIN, INPUT);
}

void displayTemperature(int sensor, float temperature) {
  lcd.setCursor(1, sensor-1);
  if (temperature == SENSOR_OFF_TEMP) {
    char buffer[16];
    sprintf(buffer, "Sensor %d: Off  ", sensor);
    lcd.print(buffer);
  }
  else if (temperature == SENSOR_DISCONNECT_TEMP){
    char buffer[16];
    sprintf(buffer, "Sensor %d: Error", sensor);
    lcd.print(buffer);
  }
  else {
    char buffer[16];
    sprintf(buffer, "Sensor %d: %.2f", sensor, temperature);
    lcd.print(buffer);
  }
}

void loop() {

  // check if buttons have been pressed
  if (temp1ButtonPressed) {
      temp1ButtonPressed = !temp1ButtonPressed;  
      sensor1Enabled = !sensor1Enabled;
      temp1 = getTemperature(sensor1, unit, sensor1Enabled);
      displayTemperature(1, temp1);
  }

  if (temp2ButtonPressed) {
      temp2ButtonPressed = !temp2ButtonPressed;
      sensor2Enabled = !sensor2Enabled;
      temp2 = getTemperature(sensor2, unit, sensor2Enabled);
      displayTemperature(2, temp2);
    }

  // update temperatures
  temp1 = getTemperature(sensor1, unit, sensor1Enabled);
  temp2 = getTemperature(sensor2, unit, sensor2Enabled);

  displayTemperature(1, temp1);
  displayTemperature(2, temp2);

  delay(50);
}
