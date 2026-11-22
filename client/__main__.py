import os
import threading

from client import stop_event
from client.game import game
from client.tcp_client import tcp_client

thread_error: BaseException | None = None

def stop_on_except(f):
	def wrapper():
		global thread_error
		try: f()
		except BaseException as e: thread_error = e
		finally: stop_event.set()
	return wrapper

threads = [threading.Thread(target=stop_on_except(target), daemon=True) for target in [tcp_client, game]]

for t in threads: t.start()

try:
	stop_event.wait()
finally:
	stop_event.set()
	for t in threads: t.join(timeout=1.0)
	os._exit(1 if thread_error else 0)