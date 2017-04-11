from socket import *
import os
import datetime
import threading

SERVER_PORT = 8001
packetSize = 1024
FILE_LOCATION = os.path.dirname(os.path.abspath(__file__))
limitRequest = 10
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

def handleConnection(clientSocket):
    request = clientSocket.recv(packetSize)
    #print request
    if not request :
        return
    r = request.split()
    #requestType = r[0]
    requestFile = r[1]
    print requestFile
    if requestFile == '/' :
        clientSocket.send(headermsg + msgHome)
        clientSocket.close()
        return
    try:
        #print FILE_LOCATION
        print os.path.join(FILE_LOCATION,requestFile)
        fileData = open(os.path.join(FILE_LOCATION,requestFile[1:]), 'r+')
        clientSocket.send(headermsg)
        for block in iter(lambda: fileData.read(packetSize), ""):
            clientSocket.send(block)
        print "Done Sending"
        fileData.close()
    except IOError:
        print "error"
        clientSocket.send(headermsg + msgError)
    finally :
        clientSocket.close()

class myThread (threading.Thread):
    def __init__(self, threadID, name, connectionsocket):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.connectionSocket = connectionsocket

    def run(self):
        print "Starting " + self.name
        handleConnection(self.connectionSocket)
        print "Exiting " + self.name



def createServer():

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('10.1.37.153', SERVER_PORT))
    serverSocket.listen(10)

    connList = []
    clientList = []

    print "Server is up and listening"
    try :
        while True:
            (clientSocket, address) = serverSocket.accept()
            a = (str(address[0]))
            temp = 0
            count = 0
            for i in range(len(clientList)) :
                if a == clientList[i][0]:
                    temp = 1
                    #print type(addr[1])
                    if int(clientList[i][1]) < limitRequest :
                         x = clientList[i][1] + 1
                         clientList[i] = (clientList[i][0],x,clientList[i][2])
                    count = clientList[i][1]
                    break
            if temp == 0 :
                clientList.append((a,0,0))
            print clientList,count
            if count >= limitRequest :
                print "Over Requesting! Fuck Off"
                continue
            print "Address : " + str(address)
            name = "ClientConnection-" + str(len(connList))
            newconnection = myThread(len(connList), name, clientSocket)
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