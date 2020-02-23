from PIL import Image
from timeit import default_timer as timer
import pygame
import pygame.gfxdraw


class MazeSolver:

    def __init__(self):
        self.mazeImage = Image.open('maze_small.png')
        self.pix = self.mazeImage.load()
        self.width = self.mazeImage.size[0]
        self.height = self.mazeImage.size[1]
        self.maze = list()
        self.solution = list()
        self.was_here = list()
        self.scale_factor = 4
        self.offset = 2
        self.entry_y = self.entry_x = self.exit_y = self.exit_x = None
        self.screen = None

    def maze_creator(self):
        for y in range(0, self.height):
            maze_x = []
            for x in range(0, self.width):
                if self.pix[x, y] == (0, 0, 0):
                    maze_x.append("B")
                elif self.pix[x, y] == (255, 255, 255):
                    maze_x.append("W")
            self.maze.append(maze_x)

    def find_points(self):
        index_a = 0
        point_a = 0
        index_b = 0
        point_b = 0
        try:
            point_a = [i for i, j in enumerate(self.maze[0]) if j == "W"][0]
            index_a = 0

            if not point_a:
                point_a = [i for i, j in enumerate(self.maze[self.height - 1]) if j == "W"][0]
                index_a = self.height - 1
            else:
                point_b = [i for i, j in enumerate(self.maze[self.height - 1]) if j == "W"][0]
                index_b = self.height - 1
        except:
            pass

        if not point_a:
            for x in range(0, len(self.maze)):
                if self.maze[x][0] == "W":
                    index_a = x
                    point_a = 0
        else:
            for x in range(0, len(self.maze)):
                if self.maze[x][0] == "W":
                    index_b = x
                    point_b = 0

        for x in range(0, len(self.maze)):
            if self.maze[x][self.width - 1] == "W":
                index_b = x
                point_b = self.width - 1
        return index_a, point_a, index_b, point_b

    def recursive_solve(self, y, x):
        while [y, x] != [self.exit_y, self.exit_x]:
            pos = [y, x]
            self.was_here.append([y, x])
            self.solution.append([y, x])
            self.visualise_solver(x, y, (255, 0, 0))
            if self.maze[y - 1][x] == "W" and [y - 1, x] not in self.was_here:
                # print("Up")
                possible_steps = [y - 1, x]
            elif self.maze[y][x + 1] == "W" and [y, x + 1] not in self.was_here:
                # print("Right")
                possible_steps = [y, x + 1]
            elif self.maze[y + 1][x] == "W" and [y + 1, x] not in self.was_here:
                # print("Down")
                possible_steps = [y + 1, x]
            elif self.maze[y][x - 1] == "W" and [y, x - 1] not in self.was_here:
                # print("Left")
                possible_steps = [y, x - 1]
            else:
                # print("Stuck", pos)
                self.solution.pop()
                possible_steps = [self.solution[-1][0], self.solution[-1][1]]
                self.solution.pop()
                self.visualise_solver(x, y, (255, 255, 255))

            y = possible_steps[0]
            x = possible_steps[1]
        self.solution.append([self.exit_y, self.exit_x])
        self.visualise_solver(self.exit_x, self.exit_y, (255, 0, 0))
        print("Solution:", self.solution)

    def print_image(self):
        for x in self.solution:
            self.pix[x[1], x[0]] = (255, 0, 0)
        self.mazeImage.save("mazeSol.png")

    def visualise(self):
        pygame.init()
        window_size = (1920, 1080)
        screen = pygame.display.set_mode(window_size, pygame.DOUBLEBUF)
        screen.set_alpha(None)
        pygame.display.set_caption('Maze Solver')
        screen.fill((255, 255, 255))

        return screen

    def visualise_maze(self):
        for y in range(0, len(self.maze)):
            for x in range(0, len(self.maze[y])):
                if self.maze[y][x] == "B":
                    rect = pygame.Rect((x * self.scale_factor) + self.offset, (y * self.scale_factor) + self.offset, self.scale_factor, self.scale_factor)
                    pygame.draw.rect(self.screen, (0, 0, 0), rect)
                    pygame.event.pump()
        pygame.display.flip()

    def visualise_solver(self, x, y, color):
        rect = pygame.Rect((x * self.scale_factor) + self.offset, (y * self.scale_factor) + self.offset, self.scale_factor, self.scale_factor)
        pygame.draw.rect(self.screen, color, rect)
        pygame.display.update(rect)
        pygame.event.pump()

    def run(self):
        self.maze_creator()
        self.entry_y, self.entry_x, self.exit_y, self.exit_x = self.find_points()
        print("Entry:", self.entry_y, self.entry_x)
        print("Exit:", self.exit_y, self.exit_x)
        self.screen = self.visualise()
        self.visualise_maze()
        self.visualise_solver(self.entry_x, self.entry_y, (0, 255, 0))
        self.visualise_solver(self.exit_x, self.exit_y, (0, 255, 0))
        start = timer()
        self.recursive_solve(self.entry_y, self.entry_x)
        self.print_image()

        time_taken = timer() - start
        print("Time Taken: ", time_taken)

        running = True

        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
