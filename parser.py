from classes import *
from rooms import *
from random import seed,randint

fillwords = ["the", "with", "on", "that", "at"]
tokens = []
 
def nextToken():
	global tokens
	if not tokens:
		return None
	return tokens.pop(0)

def readCmd():
    global tokens
    line = input('>> ')
    tokens = line.strip().lower().split()

def pObject(op):
	global fillwords
	obj = nextToken()
	while obj in fillwords:
		obj = nextToken()
	if not obj in room.objects:
		print("You can't ", op, " that.")
		return
	if op == "read":
		room.inspect_obj(obj)

def pItem(op):
	global fillwords
	item = nextToken()
	while item in fillwords:
		item = nextToken()

	if item in room.items: 			# room item
		if op == "take":
			player.take_item(room.remove_item(item)) 	# pick up
		elif op == "drop":
			print("I can't drop stuff I didn't pick up.")
	elif item in player.items:		# player inventory item
		if op == "take":
			print("I already have that.")
		elif op == "drop":
			room.add_item(player.drop_item(item)) 	# drop

def changeRoom(new_room):
	global room
	if new_room == None:
		print("You can't go there.")
		return
	print(new_room.desc)
	if new_room.traversable:
		room = new_room

def move(direction):
	if direction in ["north", "n"]:
		changeRoom(room.north)
	elif direction in ["east", "e"]:
		changeRoom(room.east)
	elif direction in ["south", "s"]:
		changeRoom(room.south)
	elif direction in ["west", "w"]:
		changeRoom(room.west)

def pDirection():
	direction = nextToken()
	while direction in fillwords:
		direction = nextToken()

	if direction in ["north", "east", "south", "west", "n", "e", "s", "w"]:
		move(direction)
	else:
		print("I can't go there.")

def attack(target):
	global player
	if randint(1,10)/10 <= player.gethitc():
		if randint(1,3) == 2:
			print("CRITICAL HIT!")
			target.attack(45)
		else:
			target.attack(20)

def defend(enemy):
	global player
	if randint(1,10)/10 <= enemy.hitchance:
		if randint(1,3) == 2:
			print("CRITICAL HIT!")
			target.attack(35)
		else:
			target.attack(15)

def pTarget():
	global fillwords
	target = nextToken()
	while target in fillwords:
		target = nextToken()
	if target in entities:
		attack(target)
	else:
		print("I can't attack that.")

def pOperation():
	global fillwords
	op = nextToken()
	while op in fillwords:
		op = nextToken()

	if op == "go":
		pDirection()
	elif op in ["north", "east", "south", "west", "n", "e", "s", "w"]:
		move(op)
	elif op == "look":
		print(room.desc)
	elif op == "read":
		pObject(op)
	elif op == "take":
		pItem(op)
	elif op == "attack":
		pTarget()
	elif op == "drop":
		pItem(op)
	else:
		print("I dont know that.")

seed()
room = rooms['opening']
lord = Entity("The Black Lord")

print("Textlive - a multiplayer text-adventure")
print("---------------------------------------\n")
player = Player(input("Please enter the name of your Character: ").strip())

print("---------------------------------------\n\n")
print(room.desc)
print("What do you do?")

while True:
    readCmd()
    pOperation()
