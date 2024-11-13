# import libraries
import pygame
import random

# game window dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Claude-Crab")

# initialize font
pygame.font.init()

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# crab class with dynamic sizing
class Crab(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # initialize size parameters
        self.base_width = 80
        self.base_height = 60
        self.current_width = self.base_width
        self.current_height = self.base_height

        # create a surface that can change size
        self.image = pygame.Surface((self.current_width, self.current_height), pygame.SRCALPHA)

        # draw initial crab
        self.draw_crab()

        # set up positioning and movement
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def draw_crab(self):
        # clear the previous image
        self.image.fill((0, 0, 0, 0)) # transparent fill

        # proportional sizing of crab parts
        body_width = int(self.current_width * 0.5)
        body_height = int(self.current_height * 0.375)
        eye_size = int(self.current_width * 0.0625)
        claw_width = int(self.current_width * 0.125)
        claw_height = int(self.current_height * 0.125)
        leg_width = int(self.current_width * 0.0625)
        leg_height = int(self.current_height * 0.125)

        # draw body
        pygame.draw.rect(self.image, red, (int(self.current_width * 0.25), int(self.current_height * 0.25), body_width, body_height))

        # draw eyes
        pygame.draw.rect(self.image, black, (int(self.current_width * 0.3125), int(self.current_height * 0.3125), eye_size, eye_size))
        pygame.draw.rect(self.image, black, (int(self.current_width * 0.625), int(self.current_height * 0.3125), eye_size, eye_size))

        # draw claws
        pygame.draw.rect(self.image, red, (int(self.current_width * 0.125), int(self.current_width * 0.375), claw_width, claw_height))
        pygame.draw.rect(self.image, red, (int(self.current_width * 0.75), int(self.current_width * 0.375), claw_width, claw_height))

        # draw legs
        leg_positions = [
            (int(self.current_width * 0.25), int(self.current_height * 0.625)),
            (int(self.current_width * 0.3125), int(self.current_height * 0.625)),
            (int(self.current_width * 0.625), int(self.current_height * 0.625)),
            (int(self.current_width * 0.6875), int(self.current_height * 0.625))
        ]

        for x, y in leg_positions:
            pygame.draw.rect(self.image, red, (x, y, leg_width, leg_height))

    def grow(self):
        # increased size by 5% each time
        growth_factor = 1.05
        self.current_width = int(self.current_width * growth_factor)
        self.current_height = int(self.current_height * growth_factor)

        # recreate the image with the new size
        self.image = pygame.Surface((self.current_width, self.current_height), pygame.SRCALPHA)
        self.draw_crab()

        # update rect to maintain position
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def reset_size(self):
        # reset the crab to its orginal size
        self.current_width = self.base_width
        self.current_height = self.base_height
        self.image = pygame.Surface((self.current_width, self.current_height), pygame.SRCALPHA)
        self.draw_crab()
        self.rect = self.image.get_rect(center=self.rect.center) # keep the crab centered

# falling objects class
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

# main game function
def main():
    # intialize pygame
    pygame.init()

    # clock for game speed
    clock = pygame.time.Clock()

    # create a player crab
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
    growth_timer = 0 # timer for crab growth
    GROWTH_INTERVAL = 120 # 2 second at 60FPS(60 * 2 = 120)

    while running:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # restart when game is over
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # reset game
                player.rect.x = SCREEN_WIDTH // 2
                player.rect.y = SCREEN_HEIGHT - 100
                player.reset_size()
                falling_objects.empty()
                game_over = False

        # movement if game is not over
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

            # growth timer
            growth_timer += 1
            if growth_timer >= GROWTH_INTERVAL:
                player.grow() # grow crab
                growth_timer = 0 # reset timer

            # update
            all_sprites.update()
            falling_objects.update()

            # collision detection
            collided_objects = pygame.sprite.spritecollide(player, falling_objects, False)
            if collided_objects:
                game_over = True

        # drawing
        screen.fill(white)
        all_sprites.draw(screen)
        falling_objects.draw(screen)

        # game over screen
        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, black)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

        # refresh the display
        pygame.display.flip()
        clock.tick(60) # limit to 60 frames per second

    pygame.quit()

# run the game
if __name__ == "__main__":
    main()

            