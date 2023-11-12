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

# 爆発gif読み込み
gif = pygame.image.load("ex05/data/explosion.gif")

#格子の追加
black_floor = pygame.image.load("ex05/data/black.png")
red_floor = pygame.image.load("ex05/data/red.png")
yellow_floor = pygame.image.load("ex05/data/yellow_lines.jpg")

# ボムのリスト
bombs = []
safe_red = 0
safe_black = 0


def back():
    """
    画像の描画関数
    """
    # 背景画像の描画
    screen.blit(background, (0, 0))

def bomb_mvdef(bomb):
    """
    ボムの移動に関する関数
    """
    # フレームごとの移動距離を計算
    seconds = 1 / time_passed  # フレームレートで割って秒に変換
    mv_x = bomb.speed_x * seconds * fps
    mv_y = bomb.speed_y * seconds * fps

    if not(24 <= bomb.x <= 194 and 133 <= bomb.y <= 410) or(555 <= bomb.x <= 744 and 133 <= bomb.y <= 410):
        # ボムがセーフゾーン外にいる場合
        if current_time - bomb.created_time > 37:
            # 37秒以上経過したらボムを停止
            mv_x = 0
            mv_y = 0

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
    elif 555 <= bomb.x <= 744 and 133 <= bomb.y <= 190 and bomb.speed_y > 0:
        bomb.speed_y *= -1

    # 赤側safezone底辺
    elif 24 <= bomb.x <= 194 and 390 <= bomb.y <= 410 and bomb.speed_y < 0:
        bomb.speed_y *= -1

    # 黒側safezone底辺
    elif 555 <= bomb.x <= 744 and 390 <= bomb.y <= 410 and bomb.speed_y < 0:
        bomb.speed_y *= -1

    # 赤側safezone右辺
    elif 168 <= bomb.x <= 202 and 150 <= bomb.y <= 390 and bomb.speed_x < 0:
        bomb.speed_x *= -1

    # 黒側safezone左辺
    elif 537 <= bomb.x <= 563 and 150 <= bomb.y <= 390 and bomb.speed_x > 0:
        bomb.speed_x *= -1

    else:
        # screen.blit(bomb_image, (bomb.x, bomb.y))
        if bomb is not None:
            if bomb.dragging:
                bomb.x, bomb.y = pygame.mouse.get_pos()
                screen.blit(bomb.image, (bomb.x, bomb.y))
            else:
                screen.blit(bomb.image, (bomb.x, bomb.y))

def safezone_def():
    """
    外枠の描画(実装時に削除・反射を確認するために描画)
    """
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
    """
    ボムがセーフゾーン内にいるかどうか判定
    """
    if 24 <= bomb.x <= 174 and 163 <= bomb.y <= 380:
        return True
    elif 555 <= bomb.x <= 744 and 163 <= bomb.y <= 380:
        return True

def safezone_af(bomb):
    """
    ボムをセーフゾーン内で反射させる関数
    """
    # 赤側safezone上辺
    if 24 <= bomb.x <= 194 and 163 <= bomb.y <= 203 and bomb.speed_y < 0:
        bomb.speed_y *= -1

    # 黒側safezone上辺
    elif 555 <= bomb.x <= 744 and 133 <= bomb.y <= 203 and bomb.speed_y < 0:
        bomb.speed_y *= -1

    # 赤側safezone底辺
    elif 24 <= bomb.x <= 194 and 340 <= bomb.y <= 410 and bomb.speed_y > 0:
        bomb.speed_y *= -1

    # 黒側safezone底辺
    elif 555 <= bomb.x <= 744 and 340 <= bomb.y <= 410 and bomb.speed_y > 0:
        bomb.speed_y *= -1

    # 赤側safezone右辺
    elif 148 <= bomb.x <= 174 and 150 <= bomb.y <= 390 and bomb.speed_x > 0:
        bomb.speed_x *= -1

    # 黒側safezone左辺
    elif 537 <= bomb.x <= 593 and 150 <= bomb.y <= 390 and bomb.speed_x < 0:
        bomb.speed_x *= -1
        
