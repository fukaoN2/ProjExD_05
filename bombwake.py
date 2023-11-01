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

# ボムの設定
bomb_image = pygame.image.load("ex05/data/bom1.png")
bomb_image = pygame.transform.rotozoom(bomb_image, 0, 0.11)
bomb_rect = bomb_image.get_rect()
bomb_spawn_interval = 3000  # ボムの出現間隔(ミリ秒)
next_bomb_spawn_time = 0

#格子の追加
black_floor = pygame.image.load("ex05/data/black.png")
red_floor = pygame.image.load("ex05/data/red.png")
yellow_floor = pygame.image.load("ex05/data/yellow_lines.jpg")

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
    if new_bomb_x < 24 or new_bomb_x > 774 - bomb_rect.width:
        bomb_speed_x *= -1
    else:
        bomb_x = new_bomb_x

    if (new_bomb_y < 76 and bomb_speed_y < 0) or new_bomb_y > 574 - bomb_rect.height:
        bomb_speed_y *= -1
    else:
        bomb_y = new_bomb_y

    # 赤側上辺
    if 24 <= bomb_x <= 194 and 110 <= bomb_y <= 170 and bomb_speed_y > 0:
        bomb_speed_y *= -1

    # 黒側上辺
    if 555 <= bomb_x <= 744 and 110 <= bomb_y <= 170 and bomb_speed_y > 0:
        bomb_speed_y *= -1

    # 赤側底辺
    if 24 <= bomb_x <= 194 and 390<= bomb_y <= 410 and bomb_speed_y < 0:
        bomb_speed_y *= -1

    # 黒側底辺
    if 555 <= bomb_x <= 744 and 390<= bomb_y <= 410 and bomb_speed_y < 0:
        bomb_speed_y *= -1

    # 赤側右辺
    if 194 <= bomb_x <= 214 and 170 <= bomb_y <= 390 and bomb_speed_x < 0:
        bomb_speed_x *= -1

    # 黒側左辺
    if 543 <= bomb_x <= 563 and 170 <= bomb_y <= 390 and bomb_speed_x > 0:
        bomb_speed_x *= -1


    # ボムの描画
    screen.blit(bomb_image, (bomb_x, bomb_y))

def safezone_def():
    # # 外枠の描画(実装時に削除・反射を確認するために描画)
    # pygame.draw.rect(background,(0,0,255),(24,76,750,498))

    # # 安全地帯の黄色の枠の範囲
    # pygame.draw.rect(background,(255,241,0),(555,170,189,240))
    # pygame.draw.rect(background,(255,241,0),(24,170,190,240))

    # 安全地帯の注意色の描画
    screen.blit(yellow_floor, (583, 180))
    screen.blit(yellow_floor, (24, 180))

    # # 安全地帯の黒と赤の四角の範囲
    # pygame.draw.rect(background,(0,0,0),(575,190,170,200))
    # pygame.draw.rect(background,(255,0,0),(24,190,169,200))

    # 安全地帯の黒と赤の格子の描画
    screen.blit(black_floor, (604, 204))
    screen.blit(red_floor, (24, -19))

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

    safezone_def()

    bomb_mvdef()



    # 画面更新
    pygame.display.update()
    clock.tick(fps)

# Pygameの終了
pygame.quit()
