
import pygame as pg
import sys
from settings import *
from sprites import *
from functions import *
import pandas as pd
pos_x=0
pos_y=0
words_list = []
selected_items=[]
word_df=pd.read_csv("word_meaning.csv")
gamestate="start_menu"
sysfont = pg.font.get_default_font()
no_of_words=5
def get_meaning(word):
    for index,row in word_df.iterrows():
        if row["word"]==word:
            return row["meaning"]
    return "not found"
def create_grid():
    df=pd.read_csv("word_meaning.csv")
    # print(df.loc[df['word'] =="abaft" ])
    # # print(word_dict["abaft"])
    
    temp_df=df.sample(n=50,replace=False)
    max_word_size=12
    list_temp=[]
    for index,row in temp_df.iterrows():
        if row["meaning"]=="not found" or row["meaning"]=="Not found":
            temp_df.drop(index,inplace=True)
        else:
            to_be_added=row["word"]
            
            list_temp.append(to_be_added)

    word_df=temp_df
    
    for i in range(no_of_words):
        if(len(list_temp[i])>max_word_size):
            max_word_size=len(list_temp[i])
    words_list.append(list_temp[0:no_of_words])
    board_temp = create_word_search(list_temp[0:no_of_words],max_word_size)
    print("this is word",words_list[0][0])
    return board_temp
board=[]
for i in range (5):
    board_temp=create_grid()
    board.append(board_temp)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        
        pass

    def new(self,x,y):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = Player(self, x, y)
        
     

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        
        self.dt = self.clock.tick(FPS) / 1000
        self.events()
        self.update()
        self.draw()
        self.fill_grid(0)
     
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def fill_grid(self,round):
       
        size=len(board[round])
        font = pg.font.Font(None, 36)
        for i in range(size):
            for j in range(size):
                
                text_surface = font.render(board[round][i][j], True, (255, 255, 255)) 
                self.player.value=board[round][i][j]
                self.screen.blit(text_surface,(i*TILESIZE,j*TILESIZE,TILESIZE,TILESIZE))  
        
        pg.display.flip()
    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    pos_x-=1
                    self.player.x=pos_x
                    
                if event.key == pg.K_RIGHT:
                    pos_x+=1
                    self.player.x=pos_x
                    
                if event.key == pg.K_UP:
                    pos_y-=1
                    self.player.y=pos_y
                    
                if event.key == pg.K_DOWN:
                    pos_y+=1
                    self.player.y=pos_y
                    

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        
        pass
    def display_words(self,list):
        font = pg.font.Font(None, 36)
        text_surface=font.render("Find the following words in the grid:",True,YELLOW)
        self.screen.blit(text_surface,(600,0,600,0))
        for i in range (no_of_words):
            text_surface=font.render(list[i],True,YELLOW)
            self.screen.blit(text_surface,(600,(i+1)*TILESIZE,600,(i+1)*TILESIZE))
        pg.display.update()
       


# create the game object
round=0
hold=False
cnt=0
g = Game()
g.new(pos_x,pos_y)
g.run()
g.display_words(words_list[round])
round_cleared=False
while True:
    
    
    if gamestate=="start_menu":
        print("start menu")
        
        g.new(pos_x,pos_y)

        ans=""
        right=True
        down=True
        select=False
        gamestate="game"
        cnt=0
        pg.display.update()
    elif gamestate=="game":
        if(not(hold)):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    g.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        g.quit()
                    if event.key == pg.K_LEFT and not(select) and pos_x>0:
                        
                        pos_x-=1
                        g.player.x=pos_x
                        g.update()
                        g.draw()
                        g.fill_grid(round)
                        g.display_words(words_list[round])
                    if event.key == pg.K_RIGHT and right :
                        pos_x+=1
                        g.player.x=pos_x
                        g.update()
                        g.draw()
                        g.fill_grid(round)
                        g.display_words(words_list[round])
                        if select:
                            temp_player=Player(g,pos_x,pos_y)
                            temp_player.image.fill((0,0,139))
                            
                            ans+=board[round][pos_x][pos_y]
                            down=False
                    if event.key == pg.K_UP and not(select) and pos_y>0:
                        pos_y-=1
                        g.player.y=pos_y
                        g.update()
                        g.draw()
                        g.fill_grid(round)
                        g.display_words(words_list[round])
                    if event.key == pg.K_DOWN and down:
                        pos_y+=1
                        g.player.y=pos_y
                        g.update()
                        g.draw()
                        g.fill_grid(round)
                        g.display_words(words_list[round])
                        if select:
                            temp_player=Player(g,pos_x,pos_y)
                            temp_player.image.fill((0,0,139))
                            
                            ans+=board[round][pos_x][pos_y]
                            right=False
                    if event.key==pg.K_s:
                        temp_player=Player(g,pos_x,pos_y)
                        temp_player.image.fill((0,0,139))
                        ans+=board[round][pos_x][pos_y]
                        key_press=event.key
                        if(not(select)):
                            select=True
                            right=True
                            down=True
                            
                        
                        
                    if event.key==pg.K_SPACE:
                        print(ans)
                        right=True
                        down=True
                        select=False
                        font = pg.font.Font(None, 36)
                        if ans in words_list[round]:
                            g.update()
                            g.draw()
                            g.fill_grid(round)
                            g.display_words(words_list[round])
                            mean=get_meaning(ans)
                            sentence= "The meaning is:"+mean
                            text_surface=font.render("Correct!",True, (0, 255, 0))
                            
                            g.screen.blit(text_surface,(0,500,0,500))
                            text_surface=font.render(sentence,True, (0, 255, 0))
                            
                            g.screen.blit(text_surface,(0,532,0,532))
                            text_surface=font.render("Press n to continue",True, (0, 255, 0))
                            
                            g.screen.blit(text_surface,(0,564,0,564))
                            ans=""
                           
                            pg.display.update()
                            hold=True
                            cnt+=1
                            if cnt==no_of_words:
                                round_cleared=True
                        
                            
                            
                        else:
                            
                        
                            g.update()
                            g.draw()
                            g.fill_grid(round)
                            g.display_words(words_list[round])
                            pg.display.update()
                            text_surface=font.render("Wrong! Try Again. Press n to restart",True, (255, 0, 0))
                            g.screen.blit(text_surface,(0,500,0,500))
                            g.new(pos_x,pos_y)
                            pg.display.update()
                            hold=True
                            cnt=0
                            ans=""
                            
                        
                    

        else:
            
            for event in pg.event.get():
                if event.type==pg.KEYDOWN:
                    if(event.key==pg.K_n):
                        print("ha ha")
                        hold=False
                        g.update()
                        g.draw()
                        g.fill_grid(round)
                        g.display_words(words_list[round])
            
    elif gamestate=="round_over":
        if round==4:
            gamestate="game_over"
        else:
            round+=1
            
            font = pg.font.SysFont("chalkduster.ttf", 48)
            text_surface=font.render("Round over! move to next round ",True, (255, 0, 0))
            g.screen.blit(text_surface,(500,200,500,200))
            pg.display.update()
            gamestate="start_menu"
            hold=True
            
            
           
    elif gamestate=="game_over":
        font = pg.font.SysFont("chalkduster.ttf", 52)
        text_surface=font.render("You win! ",True, (255, 0, 0))
        g.screen.blit(text_surface,(500,200,500,200))
        pg.display.update()


    
    if cnt==no_of_words and round_cleared and round==2:
        gamestate="game_over"
    elif cnt==no_of_words and round_cleared:
        gamestate="round_over"
        round_cleared=False
    elif cnt==no_of_words and not(round_cleared):
        gamestate="start_menu"


                    



