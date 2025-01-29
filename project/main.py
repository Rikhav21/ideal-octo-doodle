import pygame
import random
pygame.init()
WIDTH, HEIGHT = 128, 128 
SCALE = 7 
SCALED_WIDTH, SCALED_HEIGHT = WIDTH * SCALE, HEIGHT * SCALE
FPS = 60  
WHITE = (255, 255, 255)
RED = (255, 0, 0)
state = "home"
score = 0
misses = 0
surv = 0
flappy_time = 0 
jumping = False
jump_speed = 0
gravity = 0.5
anim = 0
animsp = 0.2 
flappy_speed = 1.5
pipe_gap = 40
game_surface = pygame.Surface((WIDTH, HEIGHT))  
screen = pygame.display.set_mode((SCALED_WIDTH, SCALED_HEIGHT))  
font = pygame.font.Font(None, 14)
backgrounds = {
    "home": pygame.image.load("backgrounds/home.png"),
    "apple_catch": pygame.image.load("backgrounds/apple_catch.png"),
    "dino": pygame.image.load("backgrounds/dino_jump.png"),
    "flappy": pygame.image.load("backgrounds/flappy_bird.png"),
}
sprites = {
    "dragon_jump": pygame.image.load("sprites/dragon_jump_sheet.png"),
    "dragon_idle": pygame.image.load("sprites/dragon_idle_sheet.png"),
    "apple": pygame.image.load("sprites/apple.png"),
    "basket": pygame.image.load("sprites/basket.png"),
    "cactus": pygame.image.load("sprites/cactus.png"),
    "pipe": pygame.image.load("sprites/pipe.png"),
}
for key, image in backgrounds.items():
    backgrounds[key] = pygame.transform.scale(image, (WIDTH, HEIGHT))
def split_spritesheet(sheet, frame_width, frame_height):
    frames = []
    for y in range(0, sheet.get_height(), frame_height):
        for x in range(0, sheet.get_width(), frame_width):
            frames.append(sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height)))
    return frames
