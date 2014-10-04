import socket
import netifaces as ni
import sys
import signal
from classes import *

MSG_LEN = 4096
clients = [] 	# client sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
players = {}

def signal_handler(signal, frame):
	print("Shutting down..")
	for client in clients:
		client.close()
	sock.close()
	sys.exit(0)

def updateClients(msg, source):
	for client in clients:
		if client is source:
			return
		client.send(msg.encode())

def receive(client):
	return client.recv(MSG_LEN).decode()

def handleConnection(client):
	while True:
		msg = receive(client).strip().split()
		first = msg.pop(0)
		if first == "CONNECT":
			p = msg.pop(0)
			players[p] = Player(p)
			print("added player '", p, "'")
		elif first == "DISCONNECT":
			p = msg.pop(0)
			del players[p]
			print("removed player '", p, "'")
		elif first == "MOVE":
			p = msg.pop(0)
			d = msg.pop(0)
			move(p, d)
		elif first == "SET":
			obj = msg.pop(0)
			msg.pop(0) 			# skip 'IN'
			room = msg.pop(0)
			msg.pop(0) 			# skip 'TO'
			status = msg.pop(0)	
			if status == "OPEN":
				rooms[room].objects[obj].trigger("open")
			elif status == "BREAK":
				rooms[room].objects[obj].trigger("break")
		elif first == "DECREASE":
			msg.pop(0)			# skip 'HEALTH'
			msg.pop(0)			# skip 'OF'
			p = msg.pop(0)
			msg.pop(0) 			# skip 'BY'
			amount = msg.pop(0)	
			if p.lower() in ["wizard", "dark lord", "goblin"]:
				lord.attack(amount)
			else:
				players[p].lose_health(amount)
		else:
			print("Unkown action in handleConnection()")
			break
	client.close()

signal.signal(signal.SIGINT, signal_handler)
	
addrs = ni.ifaddresses('wlan0')
host = addrs[ni.AF_INET].pop(0)['addr']
print("Your adress: ", host)
sock.bind((host, 9555))

sock.listen(3)
while True:
	client, addr = sock.accept()
	print("connection from ", addr)
	clients.append(client)
	handleConnection(client)

sock.close()
