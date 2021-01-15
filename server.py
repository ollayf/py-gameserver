from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from time import sleep
from env import HOST, PORT

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
    
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        print('Creating Server')
        Server.__init__(self, *args, **kwargs)
        self.games = []
        self.users = []
        self.queue = None

    def Connected(self, channel, addr):
        print('new connection:', channel)
        if self.queue==None:
            self.queue=BoxesGame(channel, self)
        
        self.queue.add_player(channel)
    
    def generate_gameid(self):
        return len(self.games)
    
    def name_open(self, uname):
        usernames = [cl.name for cl in self.users]
        if uname in usernames:
            return False
        else:
            return True

class BoxesGame(object):
    turn = 0
    scores = [0, 0]
    max_players = 2
    started = False

    def __init__(self, channel, server):
        self.players = [] # channels
        self.server = server
        self.id = self.server.generate_gameid()
        self.boardh = [[None for x in range(6)] for y in range(7)]
        self.boardv = [[None for x in range(7)] for y in range(6)]
        self.boxes = [[None for x in range(6)] for y in range(6)]

    def start(self):
        for player in self.players:
            p_index = self.players.index(player)
            player.Send({"action": "startgame","player":p_index, "gameid": self.id})
        self.started = True
        self.server.games.append(self)

    def end(self, last_turn):
        self.Send({'action': 'end', 'victor': last_turn})

    def add_player(self, channel):
        if len(self.players) < self.max_players:
            self.players.append(channel)
            channel.game = self
            channel.gameid = self.id
            print('Pushing user {} to game {}'.format(channel.name, self.id))
        
        if len(self.players) >= self.max_players:
            self.server.queue = None
            self.start()

    def check_turn(self, turn):
        if turn == self.turn:
            print('Move made')
            return True
        else:
            print('Cannot make move')
            return False
            
    def change_turn(self):
        self.turn = (self.turn + 1) %2
        print('Turned changed to', self.turn)
    
    def Send(self, data):
        for player in self.players:
            player.Send(data)

    def move(self, data):
        if not self.started:
            data = {'action': 'placefail'}
            self.Send(data)
            return 
        gameid = data['gameid']
        turn = data['turn']
        # verifies that it is his turn
        if self.check_turn(turn):
            x = data['x']
            y = data['y']
            is_h =data['is_horizontal']
            if is_h:
                self.boardh[y][x] = turn
            else:
                self.boardv[y][x] = turn
            data = {'action': 'place', 'x': x, 'y': y, 'gameid': gameid, 'is_h': is_h, 'player':turn}
            self.Send(data)
            changed = self.check_ownership(turn)
            if not changed:
                self.change_turn()
            self.status_update()
            
        else:
            data = {'action': 'placefail'}
            self.Send(data)

    def check_box(self, x, y):
        if self.boardh[y][x] is not None and self.boardh[y+1][x] is not None:
            if self.boardv[y][x] is not None and self.boardv[y][x+1] is not None:
                return True
        else:
            return False
    
    def status_update(self):
        data = {'action': 'status', 'scores': self.scores, 'turn': self.turn}
        self.Send(data)
    
    def giveBox(self, x, y, owner):
        self.boxes[x][y] = owner
        data = {'action': 'giveBox', 'owner': owner, 'x': x, 'y': y}
        self.Send(data)

    def check_ownership(self, last_turn):
        changed = False
        for y in range(6):
            for x in range(6):
                if self.boxes[x][y] is None:
                    res = self.check_box(x, y)
                    if res:
                        self.giveBox(x, y, last_turn)
                        self.scores[last_turn] += 1
                        changed = True
        if sum(self.scores) == 36:
            if self.scores[0] < 18:
                self.end(1)
            elif self.scores[0] > 18:
                self.end(0)
            else:
                self.end(None)

        return changed
                        


 
print("STARTING SERVER ON {}:{}".format(HOST, PORT))
server=GameServer(localaddr=(HOST, PORT))
while True:
    server.Pump()
    sleep(0.0001)
