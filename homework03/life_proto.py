import pygame
import random

from pygame.locals import *
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
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

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

            self.draw_grid()
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
        for row in range(0, self.height/self.cell_size):
            for coll in range(0, self.width/self.cell_size):
                Grid[row][coll] = random.getrandbits(1)
        return Grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(0, self.height, self.cell_size):
            for coll in range(0, self.width, self.cell_size):
                color = pygame.Color('white') if Grid[row/self.cell_size][coll/self.cell_size] == 0 else pygame.Color('green')
                pygame.draw.rect(self.screen, color, (row, coll, self.cell_size, self.cell_size))
        pass

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
        for row in range(cell[0]-1, cell[0]+1):
            for coll in range(cell[1]-1, cell[1]+1):
                if row < 0 or row == cell[0]: 
                    continue
                if coll < 0 or coll == cell[1]:
                    continue
                cells.append(Grid[row][coll])
        return cells

    def get_count_live_neighbours(self, cells: Cells) -> int:
        liveNeighb = 0
        for neighbour in range(len(cells)):
            if cells[neighbour] == 1: 
                liveNeighb += 1
        return liveNeighb

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        GridCountOfNeighb = List[List[int]]
        for row in range(len(Grid)):
            for coll in range(len(Grid[0])):
                cord = Tuple[row, coll]
                GridCountOfNeighb[row][coll] = self.get_count_live_neighbours(self.get_neighbours(cord))
        for row in range(len(Grid)):
            for coll in range(len(Grid[0])):
                if GridCountOfNeighb[row][coll] == 2 or GridCountOfNeighb[row][coll] == 3:
                    Grid[row][coll] == 1
                else: 
                    Grid[row][coll] == 0
        pass
