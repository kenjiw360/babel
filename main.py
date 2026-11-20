from vpython import sphere, vec, color, scene, rate, keysdown, vector
import threading
import socket

def udp_client(host: str, port: int):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((host, port))

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

thread_udp_client = threading.Thread(target=udp_client, args=("0.0.0.1", 8000))
thread_graphics = threading.Thread(target=graphics)
thread_controls = threading.Thread(target=controls)
thread_physics = threading.Thread(target=physics)

threads = [thread_udp_client, thread_graphics, thread_controls, thread_physics]

for t in threads: t.start()

try:
	while any(t.is_alive() for t in threads):
		for t in threads: t.join(timeout=0.1)
except KeyboardInterrupt:
	stop_event.set()
	for t in threads: t.join()s