import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		data = self.request[0].strip()
		socket = self.request[1]
		print(f"{self.client_address[0]} wrote:")
		print(data)
		socket.sendto(data.upper(), self.client_address)

HOST = "0.0.0.1"
PORT = 9999
socketserver.UDPServer((HOST, PORT), MyUDPHandler).serve_forever()