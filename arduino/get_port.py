import serial.tools.list_ports


def get_serial_ports():
    # ports = serial.tools.list_ports.comports()
    # return [port.device for port in ports]
    ports = serial.tools.list_ports.comports()
    print(ports[0].description)
    # Filter ports that match the pattern for CH340 converters
    ch340_ports = [
        port.device for port in ports if "CH340" in port.description]

    return ch340_ports


# if __name__ == "__main__":
#     serial_ports = get_serial_ports()
#     if serial_ports:
#         print("Available serial ports:")
#         for port in serial_ports:
#             print(port)
#             print(serial_ports)
#     else:
#         print("No serial ports available.")
