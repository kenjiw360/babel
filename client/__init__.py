from dataclasses import dataclass
import threading
from vpython import color, scene, sphere, vec, box

from constants import FPS

HZ = 1.0 / FPS

stop_event = threading.Event()

@dataclass
class Player:
	id: int
	username: str
	pos: tuple[float, float] = (0, 0)
	rot: tuple[float, float] = (0, 0)

room: dict[int, Player] = {}

scene.userzoom = False
scene.userspin = False
scene.userpan = False
scene.autoscale = False
scene.camera.pos = vec(0, 1, 5)

object = sphere(pos=vec(0, 1, 0), color = color.red, radius = 0.5)
floor = box(pos=vec(0, 0, 0), size=vec(40, 0.2, 40), color=color.gray(0.5))