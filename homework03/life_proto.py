import pygame
import random

from pygame.locals import *
from typing import List, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480,
                 cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        # Создание списка клеток
        # PUT YOUR CODE HERE
        self.grid = self.create_grid(randomize=True)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток.
        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.
        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            return[[random.randint(0, 1) for _ in range(self.cell_width)] for _1 in range(self.cell_height)]
        else:
            return [[0 for _ in range(self.cell_width)] for _1 in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(self.cell_height):
            for coll in range(self.cell_width):
                color = pygame.Color('green') if self.grid[row][coll] else \
                    pygame.Color('white')
                pygame.draw.rect(self.screen, color,
                                 (coll * self.cell_size,
                                  row * self.cell_size,
                                  self.cell_size,
                                  self.cell_size))

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.
        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.
        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        cells = []
        for row in range(cell[0]-1, cell[0]+2):
            for coll in range(cell[1]-1, cell[1]+2):
                if row < 0 or coll < 0 or row > self.cell_height - 1 or \
                        coll > self.cell_width - 1:
                    continue
                if row == cell[0] and coll == cell[1]:
                    continue
                cells.append(self.grid[row][coll])
        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        neithbCountGrid = self.create_grid()
        newGrid = self.create_grid()
        for row in range(self.cell_height):
            for coll in range(self.cell_width):
                neithbCountGrid[row][coll] = \
                    self.get_neighbours((row, coll)).count(1)
        for row in range(self.cell_height):
            for coll in range(self.cell_width):
                if neithbCountGrid[row][coll] == 2 and \
                        self.grid[row][coll] == 1:
                    newGrid[row][coll] = 1
                elif neithbCountGrid[row][coll] == 3:
                    newGrid[row][coll] = 1
                else:
                    newGrid[row][coll] = 0
        return newGrid

