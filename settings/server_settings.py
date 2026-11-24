class ServerSettings:
	connection: tuple[str, int]
	book_len: int
	def __init__(self, data):
		self.connection = (data["server"]["host"], data["server"]["port"])
		self.book_len = data["server"]["book_len"]