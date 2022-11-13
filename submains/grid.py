from random import randint

from .tools.mediamanadger import *


class Grid:

    def __init__(self, game, size=(16, 16)):
        # load args
        self.game = game
        self.size = size

        # number of mines
        self.mines = int(0.16*size[0]*size[1])
        # grid
        self.grid = self.set_grid()

    def set_grid(self):
        # a grid without bomb
        grid = [[Case(self, (line, column)) for column in range(self.size[1])] for line in range(self.size[0])]

        # now we add bombs
        while self.mines != 0:
            # chose randomly a case in grid
            line = randint(0, self.size[0]-1)
            column = randint(0, self.size[1]-1)
            # there is a bomb ?
            if grid[line][column].value != "bomb":
                # put a bomb !
                grid[line][column].value = "bomb"
                # reset the image
                grid[line][column].image = grid[line][column].set_image()
                self.mines -= 1

                # add 1 neighborhood
                # verify if case is'nt in radical top of radical left
                if line == 0:
                    a = 0
                else:
                    a = -1
                if column == 0:
                    b = 0
                else:
                    b = -1
                # add 1 to neighborhood
                for x in range(a, 2):
                    for y in range(b, 2):
                        try:
                            # add 1
                            grid[line + x][column + y].value += 1
                            # reset image
                            grid[line + x][column + y].image = grid[line + x][column + y].set_image()
                        except (TypeError, IndexError):
                            pass

        # return the grid
        return grid


class Case(pygame.sprite.Sprite):

    def __init__(self, grid, position: tuple, value=0, state="hidden"):
        super().__init__()
        # load args
        self.grid = grid
        self.position = position
        self.value = value  # 0-8 or bomb
        self.state = state  # hidden discovered flagged

        # load image
        self.image = self.set_image()
        # load rect
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]*self.rect.width
        self.rect.y = self.position[1]*self.rect.height

    def set_image(self):
        if self.state == "discovered":
            return self.grid.game.images.images[f"{self.value}"]
        else:
            return self.grid.game.images.images[self.state]
