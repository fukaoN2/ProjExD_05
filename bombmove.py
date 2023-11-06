import pygame
import random
import math

# Pygameの初期化
pygame.init()

# 画面の設定
screen_width = 800
screen_height = 600
fps = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ボムへいをわけろ！")

# フレームを管理する時計をclockに格納
clock = pygame.time.Clock()

# 背景画像の読み込み
background = pygame.image.load("ex05/data/background.png")

#格子画像の読み込み
black_floor = pygame.image.load("ex05/data/black.png")
red_floor = pygame.image.load("ex05/data/red.png")
yellow_floor = pygame.image.load("ex05/data/yellow_lines.jpg")

# ボムの設定
bomb_image = pygame.image.load("ex05/data/bom1.png")
bomb_image = pygame.transform.rotozoom(bomb_image, 0, 0.11)
bomb_rect = bomb_image.get_rect()
bomb_spawn_interval = 3000  # ボムの出現間隔（ミリ秒）
next_bomb_spawn_time = 0

# ボムの位置と速度
bomb_x = screen_width // 2 - bomb_rect.width // 2  # 画面の中央部分に配置
bomb_y = 0
bomb_speed_x = 0
bomb_speed_y = 0



def back():
    """
    画像の描画関数
    """
    # 背景画像の描画
    screen.blit(background, (0, 0))

    # 外枠の描画(実装時に削除・反射を確認するために描画)
    #pygame.draw.rect(background,(0,0,255),(24,76,750,498))

    # 安全地帯の注意色の描画
    screen.blit(yellow_floor, (584, 180))
    screen.blit(yellow_floor, (24, 180))

    # 安全地帯の黒と赤の格子の描画
    screen.blit(black_floor, (604, 204))
    screen.blit(red_floor, (24, -19))

    # 安全地帯の黄色の枠の範囲
    #pygame.draw.rect(screen,(255,241,0),(584,180,190,240))
    #pygame.draw.rect(screen,(255,241,0),(24,180,190,240))

    # 安全地帯の黒と赤の四角の範囲
    #pygame.draw.rect(screen,(0,0,0),(604,204,170,192))
    #pygame.draw.rect(screen,(255,0,0),(24,204,168,191))


def bomb_mvdef():
    global bomb_x, bomb_y, bomb_speed_x, bomb_speed_y

    # フレームごとの移動距離を計算
    time_passed = clock.tick(fps)
    seconds = time_passed / 3000.0  # フレームレートで割って秒に変換
    mv_x = bomb_speed_x * seconds * fps
    mv_y = bomb_speed_y * seconds * fps

    bomb_x += mv_x
    bomb_y += mv_y

    # ボムの位置更新前に壁との衝突をチェック
    new_bomb_x = bomb_x + mv_x
    new_bomb_y = bomb_y + mv_y

    # 壁との衝突チェック
    if new_bomb_x < 0 or new_bomb_x > screen_width - bomb_rect.width:
        bomb_speed_x *= -1
    else:
        bomb_x = new_bomb_x

    if new_bomb_y < 0 or new_bomb_y > screen_height - bomb_rect.height:
        bomb_speed_y *= -1
    else:
        bomb_y = new_bomb_y

    # ボムの描画
    screen.blit(bomb_image, (bomb_x, bomb_y))


bombs = []

# ボムの位置と速度
bomb_x = screen_width // 2 - bomb_rect.width // 2  # 画面の中央部分に配置
bomb_y = 0
while(True):
    c = random.randint(-1, 1)
    if not(c == 0):
        bomb_speed_x = c
        break
while(True):
    b = random.random()
    if not(b == 0):
        bomb_speed_y = b
        break
d = round(1/(bomb_speed_x**2)+(bomb_speed_y**2), 1)
a = math.sqrt(abs(d))
bomb_speed_x = bomb_speed_x * a
bomb_speed_y = bomb_speed_y * a

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    back()

    bomb_mvdef()

    # 画面更新
    pygame.display.update()
    clock.tick(fps)

# Pygameの終了
pygame.quit()
