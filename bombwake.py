import pygame
import random
import math
import time

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

# 爆発gif
gif = pygame.image.load("ex05/data/explosion.gif")

#格子の追加
black_floor = pygame.image.load("ex05/data/black.png")
red_floor = pygame.image.load("ex05/data/red.png")
yellow_floor = pygame.image.load("ex05/data/yellow_lines.jpg")

# ボムクラスを定義
class Bomb:
    def __init__(self):
        self.x = screen_width // 2 - bomb_rect.width // 2
        self.y = 0
        self.speed_x = 0  # 初期速度をゼロに設定
        self.speed_y = 0  # 初期速度をゼロに設定
        self.set_random_speed()
        self.created_time = time.time()

    def set_random_speed(self):
        # ランダムな速度を設定
        self.speed_x = random.randint(-1, 1)
        while self.speed_x == 0:
            self.speed_x = random.randint(-1, 1)

        self.speed_y = random.uniform(-1, 1)
        while self.speed_y == 0:
            self.speed_y = random.uniform(-1, 1)

        d = round(1 / (self.speed_x ** 2 + self.speed_y ** 2), 1)
        a = math.sqrt(abs(d))
        self.speed_x *= a
        self.speed_y *= a

# ボムのリスト
bombs = []

def back():
    """
    画像の描画関数
    """
    # 背景画像の描画
    screen.blit(background, (0, 0))

def bomb_mvdef(bomb):
    # フレームごとの移動距離を計算
    elapsed_time = time.time() - bomb.created_time
    time_passed = clock.tick(fps)
    seconds = time_passed / 1000.0  # フレームレートで割って秒に変換
    
    mv_x = bomb.speed_x * seconds * fps * 0.5  # 速度調整
    mv_y = bomb.speed_y * seconds * fps * 0.5  # 速度調整
    
    if not(24 <= bomb.x <= 194 and 133 <= bomb.y <= 410) or(555 <= bomb.x <= 744 and 133 <= bomb.y <= 410):
        # ボムがセーフゾーン外にいる場合
        if elapsed_time > 7:
            # 7秒以上経過したらボムを停止
            mv_x = 0
            mv_y = 0
            
    # # デバッグ情報の速度情報を表示
    # print(f"Bomb speed: {mv_x}, {mv_y}")


    bomb.x += mv_x
    bomb.y += mv_y

    # ボムの位置更新前に壁との衝突をチェック
    new_bomb_x = bomb.x + mv_x
    new_bomb_y = bomb.y + mv_y

    # 壁との衝突チェック
    if new_bomb_x < 24 or new_bomb_x > 774 - bomb_rect.width:
        bomb.speed_x *= -1
    else:
        bomb.x = new_bomb_x

    if (new_bomb_y < 76 and bomb.speed_y < 0) or new_bomb_y > 574 - bomb_rect.height:
        bomb.speed_y *= -1
    else:
        bomb.y = new_bomb_y

    # 赤側上辺
    if 24 <= bomb.x <= 194 and 133 <= bomb.y <= 190 and bomb.speed_y > 0:
        bomb.speed_y *= -1

    # 黒側上辺
    if 555 <= bomb.x <= 744 and 133 <= bomb.y <= 190 and bomb.speed_y > 0:
        bomb.speed_y *= -1

    # 赤側底辺
    if 24 <= bomb.x <= 194 and 390 <= bomb.y <= 410 and bomb.speed_y < 0:
        bomb.speed_y *= -1

    # 黒側底辺
    if 555 <= bomb.x <= 744 and 390 <= bomb.y <= 410 and bomb.speed_y < 0:
        bomb.speed_y *= -1

    # 赤側右辺
    if 174 <= bomb.x <= 204 and 150 <= bomb.y <= 390 and bomb.speed_x < 0:
        bomb.speed_x *= -1

    # 黒側左辺
    if 537 <= bomb.x <= 563 and 150 <= bomb.y <= 390 and bomb.speed_x > 0:
        bomb.speed_x *= -1

    # ボムの描画
    if elapsed_time > 10:
        # 描画位置をボムの中心に調整
        gif_rect = gif.get_rect()
        gif_x = bomb.x + (bomb_rect.width - gif_rect.width) / 2
        gif_y = bomb.y + (bomb_rect.height - gif_rect.height) / 2
        screen.blit(gif, (gif_x, gif_y))
    else:
        screen.blit(bomb_image, (bomb.x, bomb.y))

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

# ゲームループ
running = True
explosion_time = None  # 爆発が発生した時間

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    back()

    safezone_def()

    # 新しいボムを生成するタイミングを管理
    current_time = time.time()
    if current_time - next_bomb_spawn_time > bomb_spawn_interval / 2000:
        new_bomb = Bomb()  # 新しいボムのインスタンスを作成
        bombs.append(new_bomb)  # ボムをリストに追加
        next_bomb_spawn_time = current_time

    # ボムを移動して描画
    bombs_to_remove = []
    for bomb in bombs:
        bomb_mvdef(bomb)
        if current_time - bomb.created_time > 1000:  # 20秒経過でボムを消去
            bombs_to_remove.append(bomb)
        if current_time - bomb.created_time > 10 and explosion_time is None:
            explosion_time = current_time  # 爆発時間を記録
    for bomb in bombs_to_remove:
        bombs.remove(bomb)
        
    if explosion_time is not None and current_time - explosion_time > 1:
        running = False  # 爆発後1秒間でゲームを終了

    # 画面更新
    pygame.display.update()
    clock.tick(fps)

# Pygameの終了
pygame.quit()