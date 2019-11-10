import pathlib
import random
import copy
import json

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

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
            return[[random.randint(0, 1) for _ in range(self.cols)] for _1 in range(self.rows)]
        else:
            return [[0 for _ in range(self.cols)] for _1 in range(self.rows)]

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
                if row < 0 or coll < 0 or row > self.rows - 1 or \
                        coll > self.cols - 1:
                    continue
                if row == cell[0] and coll == cell[1]:
                    continue
                cells.append(self.curr_generation[row][coll])
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
        for row in range(self.rows):
            for coll in range(self.cols):
                neithbCountGrid[row][coll] = \
                    self.get_neighbours((row, coll)).count(1)
        for row in range(self.rows):
            for coll in range(self.cols):
                if neithbCountGrid[row][coll] == 2 and \
                        self.curr_generation[row][coll] == 1:
                    newGrid[row][coll] = 1
                elif neithbCountGrid[row][coll] == 3:
                    newGrid[row][coll] = 1
                else:
                    newGrid[row][coll] = 0
        self.n_generation += 1
        return newGrid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        pass

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            return self.n_generation >= self.max_generations
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(self, filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        file = open(filename, 'a+')
        gridFromFile = file.read().split('\n')
        file.close()
        grid = []
        wight = len(gridFromFile[0])
        heihgt = len(gridFromFile)
        for row in gridFromFile:
            cells = []
            for simbol in row:
                cells.append(int(simbol))
            grid.append(cells)
        fileGame = GameOfLife((heihgt, wight), False)
        fileGame.curr_generation = copy.deepcopy(grid)
        return fileGame

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, 'r')
        gridDict = {}
        gridDict.update(json.loads(file.read()))
        gridDict.update({str(self.n_generation): self.curr_generation})
        file.close()
        file = open(filename, "w")
        file.write(json.dumps(gridDict))
        pass
