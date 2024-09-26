import socket
import struct

def getIP():
    MULTICAST_GROUP = '238.0.0.0'
    MULTICAST_PORT = 12345

    # Set up the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to the server address
    sock.bind(('', MULTICAST_PORT))

    # Tell the operating system to add the socket to the multicast group on all interfaces.
    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data, addr = sock.recvfrom(1024)
        esp32_ip = data.decode('utf-8')
        return esp32_ip