#include <DS18B20.h>
#include <OneWire.h>
#include <LiquidCrystal.h>
const int rs=16, enable=17, d4=18, d5=19, d6=21, d7=22;
LiquidCrystal lcd(rs, enable, d4, d5, d6, d7);
int button1 = 1;        
int button2 = 1; 

#define ONE_WIRE_BUS 26
OneWire oneWire(ONE_WIRE_BUS);
DS18B20 sensor(&oneWire);

void setup() {
  lcd.begin(16, 2);
  pinMode(25, INPUT);    // pushbutton temp 1
  pinMode(33, INPUT);    // pushbutton temp 2
  lcd.setCursor(1, 0);
  lcd.print("Sensor 1 OFF");
  lcd.setCursor(1, 1);
  lcd.print("Sensor 2 OFF");

  sensor.begin();
  sensor.setResolution(11);
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
