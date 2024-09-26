import socket
import struct
import time


def getIP():
    """
    Get the IP address of the ESP32 from UDP multicast
    """
    MULTICAST_GROUP = "238.0.0.0"
    MULTICAST_PORT = 12345

    # set up the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", MULTICAST_PORT))

    # add socket to multicast group
    ip_bits = socket.inet_aton(MULTICAST_GROUP)
    multicast_request = struct.pack("4sl", ip_bits, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast_request)
    sock.settimeout(10)

    # default to dynamic ip: may need to be updated, read from esp thru serial
    ESP32_DYNAMIC_IP = "172.17.88.45" 
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            esp32_ip = data.decode("utf-8")
            return esp32_ip
    except socket.timeout:
        return ESP32_DYNAMIC_IP


if __name__ == "__main__":
    try:
        esp32_ip = getIP()
        if esp32_ip != ESP32_DYNAMIC_IP:
            print(f"ESP32 IP address: {esp32_ip}")
        else:
            print(f"No IP broadcast received, defaulting to ESP32_DYNAMIC_IP: {ESP32_DYNAMIC_IP}")
    except Exception as e:
        print(f"Error: {e}")