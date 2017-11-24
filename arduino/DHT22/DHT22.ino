// shrinked version of DHTtester, written by ladyada

#include "DHT.h"
#include <ArduinoJson.h>

#define DHTPIN 2     // what digital pin we're connected to

// Uncomment whatever type you're using!
//#define DHTTYPE DHT11   // DHT 11
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  float hif = dht.computeHeatIndex(f, h);
  float hic = dht.computeHeatIndex(t, h, false);

  print_json_to_serial(h, t, f, hic, hif);
}

void print_json_to_serial(float humidity, float temp_cel, float temp_fah, float heat_index_cel, float heat_index_fah) {
  
  const size_t bufferSize = JSON_OBJECT_SIZE(5);
  DynamicJsonBuffer jsonBuffer(bufferSize);
  
  JsonObject& root = jsonBuffer.createObject();
  root["humidity"] = humidity;
  root["temperature_celsius"] = temp_cel;
  root["temperature_fahrenheit"] = temp_fah;
  root["heat_index_celsius"] = heat_index_cel;
  root["heat_index_fahrenheit"] = heat_index_fah;
  
  root.printTo(Serial);
  Serial.print("\n");
}

