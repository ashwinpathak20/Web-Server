from socket import *
import os
import datetime
import threading
from time import sleep

SERVER_PORT = 8000
packetSize = 1024
FILE_LOCATION = os.path.dirname(os.path.abspath(__file__))
limitRequest = 1000000
ServerAddr  = ''
usernames = ['ashwin','vidit','iiit']
passwords = ['pathak','jain','123']
positive = 0
clientList = []
store = ''
#print FILE_LOCATION
msgHome = ("<center><h1><center>HELLO FROM THE OTHER SIDE</center>")
msgError = ("<center><h1>404 ERROR<h1><br>"
            "File Requested Not Found<br>"
            "Check FileName</center> ")
headermsg = ("HTTP/1.1 200 OK\r\n"
            "Date: " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M IST")) + "\r\n"
            "Server: Vidwin/0.1\r\n"
            "Content-Type: text/html\r\n"
            "Connection: Closed\r\n\r\n")
headerError = ("HTTP/1.1 404 Not Found\r\n"
            "Date: " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M IST")) + "\r\n"
            "Server: Vidwin/0.1\r\n"
            "Content-Type: text/html\r\n"
            "Connection: Closed\r\n\r\n")

def handleConnection(clientSocket, auth, k):
    request = clientSocket.recv(packetSize)
    if not request :
        return
    r = request.split()
    requestType = r[0]
    requestFile = r[1]
    if r[3] == 'hi':
        auth = 0
    print requestFile
    if requestFile == '/' :
        clientSocket.send(headermsg + msgHome)
        clientSocket.close()
        return
    try:
        #print FILE_LOCATION
        if requestType == 'POST' :
            lines = request.split('\n')
            i = 0
            if auth == 1:
                logs = 0
                for line in lines :
                    if 'uname' in line:
                        boundary = line.split('&')
                        print boundary,type(boundary)
                for bound in boundary :
                    if 'uname' in bound:
                        user = bound.split('=')[1]
                    if 'psw' in bound:
                        psswd = bound.split('=')[1]
                for i in range(len(usernames)):
                    if user == usernames[i] and psswd == passwords[i]:
                        auth = 0
                        requestType = 'GET'
                        logs = 1
                        x = 1
                        clientList[k] = (clientList[k][0],clientList[k][1],x)
                        #clientSocket.send(headermsg+ ("<center> <h1> SUCCESSFULLY LOGGED IN </h1> </center>"))
                if logs == 0:
                    requestType = 'GET'
                    #clientSocket.send(headermsg+ ("<center> <h1> INVALID USERNAME OR PASSWORD </h1> </center>"))            
            else:
                for line in lines :
                    if 'boundary' in line :
                        boundary = line.split('-')[-1]
                        print boundary,type(boundary)
                    if 'filename' in line :
                        f = line.split('"')
                        fileName = f[-2]
                        lineNumber = i + 3
                    i += 1
                newFile = open(fileName,'w+')
                new = []
                te = 0
                for i in range(lineNumber,len(lines)):
                    if '----------' in lines[i]:
                        te = 1
                        break
                    new.append(lines[i])
                request = ('\n').join(new)
                newFile.write(request)
                while(1) :
                    clientSocket.settimeout(2)
                    try:
                        request = clientSocket.recv(packetSize)
                        if te == 1:
                            continue
                        #print request
                        if '----------' in request:
                            r = request.split('\n')
                            new = []
                            for i in range(len(r)) :
                                if '--------' in r[i]:
                                    break
                                new.append(r[i])
                            request = ('\n').join(new)
                        newFile.write(request)
                    except :
                        break
                clientSocket.settimeout(2)
                try:
                    request = clientSocket.recv(packetSize)
                except:
                    print "Timeout"
                clientSocket.send(headermsg+("<center> <h1>DONE SENDING </center>"))
                print "Done Recieveing!!"
        if requestType == 'GET' :
            print store
            if auth == 1:
                fileData = open(os.path.join(FILE_LOCATION,'ashwin.html'), 'r+')
            else:
                print os.path.join(FILE_LOCATION,requestFile)
                fileData = open(os.path.join(FILE_LOCATION,requestFile[1:]), 'r+')
            clientSocket.send(headermsg)
            for block in iter(lambda: fileData.read(packetSize), ""):
                clientSocket.send(block)
            print "Done Sending"
            fileData.close()
    except IOError:
        print "error"
        clientSocket.send(headerError + msgError)
    finally :
        clientSocket.close()

class myThread (threading.Thread):
    def __init__(self, threadID, name, connectionsocket, auth, k):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.connectionSocket = connectionsocket
        self.auth = auth
        self.k = k

    def run(self):
        print "Starting " + self.name
        handleConnection(self.connectionSocket, self.auth, self.k)
        print "Exiting " + self.name



def createServer():

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind((ServerAddr, SERVER_PORT))
    serverSocket.listen(10)

    connList = []
    print "Server is up and listening"
    try :
        while True:
            (clientSocket, address) = serverSocket.accept()
            a = (str(address[0]))
            temp = 0
            count = 0
            auth = 0
            k = 0
            for i in range(len(clientList)) :
                if a == clientList[i][0]:
                    temp = 1
                    #print type(addr[1])
                    if int(clientList[i][1]) < limitRequest :
                         x = clientList[i][1] + 1
                         clientList[i] = (clientList[i][0],x,clientList[i][2])
                    count = clientList[i][1]
                    if int(clientList[i][2]) == 0:
                        auth = 1
                        k = i
                    break
            if temp == 0 :
                auth = 1
                clientList.append((a,0,0))
            print clientList,count
            if count >= limitRequest :
                print "Over Requesting! Fuck Off"
                continue
            print "Address : " + str(address)
            name = "ClientConnection-" + str(len(connList))
            newconnection = myThread(len(connList), name, clientSocket, auth, k)
            newconnection.start()
            connList.append(newconnection)
            for thread in connList:
                if not thread.isAlive():
                    connList.remove( thread )
                    thread.join()

    except KeyboardInterrupt:
        print("\n^C Some interrupt Detected: Terminating gracefully")
    finally:
        print("Server socket closed")
        serverSocket.close()


createServer()
