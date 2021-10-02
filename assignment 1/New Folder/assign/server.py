
import time
import sys
import socket
import threading
from socket import *
import os

#Define connection (socket) parameters
#Address + Port no
#Server would be running on the same host as Client

serverPort = int(sys.argv[1])
addmin_password = sys.argv[2]

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)
print("Waiting for clients")


def FindStrInFile(file, string):
    with open(file) as f:
        for line in f:
            if string in line:
                return True
    return False


def CheckPassword(file, username, password):
    with open(file) as f:
        for line in f:
            if username in line:
                if password in line:
                    return True
                else:
                    return False

def CheckCreation(file, username, threadname):
    with open(file) as f:
        for line in f:
            L = line.split()
            creator, thread = L[0], L[1]
            if threadname == thread:
                if username == creator:
                    return True
                else:
                    return False

            

# insert 'username password' into credentials
def InsertNewUser(filename, username, password):
    f = file(filename)
    info = []
    for line in f:
        info.append(line)
    f.close()
    new_user = '\n' + username + ' ' + password
    info.append(new_user)
    f_epheral = ''.join(info)
    f = file(filename,'w')
    f.write(f_epheral)
    f.close

# insert 'username threadname' into wocreate.txt
def InsertWhoCreate(filename, username, threadname):
    f = file(filename)
    info = []
    for line in f:
        info.append(line)
    f.close()
    new_user = username + ' ' + threadname + '\n'
    info.append(new_user)
    f_epheral = ''.join(info)
    f = file(filename,'w')
    f.write(f_epheral)
    f.close


# insert 'updated_file_name' into update_record
def InsertWhatUpdated(filename, updated_file):
    f = file(filename)
    info = []
    for line in f:
        info.append(line)
    f.close()
    new_update = updated_file + '\n'
    info.append(new_update)
    f_epheral = ''.join(info)
    f = file(filename,'w')
    f.write(f_epheral)
    f.close

    
# insert message into thread
def InsertMsg(filename, Msg):
    f = file(filename)
    info = []
    for line in f:
        info.append(line)
    f.close()
    info.append(Msg)
    f_epheral = ''.join(info)
    f = file(filename,'w')
    f.write(f_epheral)
    f.close

# sub-function of command 'RMV'
def RMV(filename, username, threadname):
    os.remove('{}.txt'.format(threadname))
    f = file(filename)
    info =[]
    for line in f:
        L = line.split()
        creator, thread = L[0], L[1]
        if creator == username and thread == threadname:
            pass
        else:
            info.append(line)
    f_epheral = ''.join(info)
    f = file(filename,'w')
    f.write(f_epheral)
    f.close

# sub-funtion of command 'MSG'
def InsertMsgTwoCase(filename, username, message):
    f = file(filename)
    num = 1
    with open(filename) as fl:
        for line in fl:
            if len(line)>0:
               L = line.split()
               seq = L[0]
               if seq.isdigit():
                   num += 1
            else:
                Msg = str(num) + ' ' + username + ': '+  message + '\n'
                InsertMsg(filename, Msg)
                return
            
        Msg = str(num) + ' ' + username + ': '+  message + '\n'
        InsertMsg(filename, Msg)
            
    
              
# get thread name from whocreate.txt mainly for 'LST'
def ExtractThreadName(filename):
    ActiveThread = []
    with open(filename) as f:
        for line in f:
            if len(line) > 2:
              L = line.split()
              threadname = L[1]
              ActiveThread.append(threadname)
    f.close
    S = '\n'.join(ActiveThread)
    return S
            
            

