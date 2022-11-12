import pygame
from dino_runner.components import text_utils
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import (BG, FPS, ICON, SCREEN_HEIGHT,SCREEN_WIDTH, TITLE, RUNNING)
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.player_hearts.player_heart_manager import PlayerHeartManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        pygame.mixer.music.load("dino_runner/assets/Other/Sound_Game.mp3")
        pygame.mixer.music.play(5)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.background = pygame.image.load("dino_runner/assets/Other/Background.jpg")

        self.player_heart_manager = PlayerHeartManager()
        self.power_up_manager = PowerUpManager()

        self.points = 0
        self.running = True
        self.death_count = 0

    def run(self):
        self.obstacle_manager.reset_obstacles()
        self.player_heart_manager.reset_hearts()
        self.power_up_manager.reset_power_ups(self.points)

        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
    
    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()

    def events(self):
        user_input = pygame.key.get_pressed()
        self.player.event(user_input)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

        self.screen.fill((255, 255, 255))

    def update(self):
        self.player.update()
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player)

    def draw(self):
        self.screen.blit(self.background, [0, 0])
        self.score()
        self.clock.tick(FPS)
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.player_heart_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))

        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    def score(self):
        self.points += 1

        if self.points % 100 == 0:
            self.game_speed += 1

        text, text_rect = text_utils.get_score_element(self.points)
        self.player.check_visibility(self.screen)
        self.screen.blit(text, text_rect)

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()

    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            text, text_rect = text_utils.get_centered_message('Press any Key to Start')
            self.screen.blit(text, text_rect)
        elif self.death_count >= 5:
            text, text_rect = text_utils.get_centered_message_GameOver('GAME OVER')
            text_lose, text_rect_lose = text_utils.get_centered_message('Press any Key to Restart', height = half_screen_height + 60)
            score, score_rect = text_utils.get_centered_message('Total Score: ' + str(self.points), height = half_screen_height + 110)
            death, death_rect = text_utils.get_centered_message('Death count: ' + str(self.death_count), height = half_screen_height + 160)
            self.screen.blit(score, score_rect)
            self.screen.blit(text, text_rect)
            self.screen.blit(text_lose, text_rect_lose)
            self.screen.blit(death, death_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                    pygame.display.quit()
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    self.points = 0
                    self.death_count = 0
                    self.run()            
        else:
            text, text_rect = text_utils.get_centered_message('Press any Key to Restart')
            score, score_rect = text_utils.get_centered_message('Your Score: ' + str(self.points), height = half_screen_height + 50)
            death, death_rect = text_utils.get_centered_message('Death count: ' + str(self.death_count), height = half_screen_height + 100)
            self.screen.blit(score, score_rect)
            self.screen.blit(text, text_rect)
            self.screen.blit(death, death_rect)
            
        self.screen.blit(RUNNING[0], (half_screen_width - 20, half_screen_height - 140))

    def show_menu(self):
        self.running = True

        white_color = (255, 255, 255)
        self.screen.fill(white_color)

        self.print_menu_elements()

        pygame.display.update()

        self.handle_key_events_on_menu()
