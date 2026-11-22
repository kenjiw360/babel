from itertools import count
import socketserver
import struct
import threading
from typing import TYPE_CHECKING, Any

from protocol import HEADER_FORMAT
from protocol.server import ServerEvents, server_event_headers

if TYPE_CHECKING:
	from server.handler import Handler

class Server(socketserver.ThreadingTCPServer):
	allow_reuse_address = True
	daemon_threads = True

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.clients: dict[int, Handler] = {}
		self.clients_lock = threading.Lock()

	def register_client(self, client):
		with self.clients_lock:
			id_set = set(self.clients.keys())
			id = next(i for i in count(1) if i not in id_set)
			self.clients[id] = client
			return id

	def unregister_client(self, id: int):
		with self.clients_lock:
			del self.clients[id]

	def broadcast(self, event: ServerEvents, data: tuple[Any, ...], exclude=()):
		format = server_event_headers[event](*data)
		buf = struct.pack(format, *data)
		N = len(format)
		with self.clients_lock:
			for client in self.clients.values():
				if client.id in exclude: continue
				client.send_raw(struct.pack(HEADER_FORMAT, event, N))
				client.send_raw(struct.pack(f"{N}s", format.encode("ASCII")))
				client.send_raw(buf)

	@property
	def client_list(self):
		return list(self.clients.values())