# Authentication    
def AskforPassword(file, username, password):
        if CheckPassword(file, username, password):
            print('{} successful login'.format(username))
            Text1 = 'Welcome to the forum'
            connectionSocket.send(Text1)
            return
        else:
            print('Incorrect password')
            Text_ER = 'Invalid password'
            connectionSocket.send(Text_ER)
            username = connectionSocket.recv(1024)
            
            if FindStrInFile(file, username):
                Text = 'Enter password:'
                connectionSocket.send(Text)
                password = connectionSocket.recv(1024)
                Judge = CheckPassword(file, username, password)
                if Judge:
                    print('{} successful login'.format(username))
                    Text1 = 'Welcome to the forum'
                    connectionSocket.send(Text1)
                    return
                else:
                    AskforPassword(file, username, password)
               
            else:
                Text = 'Enter new password'
                print('New user')
                connectionSocket.send(Text)
                password = connectionSocket.recv(1024)
                InsertNewUser('credentials.txt', username, password)
                print('{} successfully logged in'.format(username))
                return


# 'XIT'     
def XIT(command,username, socket):
    socket.close()
    print('{} exited'.format(username))
    print('Waiting for clients')
    
# sub-function of 'RDT'
def RDT(filename):
    f = file(filename)
    info = []
    for line in f:
        info.append(line)
    f.close()
    f_epheral = ''.join(info)
    return f_epheral

# check if the message belongs to current user
def EDT_ifuser(filename, username, number):
    with open(filename) as f:
        for line in f:
            L = line.split()
            num = L[0]
            init_name = L[1]
            name = init_name.replace(':','')
            if number == num:
                if username == name:
                    return True
                else:
                    return False
                
# check if the thread has that message number
def EDT_num_valid(filename, number):
    with open(filename) as f:
        for line in f:
            L = line.split()
            num = L[0]
            if number == num:
                return True
        return False
            

# sub-function of 'EDT'
def EDT(filename, msg, number):
    with open(filename) as f:
        file_list =[]
        for line in f:
            L = line.split()
            num = L[0]
            if number == num:
                L = L[:2]
                Lmsg = msg.split()
                for item in Lmsg:
                    L.append(item)
                L.append('\n')
                line = ' '.join(L)
                file_list.append(line)
            else:
                file_list.append(line)
        f_epheral =  ''.join(file_list)       
        F = file(filename,'w')
        F.write(f_epheral)
        F.close
        return
        
            
# sub-funtion of 'DLT'                
def DLT(filename, number):
    with open(filename) as f:
        file_list =[]
        for line in f:
            L = line.split()
            num = L[0]
            if number == num:
                L = ''
                file_list.append(L)
            else:
                file_list.append(line)
        f_epheral = ''.join(file_list)
        F = file(filename,'w')
        F.write(f_epheral)
        F.close
        return

# overwrite
def Write(filename, data):
    with open(filename,'wb') as f:
        f.write(data)
    f.close()
    return


