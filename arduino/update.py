

class InoFileEditor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_code(self):
        try:
            with open(self.file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            print(e.args)
            return None

    def update_code(self, my_wifi: str, my_ip: str, my_port: int):
        self.code = """#include <WiFi.h>
#include <WiFiClient.h>

const char* ssid = "%s";
//const char* password = "YOUR_WIFI_PASSWORD";
const char* host = "%s";
const int port = %d; // Choose any available port
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
    client.print("Button pressed!");
    client.print(count);
    digitalWrite(ledPin, HIGH);
    count = count +1;
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
""" % (my_wifi, my_ip, my_port)
        return self.code

    def upload_code(self, data):
        try:
            with open(self.file_path, 'w') as file:
                file.write(data)
            print("Code edited successfully.")
        except Exception as e:
            print(f"An error occurred while writing the file: {e}")

    def write_code(self, data: str):
        original_code = self.read_code()
        if original_code is not None:
            self.upload_code(data)


# Example usage:
# file_path = "sketch_test1\sketch_test1.ino"

# ino_editor = InoFileEditor(file_path)
# data = ino_editor.update_code("TCUST-FREE", "172.16.204.48", 1234)

# ino_editor.write_code(data)
