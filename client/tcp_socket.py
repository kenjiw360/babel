import socket
import struct
from typing import Any

from protocol import HEADER_FORMAT, HEADER_SIZE
from protocol.client import ClientEvents, client_event_headers
from protocol.server import ServerEvents

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
sock.settimeout(0.2)

def send(event: ClientEvents, data: tuple[Any, ...]):
	sock.sendall(
		struct.pack(HEADER_FORMAT, event, N := len(format := client_event_headers[event](*data))) +
		struct.pack(f"{N}s", format.encode("ASCII")) +
		struct.pack(format, *data)
	)

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