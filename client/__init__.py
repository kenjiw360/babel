import threading

from vpython import box, sphere, vec, color, label, compound, sin, cos

stop_event = threading.Event()
id: list[int] = []

class Player:
	id: int
	username: str
	pos: tuple[float, float]

	def __init__(self, pid: int, username: str, x: float, z: float, yaw: float):
		self.id = pid
		base = box(pos=vec(0, 0.65, 0), size=vec(0.5, 1.3, 0.5), color=color.blue)
		eye1 = sphere(pos=vec(0.25, 1.1, 0.1), color=color.black, radius=0.075)
		eye2 = sphere(pos=vec(0.25, 1.1, -0.1), color=color.black, radius=0.075)
		self.tag = label(text="JorgeLuisBorges")
		self.body = compound([base, eye1, eye2], origin=vec(0, 0, 0))
		self.attachments = [(self.tag, vec(0, 1.5, 0))]
		self.setUsername(username)
		self.setPos(x, z, yaw)
	
	def setPos(self, x: float, z: float, yaw: float):
		self.pos = (x, z)
		self.body.pos = vec(x, 0, z)
		self.body.axis = vec(cos(yaw), 0, sin(yaw))
	
	def setUsername(self, username: str):
		self.tag.text = self.username = username
	
	def hide(self):
		self.body.visible = False
		for attachment, _ in self.attachments:
			attachment.visible = False

room: dict[int, Player] = {}