from os import path
from time import time
from threading import Thread

class Action:
    MOVE = 1
    STOP = 2

class Route:
    '''
    Module for creating flight routes and use them
    '''
    @staticmethod
    def _save_route(route_name, route):
        file = path.relpath('routes/' + route_name + '.txt')
        print(file)
        with open(file, 'w') as file:
            file.writelines("%s\n" % action for action in route)

    @staticmethod
    def _load_route(route_name):
        route = []
        file = path.relpath('routes/' + route_name + '.txt')
        print(file)
        with open(file, 'r') as file:
            # Remove linebreak and add action to the route
            route = [eval(action.rstrip()) for action in file.readlines()]
        return route

    def __init__(self, drone, controller):
        self.drone = drone
        self.controller = controller
        self._reset()

    def _reset(self):
        self.route = []
        self.route_name = ''
        self.is_creating_new = False
        self.is_going = False
        self.is_stop_point = False
        self.going_direction = 1
        self.last_capture_time = 0
        self.command_number = 0

    def _get_duration(self):
        t = time()
        diff = t - self.last_capture_time
        self.last_capture_time = t
        return diff

    def capture_move(self, rc):
        if self.is_creating_new:
            self.route.append({
                'action': Action.MOVE,
                'duration': self._get_duration(),
                'values': rc
            })

    def capture_stop_point(self):
        if self.is_creating_new and self.route[-1]['action'] is not Action.STOP:
            self.route.append({ 'action': Action.STOP })

    def start_creating_new(self, route_name = 'default_route_' + str(time())):
        if not self.is_creating_new:
            print('start creating new route')
            self._reset()
            self.route_name = route_name
            self.last_capture_time = time()
            self.is_creating_new = True

    def finish_creating_new(self):
        if self.is_creating_new:
            print('finish creating new route')
            Route._save_route(self.route_name, self.route)
            self._reset()

    def _freeze_moving(self):
        self.is_stop_point = True

    def _continue_moving(self):
        self.is_stop_point = False

    def _exec_command(self, command):
        if command['action'] == Action.MOVE:
            self.controller.set_move(command['values'])
            return time() + command['duration']
        elif command['action'] == Action.STOP:
            self._freeze_moving()
        return -1

    def _exec_route(self):
        command_number = 0
        finish_time = -1
        while self.is_going:
            if not self.is_stop_point and (finish_time == -1 or time() >= finish_time):
                if (# Move on route in forward direction
                    self.going_direction > 0 and command_number < len(self.route) or
                    # Move on route in backward direction
                    self.going_direction < 0 and command_number > 0
                ):
                    command_number += self.going_direction
                    finish_time = self._exec_command(self.route[command_number])
                elif self.going_direction < 0 and command_number == 0:
                    break
        self.stop()

    def start(self, route_name):
        if not self.is_going:
            print('start route')
            self.is_going = True
            self.route = Route._load_route(route_name)
            thread = Thread(target=self._exec_route)
            thread.start()

    def stop(self):
        print('stop route')
        self.controller.freeze()
        self._reset()

    def next_stop_point(self):
        print('next step point')
        self.going_direction = 1
        self._continue_moving()

    def prev_stop_point(self):
        print('prev step point')
        self.going_direction = -1
        self._continue_moving()