# stem code
while 1:

    connectionSocket, addr = serverSocket.accept()
    print('Client connected')
    username = connectionSocket.recv(1024)

    if FindStrInFile('credentials.txt', username):
        Text = 'Enter password:'
        connectionSocket.send(Text)
        password = connectionSocket.recv(1024)
        AskforPassword('credentials.txt', username, password)

                        
    else:
        Text = 'Enter new password'
        print('New user')
        connectionSocket.send(Text)
        password = connectionSocket.recv(1024)
        InsertNewUser('credentials.txt', username, password)
        print('{} successfully logged in'.format(username))

    
    for i in range(1000):
       command = connectionSocket.recv(1024)

       # case 1
       if command == 'XIT':
           XIT(command,username, connectionSocket)
           break
           

       # case 2
       elif 'CRT' in command:
           print('{} issued CRT command'.format(username))
           L = command.split()
           threadname = L[1]
           judge = os.path.exists('{}.txt'.format(threadname))
           if judge:
               print('Thread {} exists'.format(threadname))
               message = 'exists'
               connectionSocket.send(message)
           else:
               os.mknod('{}.txt'.format(threadname))
               doc_exist = os.path.exists('whocreate.txt')
               if doc_exist:
                   InsertWhoCreate('whocreate.txt', username, threadname)
               else:
                   os.mknod('whocreate.txt')
                   InsertWhoCreate('whocreate.txt', username, threadname)
               
               print('Thread {} created'.format(threadname))
               message = 'created'
               connectionSocket.send(message)
 
       # case 3
       elif 'LST' in command:
           if len(command) == 3:
               print('{} issued LST command'.format(username))
               doc_exist = os.path.exists('whocreate.txt')
               if doc_exist:
                   message = ExtractThreadName('whocreate.txt')
                   connectionSocket.send(message)
               else:
                   message = 'empty'
                   connectionSocket.send(message)
           else:
               message = 'incorrect'
               connectionSocket.send(message)


       # case 4
       elif 'MSG' in command:
           print('{} issued MSG command'.format(username))
           L = command.split()
           threadname = L[1]
           info = L[2:]
           string = ' '.join(info)
           InsertMsgTwoCase('{}.txt'.format(threadname), username, string)
           print('{} posted to {} thread'.format(username, threadname))
           
       # case 5
       elif 'RDT' in command:
           if len(command) > 4:
               print('{} issued RDT command'.format(username))
               L = command.split()
               threadname = L[1]
               doc_exist = os.path.exists('{}.txt'.format(threadname))
               if doc_exist:
                   size = os.path.getsize('{}.txt'.format(threadname))
                   if size == 0:
                       message = 'empty'
                       connectionSocket.send(message)
                       print('Thread {} read'.format(threadname))
                   else:
                       message = RDT('{}.txt'.format(threadname))
                       connectionSocket.send(message)
                       print('Thread {} read'.format(threadname))
                                      
               else:
                   message = 'not exist'
                   connectionSocket.send(message)
                   print('Incorrect thread specified')

       # case 6
       elif 'EDT' in command:
            print('{} issued EDT command'.format(username))
            L= command.split()
            threadname = L[1]
            seq = L[2]
            num = int(seq)
            doc_exist = os.path.exists('{}.txt'.format(threadname))
            if not doc_exist:
                message = 'not exist'
                connectionSocket.send(message)
                print('Thread does not exist')
            
            else:
                filename = '{}.txt'.format(threadname)
                Validity = EDT_num_valid(filename, seq)
                if not Validity:
                    message = 'invalid msg num'
                    connectionSocket.send(message)
                    print('Message number invalid')
                else:                                  
                    message_list = L[3:]
                    message = ' '.join(message_list)
                    qualify = EDT_ifuser(filename, username, seq)
                    if qualify:
                        EDT(filename, message, seq)
                        message = 'edited'
                        connectionSocket.send(message)
                        print('Message has been edited')

                    else:
                        message = 'another'
                        connectionSocket.send(message)
                        print('Message cannot be edited')

                        
       # case 7
       elif 'DLT' in command:
            print('{} issued EDT command'.format(username))
            L= command.split()
            threadname = L[1]
            seq = L[2]
            num = int(seq)
            doc_exist = os.path.exists('{}.txt'.format(threadname))
            if not doc_exist:
                message = 'not exist'
                connectionSocket.send(message)
                print('Thread does not exist')
            else:
                filename = '{}.txt'.format(threadname)
                Validity = EDT_num_valid(filename, seq)
                if not Validity:
                    message = 'invalid msg num'
                    connectionSocket.send(message)
                    print('Message number invalid')
                else:
                    msg = ''
                    message = ' '.join(msg)
                    qualify = EDT_ifuser(filename, username, seq)
                    
                    if qualify:
                        DLT(filename, seq)
                        message = 'deleted'
                        connectionSocket.send(message)
                        print('Message has been deleted')

                    else:
                        message = 'another'
                        connectionSocket.send(message)
                        print('Message cannot be deleted')                    



       # case 8
       elif 'RMV' in command:
           print('{} issued RMV command'.format(username))
           L =command.split()
           threadname = L[1]
           filename = '{}.txt'.format(threadname)
           doc_exist = os.path.exists('{}.txt'.format(threadname))
           if not doc_exist:
               message = 'not exist'
               connectionSocket.send(message)
               print('Thread does not exist')
           else:                         
               check_origin = CheckCreation('whocreate.txt', username, threadname)
               if check_origin:               
                   RMV('whocreate.txt', username, threadname)
                   message = 'removed'
                   connectionSocket.send(message)
                   print('Thread {} removed'.format(threadname))
               
               else:
                   message = 'another'
                   connectionSocket.send(message)
                   print('Thread {} cannot be removed'.format(threadname))


       # case 9
       elif 'UPD' in command:
           print('{} issued UPD command'.format(username))
           L =command.split()
           threadname = L[1]
           filename = L[2]
           thread = '{}.txt'.format(threadname)
           doc_exist = os.path.exists('{}.txt'.format(threadname))
           if not doc_exist:
               message = 'not exist'
               connectionSocket.send(message)
               print('Thread does not exist')
           else:
               message ='exist'
               connectionSocket.send(message)
               total_data = b''
               data = connectionSocket.recv(1024)
               total_data += data
               num =len(data)
               
               while len(data)>0:
                    data = connectionSocket.recv(1024)
                    num +=len(data)
                    total_data += data
               
               
               name = '{}-{}'.format(threadname, filename)
               Write(name, total_data)
               Msg = '\n'+'{} uploaded {}'.format(username,filename)
               
               
               InsertMsg('{}.txt'.format(threadname), Msg)
               record = os.path.exists('update_record.txt')
               if record:
                   InsertWhatUpdated('update_record.txt', name)
               else:
                   os.mknod('update_record.txt')
                   InsertWhatUpdated('update_record.txt', name)
               
               print('uploaded')
               connectionSocket.close()
               connectionSocket, addr = serverSocket.accept()

       # case 10
       elif 'DWN' in command:
           print('{} issued DWN command'.format(username))
           L =command.split()
           threadname = L[1]
           filename = L[2]
           thread = '{}.txt'.format(threadname)
           doc_exist = os.path.exists('{}.txt'.format(threadname))
           if not doc_exist:
               message = 'not exist'
               connectionSocket.send(message)
               print('Thread does not exist')
           else:
               name = '{}-{}'.format(threadname, filename)
               file_exist = os.path.exists(name)
               if not file_exist :
                  message = 'file not exist'
                  connectionSocket.send(message)
                  print('File does not exist')
               else:
                  message = 'exist'
                  connectionSocket.send(message)
                  file = open(name, 'rb')
                  connectionSocket.sendall(file.read())
                  file.close()
                  print('{} downloaded from Thread {}'.format(filename,threadname))
                  connectionSocket.close()
                  connectionSocket, addr = serverSocket.accept()

       # case 11
       elif 'SHT' in command:
           if len(command)>4:
               print('{} issued SHT command'.format(username))
               L =command.split()
               psword = L[1]
               if not psword == addmin_password:
                   message = 'incorrect'
                   connectionSocket.send(message)
                   print('Incorrect password')
               else:
                   message = 'matched'
                   connectionSocket.send(message)
                   print('Server shuttting down')
                   with open('whocreate.txt') as f:
                       for line in f:
                           L = line.split()
                           thread = L[1]
                           os.remove('{}.txt'.format(thread))
                   f.close()
                   os.remove('whocreate.txt')
                   doc_exist = os.path.exists('update_record.txt')
                   if doc_exist:
                       with open('update_record.txt') as f:
                           for line in f:
                               line = line.replace('\n','')
                               os.remove('{}'.format(line))
                       f.close()
                       os.remove('update_record.txt')
                   
                   os.remove('credentials.txt')               
                   connectionSocket.close()
                   serverSocket.close()
                   sys.exit(0)
                
                   
       # case 12
       else:
           pass

               
               
