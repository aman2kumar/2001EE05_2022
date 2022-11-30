#Imported all the required libraries
import socket
import struct
import pickle
import threading

# creating a socket family INET and type to stream data sock_stream
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#binding the socket to our Server and the Port (it has to be always in a tuple)
server_socket.bind(('localhost', 9999))
#now that our socket is binded to tuple (server,port)
#we now listen i.e listening for new conections
server_socket.listen(4)

#defining list for connected clients and data of the clients
clients_connected = {}
clients_data = {}
#count variable to keep cnt of connections
count = 1


def connection_requests():
    #global scoped variable count
    global count
    # an infinite loop which will continue to listen or terminate when server crashes etc
    while True:
        print("Listening for connections....")
        #code will wait at this line and when a connection is found we store its address 
        #and a socket object that will allow us to transfer the data
        client_socket, address = server_socket.accept()
        #just to get who connected print a line
        print(f"Connections from {address} has been established")
        print(len(clients_connected))
        if len(clients_connected) == 4:
            client_socket.send('not_allowed'.encode())

            client_socket.close()
            continue
        else:
            client_socket.send('allowed'.encode())

        try:
            #recieve the message i.e the client name from the client of size 1024 bytes and decode it in the utf-8 Format
            client_name = client_socket.recv(1024).decode('utf-8')
        except:
            #in case the connection gets closed off
            print(f"{address} disconnected")
            #cleanly close of the current conection
            client_socket.close()
            continue
        # the client adress has been recognised as ... just a line in console to make things pretty
        print(f"{address} identified itself as {client_name}")
        
        count += 1
        #store the connected client in out list with the count
        clients_connected[client_socket] = (client_name, count)
        
        # recieving image of size 1024 from cliet
        image_size_bytes = client_socket.recv(1024)
        # unpacking the image recieved  struct.unpack always returns a tuple.. although it contains only one item
        image_size_int = struct.unpack('i', image_size_bytes)[0]
        
        #send the message to client side for the recieved information
        client_socket.send('received'.encode())
        #decoding the image
        image_extension = client_socket.recv(1024).decode()
        
        #define a sequence of octets (integers between 0 and 255)
        b = b''
        while True:
            # a loop which will close only when the length of data recieved equals to unpacked one
            image_bytes = client_socket.recv(1024)
            b += image_bytes
            if len(b) == image_size_int:
                break
        
        #in our defined list we add the client
        clients_data[count] = (client_name, b, image_extension)

        #pickling the client data
        clients_data_bytes = pickle.dumps(clients_data)
        #returns a bute object containing client data bytes of the format i
        clients_data_length = struct.pack('i', len(clients_data_bytes))
        
        #send the packed data length and the bytes to the client socket
        client_socket.send(clients_data_length)
        client_socket.send(clients_data_bytes)

        #the message from server side is recieved then
        if client_socket.recv(1024).decode() == 'image_received':
            #pack the count and send to the reciever side
            client_socket.send(struct.pack('i', count))

            for client in clients_connected:
                #for all except the client socket
                if client != client_socket:
                    client_socket.send('notification'.encode())
                    #pickle the data in a dictionary->data
                    data = pickle.dumps(
                        {'message': f"{clients_connected[client_socket][0]} joined the chat", 'extension': image_extension,
                         'image_bytes': b, 'name': clients_connected[client_socket][0], 'n_type': 'joined', 'id': count})
                    #pack this dictionary and send client 
                    data_length_bytes = struct.pack('i', len(data))
                    client_socket.send(data_length_bytes)
                    #first we send the size and now our data
                    client_socket.send(data)
        #Update the count variable
        count += 1
        #it is important for us now to define this thread as we don't want multiple access
        t = threading.Thread(target=receive_data, args=(client_socket,))
        t.start()
        #both of them run parallely


def receive_data(client_socket):
    #run the loop untill data is recieved from the client
    #implemented a try except for a Connection Reset/Abort  error
    while True:
        try:
            data_bytes = client_socket.recv(1024)
        except ConnectionResetError:
            print(f"{clients_connected[client_socket][0]} disconnected")

            for client in clients_connected:
                if client != client_socket:
                    #send the client notification
                    client_socket.send('notification'.encode())
                    #what the notification is to be sent is given as
                    data = pickle.dumps({'message': f"{clients_connected[client_socket][0]} left the chat",
                                         'id': clients_connected[client_socket][1], 'n_type': 'left'})

                    data_length_bytes = struct.pack('i', len(data))
                    client_socket.send(data_length_bytes)
                    #send the client side all of this
                    client_socket.send(data)
            #as the connection is reset.. we have to delete the data from our side as well
            #because if we don't there may be 
            del clients_data[clients_connected[client_socket][1]]
            del clients_connected[client_socket]
            client_socket.close()
            break
        except ConnectionAbortedError:
            #when client socket unexpectedly closed off
            print(f"{clients_connected[client_socket][0]} disconnected unexpectedly.")

            for client in clients_connected:
                if client != client_socket:
                    #similar to what we did in reset error
                    #send notification-> what the notification is -> delete the data
                    client_socket.send('notification'.encode())
                    data = pickle.dumps({'message': f"{clients_connected[client_socket][0]} left the chat",
                                         'id': clients_connected[client_socket][1], 'n_type': 'left'})
                    data_length_bytes = struct.pack('i', len(data))
                    client_socket.send(data_length_bytes)
                    client_socket.send(data)
            # to avoid error del the data.. for possible future reconnection
            del clients_data[clients_connected[client_socket][1]]
            del clients_connected[client_socket]
            client_socket.close()
            break
        #when the data is recieved encode the message from this side is enabled
        for client in clients_connected:
            if client != client_socket:
                client_socket.send('message'.encode())
                client_socket.send(data_bytes)


print("SERVER is starting....")
connection_requests()
