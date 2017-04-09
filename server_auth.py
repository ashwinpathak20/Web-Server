from socket import *
import os
import datetime

SERVER_PORT = 8000
packetSize = 1024
FILE_LOCATION = os.path.dirname(os.path.abspath(__file__))
#print FILE_LOCATION
msg = ("<center><h1><center>HELLO FROM THE OTHER SIDE</center>")
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
usernames = []
passwords = []

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
            print request
            r = request.split()
            req = r[0]
            user = r[1]
            passwd = r[2]
            requestType = r[3]
            requestFile = r[4]
            if req == 'register':
                fl = 0
                for i in usernames:
                    if user==i:
                        fl=1
                if fl==0:
                    usernames.append(user)
                    passwords.append(passwd)
                    clientSocket.send('Yo')
                    print 'registered successfully \n'

                if fl==1:
                    clientSocket.send('err1')
                    print 'not a unique username \n'
                    continue

            if req == 'auth':
                fl = 0
                for i in range(0,len(usernames)):
                    if user == usernames[i] and passwd == passwords[i]:
                        fl=1
                        break

                if fl==1:
                    clientSocket.send('Yo')
                    print 'successfully logged in \n'

                if fl==0:
                    clientSocket.send('err2')
                    print 'invalid username or password\n'
                    continue

            print requestFile
            if requestFile == '/' :
                clientSocket.send(headermsg + msg)
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
