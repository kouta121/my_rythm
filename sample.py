import pygame
from pygame.locals import *
import sys
import json

class Note:
    def __init__(self, lane, timing, travel_time):
        self.timing = timing
        self.lane = lane

        lane_x = {
            0: 210,
            1: 310,
            2: 410,
            3: 510
        }

        self.x = lane_x[lane]
        self.y = -50
        self.speed = 5
        self.hit = False
        self.judge_time = travel_time + timing

    def update(self, current_time):
        if current_time >= self.timing:
            self.y += self.speed

    def draw(self, screen, image):
        screen.blit(image, (self.x, self.y))



def main():

    pygame.init()

    # 音楽初期化
    pygame.mixer.init()
    pygame.mixer.music.load(r"audio\kazenoanthem.mp3")

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("rhythm")

    note_image = pygame.image.load(r"image\ChatGPT Image 2026年5月25日 22_14_46.png")
    note_image = pygame.transform.scale(note_image, (80, 80))

    clock = pygame.time.Clock()

    # ノート読み込み
    notes = []

    with open('charts/test.json', 'r') as f:
        note_data = json.load(f)

        for data in note_data:
            note = Note(data['lane'], data['timing'], 1830)
            notes.append(note)

    # 初期化
    score = 0

    combo = 0
    max_combo = 0

    pressed_lane = 0

    judge_text = ""
    judge_timer = 0

    scene = "title"

    font = pygame.font.Font(r"font\ContiNeue2P-1.0.1.otf", 20)

    start_time = 0

    lane_flash = [0, 0, 0, 0]

    while True:

        # ------------------------
        # イベント処理
        # ------------------------

        for event in pygame.event.get():

            if event.type == QUIT:
                print(f"Final Score: {score}")
                print(f"Max Combo: {max_combo}")

                pygame.quit()
                sys.exit()

            # ------------------------
            # タイトル画面
            # ------------------------

            if scene == "title":

                if event.type == KEYDOWN:

                    if event.key == K_SPACE:

                        scene = "game"

                        pygame.mixer.music.play()

                        start_time = pygame.time.get_ticks()

            # ------------------------
            # ゲーム画面
            # ------------------------

            elif scene == "game":

                if event.type == KEYDOWN:

                    if event.key == K_d:
                        pressed_lane = 0
                        lane_flash[0] = 10

                    elif event.key == K_f:
                        pressed_lane = 1
                        lane_flash[1] = 10

                    elif event.key == K_j:
                        pressed_lane = 2
                        lane_flash[2] = 10

                    elif event.key == K_k:
                        pressed_lane = 3
                        lane_flash[3] = 10

                    # ノート判定
                    for note in notes:

                        # 既に叩かれたノート
                        if note.hit:
                            continue

                        # レーン違い
                        if note.lane != pressed_lane:
                            continue

                        diff = abs(current_time - note.judge_time)

                        if diff <= 50:

                            print("Perfect!")

                            judge_text = "Perfect!"
                            judge_timer = 30

                            score += 100

                            combo += 1

                            if combo > max_combo:
                                max_combo = combo

                            note.hit = True
                            break

                        elif diff <= 100:

                            print("Good!")

                            judge_text = "Good!"
                            judge_timer = 30

                            score += 50

                            combo += 1

                            if combo > max_combo:
                                max_combo = combo

                            note.hit = True
                            break

        # ------------------------
        # タイトル画面描画
        # ------------------------

        if scene == "title":

            screen.fill((0, 0, 0))

            title_text = font.render(
                "Press SPACE to Start",
                True,
                (255, 255, 255)
            )

            screen.blit(title_text, (200, 300))

            pygame.display.update()

            clock.tick(60)

            continue

        # ------------------------
        # ゲーム更新
        # ------------------------

        current_time = pygame.time.get_ticks() - start_time

        # 判定文字タイマー
        if judge_timer > 0:
            judge_timer -= 1
        else:
            judge_text = ""

        # ノート更新
        for note in notes:

            if current_time >= note.timing:
                note.update(current_time)

            # Miss判定
            if not note.hit and current_time > note.judge_time + 100:

                print("Miss!")

                judge_text = "Miss!"
                judge_timer = 30

                combo = 0

                note.hit = True

        # ------------------------
        # 描画
        # ------------------------

        screen.fill((0, 0, 0))

        #レーン描画

        for i in range(4):

            pygame.draw.rect(screen, (40, 40, 40), (200 + i * 100 , 0, 100, 600))

            if lane_flash[i] > 0:

                flash_surface = pygame.Surface((100, 600), pygame.SRCALPHA)
                flash_surface.fill((255, 255, 255, 100))  # 半透明の白色
                screen.blit(flash_surface, (200 + i * 100, 0))

                lane_flash[i] -= 1

        for i in range(5):
            pygame.draw.line(screen, (255, 255, 255), (200 + i * 100, 0), (200 + i * 100, 600), 2)

        # 判定表示
        text = font.render(judge_text, True, (255, 255, 255))

        screen.blit(text, (350, 400))

        # コンボ表示
        combo_text = font.render(f"Combo: {combo}", True, (255, 255, 255))

        screen.blit(combo_text, (620, 250))

        # スコア表示
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))

        screen.blit(score_text, (0, 0))

        # ノート描画
        for note in notes:

            if not note.hit:
                note.draw(screen, note_image)

        # 判定ライン
        pygame.draw.line(screen, (255, 0, 0), (0, 500), (800, 500), 5)

        

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":
    main()