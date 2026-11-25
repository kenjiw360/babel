from threading import Lock

from client.state import state
from vpython import (
	box,
	color,
	compound,
	cos,
	label,
	sin,
	sphere,
	standardAttributes,
	vector,
)

class PlayerModel:
	owner: int = -1
	tag: label
	body: compound
	attachments: list[tuple[standardAttributes, vector, vector | None]]

	def __init__(self, username: str, rgb: vector, x: float, z: float, yaw: float):
		base = box(pos=vector(0, 0.65, 0), size=vector(0.5, 1.3, 0.5), color=color.white)
		eye1 = sphere(pos=vector(0.25, 1.1, 0.1), color=color.black, radius=0.075)
		eye2 = sphere(pos=vector(0.25, 1.1, -0.1), color=color.black, radius=0.075)
		self.tag = label(text="JorgeLuisBorges")
		self.body = compound([base, eye1, eye2], origin=vector(0, 0, 0))
		self.attachments = [(self.tag, vector(0, 1.5, 0), None)]
		self.setInfo(username, rgb)
		self.setPos(x, z, yaw)

	def setInfo(self, username: str, color: vector):
		self.tag.text = self.username = username
		self.body.color = color

	def setPos(self,  x: float, z: float, yaw: float):
		self.body.pos = vector(x, 0, z)
		self.body.axis = vector(cos(yaw), 0, sin(yaw))
		for attachment, pos, rot in self.attachments:
			if attachment is self.tag: attachment.pos = self.body.pos + pos
			else:
				attachment.pos = self.body.compound_to_world(pos)
				if rot is not None: attachment.axis = rot.rotate(angle=yaw, axis=vector(0, 1, 0))

	def available(self):
		return self.owner == -1

	def setOwner(self, owner: int):
		self.owner = owner
		self._set_visibility(owner != state.id)

	def free(self):
		self.owner = -1
		self._set_visibility(False)

	def _set_visibility(self, visibility):
		self.body.visible = visibility
		for attachment, _, _ in self.attachments:
			attachment.visible = visibility

models: list[PlayerModel] = []

class Player:
	id: int
	username: str
	color: vector
	pos: tuple[float, float]
	rot: float
	model: PlayerModel

	def __init__(self, pid: int, username: str, r: float, g: float, b: float, x: float, z: float, yaw: float):
		self.id = pid
		try: self.model = next(filter(lambda m: m.available(), models))
		except BaseException:
			self.model = PlayerModel(username, vector(r, g, b), x, z, yaw)
			models.append(self.model)
		self.model.setOwner(self.id)
		self.setInfo(username, r, g, b)
		self.setPos(x, z, yaw)
	
	def setPos(self, x: float, z: float, yaw: float):
		self.pos = (x, z)
		self.rot = yaw
		self.model.setPos(x, z, yaw)
	
	def setInfo(self, username: str, r: float, g: float, b: float):
		self.username = username
		self.color = vector(r, g, b)
		self.model.setInfo(username, self.color)

	def destroy(self):
		self.model.free()
		room.pop(self.id)
		del self

room: dict[int, Player] = {}
room_lock = Lock()