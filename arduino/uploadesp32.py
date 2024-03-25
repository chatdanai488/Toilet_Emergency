import subprocess
import serial
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")


class ArduinoSketchUploader:
    def __init__(self, sketch_path, port="COM3", upload_speed=115200):
        self.sketch_path = sketch_path
        self.port = port
        self.upload_speed = upload_speed

    def compile_sketch(self):
        command = ['arduino-cli', 'compile', '--fqbn',
                   'esp32:esp32:esp32', "--board-options",
                   "FlashMode=dio", self.sketch_path]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print("Sketch compiled successfully!")
            return True
        else:
            print("Error compiling sketch:")
            print(stderr.decode())
            return False

    def upload_sketch(self):
        command = ['arduino-cli', 'upload', '-p', self.port, '--fqbn',
                   'esp32:esp32:esp32', self.sketch_path]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print("Sketch uploaded successfully!")
            return True
        else:
            print("Error uploading sketch:")
            print(stderr.decode())
            return False

    def communicate_serial(self):
        ser = serial.Serial(self.port, self.upload_speed)

        try:
            while True:
                # Read a line from the serial port
                line = ser.readline().decode().strip()
                print(line)
                if (line == "STOP"):
                    # break
                    pass
        except KeyboardInterrupt:
            ser.close()  # Close the serial port when Ctrl+C is pressed


def main():
    # Replace 'path_to_your_sketch' with the path to your Arduino sketch
    sketch_path = r'C:\Users\diamo\OneDrive\เดสก์ท็อป\Toilet_Emergency\sender'
    # Replace 'your_port_name' with the port where your ESP32 Dev Module is connected
    port = 'COM4'  # Example port, replace it with your actual port

    uploader = ArduinoSketchUploader(sketch_path, port)
    if uploader.compile_sketch():
        if uploader.upload_sketch():
            uploader.communicate_serial()
            print("ok")


if __name__ == "__main__":
    main()
