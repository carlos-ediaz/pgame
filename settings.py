class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10, 10, 65)

        #Ship
        self.ship_speed = 1.5
        self.ship_limit = 3
        
        #Bullet
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        #Alien
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction =1#1 is right, -1 is left

        #Stars
        self.number_of_stars=100