import sys,os
from socket import *

def formRequestHeader(req_webpage_name):
    httprequestheader = ("GET /" + req_webpage_name + " HTTP/1.1\r\n\r\n")
    return httprequestheader

def main():
	try:
		host = sys.argv[1]
		port = sys.argv[2]
		file = sys.argv[3]
	except:
		print('Incomplete set of arguments')
		sys.exit()


	try:
		client = socket(AF_INET, SOCK_STREAM)
		client.connect((host, int(port)))
		print ('Connected to ' + host + ':' + port + '\n')
		request = ("GET /" + file + " HTTP/1.1\r\n\r\n")
		client.send(formRequestHeader(file))
		print("Request sent. Waiting for server's response\n")

	except:
		print('could not connect to the network')
		sys.exit()



	try:
		headers = ''
		content = ''
		fl=0
		while True:
			recv = client.recv(1024)
			content += recv
			end = content.rfind('\r\n')
			if end != -1:
				for a in content[:end+2].splitlines(True):
					headers += a
					if a == '\r\n' and headers[-2:] == '\r\n':
						content = content[2+end:]
						fl=1
						break
				if fl==0:
					content = content[2+end:]
			if fl==1:
				break

		b = 0
		d = 0
		b = headers.find('Content-Length: ')
		if b!=-1:
			b += 16
			c = headers.find('\r\n',b)
			d = int(headers[b:c])

		if len(content)<d:
			while True:
				content1 = client.recv(1024)
				content += content1
				if len(content) >= d:
					break

		if headers.split()[1] == '200':
			print('Response code 200 received: \n' + headers + content + '\n')

		else:
			print('Response code 404 received: \n' + headers + content + '\n')

	except (ValueError, IndexError):
	    print("\nReceived malformed headers. Exiting")
	except KeyboardInterrupt:
	    print("\n^C Detected. Terminating gracefully")
	finally:
	    print("Client socket closed")
	    client.close()

if __name__ == "__main__":
	main()
