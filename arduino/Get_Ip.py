import socket


def get_ip():
    hostname = socket.gethostname()
    # getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    # printing the hostname and ip_address
    return ip_address
