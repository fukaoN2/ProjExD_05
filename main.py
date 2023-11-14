import pygame
import sys
import subprocess

# Pygameの初期化
pygame.init()

# ウィンドウの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ゲームメニュー")

# 背景画像の読み込み
background = pygame.image.load("ex05/data/start.png")

# 背景音楽の読み込み
pygame.mixer.music.load("ex05/data/rule.mp3")
pygame.mixer.music.play(-1)

# メニューテキストのフォント設定
font = pygame.font.Font(None, 36)

# 日本語フォントの読み込み
jafont = pygame.font.Font("ex05/data/ipaexg.ttf", 36)

# メニューテキストを作成
start_text = font.render("Start", True, (0, 0, 0))
exit_text = font.render("exit", True, (0, 0, 0))


def setumei():
    y_position = 150
    # 説明文を作成
    setumei1 = "あかい爆弾は あかいじんち、"
    setumei2 = "くろい爆弾は くろのじんちに"
    setumei3 = "はこぼう！"
    setumei4 = "まちがった じんちに はこぶと"
    setumei5 = "だいバクハツしてしまう！！！"
    setumei6 = "爆弾ができてから 20びょうがたっても"
    setumei7 = "だいバクハツだ！！！！！！！！！！"
    for setumei_text in [setumei1, setumei2, setumei3, setumei4, setumei5, setumei6, setumei7]:
        bun = jafont.render(setumei_text, True, (255, 255, 255))
        y_position +=  40 # 各行ごとに描画
        screen.blit(bun, (80, y_position))

def run_image_animation():
    """
    星のアニメーション描画するための関数
    """
    # ウィンドウの設定
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("画像拡大アニメーション")

    # 画像を読み込む
    image = pygame.image.load("ex05/data/ダウンロード.png")

    # 初期サイズ
    width, height = 1600, 1200

    # 目標サイズ
    target_width, target_height = 12000, 9000

    # アニメーション時間（秒）
    animation_duration = 0.3

    # アニメーションのフレーム数
    frames = 60  # 60フレーム/秒

    # アニメーションの速度計算
    speed = ((target_width - width) / (frames * animation_duration), (target_height - height) / (frames * animation_duration))

    clock = pygame.time.Clock()
    elapsed_time = 0

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        width += speed[0]
        height += speed[1]

        if width >= target_width and height >= target_height:
            # 目標サイズに達したらアニメーション終了
            width = target_width
            height = target_height

        # 画像を指定サイズに拡大
        scaled_image = pygame.transform.scale(image, (int(width), int(height)))

        screen.fill((255, 255, 255))  # 白い背景
        screen.blit(scaled_image, (screen_width // 2 - width // 2, screen_height // 2 - height // 2))

        pygame.display.update()
        clock.tick(frames)

        elapsed_time += 1 / frames

        if elapsed_time >= animation_duration:
            break


# メインループ
while True:
    for event in pygame.event.get():
        # 背景画像の描画
        screen.blit(background, (0, 0))
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 700 <= mouse_x <= 750:
                if 500 <= mouse_y <= 650:
                    # "ゲームを始める" ボタンがクリックされたときの処理
                    print("ゲームを始めるが選択されました")
                    pygame.mixer.music.stop()
                    # アニメーションの実行
                    run_image_animation()

                    subprocess.run(["python", "ex05/bombwake.py"])

                    pygame.quit()
                    sys.exit()

            if 0 <= mouse_x <= 100:
                if 550 <= mouse_y <= 600:
                    # "終了" ボタンがクリックされたときの処理
                    pygame.quit()
                    sys.exit()

    setumei()
    screen.blit(start_text, (720, 550))
    screen.blit(exit_text, (30, 550))

    pygame.display.update()