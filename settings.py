import random

class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10, 10, 65)

        #Ship
        #self.ship_speed = 1.5
        self.ship_speed = 1
        self.ship_limit = 3
        
        #Bullet
        #self.bullet_speed = 1.5
        self.bullet_speed = 1.5
        #self.bullet_width = 3
        #self.bullet_height = 15
        #self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        #Alien
        #self.alien_speed = 1.0
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction =1 #1 is right, -1 is left

        #Stars
        self.number_of_stars=100
        self.star_speed = 0.5
        #self.star_speed = random.uniform(0.5, 2.0)  # Velocidad aleatoria para cada estrella
        
        #Planets
        self.number_of_planets=8
        self.planet_speed = 0.5

        #Asteroids
        self.min_time=500
        self.max_time=1500