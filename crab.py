# import libraries
import pygame
import random

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Claude-Crab Catch Game") # title

# font
pygame.font.init()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# crab creation
class Crab(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # blank space to draw crab
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA)

        # body
        pygame.draw.rect(self.image, RED, (20, 20, 40, 30))

        # eyes
        pygame.draw.rect(self.image, BLACK, (25, 25, 5, 5))
        pygame.draw.rect(self.image, BLACK, (50, 25, 5, 5))

        # claws
        pygame.draw.rect(self.image, RED, (10, 30, 10, 10))
        pygame.draw.rect(self.image, RED, (60, 30, 10, 10))

        # legs
        pygame.draw.rect(self.image, RED, (20, 50, 5, 10))
        pygame.draw.rect(self.image, RED, (25, 50, 5, 10))
        pygame.draw.rect(self.image, RED, (50, 50, 5, 10))
        pygame.draw.rect(self.image, RED, (55, 50, 5, 10))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

# falling objects
class Falling(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0)) # green object
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -50
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        # remove if falls off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# game setup
def main():
    # clock for game speed
    clock = pygame.time.Clock()

    # create player crab
    player = Crab(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

    # sprite groups
    all_sprites = pygame.sprite.Group(player)
    falling_objects = pygame.sprite.Group()

    # score
    score = 0
    font = pygame.font.SysFont('Bahaus', 36)

    # game loop
    running = True
    spawn_timer = 0

    while running:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.rect.left > 0:
            player.rect.x -= player.speed
        if keys[pygame.K_RIGHT] and player.rect.right < SCREEN_WIDTH:
            player.rect.x += player.speed

        # spawn falling objects
        spawn_timer += 1
        if spawn_timer > 60: # spawn every 60 frames
            falling_objects.add(Falling())
            spawn_timer = 0

        # update
        all_sprites.update()
        falling_objects.update()

        # collision detection
        caught = pygame.sprite.spritecollide(player, falling_objects, True)
        score += len(caught)

        # drawing
        screen.fill(WHITE)
        all_sprites.draw(screen)
        falling_objects.draw(screen)

        # draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # update display
        pygame.display.flip()

        # cap the frame rate
        clock.tick(60)

    pygame.quit()

# run the game
if __name__ == "__main__":
    main()
