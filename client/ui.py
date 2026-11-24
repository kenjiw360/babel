from vpython import button, color, scene, slider, vector, winput, wtext

from client.tcp_socket import send
from protocol.client import ClientEvents


class UI:
	def __init__(self):
		wtext(text="username: ")
		self.username_input = winput(bind=lambda: None)
		spacer()
		
		wtext(text="r: ")
		self.r_slider = slider(min=0, max=1, bind=self.set_button_color)
		spacer()
		
		wtext(text="g: ")
		self.g_slider = slider(min=0, max=1, bind=self.set_button_color)
		spacer()
		
		wtext(text="b: ")
		self.b_slider = slider(min=0, max=1, bind=self.set_button_color)
		self.b_slider.value = 1
		spacer()
		
		self.set_button = button(text="set player", bind=self.send_info)
		self.set_button_color()

	def send_info(self):
		if username := self.username_input.text:
			send(ClientEvents.INFO, (username.encode("ASCII"), self.r_slider.value, self.g_slider.value, self.b_slider.value))

	def set_button_color(self):
		r = self.r_slider.value
		g = self.g_slider.value
		b = self.b_slider.value
		self.set_button.background = vector(r, g, b)
		self.set_button.textcolor = vector(color.white if luminance(r, g, b) < 0.5 else color.black)

ui: UI | None = None

def initialize_ui():
	global ui
	ui = UI()

def luminance(r: float, g: float, b: float):
	return r * 0.299 + g * 0.587 + b * 0.114

def spacer():
	scene.append_to_caption("\n")