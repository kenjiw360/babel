from vpython import keysdown, rate, scene, norm, cross, sin, cos, vector, pi, color, sphere, box, winput, wtext

from client import room, room_lock, stop_event, id
from client.tcp_client import send
from constants import FPS
from protocol.client import ClientEvents


HZ = 1.0 / FPS
MOVE_SPEED = 5
TURN_SPEED = 3

def set_username(input: winput):
	username = input.text
	if username is not None: send(ClientEvents.USERNAME, (username.encode("ASCII"),))
wtext(text="Username: ")
username_input = winput(bind=set_username)

scene.userzoom = False
scene.userspin = False
scene.userpan = False
scene.autoscale = False
scene.camera.pos = vector(0, 1, 0)
scene.camera.axis = vector(0, 0, 1)

object = sphere(pos=vector(0, 1, 5), color = color.red, radius = 1)
floor = box(pos=vector(0, -0.1, 0), size=vector(40, 0.2, 40), color=color.gray(0.5))

pitch = 0.0
yaw = 0.5 * pi

def clamped(x):
	return max(-0.49*pi, min(0.49*pi, x))

def game():
	global pitch, yaw
	while not stop_event.is_set():
		rate(FPS)
		k = keysdown()

		if len(k): 
			if "up" in k: pitch = clamped(pitch + TURN_SPEED * HZ)
			if "down" in k: pitch = clamped(pitch - TURN_SPEED * HZ)
			if "right" in k: yaw += TURN_SPEED * HZ
			if "left" in k: yaw -= TURN_SPEED * HZ
	
			scene.camera.axis = vector(cos(yaw) * cos(pitch), sin(pitch), sin(yaw) * cos(pitch))
	
			forward = norm(vector(scene.camera.axis.x, 0, scene.camera.axis.z))
			right = cross(forward, vector(0, 1, 0))
			if "w" in k: scene.camera.pos += forward * MOVE_SPEED * HZ
			if "s" in k: scene.camera.pos -= forward * MOVE_SPEED * HZ
			if "d" in k: scene.camera.pos += right * MOVE_SPEED * HZ
			if "a" in k: scene.camera.pos -= right * MOVE_SPEED * HZ
	
			send(ClientEvents.POSITION, (scene.camera.pos.x, scene.camera.pos.z, yaw))
