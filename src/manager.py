import pygame

class Manager:
    """
    Module for managing events
    """
    def __init__(self, controller, route):
        self.controller = controller
        self.route = route

    def handle_event(self, e):
        if e.type == pygame.USEREVENT + 1:
            move_data = self.controller.update()
        else:
            self.controller.handle_event(e, self.route)

    def start(self):
        pygame.init()
        # Update drone state (send a command) every 20 milliseconds
        pygame.time.set_timer(pygame.USEREVENT + 1, 20)

        print ('Looking for joystick...')
        joystick_connected = False
        while True:
            if joystick_connected and pygame.joystick.get_count() == 0:
                self.controller.stop()
                joystick_connected = False
                print('Joystick disconnected')
                print ('Looking for joystick...')

            if not joystick_connected:
                pygame.joystick.quit()
                pygame.joystick.init()
                if pygame.joystick.get_count() > 0:
                    ds4 = pygame.joystick.Joystick(0)
                    ds4.init()
                    joystick_connected = True
                    print('Joystick connected: ' + ds4.get_name())
                    pygame.event.clear()

            if joystick_connected:
                for e in pygame.event.get():
                    self.handle_event(e)
