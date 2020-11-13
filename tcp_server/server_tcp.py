import socket
import threading
import requests
import auth
import sspider


bind_ip = "127.0.0.1"
bind_port = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))
server.listen(5)

print("[*] Listening on %s %d" %(bind_ip,bind_port))
# this is our client-handling thread
def handle_client(client_socket):
    # print out what the client sends
    request = client_socket.recv(1024)
    print ("[*] Received: %s" % request)
    code = str((request[-4:])).replace("b'","").replace("'","") #for am actual code param you need  [-348:]
    auth_token = auth.req2(code) #used the code parameter to authenticate and obtain the OAuth access token
    # fb api calls
    res = sspider.main(auth_token) #api call; places all photo IDs in a list
    analised = sspider.photo(res[1]) #creates an object for every photo
    analised.info(res[0],res[1]) #creates an object with every picture and all itds characteristics
    
    
    # send back a packet
    client_socket.send(b"HTTP/1.1 200 OK\n'Access-Control-Allow-Origin' , '*'")
    client_socket.close()
while True:
    client,addr = server.accept()
    print("[*] Accepted connection from: %s %d" % (addr[0],addr[1]))
    # spin up our client thread to handle incoming data
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()