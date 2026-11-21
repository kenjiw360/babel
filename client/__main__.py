import socket
import threading

from vpython import color, keysdown, rate, scene, sphere, vec

from constants import HOST, PORT


def udp_client():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST, PORT))

	while True:
		pass

def graphics():
	while True:
		rate(10)

def controls():
	while True:
		rate(10)
		k = keysdown()

		speed = 0

		if 'w' in k:
			speed += 1
		if 's' in k:
			speed += -1

		scene.camera.pos += scene.forward * speed

def physics():
	pass


scene.userzoom = False
scene.userspin = False
scene.userpan = False

sphere = sphere(pos=vec(0,0,0), color = color.red, radius = 0.5)

thread_udp_client = threading.Thread(target=udp_client)
thread_graphics = threading.Thread(target=graphics)
thread_controls = threading.Thread(target=controls)
thread_physics = threading.Thread(target=physics)

threads = [thread_udp_client, thread_graphics, thread_controls, thread_physics]

for t in threads: t.start()
for t in threads: t.join()