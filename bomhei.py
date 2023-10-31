import pygame
import random

# Pygameの初期化
pygame.init()

# 画面の設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ボムへいをわけろ！")

# 背景画像の読み込み
background = pygame.image.load("background.jpg")

# ボムの設定
bomb_image = pygame.image.load("bomb.png")
bomb_rect = bomb_image.get_rect()
bomb_spawn_interval = 3000  # ボムの出現間隔（ミリ秒）
next_bomb_spawn_time = 0

# ボムの位置と速度
bomb_x = random.randint(100, screen_width - 100)
bomb_y = random.randint(100, screen_height - 100)
bomb_speed_x = random.randint(1, 3)
bomb_speed_y = random.randint(1, 3)

# 安全地帯の設定
safe_zone = pygame.Rect(200, 200, screen_width - 400, screen_height - 400)

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 背景画像の描画
    screen.blit(background, (0, 0))

    # ボムの描画
    screen.blit(bomb_image, (bomb_x, bomb_y))

    # ボムの位置更新
    bomb_x += bomb_speed_x
    bomb_y += bomb_speed_y

    # ボムが壁に当たった場合の反射
    if bomb_x < 0 or bomb_x > screen_width - bomb_rect.width:
        bomb_speed_x *= -1
    if bomb_y < 0 or bomb_y > screen_height - bomb_rect.height:
        bomb_speed_y *= -1

    # ボムが安全地帯に入った場合の位置更新
    if not safe_zone.collidepoint(bomb_x, bomb_y):
        # ボムが安全地帯外に出た場合、ランダムな位置に再配置
        bomb_x = random.randint(100, screen_width - 100)
        bomb_y = random.randint(100, screen_height - 100)
        bomb_speed_x = random.randint(1, 3)
        bomb_speed_y = random.randint(1, 3)

    # ボムの出現間隔を管理
    current_time = pygame.time.get_ticks()
    if current_time > next_bomb_spawn_time:
        bomb_x = random.randint(100, screen_width - 100)
        bomb_y = random.randint(100, screen_height - 100)
        bomb_speed_x = random.randint(1, 3)
        bomb_speed_y = random.randint(1, 3)
        next_bomb_spawn_time = current_time + bomb_spawn_interval

    # 画面更新
    pygame.display.update()

# Pygameの終了
pygame.quit()
