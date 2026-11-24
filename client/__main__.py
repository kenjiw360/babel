import logging
import os
import threading

import client.ui
from client import stop_event
from client.game import game
from client.tcp_client import tcp_client

logger = logging.getLogger(__name__)
thread_error: BaseException | None = None

def stop_on_except(f):
	def wrapper():
		global thread_error
		try: f()
		except BaseException as e:
			logger.exception("Thread error")
			thread_error = e
		finally: stop_event.set()
	return wrapper

threads = [threading.Thread(target=stop_on_except(target), daemon=True) for target in [tcp_client, game]]

for t in threads: t.start()

try:
	stop_event.wait()
finally:
	stop_event.set()
	for t in threads: t.join(timeout=1.0)
	os._exit(int(thread_error is not None))