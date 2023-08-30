import socket
from colorama import Fore


UDP_IP = "192.168.109.22"
UDP_PORT = 9999

def main(message, verbose = False):
    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)
    print("message: %s" % message.encode())

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
    msg = sock.recvfrom(2048)

    if verbose:
        message_out = msg[0].decode()
        if message_out == "MESSAGE RECEIVED":
            print(Fore.GREEN + "MESSAGE RECEIVED")
        else:
            print(Fore.RED + "SEND MESSAGE FAILED")