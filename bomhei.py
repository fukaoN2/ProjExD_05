import pygame
import random

# Pygameの初期化
pygame.init()

# 画面の設定
screen_width = 768
screen_height = 575
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ボムへいをわけろ！")

class Bomb(pygame.sprite.Sprite):
    """
    ゲームキャラクターボム兵に関するクラス
    """

    def __init__(self):
        """
        ボム兵画像Surfaceを生成する
        引数1 num：ボム兵画像ファイル名の番号
        """
        super().__init__()
        bomb_image = pygame.transform.rotozoom(pygame.image.load("ex05/deta/bom1.png"), 0, 0.05)
        self.image = bomb_image
        self.rect = bomb_image.get_rect()
        # ボムの位置と速度
        bomb_x = screen_width/2
        bomb_y = 10
        self.bomb_speed_x = random.randint(-1, 1)
        self.bomb_speed_y = random.random()
        self.bomb_vx = (self.bomb_speed_x * 0.08) + bomb_x
        self.bomb_vy = (self.bomb_speed_y * 0.08) + bomb_y

    def update(self):
        """
        ボム兵を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(self.bomb_vx, self.bomb_vy * 0.08)


# 背景画像の読み込み
background = pygame.image.load("ex05/deta/background.png")

# ボムの設定

bomb_spawn_interval = 3000  # ボムの出現間隔（ミリ秒）
next_bomb_spawn_time = 0

# ボムのグループを作成
bombs = pygame.sprite.Group()

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 背景画像の描画
    screen.blit(background, (0, 0))

    # ボムの出現処理
    current_time = pygame.time.get_ticks()
    if current_time >= next_bomb_spawn_time:
        bomb = Bomb()
        bombs.add(bomb)
        # 次の出現時間を設定する
        next_bomb_spawn_time = current_time + bomb_spawn_interval

    # ボムの更新と描画
    bombs.update()
    bombs.draw(screen)

    # 画面更新
    pygame.display.update()

# Pygameの終了
pygame.quit()
