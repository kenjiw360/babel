import socketserver
import struct
import threading
from typing import TYPE_CHECKING

from constants import SERVER_FORMATS

if TYPE_CHECKING:
	from server.handler import Handler

class Server(socketserver.ThreadingTCPServer):
	allow_reuse_address = True
	daemon_threads = True

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.id_counter = 0
		self.id_lock = threading.Lock()
		self.clients: dict[int, Handler] = {}
		self.clients_lock = threading.Lock()

	def register_client(self, client):
		with self.clients_lock, self.id_lock:
			self.id_counter += 1
			self.clients[self.id_counter] = client
			return self.id_counter

	def unregister_client(self, id: int):
		with self.clients_lock:
			del self.clients[id]

	def broadcast(self, event, *data):
		buf = struct.pack(SERVER_FORMATS[event], *data)
		with self.clients_lock:
			for client in self.clients.values(): client.send_raw(buf)

	@property
	def client_list(self):
		return list(self.clients.values())