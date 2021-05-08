import sys
import traceback
import time
from djitellopy import Tello
from controller import Controller, DS4
from route import Route
from app import App
from media import Media

class DroneMock:
    def send_rc_control(self, *args):
        pass
    def set_speed(self, speed):
        print(f'set speed {speed} cm/s')
    def takeoff(self):
        print('take off')
    def land(self):
        print('land')
    def emergency(self):
        print('emergency turn off')
    def get_battery(self):
        return -1
    def temperature(self):
        return -1
    def get_frame_read(self):
        pass

def main():
    dev = True
    drone = Tello() if not dev else DroneMock()

    if not dev:
        drone.connect()
        drone.streamoff()
        drone.streamon()

    controller = Controller(drone)
    route = Route(controller)
    media = Media(drone)
    app = App(controller, route, media)

    try:
        print(f'Drone battery: {drone.get_battery()}%')
        print(f'Drone temperature: {drone.temperature()}C')
        app.start()
    except KeyboardInterrupt as e:
        pass
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(e)

    app.stop()

    if not dev:
        drone.end()


if __name__ == '__main__':
    main()
