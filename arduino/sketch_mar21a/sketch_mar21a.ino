#include <WiFi.h>

const char* ssid = "TCUST-FREE";     // Enter your Wi-Fi SSID
//const char* psw = "1234567890"; 
int LEDpin = 12;

const int buttonPin = 17;  // the number of the pushbutton pin
const int ledPin = 25;    // the number of the LED pin

// variables will change:
int buttonState = 0; 

void setup() {
  Serial.begin(115200); // Initialize serial communication for debugging
  pinMode(LEDpin,OUTPUT);



  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
  // Connect to Wi-Fi network with SSID
  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid);

  // Wait for Wi-Fi connection
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LEDpin,LOW);
    delay(500);
    Serial.println(".");
    digitalWrite(LEDpin,HIGH);
    delay(500);
  }
  Serial.println(" connected!");
  digitalWrite(LEDpin,HIGH);

  // Print ESP32's IP address
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  Serial.println("STOP");

}

void loop() {
  // Your code here
  buttonState = digitalRead(buttonPin);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
    // turn LED on:
    digitalWrite(ledPin, HIGH);
  } else {
    // turn LED off:
    digitalWrite(ledPin, LOW);
  }
}
