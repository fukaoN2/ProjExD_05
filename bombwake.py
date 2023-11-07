import pygame
import random
import math
import time
import sys

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

# 背景画像の読み込み
background = pygame.image.load("ex05/data/background.png")


# ボムの設定
bomb_image = pygame.image.load("ex05/data/bom1.png")
bombred_image = pygame.image.load("ex05/data/bomred2.png")
bomb_image = pygame.transform.rotozoom(bomb_image, 0, 0.11)
bombred_image = pygame.transform.rotozoom(bombred_image, 0, 0.11)
bomb_rect = bomb_image.get_rect()
bombred_rect = bombred_image.get_rect()
bomb_spawn_interval = 3000  # ボムの出現間隔(ミリ秒)
next_bomb_spawn_time = 0

b1 = 0
b2 = 0
c1 = 0
c2 = 0

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
        self.dragging = False


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
safe_red = []
safe_black = []

def back():
    """
    画像の描画関数
    """
    # 背景画像の描画
    screen.blit(background, (0, 0))

# ボムの移動に関する関数
def bomb_mvdef(bomb):
    # フレームごとの移動距離を計算
    elapsed_time = time.time() - bomb.created_time
    seconds = 1 / time_passed  # フレームレートで割って秒に変換
    mv_x = bomb.speed_x * seconds * fps
    mv_y = bomb.speed_y * seconds * fps

    if not(24 <= bomb.x <= 194 and 133 <= bomb.y <= 410) or(555 <= bomb.x <= 744 and 133 <= bomb.y <= 410):
        # ボムがセーフゾーン外にいる場合
        if elapsed_time > 37:
            # 37秒以上経過したらボムを停止
            mv_x = 0
            mv_y = 0

    # # デバッグ情報の速度情報を表示
    #print(f"Bomb speed: {mv_x}, {mv_y}")

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
    if elapsed_time > 40:
        # 描画位置をボムの中心に調整
        gif_rect = gif.get_rect()
        gif_x = bomb.x + (bomb_rect.width - gif_rect.width) / 2
        gif_y = bomb.y + (bomb_rect.height - gif_rect.height) / 2
        screen.blit(gif, (gif_x, gif_y))
    else:
        # screen.blit(bomb_image, (bomb.x, bomb.y))
        if bomb is not None:
            if bomb.dragging:
                bomb.x, bomb.y = pygame.mouse.get_pos()
                screen.blit(bomb.image, (bomb.x, bomb.y))
                #print(f'True : {bomb.x} : {bomb.y}')
            else:
                screen.blit(bomb.image, (bomb.x, bomb.y))
                #print(f'False : {bomb.x} : {bomb.y}')

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

def safezone_pl(bomb):
    if 24 <= bomb.x <= 174 and 163 <= bomb.y <= 380:
        c1 = 1
        return
    elif 555 <= bomb.x <= 744 and 163 <= bomb.y <= 380:
        c2 = 1
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

class Score:
    """
    scoreを描写するためのクラス
    """
    def __init__(self):
        self.font = pygame.font.Font(None, 50)
        self.color = (255, 0, 0)
        self.score = 0
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, screen_height-50

    def score_up(self):
        self.score += 40

    def update(self, screen: pygame.Surface):
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        screen.blit(self.image, self.rect)

cnt = 0
score = Score()
# ゲームループ
running = True
explosion_time = None  # 爆発が発生した時間
while running:
    time_passed = clock.tick(fps)

    back()
    safezone_def()

    # 新しいボムを生成するタイミングを管理
    current_time = time.time()
    if current_time - next_bomb_spawn_time > bomb_spawn_interval / 1000:
        new_bomb = Bomb()  # 新しいボムのインスタンスを作成
        new_bomb.image = random.choice([bomb_image, bombred_image])  # ランダムにボムの画像を選択
        if new_bomb == bomb_image:
            b1 = 1
        elif new_bomb == bombred_image:
            b2 = 1
        bombs.append(new_bomb)  # ボムをリストに追加
        next_bomb_spawn_time = current_time
        if cnt % 2 == 0 and bomb_spawn_interval >= 400:
            bomb_spawn_interval -= 100
        print(bomb_spawn_interval)
        #safezone内のボム兵リストが40なるとscoreが40プラスされる
        if len(safe_red) == 40:
            score.score_up()
            bombs.clear()
            safe_red.clear()
        if len(safe_black) == 40:
            score.score_up()
            bombs.clear()
            safe_black.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for bomb in bombs:
                bomb_xval = bomb.x - int(pygame.mouse.get_pos()[0]) 
                bomb_yval = bomb.y - int(pygame.mouse.get_pos()[1]) 
                bomb_xval = abs(bomb_xval)
                bomb_yval = abs(bomb_yval)
                
                print(f"{bomb_xval},{bomb_yval}")
                if bomb_xval <= 50 and bomb_yval <= 50:
                #if bomb.rect.collidepoint(event.pos):
                    bomb.dragging = True
            # pygame.draw.rect(background, (0, 0, 255), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 10, 10))

        elif event.type == pygame.MOUSEBUTTONUP:
            for bomb in bombs:
                bomb.dragging = False
                if (b1 == 1 and c1 == 1) or (b2 == 1 and c2 == 1):
                        break
    
    # ボムを移動して描画
    bombs_to_remove = []
    for bomb in bombs:
        bomb_mvdef(bomb)
        if safezone_pl(bomb):
            current_time = 100
            safezone_af(bomb)
        if current_time - bomb.created_time > 40 and explosion_time is None:
            explosion_time = current_time  # 爆発時間を記録
            if bomb.dragging:
                pass
            else:
                bombs_to_remove.append(bomb)
                for bomb in bombs_to_remove:
                    bombs.remove(bomb)


    if explosion_time is not None and current_time - explosion_time > 1:
        running = False  # 爆発後1秒間でゲームを終了

    clock.tick()
    # print(clock.get_fps())
    score.update(screen)

    # 画面更新
    #print(bomb.dragging)
    pygame.display.update()
    clock.tick(fps)

# Pygameの終了
pygame.quit()
