class Game:
    players = []
    max_players = 2
    started = False
    turn = None
    gameid = None
    victor = None

    def __init__(self):
        pass
    
    def _start_scores(self):
        self.scores = [0 for i in range(self.max_players)]

class BoxesGame(Game):
    def __init__(self):
        # horizontal boxes
        self.boardh = [[None for x in range(6)] for y in range(7)]
        # vertical boxes
        self.boardv = [[None for x in range(7)] for y in range(6)]
        self.boxes = [[None for x in range(6)] for y in range(6)]

    def start(self):
        self.turn = 0

    def end(self, last_turn):
        self.victor = self.last_turn

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

    def move(self, data):
        if not self.started:
            return False
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
            changed = self.check_ownership(turn)
            if not changed:
                self.change_turn()
            self.status_update()

    def check_box(self, x, y):
        if self.boardh[y][x] is not None and self.boardh[y+1][x] is not None:
            if self.boardv[y][x] is not None and self.boardv[y][x+1] is not None:
                return True
        else:
            return False
    
    def giveBox(self, x, y, owner):
        self.boxes[x][y] = owner
        self.boxes_given.append((x, y))

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
        if changed:
            if sum(self.scores) == 36:
                if self.scores[0] < 18:
                    self.end(1)
                elif self.scores[0] > 18:
                    self.end(0)
                else:
                    self.end(None)

        return changed