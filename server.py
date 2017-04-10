from socket import *
import os
import datetime

SERVER_PORT = 8000
packetSize = 1024
FILE_LOCATION = os.path.dirname(os.path.abspath(__file__))
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

def createServer():

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', SERVER_PORT))
    serverSocket.listen(10)

    print "Server is up and listening"
    try :
        while True:
            (clientSocket, address) = serverSocket.accept()
            request = clientSocket.recv(1024)
            if not request :
                continue
            r = request.split()
            requestType = r[0]
            requestFile = r[1]
            print requestFile
            if requestFile == '/' :
                clientSocket.send(headermsg + msgHome)
                continue
            try:
                print FILE_LOCATION
                print os.path.join(FILE_LOCATION,requestFile) + " " + "hi"
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
    except KeyboardInterrupt:
        print("\n^C Some interrupt Detected: Terminating gracefully")

createServer()
