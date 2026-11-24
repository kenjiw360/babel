from collections.abc import Callable
from itertools import batched
from typing import Any

import client.ui
from client import Player, id, room, room_lock
from protocol.server import ServerEvents


def room_info(cid: int, *args):
	id.append(cid)
	if client.ui.ui: client.ui.ui.username_input.text = f"Client {cid}"
	with room_lock:
		for pid, x, z, yaw, username, r, g, b in batched(args, 8):
			room[pid] = Player(pid, username.rstrip(b"\x00").decode("ASCII"), r, g, b, x, z, yaw)
			if pid == id[0]: room[pid].hide()

def player_join(pid: int, x: float, z: float, yaw: float, username: bytes, r: float, g: float, b: float):
	with room_lock:
		room[pid] = Player(pid, username.rstrip(b"\x00").decode("ASCII"), r, g, b, x, z, yaw)

def player_leave(pid: int):
	with room_lock:
		room[pid].hide()
		del room[pid]

def player_info(pid: int, username: bytes, r: float, g: float, b: float):
	with room_lock:
		room[pid].setInfo(username.rstrip(b"\x00").decode("ASCII"), r, g, b)

def player_position(pid: int, x: float, z: float, yaw: float):
	with room_lock:
		room[pid].setPos(x, z, yaw)

event_handlers: dict[ServerEvents, Callable[..., Any]] = {
	ServerEvents.ROOM_INFO: room_info,
	ServerEvents.PLAYER_JOIN: player_join,
	ServerEvents.PLAYER_LEAVE: player_leave,
	ServerEvents.PLAYER_INFO: player_info,
	ServerEvents.PLAYER_POSITION: player_position
}