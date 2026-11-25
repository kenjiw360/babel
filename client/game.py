from vpython import (
	color,
	cross,
	keysdown,
	norm,
	pi,
	rate,
	scene,
	sphere,
	vector,
)

from client import stop_event
from client.map import LevelModel
from client.state import Pair, state
from client.tcp_socket import send
from protocol.client import ClientEvents
from settings import client_settings

FPS = client_settings.fps
HZ = 1.0 / FPS
MOVE_SPEED = 5
TURN_SPEED = client_settings.turn_speed

scene.userzoom = False
scene.userspin = False
scene.userpan = False
scene.autoscale = False
scene.camera.pos = state.cam_pos
scene.camera.axis = state.cam_rot

object = sphere(pos=vector(0, 1, 5), color = color.red, radius = 1)

level = LevelModel()

def game():
	last_update = 0
	while not stop_event.is_set():
		rate(FPS)

		k = keysdown()
		if len(k): handle_keys(k)

		last_update += 1
		if len(k) or last_update > 3000:
			send_position()
			last_update = 0

def handle_keys(k: list[str]):
	if "up" in k: state.rot.b = clamped(state.rot.b + TURN_SPEED * HZ)
	if "down" in k: state.rot.b = clamped(state.rot.b - TURN_SPEED * HZ)
	if "right" in k: state.rot.a += TURN_SPEED * HZ
	if "left" in k: state.rot.a -= TURN_SPEED * HZ
	scene.camera.axis = state.cam_rot

	forward = norm(vector(scene.camera.axis.x, 0, scene.camera.axis.z))
	right = cross(forward, vector(0, 1, 0))
	if "w" in k: state.relative_pos += Pair.from_vec(forward * MOVE_SPEED * HZ)
	if "s" in k: state.relative_pos -= Pair.from_vec(forward * MOVE_SPEED * HZ)
	if "d" in k: state.relative_pos += Pair.from_vec(right * MOVE_SPEED * HZ)
	if "a" in k: state.relative_pos -= Pair.from_vec(right * MOVE_SPEED * HZ)
	scene.camera.pos = state.cam_pos

def clamped(x):
	return max(-0.49*pi, min(0.49*pi, x))

def send_position():
	send(ClientEvents.POSITION, state.tcp_pos)