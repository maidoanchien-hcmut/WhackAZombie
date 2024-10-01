from settings import *


class Zombie(pygame.sprite.Sprite):
    def __init__(self, groups, pos, frames, hit_frames):
        super().__init__(groups)

        # image
        self.hit_frames = hit_frames
        self.hit_frame_index = 0
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # rect
        self.rect = self.image.get_frect(center=pos)

        # timer
        self.is_spawning = True
        self.is_alive = False
        self.is_hit = False
        self.hit_time = 0
        self.is_despawning = False
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 1000

    def destroy(self):
        self.hit_time = pygame.time.get_ticks()
        self.is_hit = True

    def update(self, dt):
        if self.is_spawning:
            self.frame_index += 10 * dt
            if self.frame_index >= len(self.frames):
                self.frame_index = len(self.frames) - 1
                self.is_spawning = False
                self.is_alive = True
            self.image = self.frames[int(self.frame_index)]
        if self.is_alive:
            if not self.is_hit:
                if pygame.time.get_ticks() - self.spawn_time > self.life_time:
                    self.is_alive = False
                    self.is_despawning = True
            else:
                self.image = self.hit_frames[int(self.hit_frame_index)]
                self.hit_frame_index += 5 * dt
                if self.hit_frame_index >= len(self.hit_frames):
                    self.kill()
        if self.is_despawning:
            self.frame_index -= 10 * dt
            if self.frame_index <= 0:
                self.kill()
            self.image = self.frames[int(self.frame_index)]


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # image
        self.surface = pygame.image.load(
            join('image', 'mace.png')).convert_alpha()
        self.image = self.surface

        # rect
        self.rect = self.image.get_frect()

    def update(self, dt):
        self.rect.center = pygame.mouse.get_pos()


class Button:
    def __init__(self, text, width, height, pos):
        # rect
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#727272'
        self.bottom_rect = self.top_rect.copy()
        self.bottom_rect = self.bottom_rect.inflate(5, 5)
        self.bottom_color = '#000000'

        # text
        self.font = pygame.font.Font(join('font', 'MinecraftReg.otf'), 36)
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_frect(center=self.top_rect.center)

    def draw(self, screen):
        # draw button
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect)
        pygame.draw.rect(screen, self.top_color, self.top_rect)
        screen.blit(self.text_surf, self.text_rect)

        # check click
        return self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.bottom_color = '#FFFFFF'
            if pygame.mouse.get_just_pressed()[0]:
                return True
        else:
            self.bottom_color = '#000000'
