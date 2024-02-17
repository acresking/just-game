import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Psycho Shooter")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Load images
current_dir = os.path.dirname(__file__)
player_img = pygame.image.load(os.path.join(current_dir, "player.png"))
enemy_img = pygame.image.load(os.path.join(current_dir, "enemy.png"))
bg_img = pygame.image.load(os.path.join(current_dir, "bg.png"))

# Scale images
player_img = pygame.transform.scale(player_img, (100, 100))  # Increased player size
enemy_img = pygame.transform.scale(enemy_img, (70, 70))
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 8  # Increased player speed
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(70, WIDTH - 70)
        self.rect.y = random.randrange(-500, -70)
        self.speedy = random.randrange(2, 5)  # Decreased enemy speed

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(70, WIDTH - 70)
            self.rect.y = random.randrange(-500, -70)
            self.speedy = random.randrange(2, 5)


# Game variables
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for _ in range(8):
    enemy = Enemy()
    while pygame.sprite.spritecollide(enemy, enemies, False):
        enemy.rect.x = random.randrange(70, WIDTH - 70)
        enemy.rect.y = random.randrange(-500, -70)
    all_sprites.add(enemy)
    enemies.add(enemy)

# Score
score = 0
font = pygame.font.Font(None, 36)

# Splash screen
splash_screen = True
splash_font = pygame.font.Font(None, 64)
splash_text = splash_font.render("Psycho Shooter", True, WHITE)
splash_rect = splash_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if splash_screen:
        screen.blit(bg_img, (0, 0))
        screen.blit(splash_text, splash_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Show splash screen for 2 seconds
        splash_screen = False

    else:
        # Update
        all_sprites.update()

        # Collision detection
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 1
            enemy = Enemy()
            while pygame.sprite.spritecollide(enemy, enemies, False):
                enemy.rect.x = random.randrange(70, WIDTH - 70)
                enemy.rect.y = random.randrange(-500, -70)
            all_sprites.add(enemy)
            enemies.add(enemy)

        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            score += 1
            new_enemy = Enemy()
            while pygame.sprite.spritecollide(new_enemy, enemies, False):
                new_enemy.rect.x = random.randrange(70, WIDTH - 70)
                new_enemy.rect.y = random.randrange(-500, -70)
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)

        # Draw
        screen.blit(bg_img, (0, 0))
        all_sprites.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

# Quit Pygame
pygame.quit()
