from ping3 import ping
from dotenv import dotenv_values

host = dotenv_values(".env")["HOST"]


def check_connection():
	"""Check if the host is reachable"""
	if ping(host) is None:
		return False
	else:
		resp = ping(host, unit="ms")
		return resp
