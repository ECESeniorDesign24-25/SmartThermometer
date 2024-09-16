#include <WiFi.h>
#include <ESPAsyncWebServer.h> 
#include "WiFiCredentials.h" // You need to update this file locally

AsyncWebServer server(80); // Port 80

void setup() {
  Serial.begin(115200);
  
  if (WIFI_USERNAME == "your_USERNAME" || WIFI_PASSWORD == "your_PASSWORD") {
    Serial.println("Invalid username or password for wifi connection.");
  }

  WiFi.begin(WIFI_USERNAME, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.printf("Connected to WiFi with IP Address: %s\n", WiFi.localIP().toString().c_str());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "Hello from ESP32");
  });

  server.begin();
}

void loop() {
  // Nothing here
}