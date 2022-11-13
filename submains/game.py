from .scene import *


class Game:

    def __init__(self):
        # creation of the screen
        self.screen = pygame.display.set_mode((480, 480))
        # title
        pygame.display.set_caption("Demineur")
        # icon
        pygame.display.set_icon(pygame.image.load("assets/images/default/bombe.png"))

        # the font
        self.font = pygame.font.Font("assets/BebasNeue-Regular.ttf", 35)

        # default state of the game
        self.is_running = True

        # scenes, current
        self.scenes = {
            "menu": Menu(game=self),
            "game over": GameOver(game=self)
        }
        self.current_scene = self.scenes["menu"]

        # media manager
        self.images = ImageManager()
        self.sounds = SoundManager()

    def run(self):
        # the game loop
        while self.is_running:
            # print of the current scene
            # print(self.current_scene)
            # first a checking of the events
            self.current_scene.check_events()
            # updating by applying the logic of the current scene
            self.current_scene.update()
            # displays of the current scenes
            self.current_scene.display()

    def pin_up(self, text: str, coordinate: tuple, color=(0, 0, 0)):
        """
        this function show on the pygame window the text
        """
        txt = self.font.render(text, True, color)
        self.screen.blit(txt, coordinate)
