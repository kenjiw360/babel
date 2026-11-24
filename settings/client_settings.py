class ClientSettings:
	fps: int
	turn_speed: float
	connection: tuple[str, int]
	def __init__(self, data):
		self.fps = data["client"]["fps"]
		self.turn_speed = data["client"]["camera_sensitivity"]
		self.connection = (data["client"]["connection"]["host"], data["client"]["connection"]["port"])