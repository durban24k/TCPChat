import threading
import socket

host='127.0.0.1'
port=3000

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients=[]
usernames=[]

def broadcast(message):
     for client in clients:
          client.send(message)

def handle(client):
     while True:
          try:
               message=client.recv(1024)
               broadcast(message)
          except:
               index=clients.index(client)
               clients.remove(client)
               clients.close()
               username=usernames[index]
               broadcast(f'{username} left the chat'.encode('ascii'))
               usernames.remove(username)
               break

def receive():
     while True:
          client,address=server.accept()
          print(f"Connected with {str(address)}")

          client.send('USER'.encode('ascii'))
          username=client.recv(1024).decode('ascii')
          usernames.append(username)
          clients.append(client)

          print(f'Username of the client is {username}!')
          broadcast(f'{username} joined the chat!'.encode('ascii'))
          client.send('connected to the server!'.encode('ascii'))

          thread=threading.Thread(target=handle,args=(client,))
          thread.start()

print('Server is listening....')
receive()