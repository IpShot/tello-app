from time import time

class Action:
    MOVE = 1
    STOP = 2

class Route:
    '''
    Module for creating flight routes and use them
    '''
    def __init__(self, drone, controller):
        self.drone = drone
        self.route = []
        self.route_name = 'default_route_' + time()
        self.is_creating_new = False
        self.is_going = False
        self.time_point = 0

    def _capture_time(self):
        t = time()
        diff = t - self.time_point
        self.time_point = t
        return diff

    def start_creating_new(self, route_name):
        self.route_name = route_name
        self.route = []
        self.time_point = time()

    def capture_move(self, rc):
        self.route.append({
            'action': Action.MOVE,
            'time': self._capture_time(),
            'rc': rc
        })

    def capture_stop_point(self):
        self.route.append({ 'action': Action.STOP })

    def finish_creating_new(self):
        self.time_point = 0

    def start(self, route_name):
        pass

    def stop(self):
        pass
