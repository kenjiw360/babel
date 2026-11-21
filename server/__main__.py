from constants import HOST, PORT
from server.handler import Handler
from server.server import Server

with Server((HOST, PORT), Handler) as server:
	ip, port = server.server_address[:2]
	print(f"Server running on {ip}:{port}")
	server.serve_forever()