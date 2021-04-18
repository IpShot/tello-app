import pygame

class DS4:
    ARROW_UP = (0, 1)
    ARROW_DOWN = (0, -1)
    ARROW_LEFT = (-1, 0)
    ARROW_RIGHT = (1, 0)

    SQUARE = 0
    CROSS = 1
    CIRCLE = 2
    TRIANGLE = 3

    L1 = 4
    R1 = 5
    L2 = 6
    R2 = 7

    SHARE = 8
    OPTIONS = 9

    LEFT_JOY_PRESS = 10
    RIGHT_JOY_PRESS = 11

    # axis
    LEFT_JOY_X = 0
    LEFT_JOY_Y = 1
    RIGHT_JOY_X = 2
    RIGHT_JOY_Y = 5
    L2_AXIS = 3 # between -1 (unpressed) ~ 1 (pressed)
    R2_AXIS = 4 # between -1 (unpressed) ~ 1 (pressed)

    DEADZONE = 0.2

class DroneMock:
    def send_rc_control(self, *args):
        pass
    def set_speed(self, *args):
        pass
    def takeoff(self):
        pass
    def land(self):
        pass

class Controller:
    def __init__(self, drone, speed=50, dev=False, logs=True):
        pygame.init()
        pygame.joystick.init()

        self.logs = logs
        self.drone = DroneMock() if dev else drone

        # Drone velocities between -100~100
        self.forward_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.rotate_velocity = 0
        self.prev_velocities = (0, 0, 0, 0)
        self.speed = speed
        self.rc_control_enabled = False
        self.drone.set_speed(speed)


    def get_motion_speed(self, v):
        return 0 if abs(v) <= DS4.DEADZONE else int(round(v * self.speed))

    def move_left_right(self, v):
        self.left_right_velocity = self.get_motion_speed(v)

    def move_forward_back(self, v):
        self.forward_back_velocity = self.get_motion_speed(-v)

    def move_up_down(self, v):
        self.up_down_velocity = self.get_motion_speed(-v)

    def rotate(self, v):
        self.rotate_velocity = self.get_motion_speed(v)

    def lock(self):
        self.rc_control_enabled = False

    def unlock(self):
        self.rc_control_enabled = True

    def stop(self):
        self.forward_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.rotate_velocity = 0
        self.update()
        self.lock()

    def handle_event(self, e):
        # Joystics
        if e.type == pygame.locals.JOYAXISMOTION:
            if e.axis == DS4.LEFT_JOY_X:
                self.move_left_right(e.value)
            elif e.axis == DS4.LEFT_JOY_Y:
                self.move_forward_back(e.value)
            elif e.axis == DS4.RIGHT_JOY_X:
                self.rotate(e.value)
            elif e.axis == DS4.RIGHT_JOY_Y:
                self.move_up_down(e.value)

        # Arrow buttons
        elif e.type == pygame.locals.JOYHATMOTION:
            if e.value == DS4.ARROW_UP:
                if not self.rc_control_enabled:
                    self.drone.takeoff()
                    self.rc_control_enabled = True
            elif e.value == DS4.ARROW_DOWN:
                if self.rc_control_enabled:
                    self.drone.land()
                    self.rc_control_enabled = False

        # All other buttons including joysticks press
        elif e.type == pygame.locals.JOYBUTTONDOWN:
            if e.button == DS4.CROSS:
                if self.drone.is_flying:
                    if self.rc_control_enabled:
                        self.stop()
                    else:
                        self.unlock()

        elif e.type == pygame.locals.JOYBUTTONUP:
            pass

    def send_rc(self, *args):
        if self.rc_control_enabled:
            if self.prev_velocities != args:
                self.prev_velocities = args
                self.log_motion()
                self.drone.send_rc_control(*args)

    def update(self):
        self.send_rc(
            self.left_right_velocity,
            self.forward_back_velocity,
            self.up_down_velocity,
            self.rotate_velocity
        )

    def log_motion(self):
        if not self.logs:
            return

        if self.left_right_velocity < 1:
            print('left: ' + str(-self.left_right_velocity))
        elif self.left_right_velocity > 1:
            print('right: ' + str(self.left_right_velocity))
        else:
            print('Stop left-right')

        if self.forward_back_velocity < 1:
            print('forward: ' + str(-self.forward_back_velocity))
        elif self.forward_back_velocity > 1:
            print('back: ' + str(self.forward_back_velocity))
        else:
            print('Stop forward-back')

        if self.up_down_velocity < 1:
            print('up: ' + str(-self.up_down_velocity))
        elif self.up_down_velocity > 1:
            print('down: ' + str(self.up_down_velocity))
        else:
            print('Stop up-down')

        if self.rotate_velocity < 1:
            print('rotate left: ' + str(-self.rotate_velocity))
        elif self.rotate_velocity > 1:
            print('rotate right: ' + str(self.rotate_velocity))
        else:
            print('Stop rotate')
