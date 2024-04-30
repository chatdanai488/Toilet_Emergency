#include <WiFi.h>
#include <WiFiClient.h>

const char* ssid = "TCUST-FREE";
//const char* password = "YOUR_WIFI_PASSWORD";
const char* host = "172.16.201.50";
const int port = 1234; // Choose any available port
const int buttonPin = 17;  // the number of the pushbutton pin
const int ledPin = 25;    // the number of the LED pin

// variables will change:
int buttonState = 0; 
int count = 0;

WiFiClient client;

void setup() {
Serial.begin(115200);
pinMode(ledPin, OUTPUT);

pinMode(buttonPin, INPUT);
delay(100);

WiFi.begin(ssid);
while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
}
Serial.println("WiFi connected");
}

void loop() {
buttonState = digitalRead(buttonPin);
if (!client.connected()) {
    connectToServer();
}

if (buttonState == HIGH) {
    if (client.connected()) {
    client.print("B105 img\20240321_135959.jpg");
    digitalWrite(ledPin, HIGH);
    delay(200);
    }
}else{
    digitalWrite(ledPin, LOW);
    delay(200);
    }
}

void connectToServer() {
while (!client.connect(host, port)) {
    Serial.println("Connection failed, retrying...");
    Serial.println("STOP");
    delay(1000);
}
Serial.println("Connected to server");
}
