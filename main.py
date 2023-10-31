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
background = pygame.image.load("deta/start.png")

#背景音楽の読み込み
pygame.mixer.music.load("rule.mp3")
pygame.mixer.music.play(-1)

# メニューテキストのフォント設定
font = pygame.font.Font(None, 36)

# メニューテキストを作成
start_text = font.render("Start", True, (0, 0, 0))
exit_text = font.render("exit", True, (0, 0, 0))

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
                    subprocess.run(["python", "bomhei.py"])
                    # Pygameの終了
                    pygame.quit()
                    sys.exit()
            if 0 <= mouse_x <= 100:
                if 550 <= mouse_y <= 600:
                    # "終了" ボタンがクリックされたときの処理
                    pygame.quit()
                    sys.exit()


    screen.blit(start_text, (720, 550))
    screen.blit(exit_text, (30, 550))

    pygame.display.update()
