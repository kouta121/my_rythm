import pygame
from pygame.locals import *
import sys
import time
import json

class Note:
    def __init__(self, lane, timing, travel_time):
        self.timing = timing
        self.lane = lane
        lane_x = {
            0:200,
            1:300,
            2:400, 
            3:500
        }
        self.x = lane_x[lane]
        self.y = -50
        self.speed = 5
        self.hit = False
        self.judge_time = travel_time + timing

    def update(self, current_time):
        if current_time >= self.timing:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, 50, 50))

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("rhythm")

    clock = pygame.time.Clock()

    lane_x = 350
    notes = []

    # JSONファイルからノートの情報を読み込む
    with open('charts/test.json', 'r') as f:
        note_data = json.load(f)
        for data in note_data:
            note = Note(data['lane'], data['timing'], 1830)  # ノートの位置とタイミングを設定
            notes.append(note)

    note_speed = 5

    note_time = 2000

    score = 0

    combo = 0
    max_combo = 0

    pressed_lane = 0

    font = pygame.font.Font(None, 50)


    while True:

        current_time = pygame.time.get_ticks()

        

        for event in pygame.event.get():
            if event.type == QUIT:
                print(f"Final Score: {score}")
                print(f"Max Combo: {max_combo}")
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_d:
                    pressed_lane = 0
                elif event.key == K_f:
                    pressed_lane = 1
                elif event.key == K_j:
                    pressed_lane = 2
                elif event.key == K_k:
                    pressed_lane = 3
                    
                for note in notes:

                    if note.hit:
                            continue
                    if note.lane != pressed_lane:
                            continue

                    diff = abs(current_time - note.judge_time)

                    if diff <= 50:
                        print("Perfect!")
                        score += 100
                        combo += 1
                        if combo > max_combo:
                            max_combo = combo
                        note.hit = True
                        break

                    elif diff <= 100:
                        print("Good!")
                        score += 50
                        combo += 1
                        if combo > max_combo:
                            max_combo = combo
                        note.hit = True
                        break
            


        for note in notes:

            if current_time >= note.timing:
                note.update(current_time)

            if not note.hit and current_time > note.judge_time + 100:
                print("Miss!")
                combo = 0
                note.hit = True

        screen.fill((0, 0, 0))

        for note in notes:
            if not note.hit:   
                note.draw(screen)
        pygame.draw.line(screen, (255, 0 , 0), (0, 500), (800, 500), 5)
        pygame.display.update()

        clock.tick(60)

if __name__ == "__main__":
    main()