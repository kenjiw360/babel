from server.handler import Handler
from server.server import Server
from settings import server_settings

with Server(server_settings.connection, Handler) as server:
	ip, port = server.server_address[:2]
	print(f"Server running on {ip}:{port}")
	server.serve_forever()