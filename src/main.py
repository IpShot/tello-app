import sys
import traceback
import time
import pygame
import pygame.locals
from djitellopy import Tello
from controller import Controller

def main():
	dev = False
	tello = Tello()

	if not dev:
		tello.connect()
		tello.streamoff()
		tello.streamon()

	controller = Controller(tello, dev=dev)

	# Update drone state (send a command) every 20 milliseconds
	pygame.time.set_timer(pygame.USEREVENT + 1, 20)

	try:
		print ('Looking for joystick...')
		if pygame.joystick.get_count() > 0:
			ds4 = pygame.joystick.Joystick(0)
			ds4.init()
			print('Joystick connected: ' + ds4.get_name())
		else:
			print('Joystick hasn\'t connected')
			exit(0)

		while True:
			for e in pygame.event.get():
				if e.type == pygame.USEREVENT + 1:
					controller.update()
				else:
					controller.handle_event(e)

	except KeyboardInterrupt as e:
		pass
	except Exception as e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		print(e)

	if not dev:
		tello.end()


if __name__ == '__main__':
	main()
