import pygame


class ImageManager:

    def __init__(self, theme="/default"):
        # load args
        self.theme = theme

        # load images
        self.images = {
            "bomb": pygame.image.load(f"assets/images{self.theme}/bombe.png"),
            "hidden": pygame.image.load(f"assets/images{self.theme}/cache.png"),
            "flagged": pygame.image.load(f"assets/images{self.theme}/drapeau.png")
        }
        for i in range(9):
            self.images[str(i)] = pygame.image.load(f"assets/images{self.theme}/{i}.png")


class SoundManager:

    def __init__(self):

        # load the sounds
        self.sounds = {
            "click": pygame.mixer.Sound("assets/sounds/click.ogg")
        }

    def play(self, music: str):
        self.sounds[music].play()

    def stop(self, music: str):
        self.sounds[music].stop()
