import pygame
import random

WIDTH = 800
HEIGHT = 800

CELLS = 15

SIZE = WIDTH//CELLS #20 pixels by 20pixels

BLUE = (0,0,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)

NUM = 30
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

class Rover:
    def __init__(self, x, y, obstacles):
        self.x = x
        self.y = y
        self.obstacles = obstacles  #now the rover is given an initial set of obstacles so it can figure the path out

    def get_current_pos(self):
        return (self.x,self.y)
    
    def get_neighbors(self):
        neighbors = set()
        if(self.x + 1 < CELLS):
            neighbors.add((self.x+1,self.y))
        if(self.y + 1 < CELLS):
            neighbors.add((self.x,self.y+1))
        if(self.y - 1 >= 0):
            neighbors.add((self.x,self.y-1))
        if(self.x - 1 >= 0):
            neighbors.add((self.x-1,self.y))
        return neighbors

    def get_movable_pos(self):
        movable = set()
        for n in self.get_neighbors():
            if n not in self.obstacles:
                movable.add(n)
        return movable
    
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x * SIZE, self.y * SIZE, SIZE, SIZE))
    
class Grid:
    def __init__(self, obstacles): #draw grid of rows and columns
        self.name = "grid" #not sure what to do here for now
        self.obstacles = obstacles
    
    def draw(self,start):
        #draw horizontal lines and then vertical lines
        for row in range (0, SIZE):
            pygame.draw.line(screen, WHITE, (0, row * SIZE), (WIDTH, row * SIZE))
        for col in range (0, SIZE):
            pygame.draw.line(screen, WHITE, (col * SIZE, 0),  (col * SIZE, HEIGHT))

        pygame.draw.rect(screen, GREEN, (start[0] * SIZE, start[1] * SIZE, SIZE, SIZE)) #draw target

    def get_start(self, end):
        start = (random.randint(0,CELLS-1), random.randint(0,CELLS-1))
        while start in self.obstacles or start == end:
            start = (random.randint(0,CELLS-1), random.randint(0,CELLS-1))

        return start

class Obstacles: #generates num obstacles from given cells
    def __init__(self, num):
        #num obstacles
        self.num = num
        self.obstacles = set()

    def generate_obstacles(self):
        while len(self.obstacles) != self.num:
            x = random.randint(0,CELLS-1) #cell locations are from 0-19 in x and y dir
            y = random.randint(0,CELLS-1)
            self.obstacles.add((x,y))
        
        return self.obstacles
    
    def draw(self): #draws obstacles on grid
        for o in self.obstacles:
            pygame.draw.rect(screen, RED, (o[0] * SIZE, o[1] * SIZE, SIZE, SIZE))

class PathFinder:
    #finds the path
    #ask rover to print it 
    #does all calculation here!
    def __init__(self, target, start, obs):
        self.target = target
        self.start = start
        self.obstacles = obs
    
    #is there a requirement for a node?
    def solve(self):
        frontier = []
        visited = [] #visited nodes go in here
        
        


class Node:
    def __init__(self, prev, x, y, target):
        self.prev = prev
        self.x = x
        self.y = y
        self.target = target
        self.h = self.heuristic_from_node()
        self.g = self.get_g()
        self.f = self.h + self.g #f = g + h for every node

    def heuristic_from_node(self):
        return (self.target[0]-self.x)**2 + (self.target[1]-self.y)**2
    
    def getPrev(self):
        return self.prev
    
    def get_g(self):
        if self.prev:
            return 1 + self.prev.g
        else:
            return 1
        

def main():
    obs = Obstacles(NUM) #future add mode: can be random or can be human generated using array
    obstacles = obs.generate_obstacles()
    grid = Grid(obstacles)
    start = grid.get_start((-15,15))
    target = grid.get_start(start) #same function essentially
    rover = Rover(start[0], start[1], obstacles)

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  
            
            
        screen.fill(BLACK)
        grid.draw(target)
        obs.draw()
        rover.draw()
        pygame.display.update()
        clock.tick(60)
    

if __name__ == '__main__':
    main()