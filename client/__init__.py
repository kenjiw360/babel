import threading

from vpython import box, sphere, vector, color, label, compound, sin, cos, standardAttributes

id: list[int] = []
stop_event = threading.Event()

class Player:
	id: int
	username: str
	color: tuple[float, float, float]
	pos: tuple[float, float]
	tag: label
	body: compound
	attachments: list[tuple[standardAttributes, vector, vector | None]]

	def __init__(self, pid: int, username: str, r: float, g: float, b: float, x: float, z: float, yaw: float):
		self.id = pid
		base = box(pos=vector(0, 0.65, 0), size=vector(0.5, 1.3, 0.5), color=vector(r, g, b))
		eye1 = sphere(pos=vector(0.25, 1.1, 0.1), color=color.black, radius=0.075)
		eye2 = sphere(pos=vector(0.25, 1.1, -0.1), color=color.black, radius=0.075)
		self.tag = label(text="JorgeLuisBorges")
		self.body = compound([base, eye1, eye2], origin=vector(0, 0, 0))
		self.attachments = [(self.tag, vector(0, 1.5, 0), None)]
		self.setInfo(username, r, g, b)
		self.setPos(x, z, yaw)
	
	def setPos(self, x: float, z: float, yaw: float):
		self.pos = (x, z)
		self.body.pos = vector(x, 0, z)
		self.body.axis = vector(cos(yaw), 0, sin(yaw))
		for attachment, pos, rot in self.attachments:
			if attachment is self.tag: attachment.pos = self.body.pos + pos
			else:
				attachment.pos = self.body.compound_to_world(pos)
				if rot is not None: attachment.axis = rot.rotate(angle=yaw, axis=vector(0, 1, 0))
	
	def setInfo(self, username: str, r: float, g: float, b: float):
		self.tag.text = self.username = username
		self.color = (r, g, b)
	
	def hide(self):
		self.body.visible = False
		for attachment, _, _ in self.attachments:
			attachment.visible = False

room: dict[int, Player] = {}
room_lock = threading.Lock()