import pygame.font
from pygame.sprite import Group
from heart import Heart



class Scoreboard:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self, msg=""):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{msg} High score: {high_score:.2f}" if msg!="" else f"High score is:{high_score:,}"
        #high_score_str = f"${msg}: High score:", "{:,}".format(high_score)
        self.prep_high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        
        self.prep_high_score_rect = self.prep_high_score_image.get_rect()
        self.prep_high_score_rect.centerx = self.screen_rect.centerx
        self.prep_high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            msg = "New Record!"
            self.prep_high_score(msg)
        else:
            msg = ""
            self.prep_high_score(msg)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.prep_high_score_image, self.prep_high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.hearts.draw(self.screen)


    def prep_level(self):
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_lives(self):
        self.hearts = Group()
        for heart_number in range(self.stats.ships_left):
            heart = Heart(self.ai_game)
            #self.image = pygame.transform.scale(self.image, (8, 8))
            heart.rect.x = 4 + heart_number * heart.rect.width
            heart.rect.y = 4
            self.hearts.add(heart)