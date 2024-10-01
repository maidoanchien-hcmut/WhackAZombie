from settings import *
from sprites import *


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Whack a Zombie")
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.player_sprite = pygame.sprite.GroupSingle()
        self.zombie_sprite = pygame.sprite.Group()

        # sprites
        self.player = Player(self.player_sprite)
        self.button = PlayButton(
            'Start Game', 400, 50, (WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 2 + 25))
        self.play_again = PlayButton(
            'Play Again', 400, 50, (WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT - 200))
        self.menu = PlayButton(
            'Menu', 400, 50, (WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT - 100))
        # zombie timer
        self.zombie_spawn = pygame.event.custom_type()
        pygame.time.set_timer(self.zombie_spawn, 2000)

        self.hole_pos = [(320, 550), (640, 550), (960, 550),
                         (320, 400), (640, 400), (960, 400)]

        # setup
        self.load_images()

        # game time
        self.time_length = 300
        self.time_width = 30
        self.time_color = (255, 255, 255)
        self.time_x = (WINDOW_WIDTH - self.time_length) / 2
        self.time_y = 10
        self.time_rate = 30

        # score
        self.hit = 0
        self.miss = -1

        # game state
        self.start_game = False
        self.in_game = False
        self.game_over = False

        # font
        self.title_font = pygame.font.Font(
            join('font', 'Minecrafter.Alt.ttf'), 100)
        self.game_over_font = pygame.font.Font(
            join('font', 'Minecrafter.Reg.ttf'), 75)
        self.score_font = pygame.font.Font(
            join('font', 'MinecraftReg.otf'), 40)
        self.game_over_score_font = pygame.font.Font(
            join('font', 'MinecraftReg.otf'), 36)
        # sound
        self.start_bg_sound = pygame.mixer.music.load(
            join('sound', 'minecraft.mp3'))
        self.start_bg_sound = pygame.mixer.music.play(-1)
        self.zombie_hit_sound = pygame.mixer.Sound(
            join('sound', 'zombie_hit.ogg'))
        self.zombie_death_sound = pygame.mixer.Sound(
            join('sound', 'zombie_death.ogg'))
        self.zombie_spawn_sound = pygame.mixer.Sound(
            join('sound', 'zombie_spawn.ogg'))
        self.zombie_spawn_sound.set_volume(0.5)

    def load_images(self):
        self.zombie_frames = []
        for i in range(1, 5):
            zombie = pygame.image.load(
                join('image', f'zombie-spawn{i}.png')).convert_alpha()
            self.zombie_frames.append(zombie)
        self.zombie_hit_frames = []
        for i in range(1, 3):
            zombie_hit = pygame.image.load(
                join('image', f'zombie-hit{i}.png')).convert_alpha()
            self.zombie_hit_frames.append(zombie_hit)

        self.background = pygame.image.load(join('image', 'bg.png'))
        self.dirt = pygame.image.load(join('image', 'dirt.png'))
        self.dirt.set_alpha(128)

        self.tint = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint.set_alpha(32)
        self.tint.fill((255, 0, 0))

    def collision(self):
        if pygame.mouse.get_just_pressed()[0]:
            self.player.image = pygame.transform.rotozoom(
                self.player.surface, -30, 1)
            collision_sprite = pygame.sprite.spritecollide(
                self.player, self.zombie_sprite, False, pygame.sprite.collide_mask)
            if collision_sprite and not collision_sprite[0].is_hit:
                random.choice((self.zombie_death_sound,
                              self.zombie_hit_sound)).play()
                self.hit += 1
                collision_sprite[0].destroy()
            else:
                self.miss += 1
        if pygame.mouse.get_just_released()[0]:
            self.player.image = self.player.surface

    def display_score(self):
        score_surface = self.score_font.render(
            f'Hit: {self.hit}\nMiss: {self.miss}', True, (255, 255, 255))
        score_rect = score_surface.get_frect(topleft=(10, 10))
        self.display_surface.blit(score_surface, score_rect)

    def display_time(self):
        time_surface = self.score_font.render('Time:', True, (255, 255, 255))
        time_rect = time_surface.get_frect(right=self.time_x - 10, top=5)
        self.display_surface.blit(time_surface, time_rect)
        delta_time = self.clock.get_time() / 1000
        self.time_length -= self.time_rate * delta_time
        if self.time_length < 0:
            pygame.mixer.music.unload()
            pygame.mixer.music.load(join('sound', 'minecraft.mp3'))
            pygame.mixer.music.play(-1)
            self.time_length = 0
            self.in_game = False
            self.game_over = True
        else:
            pygame.draw.rect(self.display_surface, self.time_color, (
                self.time_x, self.time_y, self.time_length, self.time_width))

    def run(self):
        self.start_game = True
        while self.running:
            # dt
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.in_game and event.type == self.zombie_spawn:
                    self.zombie_spawn_sound.play()
                    Zombie(self.zombie_sprite, random.choice(
                        self.hole_pos), self.zombie_frames, self.zombie_hit_frames)

            if self.start_game:
                self.display_surface.blit(self.background, (0, 0))

                title_surface = self.title_font.render(
                    'Whack a Zombie', True, (255, 255, 255))
                title_rect = title_surface.get_frect(
                    center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
                self.display_surface.blit(title_surface, title_rect)

                if self.button.draw(self.display_surface):
                    self.start_game = False
                    self.in_game = True
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(join('sound', 'pigstep.mp3'))
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.2)

            if self.in_game:
                pygame.mouse.set_visible(False)
                # update
                self.zombie_sprite.update(dt)
                self.player_sprite.update(dt)
                self.collision()

                # draw
                self.display_surface.blit(self.background, (0, 0))
                for i in range(0, 6):
                    self.dirt_rect = self.dirt.get_frect(
                        midtop=self.hole_pos[i])
                    self.dirt_rect.centery += 32
                    self.display_surface.blit(self.dirt, self.dirt_rect)
                self.display_score()
                self.zombie_sprite.draw(self.display_surface)
                self.player_sprite.draw(self.display_surface)
                self.display_time()

            if self.game_over:
                pygame.mouse.set_visible(True)
                self.display_surface.blit(self.background, (0, 0))
                self.display_surface.blit(self.tint, (0, 0))

                title_surface = self.game_over_font.render(
                    'Game Over!', True, (255, 255, 255))
                title_rect = title_surface.get_frect(
                    midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
                self.display_surface.blit(title_surface, title_rect)

                score_surface = self.game_over_score_font.render(
                    f'Hit: {self.hit}\nMiss: {self.miss}', True, (255, 255, 255))
                score_rect = score_surface.get_frect(
                    center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
                self.display_surface.blit(score_surface, score_rect)

                if self.play_again.draw(self.display_surface):
                    self.hit = 0
                    self.miss = 0
                    self.time_length = 300
                    self.in_game = True
                    self.game_over = False
                    self.zombie_sprite.empty()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(join('sound', 'pigstep.mp3'))
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.2)

                if self.menu.draw(self.display_surface):
                    self.hit = 0
                    self.miss = -1
                    self.time_length = 300
                    self.start_game = True
                    self.game_over = False
                    self.zombie_sprite.empty()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(join('sound', 'minecraft.mp3'))
                    pygame.mixer.music.play(-1)

            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
