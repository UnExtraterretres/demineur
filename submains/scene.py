import pygame.sprite

from .grid import *


# parent of all scenes
class Scene:

    def __init__(self, game, bg_color=(100, 100, 100)):
        # load args
        self.game = game
        self.bg_color = bg_color

        # key pressed
        self.pressed = {}

    def check_events(self):
        # checking of events
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                # check the closing
                self.game.is_running = False
            # get key pressed
            elif event.type == pygame.KEYDOWN:
                self.pressed[event.key] = True
            # get key release
            elif event.type == pygame.KEYUP:
                self.pressed[event.key] = False

    def update(self):
        pass

    def display(self):
        # display the background
        self.game.screen.fill(self.bg_color)

        # NB : thing to add the flip of pygame after displays


class Menu(Scene):

    def __init__(self, game):
        super().__init__(game)

    def check_events(self):
        super().check_events()

        # if <return> pressed --> scene = level
        if self.pressed.get(pygame.K_RETURN):
            # play 'click'
            self.game.sounds.play("click")

            # change current scene
            self.game.scenes["level"] = Level(self.game)
            self.game.current_scene = self.game.scenes["level"]

    def update(self):
        super().update()

    def display(self):
        super().display()

        # display texts
        self.game.pin_up(text="press <return> to start", coordinate=(10, 10), color=(255, 255, 255))

        # flip pygame
        pygame.display.flip()


class Level(Scene):

    def __init__(self, game):
        super().__init__(game)

        # the grid
        self.grid = Grid(self.game)

    def check_events(self):
        super().check_events()

        # add the player's interactions

        # LEFT CLICK (<d> discover) =>
        # if case.value == "bomb": current scene = "game over"
        # elif case.value == 0: discover all cases (value!="bomb") in neighborhood
        # RIGHT CLICK (<f> flag) =>
        # if case.state == "flagged": case.state = "hidden" (change image)
        # elif case.state == "hidden": case.state = "flagged" (change image)
        if self.pressed.get(pygame.K_d):
            # get the case
            case = self.get_case()

            # case is now discovered
            case.state = "discovered"
            case.image = case.set_image()
            # GAME OVER !!
            if case.value == "bomb":
                # change current scene
                self.game.scenes["game over"] = GameOver(self.game)
                self.game.current_scene = self.game.scenes["game over"]
            elif case.value == 0:
                # show all cases (value!="bomb") in the neighborhood
                self.show_neighborhood(case.position)

        if self.pressed.get(pygame.K_f):
            # get the case
            case = self.get_case()

            # add or remove a flag
            if case.state == "flagged":
                case.state = "hidden"
                case.image = case.set_image()
            elif case.state == "hidden":
                case.state = "flagged"
                case.image = case.set_image()

    def update(self):
        super().update()

    def display(self):
        super().display()

        # display the grid
        for l, line in enumerate(self.grid.grid):
            for c, column in enumerate(line):
                # display the case
                self.game.screen.blit(self.grid.grid[l][c].image, self.grid.grid[l][c].rect)

        # flip pygame
        pygame.display.flip()

    # little function to get the case of cursor position
    def get_case(self):
        pos = pygame.mouse.get_pos()
        x = int(pos[0] // (self.game.screen.get_size()[0] / self.grid.size[0]))
        y = int(pos[1] // (self.game.screen.get_size()[1] / self.grid.size[1]))
        return self.grid.grid[x][y]

    # function to show the neighborhood no bomb
    def show_neighborhood(self, position):
        # define data
        positions = [position]
        positions_bin = []

        while len(positions) > 0:
            for pos in positions:
                if pos not in positions_bin:
                    # get case's coordinates
                    x, y = pos

                    try:
                        # there no bomb in the neighborhood
                        if self.grid.grid[x][y].value == 0:

                            # verify if case is'nt in radical top of radical left
                            if x == 0:
                                a = 0
                            else:
                                a = -1
                            if y == 0:
                                b = 0
                            else:
                                b = -1
                            # add neighbors to positions
                            for i in range(a, 2):
                                for j in range(b, 2):
                                    try:
                                        # add position to positions
                                        if (x+i, y+j) != pos:
                                            positions.append(self.grid.grid[x + i][y + j].position)
                                            # print((x+i, y+j), "added to positions")
                                    except IndexError:
                                        pass

                            # change texture of case
                            self.grid.grid[x][y].state = "discovered"
                            self.grid.grid[x][y].image = self.grid.grid[x][y].set_image()
                        # case is not a bomb
                        elif self.grid.grid[x][y].value != "bomb":
                            # change texture of case
                            self.grid.grid[x][y].state = "discovered"
                            self.grid.grid[x][y].image = self.grid.grid[x][y].set_image()

                    except TypeError:
                        pass
                # remove case from positions
                positions.remove(pos)
                positions_bin.append(pos)


class GameOver(Scene):

    def __init__(self, game):
        super().__init__(game)

    def check_events(self):
        super().check_events()

        # if <return> pressed --> scene = main
        if self.pressed.get(pygame.K_r):
            # play 'click'
            self.game.sounds.play("click")

            # change current scene
            self.game.scenes["menu"] = Menu(self.game)
            self.game.current_scene = self.game.scenes["menu"]

    def update(self):
        super().update()

    def display(self):
        super().display()

        # display text
        self.game.pin_up(text="Game Over...", coordinate=(10, 10), color=(255, 0, 0))
        self.game.pin_up(text="Main menu : <r>", coordinate=(10, 100), color=(255, 255, 255))

        # flip pygame
        pygame.display.flip()
