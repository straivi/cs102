import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)
        self.speed = speed
        self.cell_size = cell_size
        self.screen_size = self.life.cols * cell_size, self.life.rows * cell_size
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        # Copy from previous assignment
        """ Отрисовать сетку """
        for x in range(0, self.screen_size[0], self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.screen_size[1]))
        for y in range(0, self.screen_size[1], self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.screen_size[0], y))
        pass

    def draw_grid(self) -> None:
        # Copy from previous assignment
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(self.life.rows):
            for coll in range(self.life.cols):
                color = pygame.Color('green') if self.life.curr_generation[row][coll] == 1 else \
                    pygame.Color('white')
                pygame.draw.rect(self.screen, color,
                                 (coll * self.cell_size,
                                  row * self.cell_size,
                                  self.cell_size,
                                  self.cell_size))
        pass

    def run(self) -> None:
        # Copy from previous assignment
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        # Создание списка клеток
        # PUT YOUR CODE HERE
        self.life.curr_generation = self.life.create_grid(randomize=True)
        running = True
        paused = False

        while running and self.life.is_changing and not self.life.is_max_generations_exceed:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN and event.key == K_SPACE:
                    paused = not paused
                if paused and event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    y, x = pos[0]//self.cell_size, pos[1]//self.cell_size
                    self.life.curr_generation[x][y] = 1 if self.life.curr_generation[x][y] == 0 else 0
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.draw_grid()
            self.draw_lines()
            if not paused:
                self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
        if self.life.is_max_generations_exceed:
            print("Life exceed max generation")
        else:
            print("Life got stable configuration")
        pass
