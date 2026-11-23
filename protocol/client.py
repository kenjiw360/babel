from collections.abc import Callable
from enum import IntEnum


class ClientEvents(IntEnum):
	USERNAME = 0
	POSITION = 1

client_event_headers: dict[ClientEvents, Callable[..., str]] = {
	ClientEvents.USERNAME: lambda *_: "!15s",
	ClientEvents.POSITION: lambda *_: "!3d"
}