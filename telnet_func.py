# from loguru import logger
from telnetlib import Telnet

host = "46.149.176.84"  # VPN
port = 1723
timeout = 1


def telnet_connection():
	try:
		with Telnet(host=host, port=port, timeout=timeout) as telnet:
			telnet.close()
			result = "Success"
	except TimeoutError as ex:
		# logger.warning(f"Timeout Error occurred ({timeout} sec.): {ex}")
		result = "TimeoutError"
	except ConnectionRefusedError as ex:
		# logger.warning(f"Connection Refused Error occurred: {ex}")
		result = "ConnectionRefusedError"
	except Exception as ex:
		# logger.warning(f"Exception occurred: {ex}")
		result = "AnotherException"

	return result
