from vpython import keysdown, rate, scene, norm, cross, sin, cos, vec, pi, color, sphere, box
from client.tcp_client import send
from constants import FPS
from client import stop_event
from protocol.client import ClientEvents

HZ = 1.0 / FPS
MOVE_SPEED = 5
TURN_SPEED = 3

scene.userzoom = False
scene.userspin = False
scene.userpan = False
scene.autoscale = False
scene.camera.pos = vec(0, 1, 5)
scene.camera.axis = vec(0, 0, -1)

object = sphere(pos=vec(0, 1, 0), color = color.red, radius = 0.5)
floor = box(pos=vec(0, 0, 0), size=vec(40, 0.2, 40), color=color.gray(0.5))

pitch = 0.0
yaw = -0.5 * pi

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
	
			scene.camera.axis = vec(cos(yaw) * cos(pitch), sin(pitch), sin(yaw) * cos(pitch))
	
			forward = norm(vec(scene.camera.axis.x, 0, scene.camera.axis.z))
			right = cross(forward, vec(0, 1, 0))
			if "w" in k: scene.camera.pos += forward * MOVE_SPEED * HZ
			if "s" in k: scene.camera.pos -= forward * MOVE_SPEED * HZ
			if "d" in k: scene.camera.pos += right * MOVE_SPEED * HZ
			if "a" in k: scene.camera.pos -= right * MOVE_SPEED * HZ
	
			send(ClientEvents.POSITION, (scene.camera.pos.x, scene.camera.pos.z, yaw, pitch))