from collections.abc import Callable
from enum import IntEnum

class ServerEvents(IntEnum):
	ROOM_INFO = 0
	PLAYER_USERNAME = 1
	PLAYER_POSITION = 2

server_event_headers: dict[ServerEvents, Callable[..., str]] = {
	ServerEvents.ROOM_INFO: lambda *args: f"!I{"I4d15s" * (len(args) // 6)}",
	ServerEvents.PLAYER_USERNAME: lambda *_: "!I15s",
	ServerEvents.PLAYER_POSITION: lambda *_: "!I4d",
}