import socket

HOST = '224.0.0.1'
PORT = 5225
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST,PORT))
while 1:
    data, addr = s.recvfrom(1024);
    if not data: break
    reply = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print "replying to ", addr[0]
    reply.connect((addr[0],PORT))
    reply.send(data)
    reply.close()
