from collections.abc import Callable
from enum import IntEnum


class ServerEvents(IntEnum):
	ROOM_INFO = 0
	PLAYER_JOIN = 1
	PLAYER_LEAVE = 2
	PLAYER_USERNAME = 3
	PLAYER_POSITION = 4

server_event_headers: dict[ServerEvents, Callable[..., str]] = {
	ServerEvents.ROOM_INFO: lambda *args: f"!I{"I3d15s" * (len(args) // 5)}",
	ServerEvents.PLAYER_JOIN: lambda *_: "!I3d15s",
	ServerEvents.PLAYER_LEAVE: lambda *_: "!I",
	ServerEvents.PLAYER_USERNAME: lambda *_: "!I15s",
	ServerEvents.PLAYER_POSITION: lambda *_: "!I3d"
}