from dino_runner.utils.constants import RUNNING

class Dinosaur:
    X_POS = 80
    Y_POS = 310

    def __init__(self):
        self.image = RUNNING [0]
        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.step_index = 0

    def event(self):
        pass

    def update(self):
        self.run()
        
        if self.step_index >= 10:
            self.step_index = 0

    def run(self):
        if self.step_index < 5:
            self.image = RUNNING[0]
        else:
            self.image = RUNNING[1]

        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.step_index += 1

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect))



