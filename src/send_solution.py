import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host ="142.168.109.22"
port =9999
s.connect((host,port))

def ts(str):
   s.send('e'.encode()) 
   data = ''
   data = s.recv(1024).decode()
   print (data)

s.close ()


def main(path):
    pass
