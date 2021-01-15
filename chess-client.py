import pygame
import math
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
from env import HOST, PORT
import time

class ServerConnection(ConnectionListener):
    # to be updated by the user in the beginning
    game = None
    username = None

    scores = [0, 0]
    player = 0
    min_click_time = 0.2
    menu = True
    input_boxes = [] # list of boxes that are waiting for response

    def __init__(self, host, port):

        # connect to the server
        print('client connecting to {}:{}'.format(host, port))
        self.Connect((host, port))
        print('Connected!')

        self.last_click = time.time()

        self.gameid = None
        self.num = None
        #put something here that will run when you init the class.
        # initiate the main game stuffs
        pygame.init()
        pygame.font.init()
        width, height = 389, 489
        #initialize the screen
        self.screen = pygame.display.set_mode((width, height))

    def draw_startMenu(self):
        '''Generates the start menu of the game server'''
        screen.fill((255, 255, 255))
        uname_box = InputBox(100, 100, 140, 32)
        self.input_boxes = [uname_box]

    def update(self):
        connection.Pump()
        self.Pump()
        #sleep to make the game 60 fps
        self.clock.tick(60)

        #clear the screen
        self.screen.fill(0)
        self.drawBoard()

        for event in pygame.event.get():
            #quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()
        # setting up the mouse positioning
        # get the position of mouse
        mouse = pygame.mouse.get_pos()

        # in relation to the grid because each square is 64x64 pixels
        xpos = int(math.ceil((mouse[0]-32)/64.0))
        ypos = int(math.ceil((mouse[1]-32)/64.0))

        # check if the mouse is closer to the horizontal or vertical line
        is_horizontal = abs(mouse[1] - ypos*64) < abs(mouse[0] - xpos*64)

        # get new postiion on the grid based on is_horizontal variable
        ypos = ypos - 1 if mouse[1] - ypos*64 < 0 and not is_horizontal else ypos
        xpos = xpos - 1 if mouse[0] - xpos*64 < 0 and is_horizontal else xpos

        # initialise the board variable based on whichever is correct
        board=self.boardh if is_horizontal else self.boardv 
        isoutofbounds=False

        # draw the hover line, checks if out of bounds. If the line is alr drawn, don't draw the hover line
        try: 
            if board[ypos][xpos] is None: self.screen.blit(self.hoverlineh if is_horizontal else self.hoverlinev, [xpos*64+5 if is_horizontal else xpos*64, ypos*64 if is_horizontal else ypos*64+5])
        except:
            isoutofbounds=True
            pass
        if not isoutofbounds:
            owner = board[ypos][xpos]
        else:
            owner = None
        
        # what happens in the game when you click the button
        
        if pygame.mouse.get_pressed()[0] and owner is None and not isoutofbounds:
            if time.time() - self.last_click > self.min_click_time:
                self.last_click = time.time()
                print("click")
                self.Send({"action": "place", "x":xpos, "y":ypos, "is_horizontal": is_horizontal, "gameid": self.gameid, "num": self.num,
                'turn': self.player})

        #update the screen
        pygame.display.flip()

    def Network_place(self, data):
        x = data['x']
        y = data['y']
        is_h = data['is_h']
        player = data['player']
        if is_h:
            self.boardh[y][x] = player
        else:
            self.boardv[y][x] = player

    def Network_status(self, data):
        scores = data['scores']
        turn = data['turn']

        print('Scores', scores)
        print('Turn', turn)
        self.turn = turn
        self.scores = scores

    def Network_startgame(self, data):
        self.started = True
        self.player = data['player']
        self.gameid = data['gameid']
        print('Game Started!')

    def Network_placefail(self, data):
        '''
        Called when user tries to place even though it is not his turn
        '''
        print('place failed')

    def Network_end(self, data):
        victor = data['victor']
        self.finished(victor)

    def Network_unameRes(self, data):
        print('Returned uname setting')
        res = data['res']
        uname = data['uname']
        if res:
            self.uname = uname
            print('Username set to {}'.format(uname))
        else:
            print('Username already taken')

    def Network_giveBox(self, data):
        print('Giving box')
        owner = data['owner']
        x = data['x']
        y = data['y']
        self.boxes[x][y] = owner
        self.scores[owner] += 1



