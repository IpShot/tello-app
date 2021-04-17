import sys
import traceback
import time
import pygame
from djitellopy import Tello
from controller import Controller

def main():
	tello = Tello()
	controller = Controller(tello)

	# tello.connect()
	# tello.set_speed(10)

	try:
		print ('Looking for joystick...')
		while True:
			time.sleep(1)
			if pygame.joystick.get_count() != 0:
				ds4 = pygame.joystick.Joystick(0)
				ds4.init()
				print('Joystick name: ' + ds4.get_name())
				break

		while True:
			time.sleep(0.01)
			for e in pygame.event.get():
				print (e)
				# controller.event(e)
	except KeyboardInterrupt as e:
		print(e)
	except Exception as e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		print(e)


if __name__ == '__main__':
	main()
