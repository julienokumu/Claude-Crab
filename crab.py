# import libraries
import pygame
import random

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Claude-Crab Dodge Game")

# font
pygame.font.init()

# colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# crab creation
class Crab(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # blank space to draw crab
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA)

        # body
        pygame.draw.rect(self.image, red, (20, 20, 40, 30))

        # eyes
        pygame.draw.rect(self.image, black, (25, 25, 5, 5))
        pygame.draw.rect(self.image, black, (50, 25, 5, 5))

        # claws
        pygame.draw.rect(self.image, red, (10, 30, 10, 10))
        pygame.draw.rect(self.image, red, (60, 30, 10, 10))

        # legs
        pygame.draw.rect(self.image, red, (20, 50, 5, 10))
        pygame.draw.rect(self.image, red, (25, 50, 5, 10))
        pygame.draw.rect(self.image, red, (50, 50, 5, 10))
        pygame.draw.rect(self.image, red, (55, 50, 5, 10))

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
        self.speed = random.randint(10, 12)

    def update(self):
        self.rect.y += self.speed
        # remove if falls off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# game setup
def main():
    # initialize pygame
    pygame.init()

    # clock for game speed
    clock = pygame.time.Clock()

    # create player crab
    player = Crab(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

    # sprite groups
    all_sprites = pygame.sprite.Group(player)
    falling_objects = pygame.sprite.Group()

    # font and game over tracking
    game_over = False
    font = pygame.font.SysFont('Arial', 36)

    # game loop
    running = True
    spawn_timer = 0

    while running:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Add restart functionality when game is over
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # reset game
                player.rect.x = SCREEN_WIDTH // 2
                player.rect.y = SCREEN_HEIGHT - 100
                falling_objects.empty()
                game_over = False

        # only allow movement if game is not over
        if not game_over:
            # player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.rect.left > 0:
                player.rect.x -= player.speed
            if keys[pygame.K_RIGHT] and player.rect.right < SCREEN_WIDTH:
                player.rect.x += player.speed

            # spawn falling objects
            spawn_timer += 1
            if spawn_timer > 15: # spawn every 15 frames
                falling_objects.add(Falling())
                spawn_timer = 0

            # update
            all_sprites.update()
            falling_objects.update()

            # collision detection
            if pygame.sprite.spritecollideany(player, falling_objects):
                game_over = True

        # drawing
        screen.fill(white)
        all_sprites.draw(screen)
        falling_objects.draw(screen)

        # game over screen
        if game_over:
            game_over_text = font.render("Game Over Press R to Restart.", True, red)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

        # update display
        pygame.display.flip()

        # cap the frame rate
        clock.tick(60)

    pygame.quit()

# run game
if __name__ == "__main__":
    main()


    