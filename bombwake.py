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

    #通常フィールド(実装時には要らないが反射確認のために描画)
    pygame.draw.rect(background,(0,0,255),(24,72,720,480))

    #安全地帯の黄色の枠
    pygame.draw.rect(background,(255,241,0),(555,170,189,240))
    pygame.draw.rect(background,(255,241,0),(24,170,190,240))

    #安全地帯の黒と赤の四角
    pygame.draw.rect(background,(0,0,0),(575,190,170,200))
    pygame.draw.rect(background,(255,0,0),(24,190,169,200))
    
    # 背景画像の描画
    screen.blit(background, (0, 0))

    # 画面更新
    pygame.display.update()

# Pygameの終了
pygame.quit()
