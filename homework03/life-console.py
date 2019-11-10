import curses

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')
        pass

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for row in range(self.life.rows):
            for coll in range(self.life.cols):
                simbol = '@' if self.life.curr_generation[row][coll] == 1 else ' '
                try:
                    screen.addstr(row + 1, coll + 1, simbol)
                except curses.error:
                    pass
        pass

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        self.life.curr_generation = self.life.create_grid(True)
        running = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceed:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            screen.refresh()
        curses.endwin()

if __name__ == '__main__':
    gui = Console(GameOfLife((100, 100), True, 50))
    gui.run()
