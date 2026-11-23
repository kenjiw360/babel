import threading

from vpython import box, sphere, vector, color, label, compound, sin, cos, standardAttributes

stop_event = threading.Event()
id: list[int] = []

class Player:
	id: int
	username: str
	pos: tuple[float, float]
	tag: label
	body: compound
	attachments: list[tuple[standardAttributes, vector]]

	def __init__(self, pid: int, username: str, x: float, z: float, yaw: float):
		self.id = pid
		base = box(pos=vector(0, 0.65, 0), size=vector(0.5, 1.3, 0.5), color=color.blue)
		eye1 = sphere(pos=vector(0.25, 1.1, 0.1), color=color.black, radius=0.075)
		eye2 = sphere(pos=vector(0.25, 1.1, -0.1), color=color.black, radius=0.075)
		self.tag = label(text="JorgeLuisBorges")
		self.body = compound([base, eye1, eye2], origin=vector(0, 0, 0))
		self.attachments = [(self.tag, vector(0, 1.5, 0))]
		self.setUsername(username)
		self.setPos(x, z, yaw)
	
	def setPos(self, x: float, z: float, yaw: float):
		self.pos = (x, z)
		self.body.pos = vector(x, 0, z)
		self.body.axis = vector(cos(yaw), 0, sin(yaw))
		for attachment, pos in self.attachments:
			attachment.pos = self.body.compound_to_world(pos)
	
	def setUsername(self, username: str):
		self.tag.text = self.username = username
	
	def hide(self):
		self.body.visible = False
		for attachment, _ in self.attachments:
			attachment.visible = False

room: dict[int, Player] = {}
room_lock = threading.Lock()
