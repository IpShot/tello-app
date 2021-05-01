import pygame

class Manager:
    """
    Module for managing events
    """
    def __init__(self, controller, route):
        self.controller = controller
        self.route = route

        # Update drone state (send a command) every 20 milliseconds
        pygame.time.set_timer(pygame.USEREVENT + 1, 20)

    def handle_event(self, e):
        if e.type == pygame.USEREVENT + 1:
            move_data = self.controller.update()
        else:
            self.controller.handle_event(e, self.route)

    def start(self):
        joystick_connected = False
        print ('Looking for joystick...')
        while True:
            if not joystick_connected and pygame.joystick.get_count() > 0:
                ds4 = pygame.joystick.Joystick(0)
                ds4.init()
                print('Joystick connected: ' + ds4.get_name())
                joystick_connected = True

            if joystick_connected:
                for e in pygame.event.get():
                    manager.handle_event(e)
