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
    sock.settimeout(5)

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            esp32_ip = data.decode("utf-8")
            return esp32_ip
    except socket.timeout:
        return None
