from collections.abc import Callable
from itertools import batched
import socket
import struct
from typing import Any

from client import stop_event, room, Player
from constants import HOST, PORT, USERNAME
from protocol import HEADER_FORMAT, HEADER_SIZE
from protocol.client import ClientEvents, client_event_headers
from protocol.server import ServerEvents

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(0.2)
id: int

def send(event: ClientEvents, data: tuple[Any, ...]):
	format = client_event_headers[event](*data)
	sock.sendall(struct.pack(HEADER_FORMAT, event, N := len(format)))
	sock.sendall(struct.pack(f"{N}s", format.encode("ASCII")))
	sock.sendall(struct.pack(format, *data))

def room_info(cid: int, *args):
	global id
	id = cid
	for pid, x, z, yaw, pitch, username in batched(args, 6):
		room[pid] = Player(pid, username.rstrip(b"\x00").decode("ASCII"), (x, z), (yaw, pitch))
	print(room)

def player_username(pid: int, username: bytes):
	room[pid].username = username.rstrip(b"\x00").decode("ASCII")

def player_position(pid: int, x: float, z: float, yaw: float, pitch: float):
	room[pid].pos = (x, z)
	room[pid].rot = (yaw, pitch)

event_handlers: dict[ServerEvents, Callable[..., Any]] = {
	ServerEvents.ROOM_INFO: room_info,
	ServerEvents.PLAYER_USERNAME: player_username,
	ServerEvents.PLAYER_POSITION: player_position
}

def recv_size(size: int):
	buf = bytearray()
	while len(buf) < size:
		chunk = sock.recv(size - len(buf))
		if not chunk: return None
		buf.extend(chunk)
	return bytes(buf)

def recv():
	raw_header = recv_size(HEADER_SIZE)
	if not raw_header: raise ValueError
	event, format_length = struct.unpack(HEADER_FORMAT, raw_header)
	event = ServerEvents(event)
	
	raw_format = recv_size(format_length)
	if not raw_format: raise ValueError
	format: str = struct.unpack(f"{format_length}s", raw_format)[0].decode("ASCII")
	
	raw_data = recv_size(struct.calcsize(format))
	if not raw_data: raise ValueError
	data = struct.unpack(format, raw_data)
	
	return (event, data)

def tcp_client():
	sock.connect((HOST, PORT))
	send(ClientEvents.USERNAME, (USERNAME.encode("ASCII"),))
	while not stop_event.is_set():
		try: event, data = recv()
		except TimeoutError: continue
		except Exception: return stop_event.set()
		event_handlers[event](*data)
	sock.close()