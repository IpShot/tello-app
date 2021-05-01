import sys
import traceback
import time
from djitellopy import Tello
from controller import Controller, DS4
from route import Route
from manager import Manager

def main():
    dev = True
    drone = Tello()

    if not dev:
        drone.connect()
        drone.streamoff()
        drone.streamon()

    controller = Controller(drone, dev=dev)
    route = Route(drone, controller)
    manager = Manager(controller, route)

    try:
        manager.start()
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
