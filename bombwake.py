import pygame
import random
import math

# Pygameの初期化
pygame.init()

# 画面の設定
screen_width = 768
screen_height = 575
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ボムへいをわけろ！")

# 背景画像の読み込み
background = pygame.image.load("ex05/deta/background.png")

#背景音楽の読み込み
pygame.mixer.music.load("ex05/deta/BGM.mp3")
pygame.mixer.music.play(-1)

# ボムの設定
bomb_image = pygame.image.load("ex05/deta/bom1.png")
bomb_image = pygame.transform.rotozoom(bomb_image, 0, 0.05)
bomb_rect = bomb_image.get_rect()
bomb_spawn_interval = 3000  # ボムの出現間隔（ミリ秒）
next_bomb_spawn_time = 0


# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 背景画像の描画
    screen.blit(background, (0, 0))

    # 画面更新
    pygame.display.update()

# Pygameの終了
pygame.quit()
