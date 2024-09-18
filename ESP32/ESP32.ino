#include <WiFi.h>
#include <ESPmDNS.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include "Constants.h"
#include "SensorUtils.h"
#include <DS18B20.h>
#include <OneWire.h>
#include "LiquidCrystal.h"

bool powerOn = true;
bool button1On = false;
bool button2On = false;

int powerState = HIGH;
int button1State = LOW;
int button2State = LOW;

int lastPowerState = HIGH;
int lastButton1State = LOW;
int lastButton2State = LOW;

unsigned long lastPowerDebounceTime = 0;
unsigned long lastButton1DebounceTime = 0;
unsigned long lastButton2DebounceTime = 0;

unsigned long debounceDelay = 50;
float temp1 = 0;
float temp2 = 0;

OneWire oneWire(ONE_WIRE_BUS);
DS18B20 sensor(&oneWire);

LiquidCrystal lcd(RS_PIN, ENABLE_PIN, D4_PIN, D5_PIN, D6_PIN, D7_PIN);


void setup() {
  lcd.begin(16, 2);
  // pinMode(25, INPUT);    // pushbutton temp 1
  // pinMode(33, INPUT);    // pushbutton temp 2
  lcd.setCursor(1, 0);
  lcd.print("Sensor 1 OFF");
  lcd.setCursor(1, 1);
  lcd.print("Sensor 2 OFF");

  sensor.begin();
  sensor.setResolution(11);
  pinMode(POWER_SWITCH_PIN, INPUT_PULLUP);
  pinMode(TEMP1_BUTTON_PIN, INPUT); // INPUT_PULLUP);
  pinMode(TEMP2_BUTTON_PIN, INPUT); //INPUT_PULLUP);
  pinMode(TEMP1_SENSOR_PIN, INPUT);
  pinMode(TEMP2_SENSOR_PIN, INPUT);
  launchServer(80);
}

void loop() {
  sensor.requestTemperatures();
  while (!sensor.isConversionComplete()) {
    delay(1);
  }
  double temp = sensor.getTempC();
  button1 = digitalRead(33);
  if (button1 == LOW) {
      lcd.clear();
      lcd.setCursor(1, 0);
      lcd.print(temp);
    }
  else {
      lcd.setCursor(1, 0);
      lcd.print("Sensor 1 OFF");
    }
  button2 = digitalRead(25);
  if (button2 == LOW) {
      lcd.setCursor(1, 1);
      lcd.print("Sensor 2 ON ");
    }
  else {
      lcd.setCursor(1, 1);
      lcd.print("Sensor 2 OFF");
    }
}

void launchServer(int port) {
  AsyncWebServer server(port);

  Serial.begin(115200);
  
  if (WIFI_USERNAME == "" || WIFI_PASSWORD == "") {
    Serial.println("Invalid username or password for wifi connection.");
  }

  WiFi.begin(WIFI_USERNAME, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.printf("Connected to WiFi with IP Address: %s\n", WiFi.localIP().toString().c_str());

  if (!MDNS.begin("esp32")) {
    Serial.println("Error setting up MDNS.");
    while (1) {
      delay(1000);
    }
  }
  Serial.println("mDNS started.");

  // Endpoint for power switch status
  server.on("/power", HTTP_GET, [](AsyncWebServerRequest* request) {
    int powerRead = digitalRead(POWER_SWITCH_PIN);
    checkButtonStatus(powerRead, powerOn, powerState, lastPowerState, debounceDelay, lastPowerDebounceTime);
    request->send(200, "text/plain", String(powerOn));
  });

  // Endpoint for temperature1 value
  server.on("/temperature1", HTTP_GET, [](AsyncWebServerRequest* request) {
    int buttonRead = digitalRead(TEMP1_BUTTON_PIN);
    checkButtonStatus(buttonRead, button1On, button1State, lastButton1State, debounceDelay, lastButton1DebounceTime);
    int temp = digitalRead(TEMP1_SENSOR_PIN);
    request->send(200, "text/plain", String(calculateTemperature(button1On, temp)));
  });


  // Endpoint for temperature2 value
  server.on("/temperature2", HTTP_GET, [](AsyncWebServerRequest* request) {
    int buttonRead = digitalRead(TEMP2_BUTTON_PIN);
    checkButtonStatus(buttonRead, button2On, button2State, lastButton2State, debounceDelay, lastButton2DebounceTime);
    int temp = digitalRead(TEMP2_SENSOR_PIN);
    request->send(200, "text/plain", String(calculateTemperature(button2On, temp)));
  });

  server.begin();
}