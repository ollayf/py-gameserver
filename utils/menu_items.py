import pygame
import time

class PageItems(object):
    menu = None
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    response = None
    txt_surface = None

    def __init__(self):
        self.FONT = pygame.font.Font(None, 32)
        self.color = self.COLOR_INACTIVE

class InputBox(PageItems):

    def __init__(self, x, y, w, h, prompt=''):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.prompt = prompt
        self.prompt_surface = self.FONT.render(prompt, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.response = self.response[:-1]
                else:
                    if not event.unicode in ['\r', '\t']:
                        if self.response is None:
                            self.response = event.unicode
                        else:
                            new_response = self.response + event.unicode
                            # Re-render the response.
                            new_txt_surface = self.menu.FONT.render(new_response, True, self.color)
                            if new_txt_surface.get_width() <= self.rect.w:
                                self.response = new_response

        self.txt_surface = self.menu.FONT.render(self.response, True, self.color)

    def draw(self):
        # Blit the prompt
        self.menu.screen.blit(self.prompt_surface, (self.rect.x+5, self.rect.y-20))
        # Blit the response.
        if self.txt_surface:
            self.menu.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(self.menu.screen, self.color, self.rect, 2)

class Button(PageItems):
    def __init__(self, x, y, h, prompt=''):
        super().__init__()
        self.prompt = prompt
        self.prompt_surface = self.FONT.render(prompt, True, self.COLOR_ACTIVE)
        w = self.prompt_surface.get_width() + 10
        self.rect = pygame.Rect(x, y, w, h)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.menu.submit()
    
    def draw(self):
        # Blit the rect.
        pygame.draw.rect(self.menu.screen, self.color, self.rect)
        # Blit the prompt
        self.menu.screen.blit(self.prompt_surface, (self.rect.x+5, self.rect.y + 5))



class Menu():
    objects = []
    response = None
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')

    def __init__(self, win_size=(389, 489), default_color=(255, 255 ,255), submit_interval=0.2):
        self.last_submit =time.time()
        self.submit_interval = submit_interval
        self.default_color = default_color
        self.clock = pygame.time.Clock()
        pygame.init()
        self.screen = pygame.display.set_mode(win_size)
        pygame.display.set_caption('Welcome to the Gameserver')
        self.FONT = pygame.font.Font(None, 32)

    def submit(self):
        # makes sure that pressing enter doesnt spam the output
        if time.time() - self.last_submit > self.submit_interval:
            self.last_submit = time.time()
            self.response = {}
            for obj in self.objects:
                self.response[obj.prompt] = obj.response
                obj.response = None
        else:
            self.response = None

    def add_object(self, obj):
        obj.menu = self
        obj.COLOR_INACTIVE = self.COLOR_INACTIVE
        obj.COLOR_ACTIVE = self.COLOR_ACTIVE
        self.objects.append(obj)

    def update(self, events):
        # needs to get events out of the loop
        self.screen.fill(self.default_color)
        for obj in self.objects:
            for event in events:
                # breaks out of the loops if the game is closed
                if event.type == pygame.QUIT:
                    self.quit()
                # breaks out of the loop when submissions is made
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.submit()
                # nested else
                obj.handle_event(event)
            # draws each item within the page
            obj.draw()
    
        pygame.display.flip()
        self.clock.tick(30)
        return None
        
    def quit(self):
        '''
        Called when user quits the app
        '''
        pygame.quit()
        exit()


if __name__ == '__main__':
    menu = Menu()
    menu.add_object(Button(50,300, 32, 'Submit'))
    menu.add_object(InputBox(50, 100, 200, 32, 'Username'))
    menu.add_object(InputBox(50, 200, 200, 32, 'Game Code'))
    while True:
        events = pygame.event.get()
        menu.update(events)
    # quits if the user closes the thingy
    pygame.quit()