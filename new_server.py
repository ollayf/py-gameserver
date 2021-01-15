from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from time import sleep
from env import HOST, PORT, games

class ClientChannel(Channel):
    name = None
    game = None

    def __init__(self, *args, **kwargs):
        print('Creating client channel')
        Channel.__init__(self, *args, **kwargs)

    def Network(self, data):
        print(data)
    
    def Network_place(self, data):
        self.game.move(data)

    def Network_unameRes(self, data):
        print('Pushing username data to server')
        uname = data['uname']
        # res = self.add_player(uname)
        res = self._server.name_open(uname)
        if res:
            self.name = uname
        self.Send({'action': 'unameRes', 'uname': uname, 'res': res})

 
class GameServer(Server):
    queues = {}
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        print('Creating Server')
        Server.__init__(self, *args, **kwargs)
        self.players_map = []
        self.floaters = []
        self.gamerooms = []
        self.disconnected = []
        self.users = []

    def _empty_queues(self):
        self

    def Connected(self, channel, addr):
        print('new connection:', channel)
        self.add_player(channel)

    def push_player(self, game_code):

    
    def disconnect(self, player):
        self.disconnected.append(player)
    
    def reconnect(self, player):
        self.disconnected.remove(player)

    def generate_gameid(self):
        return len(self.games)
    
    def name_open(self, uname):
        usernames = [cl.name for cl in self.users]
        if uname in usernames:
            return False
        else:
            return True
    
    def close_room(self, room):
        self.gamerooms.remove(room)


class GameRoom:
    started = False
    '''
    A room that holds multiple games
    '''
    def __init__(self, game, server):
        self.server = server
        self.game = game
        self.players = []

    def add_player(self, player):
        self.players.append(player)
    
    def rem_player(self, player):
        self.players.remove(player)

    def disconnect(self, player):
        self.started = False
        self.server.disconnect(player)
        self.game.disconnect()

    def reconnect(self, player):
        self.started = True
        self.server.reconnect(player)
        self.game.reconnect()
    
    def update(self):
        if self.started:
            self.game.update()

    def start(self):
        self.game.start()
        self.started = True

    def close(self):
        self.server.close_room(self)

if __name__ == '__main__':
    print("STARTING SERVER ON {}:{}".format(HOST, PORT))
    server=GameServer(localaddr=(HOST, PORT))
    while True:
        server.Pump()
        sleep(0.0001)
