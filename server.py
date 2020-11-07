import socket
import threading
from send import Message
import pickle


HEADER = 64
PORT = 5050
SERVER = '192.168.0.18'
#SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
CONNS = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def broadcast(msg):
	msg = pickle.dumps(msg)
	msgLen = str(len(msg)).encode(FORMAT)
	msgLen += b' ' * (HEADER - len(msgLen))
	for client in CONNS:
		conn = client[0]
		conn.send(msgLen)
		conn.send(msg)

def send(msg, conn):
	msg = pickle.dumps(msg)
	msgLen = str(len(msg)).encode(FORMAT)
	msgLen += b' ' * (HEADER - len(msgLen))
	conn.send(msgLen)
	conn.send(msg)

def handleClient(conn, addr):
	print(f"[NEW CONNECTION] {addr} connected")

	connected = True
	while connected:
		#msgLen = conn.recv(HEADER).decode(FORMAT)
		
		#if msgLen:
			#msgLen = int(msgLen)
		msg = conn.recv(HEADER).decode(FORMAT)
		if msg:
			msgLen = int(msg)
			msg = conn.recv(msgLen)
			msg = pickle.loads(msg)
			#print(msg.msgType)
			msg.msgSender = addr
			if msg.msgType == "DISCONNECT":
				print(f"[{CONNS[(conn, addr)]}] disconnected")
				del CONNS[(conn, addr)]
				break
			if msg.msgType == 'SETNAME':
				name = msg.msg
				if name in CONNS.values():
					conn.send("0".encode(FORMAT))
				else:
					conn.send("1".encode(FORMAT))
					CONNS[(conn, addr)] = name
					print(f"[SETNAME] {(conn, addr)} to {name}")

					for client in CONNS:
						send(Message(CONNS[client], 'SETNAME', msgSender = client[1]), conn)


			else:
				print(f"[{CONNS[(conn, addr)]}] {msg.msg}")
			
			broadcast(msg)
	conn.close()
		

def start():
	server.listen()
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target = handleClient, args = (conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print(f"[STARTING] on {SERVER}")
start()
