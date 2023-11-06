import pygame
import random
import math
import time
import cv2

# Pygameの初期化
pygame.init()

# 画面の設定
screen_width = 800
screen_height = 600
fps = 60
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ボムへいをわけろ！")

# フレームを管理する時計をclockに格納
clock = pygame.time.Clock()
running = True

# 背景画像の読み込み
background = pygame.image.load("ex05/deta/background.png")

# ボムの設定
bomb_image = pygame.image.load("ex05/deta/bom1.png")
bombred_image = pygame.image.load("ex05/deta/bomred2.png")
bomb_image = pygame.transform.rotozoom(bomb_image, 0, 0.11)
bombred_image = pygame.transform.rotozoom(bombred_image, 0, 0.11)
bomb_rect = bomb_image.get_rect()
bombred_rect = bombred_image.get_rect()
bomb_spawn_interval = 3000  # ボムの出現間隔(ミリ秒)
next_bomb_spawn_time = 0

#動画用
video_file = "deta/bom.mp4"
cap = cv2.VideoCapture(video_file)
frame_rate = 60  # 動画のフレームレート

# 動画の幅と高さを取得
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_size = (video_width, video_height)

# Pygameのスクリーンと同じサイズに動画をリサイズ
video_surface = pygame.Surface(video_size)


#格子の追加
black_floor = pygame.image.load("ex05/deta/black.png")
red_floor = pygame.image.load("ex05/deta/red.png")
yellow_floor = pygame.image.load("ex05/deta/yellow_lines.jpg")

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

        self.speed_y = random.random()
        while self.speed_y == 0:
            self.speed_y = random.random()

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

# ボムの移動に関する関数
def bomb_mvdef(bomb):
    # フレームごとの移動距離を計算
    seconds = 1 / time_passed  # フレームレートで割って秒に変換
    mv_x = bomb.speed_x * seconds * fps
    mv_y = bomb.speed_y * seconds * fps

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

    # ボムがsafezoneに接触したとき
    # 赤側safezone上辺
    if 24 <= bomb.x <= 194 and 133 <= bomb.y <= 190 and bomb.speed_y > 0:
        bomb.speed_y *= -1

    # 黒側safezone上辺
    if 555 <= bomb.x <= 744 and 133 <= bomb.y <= 190 and bomb.speed_y > 0:
        bomb.speed_y *= -1

    # 赤側safezone底辺
    if 24 <= bomb.x <= 194 and 390 <= bomb.y <= 410 and bomb.speed_y < 0:
        bomb.speed_y *= -1

    # 黒側safezone底辺
    if 555 <= bomb.x <= 744 and 390 <= bomb.y <= 410 and bomb.speed_y < 0:
        bomb.speed_y *= -1

    # 赤側safezone右辺
    if 174 <= bomb.x <= 204 and 150 <= bomb.y <= 390 and bomb.speed_x < 0:
        bomb.speed_x *= -1

    # 黒側safezone左辺
    if 537 <= bomb.x <= 563 and 150 <= bomb.y <= 390 and bomb.speed_x > 0:
        bomb.speed_x *= -1

    # ボムの描画
    # screen.blit(bomb_image, (bomb.x, bomb.y))
    if bomb is not None:
        screen.blit(bomb.image, (bomb.x, bomb.y))

def safezone_def():
    # # 外枠の描画(実装時に削除・反射を確認するために描画)
    # pygame.draw.rect(background,(0,0,255),(24,76,750,498))

    # # 安全地帯の黄色の枠の範囲
    # pygame.draw.rect(background,(255,241,0),(555,170,189,240))
    # pygame.draw.rect(background,(255,241,0),(24,170,190,240))

    # safezoneの注意色の描画
    screen.blit(yellow_floor, (583, 180))
    screen.blit(yellow_floor, (24, 180))

    # # 安全地帯の黒と赤の四角の範囲
    # pygame.draw.rect(background,(0,0,0),(575,190,170,200))
    # pygame.draw.rect(background,(255,0,0),(24,190,169,200))

    # 安全地帯内側の黒と赤の格子の描画
    screen.blit(black_floor, (604, 204))
    screen.blit(red_floor, (24, -19))

b1 = 0
b2 = 0
def safezone_pl(bomb):
    if 24 <= bomb.x <= 174 and 163 <= bomb.y <= 380:
        b1 = 1
        return
    elif 555 <= bomb.x <= 744 and 163 <= bomb.y <= 380:
        b2 = 1
        return

def safezone_af(bomb):
    # ボムがsafezoneに接触したとき
    # 赤側safezone上辺
    if 24 <= bomb.x <= 194 and 163 <= bomb.y <= 203 and bomb.speed_y < 0:
        bomb.speed_y *= -1

    # 黒側safezone上辺
    if 555 <= bomb.x <= 744 and 133 <= bomb.y <= 203 and bomb.speed_y < 0:
        bomb.speed_y *= -1

    # 赤側safezone底辺
    if 24 <= bomb.x <= 194 and 340 <= bomb.y <= 410 and bomb.speed_y > 0:
        bomb.speed_y *= -1

    # 黒側safezone底辺
    if 555 <= bomb.x <= 744 and 340 <= bomb.y <= 410 and bomb.speed_y > 0:
        bomb.speed_y *= -1

    # 赤側safezone右辺
    if 174 <= bomb.x <= 204 and 150 <= bomb.y <= 390 and bomb.speed_x > 0:
        bomb.speed_x *= -1

    # 黒側safezone左辺
    if 537 <= bomb.x <= 563 and 150 <= bomb.y <= 390 and bomb.speed_x < 0:
        bomb.speed_x *= -1

def play_gameover():
    running = True  # running変数を初期化
    is_paused = False  # is_paused変数を初期化
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_paused = not is_paused

        if not is_paused:
            ret, frame = cap.read()
            if not ret:
                # 動画が終了した場合、再生を終了
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame)
            video_surface.blit(frame, (0, 0))

        screen.fill((0, 0, 0))
        screen.blit(video_surface, (0, 0))
        pygame.display.flip()
        clock.tick(frame_rate)

    cap.release()

cnt = 0
# ゲームループ
running = True

play_gameover()
while running:
    # time_passed = clock.tick(fps)
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False

    # back()

    # safezone_def()

    # # 新しいボムを生成するタイミングを管理
    # current_time = time.time()
    # if current_time - next_bomb_spawn_time > bomb_spawn_interval / 1000:
    #     new_bomb = Bomb()  # 新しいボムのインスタンスを作成
    #     new_bomb.image = random.choice([bomb_image, bombred_image])  # ランダムにボムの画像を選択
    #     bombs.append(new_bomb)  # ボムをリストに追加
    #     next_bomb_spawn_time = current_time
    #     if cnt % 2 == 0 and bomb_spawn_interval >= 400:
    #         bomb_spawn_interval -= 100
    #     print(bomb_spawn_interval)
    #     cnt += 1

    # # ボムを移動して描画
    # bombs_to_remove = []
    # for bomb in bombs:
    #     bomb_mvdef(bomb)
    #     if safezone_pl(bomb):
    #         if (b1 == 1 and bomb_image) or (b2 == 1 and bombred_image):
    #                 break
    #         current_time = 100
    #         safezone_af(bomb)
    #     if current_time - bomb.created_time > 100:  # 20秒経過でボムを消去
    #         bombs_to_remove.append(bomb)
    # for bomb in bombs_to_remove:
    #     bombs.remove(bomb)

    # clock.tick()
    # # print(clock.get_fps())

    # 画面更新
    pygame.display.update()
    clock.tick(fps)

# Pygameの終了
pygame.quit()