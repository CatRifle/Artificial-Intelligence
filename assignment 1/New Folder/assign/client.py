
import time
import sys
import socket
import threading
from socket import *

#Define connection (socket) parameters
#Address + Port no
#Server would be running on the same host as Client

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

serverName = 'localhost'
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))
username = raw_input('Enter username: ')
clientSocket.send(username)

Text = clientSocket.recv(1024)
if 'new' in Text:
    password = raw_input('Enter new password for {}: '.format(username))
else:
    password = raw_input('Enter password: ')
clientSocket.send(password)

if 'new' not in Text:
  for i in range(1,100):
    response = clientSocket.recv(1024)
    if 'Invalid' in response:
        print('Invalid password')
        username = raw_input('Enter username: ')
        clientSocket.send(username)
        response = clientSocket.recv(1024)
        
        if 'new' in response:
            password = raw_input('Enter new password for {}: '.format(username))
            clientSocket.send(password)
            break
        
        else:
            password = raw_input('Enter password: ')
            clientSocket.send(password)

    if 'Welcome' in response:
        print('Welcome to the forum')
        break
            

for i in range(1,1000):
  Command = raw_input('Enter one of the following commands: CRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT, SHT: ')
  if not 'UPD' in Command and not 'DWN' in Command:
    clientSocket.send(Command)
    
    if Command == 'XIT':
       print('Goodbye')
       clientSocket.close()
       break
    
    elif 'CRT' in Command:
       L = Command.split()
       threadname = L[1]
       message = clientSocket.recv(1024)
       if message == 'exists':
           print('Thread {} exists'.format(threadname))
       if message == 'created':
           print('Thread {} created'.format(threadname))
       

    elif 'LST' in Command:
        message = clientSocket.recv(1024)
        if message == 'empty':
            print('No threads to list')
        elif message == 'incorrect':
            print('Incorrect syntax for LST')
        else:
            '\n'.join(message)
            print('The list of active threads:')
            print(message)
            

    elif 'MSG' in Command:
        L = Command.split()
        threadname = L[1]
        print('Message posted to {} thread'.format(threadname))
        

    elif 'RDT' in Command:
        if len(Command) ==3:
            print('Incorrect syntax for RDT')
        else:
            L = Command.split()
            threadname = L[1]
            message = clientSocket.recv(1024)
            if message == 'not exist':
                print('Thread {} does not exist'.format(threadname))
            elif message == 'empty':
                print('Thread {} is empty'.format(threadname))
            else:
                print(message)


    elif 'EDT' in Command:
        message = clientSocket.recv(1024)
        if message == 'edited':
            print('The message has been edited')
        elif message == 'another':
            print('The message belongs to another user and cannot be edited')
        elif message == 'not exist':
            print('The thread does not exist')
        elif message == 'invalid msg num':
            print('The message number is invalid')


    elif 'DLT' in Command:
        message = clientSocket.recv(1024)
        if message == 'deleted':
            print('The message has been deleted')
        elif message == 'another':
            print('The message belongs to another user and cannot be deleted')
        elif message == 'not exist':
            print('The thread does not exist')
        elif message == 'invalid msg num':
            print('The message number is invalid')
            


    elif 'RMV' in Command:
        message = clientSocket.recv(1024)
        if message == 'not exist':
            print('The thread does not exist')
        elif message == 'removed':
            print('The thread has been removed')
        elif message == 'another':
            print('The thread was created by another user and cannot be removed')


    elif 'SHT' in Command:
           
           if Command =='SHT':
               print('Incorrect syntax for SHT')
           else:
               message = clientSocket.recv(1024)
               if message == 'incorrect':
                   print('Incorrect password')
               elif message == 'matched':
                   print('Goodbye. Server shutting down')
                   clientSocket.close()
                   sys.exit(0)

    else:
        print('Invalid command')





  else:
    if 'UPD' in Command:
        clientSocket.send(Command)
        L = Command.split()
        threadname = L[1]
        filename = L[2]
        message = clientSocket.recv(1024)
        if message =='not exist':
            print('The thread does not exist')
        elif message == 'exist':
            
            file = open(filename, 'rb')
            clientSocket.sendall(file.read())
            file.close()
            print('{} uploaded to {} thread'.format(filename, threadname))
            clientSocket.close()
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))



    elif 'DWN' in Command:
        clientSocket.send(Command)
        L = Command.split()
        threadname = L[1]
        filename = L[2]
        message = clientSocket.recv(1024)
        if message == 'not exist':
            print('The thread does not exist')
        elif message == 'file not exist':
            print('File does not exist in Thread {}'.format(threadname))
        elif message == 'exist':
            total_data =b''
            data = clientSocket.recv(1024)
            total_data += data
            num = len(data)
            while len(data)>0:
                data = clientSocket.recv(1024)
                num = num + len(data)
                total_data += data
                
            with open(filename,'wb') as f:
                f.write(total_data)
            f.close()
            print('{} successfully downloaded'.format(filename))

            clientSocket.close()
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))

            
        
        
            

                

