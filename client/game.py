from vpython import keysdown, rate, scene, norm, cross, sin, cos, vec, pi
from client.tcp_client import send
from constants import FPS, HZ, MOVE_SPEED, TURN_SPEED
from client import stop_event
from protocol.client import ClientEvents

pitch = 0.0
yaw = -0.5 * pi
scene.camera.axis = vec(cos(yaw) * cos(pitch), sin(pitch), sin(yaw) * cos(pitch))

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