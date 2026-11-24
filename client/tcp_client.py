import logging

from client import stop_event
from client.event_handlers import event_handlers
from client.tcp_socket import recv, sock
from settings import client_settings

logger = logging.getLogger(__name__)

def tcp_client():
	sock.connect(client_settings.connection)
	while not stop_event.is_set():
		try: event, data = recv()
		except TimeoutError: continue
		except Exception:
			logger.exception("TCP client error")
			raise
		event_handlers[event](*data)
	sock.close()