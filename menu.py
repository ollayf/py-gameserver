import pygame
import utils.menu_items as menu_items
from env import games

class MenuSelector:
    usernames = []

    def __init__(self):
        self._start_menu()

    def check_startmenu(self, response):
        if response:
            username = response['Username']
            game_code = response['Game Code']
            if username and game_code:
                retcode = self.uname_status(username)
                if self.check_gc(game_code):
                    return retcode
        return None
    
    def check_gc(self, game_code):
        if game_code in games.keys():
            return games[game_code]
        return None
    
    def uname_status(self, username):
        if username not in self.usernames:
            self.usernames.append(username)
            return 0
        return 1
    
    def update(self):
        events = pygame.event.get()
        self.menu.update(events)
        if self.menu.response:
            ret = self.menu.response.copy()
            self.menu.response = None
            return ret
        return None
    
    def _start_menu(self):
        self.menu = menu_items.Menu()
        self.menu.add_object(menu_items.Button(50,300, 32, 'Submit'))
        self.menu.add_object(menu_items.InputBox(50, 100, 200, 32, 'Username'))
        self.menu.add_object(menu_items.InputBox(50, 200, 200, 32, 'Game Code'))

if __name__ == '__main__':
    ms = MenuSelector()
    while True:
        ret = ms.update()
        if ret:
            print('Ret:', ret)
            retcode = ms.check_startmenu(ret)
            print('retcode:', retcode)