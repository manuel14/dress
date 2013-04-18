import socket
s1=socket.socket()
s1.bind(("local host",9999))
s1.listen(10)
c1,(host_c, puerto_c) = s1.accept()
recibido=c1.recv(1024)
print(recibido)
s1.send(recibido)