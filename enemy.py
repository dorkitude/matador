import pygame
import random
from globals import *
from base_sprites import BaseCharacter
from sprites import Harmable, Weapon, sprites_to_render_third

class Enemy(BaseCharacter, Harmable, Weapon):

    default_status = "pursuing"
    all_enemies = pygame.sprite.Group()
    resolved_enemies = pygame.sprite.Group()
    pursuing_enemies = pygame.sprite.Group()
    death_sequence_duration = 1000
    stunned_until_time = None
    stun_sequence = None

    speed = 2
    hit_points = 10
    _damage = 1

    def __init__(self):
        super().__init__()

        self.status = self.default_status

        if random.randint(1,10) > 9:
            self.hit_points = 5
            self.image = pygame.image.load("sprites/lizard_f_idle_anim_f3.png").convert_alpha()
        else:
            self.hit_points = 15
            self._damage = 3
            self.image = pygame.image.load("sprites/skull_v1_4.png").convert_alpha()
        self.rect = self.image.get_rect()


        self.hurt_sound = pygame.mixer.Sound("sounds/punch.wav")

    @property
    def damage(self):
        return self._damage

    @classmethod
    def spawn_enemies(cls):
        # Ramp:  every 5 seconds since launch, increase the spawn rate
        spawn_count = random.randint(1,3)
        seconds_since_launch = now() - start_time
        spawn_count += 2*int(seconds_since_launch / 5000)

        # print(f"spawning {spawn_count} enemies")
        zone_topleft = (750, 50)
        zone_bottomright = (950, 700)

        for i in range(spawn_count):
            enemy = Enemy()
            enemy.x = random.randint(zone_topleft[0], zone_bottomright[0])
            enemy.y = random.randint(zone_topleft[1], zone_bottomright[1])

            # try not to let this enemy overlap with any others
            placement_tries = 10
            tries_attempted = 0
            skip_this_enemy = False
            while tries_attempted < placement_tries and enemy.collides_with_any(Enemy.all_enemies):
                tries_attempted += 1
                print(f"attempt {tries_attempted} collided: {enemy.collides_with_any(Enemy.all_enemies).rect}")
                enemy.x = random.randint(zone_topleft[0], zone_bottomright[0])
                enemy.y = random.randint(zone_topleft[1], zone_bottomright[1])
                if tries_attempted == placement_tries:
                    skip_this_enemy = True

            if skip_this_enemy:
                enemy.kill()
                continue
            else:
                sprites_to_render_third.add(enemy)
                Enemy.all_enemies.add(enemy)
                Enemy.pursuing_enemies.add(enemy)

    def after_damage_taken(self):
        self.hurt_sound.play()


    def __str__(self):
        return f"An Enemy {self.id}"

    def update(self, control):
        if self.status == "pursuing":
            self.pursue(control.player)

        if self.is_stunned():
            knockback_vector = self.get_knockback_vector(control.player)
            self.move(knockback_vector, speed_scalar=3)

        if self.status == "dying":
            dead_at = self.started_dying_at + self.death_sequence_duration

            if now() > dead_at:
                self.kill()
            else:
                self.image.set_alpha(255 * 0.5 * (1 - (now() - self.started_dying_at) / self.death_sequence_duration))

    def pursue(self, sprite):
        destination_x = sprite.position[0] + random.randint(1,sprite.width)
        destination_y = sprite.position[1] + random.randint(1,sprite.height)
        direction = vec((destination_x-self.x, destination_y-self.y))
        self.move(direction, Enemy.resolved_enemies)

    def render(self, screen):
        super().render(screen)

        if self.is_stunned():
            # print(f"{self} is stunned")
            # Increment the stun sequence counter
            self.stun_sequence += 1

            # If the counter has reached a certain value, reset it to 0
            if self.stun_sequence >= 10:
                self.stun_sequence = 0

            # Draw the enemy with alpha blending
            alphas = [100, 200, 100, 200, 100, 200, 100, 200, 100, 200]
            alpha = alphas[self.stun_sequence]
            light_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            light_surface.fill((255, 255, 255, alpha))
            screen.blit(light_surface, self.rect)


    def die(self):
        self.status = "dying"
        self.started_dying_at = now()
        print(f"{self} has died")

    def is_stunned(self):
        if self.status == "stunned":
            if self.stunned_until_time is None:
                self.status = self.default_status
                return False
            elif now() > self.stunned_until_time:
                self.stunned_until_time = None
                self.status = self.default_status
                return False
            else:
                return True
        else:
            return False

    def stun(self, duration):
        # This method will prevent the sprite from moving for the specified duration
        self.status = "stunned"
        instant = now()
        self.stunned_until_time = instant + duration
        self.stun_start_time = instant
        self.stun_sequence = 0