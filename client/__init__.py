from dataclasses import dataclass
import threading
from vpython import color, scene, sphere, vec, box

from constants import FPS


stop_event = threading.Event()

@dataclass
class Player:
	id: int
	username: str
	pos: tuple[float, float] = (0, 0)
	rot: tuple[float, float] = (0, 0)

room: dict[int, Player] = {}