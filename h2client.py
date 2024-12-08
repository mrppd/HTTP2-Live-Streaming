import socket
import h2.connection
import h2.events
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8080        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(b'Hello, world')
    data = s.recv(65535)
    
    conn = h2.connection.H2Connection(client_side=True)
    conn.initiate_connection()
    s.sendall(conn.data_to_send())
    events = conn.receive_data(data)
    #conn = h2.connection.H2Connection(client_side=False)
    #conn.initiate_connection()
#print(events.data)
print('Received', repr(events))