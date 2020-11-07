import threading
import socket
import pickle
from send import Message


PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT' 
SERVER = '192.168.0.18'
ADDR = (SERVER, PORT)
HEADER = 64
CONNS = {}


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def getBroadcasts():
	print('ok')
	while True:
		msg = client.recv(HEADER).decode(FORMAT)
		if msg:
			msgLen = int(msg)
			msg = client.recv(msgLen)
			msg = pickle.loads(msg)

			if msg.msgType == 'SETNAME':
				CONNS[msg.msgSender] = msg.msg

			if msg.msgType == 'MESSAGE':
				print(f"[{CONNS[msg.msgSender]}] {msg.msg}")



def send(msg):
	msg = pickle.dumps(msg)
	msgLen = str(len(msg)).encode(FORMAT)
	msgLen += b' ' * (HEADER - len(msgLen))

	client.send(msgLen)
	client.send(msg)

while 0==0:
	name = input('ENTER NAME: ')
	send(Message(name, 'SETNAME'))
	valid = client.recv(1).decode(FORMAT)
	if valid == "0":
		print('Sorry, that name is already in use, please use a different name')
	else:
		break

clientThread = threading.Thread(target = getBroadcasts)
clientThread.start()
while 0==0:
	sendMsg = input('>> ')
	if sendMsg == '!DISCONNECT':
		send(Message('disconnect', 'DISCONNECT'))
		break
	else:
		send(Message(sendMsg, 'MESSAGE'))


client.close()
