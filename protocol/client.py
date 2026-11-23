from collections.abc import Callable
from enum import IntEnum


class ClientEvents(IntEnum):
	INFO = 0
	POSITION = 1

client_event_headers: dict[ClientEvents, Callable[..., str]] = {
	ClientEvents.INFO: lambda *_: "!15s3d",
	ClientEvents.POSITION: lambda *_: "!3d"
}