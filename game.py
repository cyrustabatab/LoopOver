import pygame,sys
import random
from pprint import pprint

pygame.init()
SCREEN_WIDTH = SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("LOOPOVER")


clock = pygame.time.Clock()
FPS = 30
WHITE = (255,255,255)
BLACK = (0,) * 3


LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

class Square(pygame.sprite.Sprite):
    font = pygame.font.SysFont("calibri",40)
    def __init__(self,number,square_size,square_color=WHITE):
        super().__init__()


        self.image = pygame.Surface((square_size,square_size))
        self.image.fill(square_color)
        self.number = number
        number_text = self.font.render(str(number),True,BLACK)

        self.image.blit(number_text,(self.image.get_width()//2 - number_text.get_width()//2,self.image.get_height()//2 - number_text.get_height()//2))

    def draw(self,x,y):

        screen.blit(self.image,(x,y))


    def __repr__(self):
        return str(self.number)


def display_board(grid):
    pass






def game(n=5):

    
    square_size = SCREEN_WIDTH//n
    numbers = list(range(1,n**2 + 1))


    random.shuffle(numbers)


    grid = []

    squares = pygame.sprite.Group()
    for row in range(n):
        grid_row = []
        for col in range(n):
            number = numbers[row * n + col]
            square_color = [random.randint(50,255) for _ in range(3)]
            square = Square(number,square_size,square_color)
            squares.add(square)
            grid_row.append(square)
        grid.append(grid_row)
    

    def draw_board():

        
        for row in range(n):
            for col in range(n):
                square = grid[row][col]
                square.draw(col * square_size,row * square_size)




        for row in range(0,SCREEN_HEIGHT + 1,square_size):
            pygame.draw.line(screen,BLACK,(0,row),(SCREEN_WIDTH,row))
            pygame.draw.line(screen,BLACK,(row,0),(row,SCREEN_HEIGHT))



    
    mouse_held_down = False
    threshold = 60
    while True:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_held_down = True
                mouse_start_x,mouse_start_y = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_held_down= False



        
        if mouse_held_down:
            current_mouse_x,current_mouse_y = pygame.mouse.get_pos()
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
                print('here')
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






        draw_board()

        pygame.display.update()
        clock.tick(FPS)







if __name__ == "__main__":
    game()














