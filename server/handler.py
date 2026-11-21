import socketserver
import struct
from typing import cast

from constants import CLIENT_FORMATS, CLIENT_SIZE, HEADER_FORMAT, HEADER_SIZE, SERVER_FORMATS
from server.server import Server


class Handler(socketserver.BaseRequestHandler):
	id: int
	username: str

	def setup(self):
		self.id = self.game_server.register_client(self)
		self.username = f"Client {self.id}"
		print(f"Client {self.id} connected from {self.client_address}")

	def finish(self):
		print(f"Client {self.id} ({self.username}): disconnected")
		self.game_server.unregister_client(self.id)
	
	def handle(self):
		while True:
			event, data = self.recv()
			if event is None or data is None: break
			self.event_handlers[event](*data)

	def handle_username(self, username: str):
		print(f"Client {self.id} ({self.username}): username={username}")
		self.username = username

	def handle_position(self, x: float, y: float, z: float):
		print(f"Client {self.id} ({self.username}): pos=({x}, {y}, {z})")
		
	def recv(self):
		raw_header = self.recv_size(HEADER_SIZE)
		if not raw_header: return (None, None)
		header = struct.unpack(HEADER_FORMAT, raw_header)[0]
		if header >= len(CLIENT_FORMATS): return (None, None)
		raw_data = self.recv_size(CLIENT_SIZE[header])
		if not raw_data: return (None, None)
		data = struct.unpack(CLIENT_FORMATS[header], raw_data)
		return (header, data)
	
	def recv_size(self, size: int):
		buf = bytearray()
		while len(buf) < size:
			chunk = self.request.recv(size - len(buf))
			if not chunk: return None
			buf.extend(chunk)
		return bytes(buf)

	def send(self, event: int, *data):
		self.send_raw(struct.pack(SERVER_FORMATS[event], *data))

	def send_raw(self, buf: bytes):
		self.request.sendall(buf)

	@property
	def event_handlers(self):
		return [self.handle_username, self.handle_position]

	@property
	def game_server(self) -> Server:
		return cast(Server, self.server)