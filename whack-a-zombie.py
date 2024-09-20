import pygame
import random
from os.path import join


class Zombie(pygame.sprite.Sprite):
    def __init__(self, groups, surface, pos):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        if pygame.time.get_ticks() - self.spawn_time > 1000:
            self.kill()


# game setup
pygame.init()
WINDOWS_WIDTH, WINDOWS_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
pygame.display.set_caption("Whack a Zombie")
running = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
score = 0

holes = [(320, 240), (640, 240), (960, 240), (320, 480), (640, 480), (960, 480)]

# imports
zombie_surface = pygame.image.load(join("image", "zombie.png")).convert_alpha()
zombie_surface = pygame.transform.smoothscale_by(zombie_surface, 0.8)
# sprite
all_sprites = pygame.sprite.Group()

# custom events
zombie_spawn = pygame.event.custom_type()
pygame.time.set_timer(zombie_spawn, 1000)

while running:
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == zombie_spawn:
            Zombie(
                all_sprites,
                zombie_surface,
                (random.choice(holes)),
            )
            print("zombie spawned")
    # update the game
    all_sprites.update(dt)

    # draw the game
    display_surface.fill("grey21")
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
