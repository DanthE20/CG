from dino_runner.components.obstacles.cactus import Cactus
import random

from dino_runner.utils.constants import SMALL_CACTUS

class SmallCactus(Cactus):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        self.image = SMALL_CACTUS[self.type]
        self.rect.y = 325
        super().__init__(image, self.type)