def game_over(bomb):
    """
    ゲームオーバー時の関数
    """
    bomb.speed_x = 0
    bomb.speed_y = 0
    gif_rect = gif.get_rect()
    gif_x = bomb.x + (bomb_rect.width - gif_rect.width) / 2
    gif_y = bomb.y + (bomb_rect.height - gif_rect.height) / 2
    screen.blit(gif, (gif_x, gif_y))
    pygame.display.update()  # 画面を更新して爆発を表示
    bombs.remove(bomb)
    pygame.time.delay(2000)  # 2000ミリ秒（2秒）停止
    
    
class Bomb:
    """
    ボム兵を描写するためのクラス
    """
    def __init__(self):
        self.x = screen_width // 2 - bomb_rect.width // 2
        self.y = 0
        self.speed_x = 0  # 初期速度をゼロに設定
        self.speed_y = 0  # 初期速度をゼロに設定
        self.set_random_speed()
        self.created_time = time.time()
        self.dragging = False
        self.image = None
        self.in_safezone = False


    def set_random_speed(self):
        # ランダムな角度を設定
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
        self.score += 5 # スコアを5ずつ更新

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
        bombs.append(new_bomb)  # ボムをリストに追加
        next_bomb_spawn_time = current_time
        if cnt % 2 == 0 and bomb_spawn_interval >= 400:
            bomb_spawn_interval -= 100
        print(bomb_spawn_interval)
        # セーフゾーン内のボムを抽出
    safe_red_bombs = [bomb for bomb in bombs if bomb.in_safezone and bomb.image == bombred_image]
    safe_black_bombs = [bomb for bomb in bombs if bomb.in_safezone and bomb.image == bomb_image]

    # セーフゾーン内のボムが5体に達したらスコアを加算して描画対象から除外
    if len(safe_red_bombs) == 5:
        score.score_up()
        bombs = [bomb for bomb in bombs if not (bomb.in_safezone and bomb.image == bombred_image)]
        safe_red = 0

    if len(safe_black_bombs) == 5:
        score.score_up()
        bombs = [bomb for bomb in bombs if not (bomb.in_safezone and bomb.image == bomb_image)]
        safe_black = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for bomb in bombs:
                bomb_xval = bomb.x - int(pygame.mouse.get_pos()[0]) 
                bomb_yval = bomb.y - int(pygame.mouse.get_pos()[1]) 
                bomb_xval = abs(bomb_xval)
                bomb_yval = abs(bomb_yval)
                
                if bomb_xval <= 50 and bomb_yval <= 50:
                    bomb.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for bomb in bombs:
                bomb.dragging = False
                if 24 <= bomb.x <= 174 and 163 <= bomb.y <= 380:
                    if bomb.image == bombred_image and not bomb.in_safezone:
                        safe_red += 1
                        bomb.in_safezone = True  # ボムがセーフゾーンに入ったことをマーク
                        print(f"Red Safezone: {safe_red}")
                        safezone_af(bomb)
                    elif bomb.image == bomb_image and not bomb.in_safezone:
                        explosion_time = current_time
                        game_over(bomb)
                        running = False  # ゲーム終了
                elif 555 <= bomb.x <= 744 and 163 <= bomb.y <= 380:
                    if bomb.image == bombred_image and not bomb.in_safezone:
                        explosion_time = current_time
                        game_over(bomb)
                        running = False  # ゲーム終了
                    elif bomb.image == bomb_image and not bomb.in_safezone:
                        safe_black += 1
                        bomb.in_safezone = True  # ボムがセーフゾーンに入ったことをマーク
                        print(f"Black Safezone: {safe_black}")
                        safezone_af(bomb)
    
    # ボムを移動して描画
    bombs_to_remove = []
    for bomb in bombs:
        bomb_mvdef(bomb)
        if safezone_pl(bomb):
            current_time = 100
            safezone_af(bomb)
        if current_time - bomb.created_time > 40 and explosion_time is None:
            game_over(bomb)
            pygame.time.delay(2000)  # 2000ミリ秒（2秒）停止
            if bomb.dragging:
                pass
            else:
                bombs_to_remove.append(bomb)
                for bomb in bombs_to_remove:
                    bombs.remove(bomb)

    clock.tick()
    score.update(screen)

    # 画面更新
    pygame.display.update()
    clock.tick(fps)

# Pygameの終了
pygame.quit()