class BoxesDisplay(Game):

    def __init__(self, uname):


    def setup_board(self):
        pygame.display.set_caption("Boxes")
        self.boardh = [[None for x in range(6)] for y in range(7)]
        self.boardv = [[None for x in range(7)] for y in range(6)]
        self.boxes = [[None for x in range(6)] for y in range(6)]

        self.initGraphics()

        # to track scores
        self.turn = 0
        self.didiwin=False

    def start_menu(self):
        self.screen
    
    def set_username(self, username):
        print('Sending Username to server')
        self.Send({'action': 'set_uname', 'uname': username})

    def drawBoard(self):
        for x in range(6):
            for y in range(7):
                if self.boardh[y][x] is None:
                    self.screen.blit(self.none_lineh, [(x)*64+5, (y)*64])
                elif self.boardh[y][x] == 0:
                    self.screen.blit(self.green_lineh, [(x)*64+5, (y)*64])
                elif self.boardh[y][x] == 1:
                    self.screen.blit(self.red_lineh, [(x)*64+5, (y)*64])
        
        for x in range(7):
            for y in range(6):
                if self.boardv[y][x] is None:
                    self.screen.blit(self.none_linev, [(x)*64, (y)*64+5])
                elif self.boardv[y][x] == 0:
                    self.screen.blit(self.green_linev, [(x)*64, (y)*64+5])
                elif self.boardv[y][x] == 1:
                    self.screen.blit(self.red_linev, [(x)*64, (y)*64+5])
        
        for x in range(7):
            for y in range(7):
                self.screen.blit(self.separators, [x*64, y*64])

        self.drawHUD()
        self.drawOwnermap()
        if self.turn == 0:
            self.screen.blit(self.green_player, (220, 395))
        else:
            self.screen.blit(self.red_player, (220, 395))
    
    def drawOwnermap(self):
        for x in range(6):
            for y in range(6):
                if self.boxes[x][y] == 0:
                    self.screen.blit(self.green_box, [(x)*64+5, (y)*64+5])
                if self.boxes[x][y] == 1:
                    self.screen.blit(self.red_box, [(x)*64+5, (y)*64+5])

    
    def drawHUD(self):
        #draw the background for the bottom:
        self.screen.blit(self.score_panel, [0, 389])
        #create font
        myfont = pygame.font.SysFont(None, 32)

        #create text surface
        if self.turn == self.player:
            label = myfont.render("Your Turn:", 1, (255,255,255))
        else:
            label = myfont.render("Opponent's Turn:", 1, (255,255,255))

        #draw surface
        self.screen.blit(label, (10, 400))
    
        #same thing here
        myfont64 = pygame.font.SysFont(None, 64)
        myfont20 = pygame.font.SysFont(None, 20)

        scoreme = myfont64.render(str(self.scores[self.player]), 1, (255,255,255))
        scoreother = myfont64.render(str(self.scores[(self.player + 1) % 2]), 1, (255,255,255))
        scoretextme = myfont20.render("You", 1, (255,255,255))
        scoretextother = myfont20.render("Other Player", 1, (255,255,255))

        self.screen.blit(scoretextme, (10, 425))
        self.screen.blit(scoreme, (10, 435))
        self.screen.blit(scoretextother, (280, 425))
        self.screen.blit(scoreother, (340, 435))

    
    def initGraphics(self):
        self.none_linev = pygame.image.load("boxes/none_line.png")
        self.none_lineh = pygame.transform.rotate(pygame.image.load("boxes/none_line.png"), -90)
        self.blue_linev = pygame.image.load("boxes/cyan_line.png")
        self.blue_lineh = pygame.transform.rotate(pygame.image.load("boxes/cyan_line.png"), -90)
        self.green_linev = pygame.image.load("boxes/green_line.png")
        self.green_lineh = pygame.transform.rotate(pygame.image.load("boxes/green_line.png"), -90)
        self.red_linev = pygame.image.load("boxes/red_line.png")
        self.red_lineh = pygame.transform.rotate(pygame.image.load("boxes/red_line.png"), -90)
        self.hoverlinev = pygame.image.load("boxes/hoverline.png")
        self.hoverlineh = pygame.transform.rotate(pygame.image.load("boxes/hoverline.png"), -90)

        # adding separators
        self.separators=pygame.image.load("boxes/separators.png")
        self.red_player=pygame.image.load("boxes/red_player.png")
        self.green_player=pygame.image.load("boxes/green_player.png")
        self.green_box=pygame.image.load("boxes/green_box.png")
        self.red_box=pygame.image.load("boxes/red_box.png")
        self.winningscreen=pygame.image.load("boxes/youwin.png")
        self.gameover=pygame.image.load("boxes/gameover.png")
        self.drawscreen = pygame.image.load("boxes/draw.png")
        self.score_panel=pygame.image.load("boxes/score_panel.png")
    

    def finished(self, victor):
        if victor == None:
            self.screen.blit(self.drawscreen, (0,0))
        elif victor == self.player:
            self.screen.blit(self.winningscreen, (0,0))
        else:
            self.screen.blit(self.gameover, (0,0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()


if __name__ == '__main__':
    gc = GameClient(HOST, PORT)
    while True:
        gc.update()