dragon_jump_frames = split_spritesheet(sprites["dragon_jump"], 21, 14)
dragon_idle_frames = split_spritesheet(sprites["dragon_idle"], 32, 32)
dragon_rect = dragon_jump_frames[0].get_rect(midbottom=(30, 120))
basket_rect = sprites["basket"].get_rect(midbottom=(64, 120))
apples = [{"rect": sprites["apple"].get_rect(center=(random.randint(10, 118), -10)), "speed": 1}]
cacti = [{"rect": sprites["cactus"].get_rect(midbottom=(random.randint(150, 300), 120)), "speed": 2}]
pipes = [{"rect": sprites["pipe"].get_rect(midtop=(WIDTH + 20, random.randint(-60, -20)))}]
clock = pygame.time.Clock()
def reset_variables():
    global score, misses, surv, flappy_time, jumping, jump_speed, cacti, pipes, dragon_rect
    score = 0
    misses = 0
    surv = 0
    flappy_time = 0
    jumping = False
    jump_speed = 0
    dragon_rect = dragon_jump_frames[0].get_rect(midbottom=(30, 120))
    cacti = [{"rect": sprites["cactus"].get_rect(midbottom=(random.randint(150, 300), 120)), "speed": 2}]
    pipes = [{"rect": sprites["pipe"].get_rect(midtop=(WIDTH + 20, random.randint(-60, -20)))}]
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    anim += animsp
    if (state == "home" or state == "done") and anim >= len(dragon_idle_frames):
        anim = 0
    elif anim >= len(dragon_jump_frames):
        anim = 0
    if state == "home":
        game_surface.blit(backgrounds["home"], (0, 0))
        text = font.render("Press SPACE to Start!", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        game_surface.blit(text, text_rect)
        idle_dragon_rect = dragon_idle_frames[int(anim)].get_rect(center=(WIDTH // 2, HEIGHT // 2 + 34))
        game_surface.blit(dragon_idle_frames[int(anim)], idle_dragon_rect)

        if keys[pygame.K_SPACE]:
            state = "apple_catch"
            reset_variables()

    elif state == "apple_catch":
        game_surface.blit(backgrounds["apple_catch"], (0, 0))
        game_surface.blit(sprites["basket"], basket_rect)
        if basket_rect.bottom > HEIGHT:
            basket_rect.bottom = HEIGHT
        if keys[pygame.K_LEFT] and basket_rect.left > 0:
            basket_rect.x -= 4
        if keys[pygame.K_RIGHT] and basket_rect.right < WIDTH:
            basket_rect.x += 4
        for apple in apples:
            apple["rect"].y += apple["speed"]
            game_surface.blit(sprites["apple"], apple["rect"])
            if apple["rect"].colliderect(basket_rect):
                score += 1
                apple["rect"].center = (random.randint(10, 118), -10)
                apple["speed"] = random.randint(1, 2)
            elif apple["rect"].y > HEIGHT:
                misses += 1
                apple["rect"].center = (random.randint(10, 118), -10)
                apple["speed"] = random.randint(1, 2)
        score_text = font.render(f"Score: {score}", True, WHITE)
        misses_text = font.render(f"Misses: {misses}", True, RED)
        game_surface.blit(score_text, (5, 5))
        game_surface.blit(misses_text, (5, 15))
        if score >= 15:
            state = "dino"
            cacti[0]["rect"].x = 150
        elif misses >= 5:
            state = "home"
    elif state == "dino":
        game_surface.blit(backgrounds["dino"], (0, 0))
        if not jumping:
            game_surface.blit(dragon_jump_frames[0], dragon_rect) 
            if keys[pygame.K_SPACE]:
                jumping = True
                jump_speed = -6
        else:
            game_surface.blit(dragon_jump_frames[int(anim)], dragon_rect) 
            dragon_rect.y += jump_speed
            jump_speed += gravity
            if dragon_rect.bottom >= HEIGHT - 8:
                jumping = False
                dragon_rect.bottom = HEIGHT - 8
        for cactus in cacti:
            cactus["rect"].x -= cactus["speed"]
            game_surface.blit(sprites["cactus"], cactus["rect"])
            if cactus["rect"].right < 0:
                cactus["rect"].x = random.randint(150, 300)
            if dragon_rect.colliderect(cactus["rect"]):
                state = "home"
        surv += 1 / FPS
        timer_text = font.render(f"Time: {int(surv)}", True, WHITE)
        game_surface.blit(timer_text, (5, 5))
        if surv >= 45:
            state = "flappy"
            pipes = [
                {"rect": sprites["pipe"].get_rect(midtop=(WIDTH + 20, random.randint(-60, -20)))}
            ]
    elif state == "flappy":
        game_surface.blit(backgrounds["flappy"], (0, 0))
        dragon_rect.y += 1
        if keys[pygame.K_SPACE]:
            dragon_rect.y -= 2
        game_surface.blit(dragon_jump_frames[int(anim)], dragon_rect)
        for pipe in pipes:
            pipe["rect"].x -= flappy_speed
            game_surface.blit(sprites["pipe"], pipe["rect"])
            bottom_rect = pygame.Rect(
                pipe["rect"].left,
                pipe["rect"].bottom + pipe_gap,
                pipe["rect"].width,
                HEIGHT,
            )
            game_surface.blit(sprites["pipe"], bottom_rect)
            if pipe["rect"].right < 0:
                pipe["rect"].x = WIDTH + 20
                pipe["rect"].y = random.randint(-60, -20)
            if dragon_rect.colliderect(pipe["rect"]) or dragon_rect.colliderect(bottom_rect):
                state = "home"
        if dragon_rect.top < 0 or dragon_rect.bottom > HEIGHT:
            state = "home"
        flappy_time += 1 / FPS
        if flappy_time >= 45:
            print("YOU WON!") 
            state = "done"
    elif state == "done":
        game_surface.blit(backgrounds["home"], (0, 0))
        text = font.render("YOU WIN !", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        game_surface.blit(text, text_rect)
        idle_dragon_rect = dragon_idle_frames[int(anim)].get_rect(center=(WIDTH // 2, HEIGHT // 2 +34))
        game_surface.blit(dragon_idle_frames[int(anim)], idle_dragon_rect)
    scaled_surface = pygame.transform.scale(game_surface, (SCALED_WIDTH, SCALED_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
