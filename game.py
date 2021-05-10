import pygame,sys,time
import random
from pprint import pprint
import os
x = 300
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

pygame.init()
BOARD_WIDTH = SCREEN_HEIGHT = 500

SCREEN_WIDTH = BOARD_WIDTH + 300
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("LOOPOVER")


clock = pygame.time.Clock()
FPS = 30
WHITE = (255,255,255)
BLACK = (0,) * 3
RED = (255,0,0)


LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

class Square(pygame.sprite.Sprite):
    font = pygame.font.SysFont("calibri",40)
    def __init__(self,number,square_size,font,square_color=WHITE):
        super().__init__()


        self.image = pygame.Surface((square_size,square_size))
        self.image.fill(square_color)
        self.number = number
        number_text = font.render(str(number),True,BLACK)

        self.image.blit(number_text,(self.image.get_width()//2 - number_text.get_width()//2,self.image.get_height()//2 - number_text.get_height()//2))

    def draw(self,x,y):

        screen.blit(self.image,(x,y))


    def __repr__(self):
        return str(self.number)






class Button(pygame.sprite.Sprite):

    def __init__(self,x,y,text,button_width,button_height,button_font,button_color=RED,text_color=BLACK):
        super().__init__()

        self.original_image = pygame.Surface((button_width,button_height))
        self.original_image.fill(button_color)

        text = button_font.render(text,True,text_color)

        self.original_rect = self.original_image.get_rect(topleft=(x,y))
        self.original_image.blit(text,(self.original_image.get_width()//2 - text.get_width()//2,self.original_image.get_height()//2 - text.get_height()//2))

        self.image = self.original_image
        self.rect = self.original_rect

        self.expanded_image = pygame.Surface((button_width + 10,button_height + 10))

        self.expanded_image.fill(button_color)
        self.expanded_rect = self.expanded_image.get_rect(center=self.rect.center)


        self.expanded_image.blit(text,(self.expanded_image.get_width()//2 - text.get_width()//2,self.expanded_image.get_height()//2 - text.get_height()//2))



        self.hovered_on = False


    def update(self,point):

        collided = self.rect.collidepoint(point)
        if not self.hovered_on and collided:
            self.hovered_on = True
            self.image = self.expanded_image
            self.rect = self.expanded_rect
        elif self.hovered_on and not collided:
            self.hovered_on = False
            self.image =self.original_image
            self.rect = self.original_rect

    
    def is_clicked_on(self,point):


        return self.rect.collidepoint(point)


    

        




def game(n=10):
    global SCREEN_HEIGHT,BOARD_WIDTH,SCREEN_WIDTH
    
    if n >= 10:
        SCREEN_HEIGHT = BOARD_WIDTH = 800
        SCREEN_WIDTH = BOARD_WIDTH + 300

        


    square_size = BOARD_WIDTH//n
    BOARD_WIDTH = SCREEN_HEIGHT = square_size *n

    pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    print(square_size)
    numbers = list(range(1,n**2 + 1))

    
    def check_win():

        start_number = 1

        for row in range(n):
            for col in range(n):
                if board[row][col] == start_number:
                    start_number += 1
                else:
                    return False

        return True


    def scramble():
        random.shuffle(numbers)

        grid = []
        font = pygame.font.SysFont("calibri",40) if n <= 12 else pygame.font.SysFont("calibri",20) if n <= 25 else pygame.font.SysFont("calibri",12) if n <= 31 else pygame.font.SysFont("calibri",10)
        squares = pygame.sprite.Group()
        for row in range(n):
            grid_row = []
            for col in range(n):
                number = numbers[row * n + col]
                square_color = [random.randint(50,255) for _ in range(3)]
                square = Square(number,square_size,font,square_color)
                squares.add(square)
                grid_row.append(square)
            grid.append(grid_row)
        
        return grid
    

    grid = scramble()
    def draw_board():

        
        for row in range(n):
            for col in range(n):
                square = grid[row][col]
                square.draw(col * square_size,row * square_size)




        for row in range(0,SCREEN_HEIGHT + 1,square_size):
            pygame.draw.line(screen,BLACK,(0,row),(BOARD_WIDTH,row))
            pygame.draw.line(screen,BLACK,(row,0),(row,SCREEN_HEIGHT))

   
    button_width = 200 
    button_height = button_width//2
    button_font = pygame.font.SysFont("calibri",40)
    scramble_button = Button(BOARD_WIDTH + (SCREEN_WIDTH - BOARD_WIDTH)//2 - button_width//2,SCREEN_HEIGHT//2 - button_height//2,"SCRAMBLE",button_width,button_height,button_font)
    menu_button = Button(BOARD_WIDTH + (SCREEN_WIDTH - BOARD_WIDTH)//2 - button_width//2,SCREEN_HEIGHT//2 - button_height//2 - 50 - button_height,"MENU",button_width,button_height,button_font)
    

    button = pygame.sprite.Group(scramble_button,menu_button)
    mouse_held_down = False
    threshold = 60
    moves = 0
    moves_text = button_font.render("MOVES: 0",True,BLACK)

    moves_y = SCREEN_HEIGHT//2  + button_height//2 + 50
    moves_text_rect = moves_text.get_rect(center=(BOARD_WIDTH + (SCREEN_WIDTH - BOARD_WIDTH)//2,moves_y))
    start_time = time.time()
    start_text = button_font.render("00:00.000",True,BLACK)
    start_text_rect = moves_text.get_rect(center=(BOARD_WIDTH + (SCREEN_WIDTH - BOARD_WIDTH)//2,moves_y + moves_text.get_height() + 50))
    while True:
        
        current_time = time.time()
        difference = current_time - start_time
        minutes= int(difference//60)
        seconds = round(difference - minutes * 60,1)

        start_text = button_font.render(f"{str(minutes).zfill(2)}:{seconds}",True,BLACK)





        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                point= pygame.mouse.get_pos()
                x,y = point
                if x <= BOARD_WIDTH:
                    mouse_held_down = True
                    mouse_start_x,mouse_start_y = pygame.mouse.get_pos()
                else:
                    if scramble_button.is_clicked_on(point):
                        grid = scramble()
                        moves_text = button_font.render("MOVES: 0",True,BLACK)
                        start_text = button_font.render("00:00.000",True,BLACK)
                        moves_text_rect = moves_text.get_rect(center=(BOARD_WIDTH + (SCREEN_WIDTH - BOARD_WIDTH)//2,moves_y))
                        moves = 0
                        start_time = time.time()
                    elif menu_button.is_clicked_on(point):
                        return

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_held_down= False


        point = pygame.mouse.get_pos()
        
        button.update(point)

        
        if mouse_held_down:
            current_mouse_x,current_mouse_y = point
            col,row = current_mouse_x // square_size,current_mouse_y//square_size
            direction = None
            if abs(mouse_start_x - current_mouse_x) >= threshold:
                if current_mouse_x < mouse_start_x:
                    direction = LEFT
                else:
                    direction = RIGHT
            elif abs(mouse_start_y - current_mouse_y) >= threshold:
                if current_mouse_y > mouse_start_y:
                    direction = DOWN
                else:
                    direction = UP

            if direction:
                moves += 1
                moves_text = button_font.render(f"MOVES: {moves}",True,BLACK)
                moves_text_rect = moves_text.get_rect(center=(BOARD_WIDTH + (SCREEN_WIDTH - BOARD_WIDTH)//2,moves_y))
            if direction == LEFT:
                row_copy = grid[row].copy()
                for col in range(n):
                    swap_col = col + 1
                    if swap_col >= n:
                        swap_col = 0
                    grid[row][col] = row_copy[swap_col]
            elif direction == RIGHT:
                row_copy = grid[row].copy()
                for col in range(n):
                    swap_col = col - 1
                    if swap_col < 0:
                        swap_col = -1

                    grid[row][col] = row_copy[swap_col]
            elif direction == UP:
                col_copy = [grid[r][col] for r in range(n)]
                for row in range(n):
                    swap_row = row + 1
                    if swap_row == n:
                        swap_row = 0

                    grid[row][col] = col_copy[swap_row]
            elif direction == DOWN:
                col_copy = [grid[r][col] for r in range(n)]
                for row in range(n):
                    swap_row = row - 1
                    if swap_row < 0:
                        swap_row = -1

                    grid[row][col] = col_copy[swap_row]

            

            if direction:
                mouse_start_x,mouse_start_y = current_mouse_x,current_mouse_y





        screen.fill(WHITE)
        draw_board()
        button.draw(screen)
        screen.blit(moves_text,moves_text_rect)
        screen.blit(start_text,start_text_rect)
        
        pygame.display.update()
        clock.tick(FPS)


def start_screen():
    
    title_font = pygame.font.SysFont("calibri",80)
    
    title_text = title_font.render("BOARD SIZE",True,BLACK)

    
    text = '|'
    flickering_event = pygame.USEREVENT + 2
    flickering_milliseconds = 400
    pygame.time.set_timer(flickering_event,flickering_milliseconds)
    invalid_font = pygame.font.SysFont("calibri",40)
    invalid_text = invalid_font.render("BOARD SIZE MUST BE AT LEAST 2",True,BLACK)

    backspace_pressed = False
    invalid = False
    while True:
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == flickering_event:

                if text and text[-1] == '|':
                    text = text[:-1]
                else:
                    text += '|'
            elif event.type == pygame.KEYDOWN:

                if pygame.K_0 <= event.key <= pygame.K_9:
                    if text and text[-1] == '|':
                        text = text[:-1] + chr(event.key) + '|'
                    else:
                        text += chr(event.key)
                elif event.key == pygame.K_RETURN:

                    if text and text[-1] == '|':
                        n = int(text[:-1])
                    elif text:
                        n = int(text)
                    else:
                        print("empty")
                        continue
                    if n < 2:
                        invalid = True
                        invalid_start = time.time()
                    else:
                        return n
        if invalid:            
            if current_time - invalid_start >= 1:
                invalid = False
                     
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_BACKSPACE]:
            do = False
            if not backspace_pressed:
                backspace_pressed = True
                backspace_start= time.time()
                do = True
            else:
                if current_time - backspace_start >= 0.1:
                    do = True
                    backspace_start = current_time
                else:
                    do = False

            if do:
                if text and text[-1] == '|':
                    text = text[:-2]
                elif text:
                    text = text[:-1]
        elif backspace_pressed:
            backspace_pressed = False





                    









        screen.fill(WHITE)
        screen.blit(title_text,(SCREEN_WIDTH//2 - title_text.get_width()//2,50))
        _text= title_font.render(text,True,BLACK)
        width = _text.get_width()
        if text and text[-1] == '|':
            _text_1 = title_font.render(text[:-1],True,BLACK)
            width = _text_1.get_width()

        screen.blit(_text,(SCREEN_WIDTH//2 - width//2,SCREEN_HEIGHT//2 - _text.get_height()//2))
        if invalid:
            screen.blit(invalid_text,(SCREEN_WIDTH//2 - invalid_text.get_width()//2,SCREEN_HEIGHT-50 - invalid_text.get_height()))
        pygame.display.update()

def menu():
    global SCREEN_WIDTH,SCREEN_HEIGHT,BOARD_WIDTH,screen

    title_font = pygame.font.SysFont("calibri",80)

    title_text = title_font.render("LOOPOVER",True,BLACK)
    top_gap = 50 + title_text.get_height()//2
    title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH//2,top_gap))

    button_width = 300 
    button_height = button_width//2

    gap_between_title_and_button = 50
    start_button = Button(SCREEN_WIDTH//2 -button_width//2 ,title_text_rect.bottom + gap_between_title_and_button,"START",button_width,button_height,title_font)
    button = pygame.sprite.GroupSingle(start_button)
    while True:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                point = pygame.mouse.get_pos()
                if button.sprite.is_clicked_on(point):
                    n = start_screen()
                    game(n)
                    BOARD_WIDTH = SCREEN_HEIGHT = 500

                    SCREEN_WIDTH = BOARD_WIDTH + 300
                    pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                n = start_screen()
                game(n)
                BOARD_WIDTH = SCREEN_HEIGHT = 500

                SCREEN_WIDTH = BOARD_WIDTH + 300
                screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))



        
        point = pygame.mouse.get_pos()
        button.update(point)

        screen.fill(WHITE)
        screen.blit(title_text,title_text_rect)
        button.draw(screen)

        pygame.display.update()










if __name__ == "__main__":
    menu()














