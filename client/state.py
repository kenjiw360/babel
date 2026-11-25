from dataclasses import dataclass

from vpython import cos, sin, vector


@dataclass
class Pair[T]:
	a: T
	b: T

	@staticmethod
	def from_vec(vec: vector):
		return Pair(vec.x, vec.z)

	def __add__(self, other: "Pair"):
		return Pair(self.a + other.a, self.b + other.b)
	
	def __sub__(self, other: "Pair"):
		return Pair(self.a - other.a, self.b - other.b)
	
	def __mul__(self, other):
		return Pair(self.a * other, self.b * other)

	@property
	def tuple(self):
		return (self.a, self.b)

class State:
	id: int = -1
	room_id: Pair[int]
	relative_pos: Pair[float]
	rot: Pair[float]
	
	def __init__(self):
		self.room_id = Pair(0, 0)
		self.relative_pos = Pair(0, 0)
		self.rot = Pair(0, 0)

	def set_id(self, id: int):
		self.id = id

	def global_pos(self) -> tuple[float, float]:
		return (0, 0)
	
	def move(self, offset: vector):
		self.relative_pos += Pair[float](offset.x, offset.z)
		# collision + teleportation stuff
		# subtract by door midpoint * 2

	@property
	def cam_pos(self):
		return vector(self.relative_pos.a, 1, self.relative_pos.b)

	@property
	def cam_rot(self):
		return vector(cos(self.rot.a) * cos(self.rot.b), sin(self.rot.b), sin(self.rot.a) * cos(self.rot.b))

	@property
	def tcp_pos(self):
		return self.relative_pos.tuple + (self.rot.a,)

state = State()