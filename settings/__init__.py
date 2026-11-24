import yaml

from settings.client_settings import ClientSettings
from settings.server_settings import ServerSettings

with open("config.yml", "r", encoding="utf-8") as file:
	data = yaml.safe_load(file)

server_settings = ServerSettings(data)
client_settings = ClientSettings(data)