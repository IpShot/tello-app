import sys
import traceback
import time
import pygame
import pygame.locals
from djitellopy import Tello
from controller import Controller, DS4
from route import Route

def main():
	dev = False
	drone = Tello()

	if not dev:
		drone.connect()
		drone.streamoff()
		drone.streamon()

	controller = Controller(drone, dev=dev)
	route = Route(drone, controller)

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
					move_data = controller.update()
				else:
					controller.handle_event(e, route)

	except KeyboardInterrupt as e:
		pass
	except Exception as e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		print(e)

	if not dev:
		drone.end()


if __name__ == '__main__':
	main()
