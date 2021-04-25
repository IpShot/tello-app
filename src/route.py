from time import time

class Action:
    MOVE = 1
    STOP = 2

class Route:
    '''
    Module for creating flight routes and use them
    '''
    @staticmethod
    def _save_route(route_name, route):
        with open(route_name, 'w') as file:
            file.writelines("%s\n" % action for action in route)

    @staticmethod
    def _load_route(route_name):
        route = []
        with open(route_name, 'r') as file:
            # Remove linebreak and add action to the route
            places = [action.rstrip() for action in file.readlines()]
        return route

    def __init__(self, drone, controller):
        self.drone = drone
        self.route = []
        self.route_name = ''
        self.is_creating_new = False
        self.is_going = False
        self.last_capture_time = 0

    def _get_duration(self):
        t = time()
        diff = t - self.last_capture_time
        self.last_capture_time = t
        return diff

    def start_creating_new(self, route_name = 'default_route_' + time()):
        self.route_name = route_name
        self.route = []
        self.last_capture_time = time()
        self.is_creating_new = True

    def capture_move(self, rc):
        self.route.append({
            'action': Action.MOVE,
            'duration': self._get_duration(),
            'values': rc
        })

    def capture_stop_point(self):
        self.route.append({ 'action': Action.STOP })

    def finish_creating_new(self):
        Route._save_route(self.route_name, self.route)
        self.is_creating_new = False

    def start(self, route_name):
        self.route = Route._load_route(route_name)
        self.is_going = True

    def stop(self):
        self.is_going = False
