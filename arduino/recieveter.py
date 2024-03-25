import socket

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 1234  # Port used in ESP32 code

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

print("TCP server started")

conn, addr = sock.accept()
print('Connected by', addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Received message:", data.decode())

conn.close()
