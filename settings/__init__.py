import os
import shutil

import yaml

from settings.client_settings import ClientSettings
from settings.server_settings import ServerSettings

CONFIG_PATH = "config.yml"
DEFAULT_CONFIG_PATH = "config.default.yml"

if not os.path.exists("config.yml"): shutil.copy(DEFAULT_CONFIG_PATH, CONFIG_PATH)
with open("config.yml", "r", encoding="utf-8") as file:
	data = yaml.safe_load(file)

server_settings = ServerSettings(data)
client_settings = ClientSettings(data)