// shrinked version of DHTtester, written by ladyada

#include "DHT.h"

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

  while (Serial.available()) {
    String received = Serial.readString();
    handle_call(received);
  }
}

void handle_call(String &methodName) {
  if (methodName.equals("temp_cel")) {
    // Read temperature as Celsius (the default)
    float t = dht.readTemperature();
    if (isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
    else {
      Serial.println(t);
    }
  }
  else if (methodName.equals("temp_fah")) {
    // Read temperature as Fahrenheit (isFahrenheit = true)
    float f = dht.readTemperature(true);
    if (isnan(f)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
    else {
      Serial.println(f);
    }
  }
  else if (methodName.equals("humidity")) {
    float h = dht.readHumidity();
    if (isnan(h)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
    else {
      Serial.println(h);
    }
  }
  else if (methodName.equals("heat_index_cel")) {
    // Read temperature as Celsius (the default)
    float t = dht.readTemperature();
    float h = dht.readHumidity();

    if (isnan(t) || isnan(h)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
    else {
      float hic = dht.computeHeatIndex(t, h, false);
      Serial.println(hic);
    }
  }
  else if (methodName.equals("heat_index_fah")) {
    // Read temperature as Fahrenheit (isFahrenheit = true)
    float f = dht.readTemperature(true);
    float h = dht.readHumidity();

    if (isnan(f) || isnan(h)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
    else {
      float hif = dht.computeHeatIndex(f, h);
      Serial.println(hif);
    }
  }
  else {
    Serial.println("Unknown call: " + methodName);
  }
}

