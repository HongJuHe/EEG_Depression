import socket
import sys

# LOCAL: 172.24.208.1
# SERVER: 18.222.27.87
HOST = '18.221.204.61'
PORT = 8080

#print("before sending")
f = open("D:/ThinkGearData/parsed_data1.txt", "r")
con = f.readlines()
f.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
for i in con:
    data = str(i)
    client_socket.send(data.encode())

#print("after sending")
data = "end"
client_socket.send(data.encode())
#print("after empty")

data = client_socket.recv(1024)
print('Received', data.decode())

client_socket.close()

#def return():
#    return data
