import sys
import pygame
import random
from time import sleep
from random import randint
import asyncio

from settings import Settings

from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from explosion import Explosion
from asteroid import Asteroid
from planet import Planet
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
 
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)

        self.explosions = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.planets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.next_asteroid_time = pygame.time.get_ticks() + random.randint(self.settings.min_time, self.settings.max_time)

        self._create_stars()
        self._create_planets()
        self._create_asteroids()
        self._create_fleet()
        
        self.play_button = Button(self, "Play")

    async def run_game(self):
        """Start the main loop for the game."""
    
        while True:
            self._check_events()
            running=1
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_stars()
                self._update_planets()
                current_time = pygame.time.get_ticks()
                if current_time >= self.next_asteroid_time:
                    self._create_asteroids()
                    self.next_asteroid_time = current_time + random.randint(self.settings.min_time, self.settings.max_time)

                # Actualizar asteroides
                self.asteroids.update()
            
            self.bullets.update()
            self._update_screen()

            await asyncio.sleep(0)
            if not running:
                pygame.quit()
                return

    def _check_events(self):
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:

            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_lives()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
                
    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key == pygame.K_UP:
            self.ship.moving_up=True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down=True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        #Redraw the screen:
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.planets.draw(self.screen)
        self.asteroids.draw(self.screen)
        self.ship.blitme() #Draw the ship on the screen

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.sb.show_score()
        self.explosions.update()
        self.explosions.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.sb.check_high_score()
        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_colisions()

    def _check_bullet_alien_colisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                for alien in aliens:
                    # Crear una explosión en la posición del alien destruido
                    explosion = Explosion(self, alien.rect.center)
                    self.explosions.add(explosion)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level +=1
            self.sb.prep_level()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (2*alien_height) - ship_height)
        number_rows = available_space_y // (2*alien_height)

        for row_number in range(number_rows):
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien= Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width *alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 *alien_height*row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _ship_hit(self):
        explosion = Explosion(self, self.ship.rect.center)
        self.explosions.add(explosion)
        sleep(0.5)

        if self.stats.ships_left>0:

            self.stats.ships_left -=1
            self.sb.prep_lives()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
           
        else:
            self.stats.game_active = False

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >=screen_rect.bottom:
                self._ship_hit()
                break

    def _create_stars(self):
        star = Star(self)
        star_width, star_height = star.rect.size
        available_space_x = self.settings.screen_width
        number_stars_x = available_space_x // (star_width)

        available_space_y = self.settings.screen_height
        number_rows = available_space_y // (star_height)

        self._create_star(number_rows, number_stars_x, self.settings.number_of_stars)
    
    def _create_star(self, rows, columns, total_stars):
        
        for i in range(total_stars):
            star= Star(self)
            star_width, star_height = star.rect.size
            col=randint(0,columns)
            row=randint(0,rows)
            star.rect.x = star_width*col
            star.rect.y = star_height*row
            self.stars.add(star)

    def _update_stars(self):
        """Update the position of stars and reset them when they leave the screen."""
        for star in self.stars.sprites():
            star.rect.y += self.settings.star_speed
            # Reset star to the top if it goes out of screen
            if star.rect.top > self.settings.screen_height:
                star.rect.y = 0#-star.rect.height
                star.rect.x = random.randint(0, self.settings.screen_width - star.rect.width)

    def _create_asteroids(self):
        asteroid = Asteroid(self)
        self.asteroids.add(asteroid)

    def _create_planets(self):
        planet = Planet(self)
        planet_width, planet_height = planet.rect.size
        available_space_x = self.settings.screen_width
        number_planets_x = available_space_x // (planet_width)

        available_space_y = self.settings.screen_height
        number_rows = available_space_y // (planet_height)

        self._create_planet(number_rows, number_planets_x, self.settings.number_of_planets)
    
    def _create_planet(self, rows, columns, total_planets):
        for i in range(total_planets):
            planet=Planet(self)
            planet_width, planet_height = planet.rect.size
            col=randint(0,columns)
            row=randint(0,rows)
            planet.rect.x = planet_width*col
            planet.rect.y = planet_height*row
            self.planets.add(planet)

    def _update_planets(self):
        """Update the position of stars and reset them when they leave the screen."""
        for planet in self.planets.sprites():
            planet.rect.y += self.settings.planet_speed
            # Reset star to the top if it goes out of screen
            if planet.rect.top > self.settings.screen_height:
                planet.rect.y = 0#-star.rect.height
                planet.rect.x = random.randint(0, self.settings.screen_width - planet.rect.width)

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    #ai.run_game()
    asyncio.run(ai.run_game())