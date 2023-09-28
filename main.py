import pygame
import random

WIDTH = 800
HEIGHT = 800

CELLS = 15

SIZE = WIDTH//CELLS #20 pixels by 20pixels

BLUE = (0,0,255)
LIGHTBLUE = (0,0,200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)

NUM = 30
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

class Rover:
    def __init__(self, x, y, obstacles, target):
        self.x = x
        self.target = target
        self.y = y
        self.obstacles = obstacles  #now the rover is given an initial set of obstacles so it can figure the path out

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x * SIZE, self.y * SIZE, SIZE, SIZE))

    def draw_path(self, path):

        for i in range(len(path)-1, -1,-1):
            color = LIGHTBLUE
            if path[i] == self.target:
                color = GREEN
            if path[i] == (self.x, self.y):
                color = BLUE
            pygame.draw.rect(screen, color, (path[i][0] * SIZE, path[i][1] * SIZE, SIZE, SIZE))
            pygame.time.delay(100)
            pygame.display.update()
    
class Grid:
    def __init__(self, obstacles): #draw grid of rows and columns
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
        currentNode = Node(None, self.start[0], self.start[1], self.target)
        frontier.append(currentNode) #startNode will be the first member of frontier
        frontier = sorted(frontier, key = lambda n: n.f)
        targetFound = False
        targetNode = None
        while len(frontier) != 0 and not targetFound:
            #look for lowest f square in open list
            #pop frontier and move to closed list, call this current node
            currentNode = frontier.pop(0)
            #check if target added to visited
            visited.append(currentNode)
            if currentNode.x == self.target[0] and currentNode.y == self.target[1]:
                targetFound = True #exit out of while loop really doesn't matter waht happens after this
                targetNode = currentNode
                continue

            for neighbor in currentNode.get_neighbors():
                exists = False
                for element in frontier: #if element in open list
                    if element.x == neighbor[0] and element.y == neighbor[1] and (neighbor[0],neighbor[1]) not in self.obstacles: #element exists in openlist
                        exists = True
                        #compare g values
                        if element.g > currentNode.g + 1: #current path is better
                            element.f = element.f - element.g
                            element.g = currentNode.g + 1
                            element.f = element.f + element.g
                            element.prev = currentNode #change prev of frontier element

                if exists == False and (neighbor[0],neighbor[1]) not in self.obstacles: #if element not in open list
                    frontier.append(Node(currentNode, neighbor[0],neighbor[1], self.target))

            frontier = sorted(frontier, key = lambda n: n.f)


        path = [] #plan is to get a list of tuples out of this
        #targetNode  
        while targetNode: #if targetNode is not none:
            #go backwards to find path
            path.append((targetNode.x,targetNode.y))
            targetNode = targetNode.prev

        return path
    

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
    
        

def main():
    obs = Obstacles(NUM) #future add mode: can be random or can be human generated using array
    obstacles = obs.generate_obstacles()
    grid = Grid(obstacles)
    # start = grid.get_start((-15,15))
    start = grid.get_start((0,0))
    target = grid.get_start(start) #same function essentially
    # start = (0,0)
    # target = (CELLS-1, CELLS-1)
    rover = Rover(start[0], start[1], obstacles, target)

    aStar = PathFinder(target, start, obstacles)
    path = aStar.solve()
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  
        screen.fill(BLACK)
        grid.draw(target)
        obs.draw()
        rover.draw()
        rover.draw_path(path)
        pygame.display.update()
        clock.tick(60)
    

if __name__ == '__main__':
    main()