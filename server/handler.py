import socketserver
import struct

from collections.abc import Callable
from itertools import chain
from typing import Any, cast
from vpython import pi

from protocol import HEADER_FORMAT, HEADER_SIZE
from protocol.client import ClientEvents
from protocol.server import ServerEvents, server_event_headers
from server.server import Server


class Handler(socketserver.BaseRequestHandler):
	id: int
	username: str
	color: tuple[float, float, float] = (0.0, 0.0, 1.0)
	pos: tuple[float, float, float] = (0.0, 0.0, 0.5 * pi)

	def setup(self):
		self.id = self.game_server.register_client(self)
		self.username = f"Client {self.id}"
		print(f"Client {self.id} connected from {self.client_address}")
		with self.game_server.clients_lock:
			self.send(ServerEvents.ROOM_INFO, (self.id, *chain.from_iterable((client.id, *client.pos, client.username.encode("ASCII"), *client.color) for client in self.game_server.client_list)))
		self.broadcast(ServerEvents.PLAYER_JOIN, (self.id, *self.pos, self.username.encode("ASCII"), *self.color))
				

	def finish(self):
		print(f"Client {self.id} ({self.username}): disconnected")
		self.game_server.unregister_client(self.id)
		self.broadcast(ServerEvents.PLAYER_LEAVE, (self.id,))
	
	def handle(self):
		while True:
			try: event, data = self.recv()
			except Exception: break
			self.event_handlers[event](*data)

	@property
	def event_handlers(self) -> dict[ClientEvents, Callable[..., Any]]:
		return {
			ClientEvents.INFO: self.handle_info,
			ClientEvents.POSITION: self.handle_position
		}

	def handle_info(self, username: bytes, r: float, g: float, b: float):
		self.username = username.rstrip(b"\x00").decode("ASCII")
		self.color = (r, g, b)
		self.broadcast(ServerEvents.PLAYER_INFO, (self.id, username, r, g, b))
		print(f"Client {self.id}: username={self.username}")

	def handle_position(self, x: float, z: float, yaw: float):
		self.pos = (x, z, yaw)
		self.broadcast(ServerEvents.PLAYER_POSITION, (self.id, x, z, yaw))
		
	def recv(self):
		raw_header = self.recv_size(HEADER_SIZE)
		if not raw_header: raise ValueError
		event, format_length = struct.unpack(HEADER_FORMAT, raw_header)
		try: event = ClientEvents(event)
		except ValueError: raise ValueError
		
		raw_format = self.recv_size(format_length)
		if not raw_format: raise ValueError
		format: str = struct.unpack(f"{format_length}s", raw_format)[0].decode("ASCII")
		
		raw_data = self.recv_size(struct.calcsize(format))
		if not raw_data: raise ValueError
		data = struct.unpack(format, raw_data)
		
		return (event, data)
	
	def recv_size(self, size: int):
		buf = bytearray()
		while len(buf) < size:
			chunk = self.request.recv(size - len(buf))
			if not chunk: return None
			buf.extend(chunk)
		return bytes(buf)

	def broadcast(self, event: ServerEvents, data: tuple[Any, ...]):
		self.game_server.broadcast(event, data, exclude=(self.id,))

	def send(self, event: ServerEvents, data: tuple[Any, ...]):
		self.send_raw(
			struct.pack(HEADER_FORMAT, event, N := len(format := server_event_headers[event](*data))) +
			struct.pack(f"{N}s", format.encode("ASCII")) +
			struct.pack(format, *data)
		)

	def send_raw(self, buf: bytes):
		self.request.sendall(buf)

	@property
	def game_server(self) -> Server:
		return cast(Server, self.server)