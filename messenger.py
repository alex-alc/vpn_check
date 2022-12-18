from dotenv import dotenv_values
import pywhatkit

config = dotenv_values(".env")
phone_number_1 = str(config['PHONE_NUMBER_1'])


def notification(msg, sending_h, sending_m):
	pywhatkit.sendwhatmsg(phone_number_1, msg, sending_h, sending_m, tab_close=True)
