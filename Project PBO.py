import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Powerpuff jump")

clock = pygame.time.Clock()

#gambar
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (70, 70))

bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

#musik
loncat_sound = pygame.mixer.Sound("loncat_sound.mp3")
jatuh_sound = pygame.mixer.Sound("jatuh_sound.mp3")

loncat_channel = pygame.mixer.Channel(0)
jatuh_channel = pygame.mixer.Channel(1)

loncat_sound.set_volume(0.4)

#Class
class Character:
    def __init__(self, x, y, w, h, image):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = image
        self.vel_y = 0
        self.on_ground = False

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Player(Character):  # inheritance
    def jump(self):
        if self.on_ground:
            self.vel_y = -10
            self.on_ground = False

    def gravity(self):
        self.vel_y += 0.5
        self.y += self.vel_y


class Platform:
    def __init__(self, x, y, w, h, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, (128,0,128), self.rect)


#Object
player = Player(100, 235, 55, 55, player_img)

platforms = []
start_y = 300

for i in range(1):
    platforms.append(Platform(i*150, start_y, 600, 20, 5))

font = pygame.font.SysFont(None, 20)

game_started = False
game_over = False
score = 0

#GAME LOOP

running = True
while running:
    clock.tick(60)

    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                game_started = True
                if event.key == pygame.K_SPACE:
                    player.jump()
                    loncat_channel.play(loncat_sound)

    if game_started and not game_over:
        player.gravity()

        for p in platforms:
            p.move()

        platforms = [p for p in platforms if p.rect.right > 0]

        if len(platforms) < 5:
            last = platforms[-1]

            gap = random.randint(110, 180)

            new_y = last.rect.y + random.randint(-50, 50)
            new_y = max(170, min(330, new_y))

            new_width = random.randint(100,140)

            new_x = last.rect.right + gap

            platforms.append(
                Platform(new_x, new_y, new_width, 20, 5)
            )

        player.on_ground = False
        for p in platforms:
            if (player.y + player.h <= p.rect.y + 10 and
                player.y + player.h + player.vel_y >= p.rect.y and
                player.x + player.w > p.rect.x and
                player.x < p.rect.x + p.rect.width):

                player.y = p.rect.y - player.h
                player.vel_y = 0
                player.on_ground = True

        if player.y > HEIGHT:
            if not game_over:
                jatuh_channel.play(jatuh_sound)
            game_over = True

        score += 1

    player.draw()
    for p in platforms:
        p.draw()

    if not game_started:
        text = font.render("Tekan tombol spasi untuk mulai", True, (0,0,0))
        screen.blit(text, (190, 190))

    score_text = font.render("Score: " + str(score), True, (0,0,0))
    screen.blit(score_text, (10, 10))

    if game_over:
        over = font.render("GAME OVER", True, (255,0,0))
        screen.blit(over, (250, 200))

    pygame.display.update()

pygame.quit()