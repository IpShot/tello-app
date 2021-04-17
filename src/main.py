import sys
import traceback
import time
import pygame
import pygame.locals
from djitellopy import Tello
from controller import Controller

def main():
	tello = Tello()
	controller = Controller(tello, mock=True)

	try:
		print ('Looking for joystick...')
		while True:
			time.sleep(1)
			if pygame.joystick.get_count() != 0:
				ds4 = pygame.joystick.Joystick(0)
				ds4.init()
				print('Joystick connected: ' + ds4.get_name())
				break

		tello.connect()

		while True:
			time.sleep(0.01)
			controller.update()
			for e in pygame.event.get():
				controller.handle_event(e)

	except KeyboardInterrupt as e:
		print(e)
	except Exception as e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		print(e)

	tello.end()


if __name__ == '__main__':
	main()
