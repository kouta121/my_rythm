import pygame
from pygame.locals import *
import sys

def main():
    pygame.init()                                   # Pygameの初期化
    screen = pygame.display.set_mode((800, 600))    # 800 x 600の大きさの画面を作る
    pygame.display.set_caption("rythm")              # 画面上部に表示するタイトルを設定

    x = 100
    y = 100

    lane_x = 300
    lane_y = 600
    lane_width = 100
    lane_height = 100

    while True:
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()       # Pygameの終了(画面閉じられる)
                sys.exit()

        notes = []
        current_time = pygame.time.get_ticks()  # 現在の時間をミリ秒で取得
        if current_time >= note_time:  # ノートの時間が来たら
            note.visible = True  # ノートを表示する

        diff = abs(current_time - note.time)  # ノートの時間と現在の時間の差を計算
        if diff <= 50:  # タイミングが50ms以内ならヒットとする
            print("Perfect!")
        if diff <= 100:  # タイミングが100ms以内ならグッドとする
            print("Good!")
        else:  # タイミングが100ms以上ならミスとする
            print("Miss!")

        screen.fill((0,0,0))        # 画面を黒色に塗りつぶし
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 50, 50))  # 赤色の四角形を描画
        pygame.display.update()     # 画面を更新


if __name__ == "__main__":
    main()
