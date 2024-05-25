/*
 Basic ESP8266 MQTT publish client example
*/
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "dct";
const char* password = "13071307";

const char* mqtt_server = "localhost"; 
const char* mqtt_user = "admin1";
const char* mqtt_pass= "admin1";

const int lm35 = A0; 

float vref = 3.3;
float resolution = vref/1023;

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  // Connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  Serial.println("In reconnect...");
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266_LM35", mqtt_user, mqtt_pass)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  char temp[8];
  if (!client.connected()) {
    reconnect();
  }
  
 float temperature = analogRead(A0);
 temperature = (temperature*resolution);
 temperature = temperature*100;
 sprintf(temp,"%i",temperature);
 client.publish("mq2_mqtt", temp);
 Serial.println(temperature);
// delay(1000);

  delay(5000);
}
