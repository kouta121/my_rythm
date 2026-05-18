import pygame
from pygame.locals import *
import sys

class Note:
    def __init__(self, x, timing):
        self.timing = timing
        self.x = x
        self.y = -50
        self.speed = 5
        self.hit = False

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
    notes = [Note(350, 2000),
             Note(350, 3000),
            Note(350, 4000)
        ]  # ノートの初期位置とタイミングを設定

    note_speed = 5

    note_time = 2000

    while True:

        current_time = pygame.time.get_ticks()
        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    for note in notes:

                        if note.hit:
                            continue

                        diff = abs(current_time - note.timing)

                        if diff <= 50:
                            print("Perfect!")
                            note.hit = True
                            break

                        elif diff <= 100:
                            print("Good!")
                            note.hit = True
                            break



        for note in notes:
            if current_time >= note.timing:
                note.update(current_time)

        screen.fill((0, 0, 0))

        for note in notes:
            if not note.hit:   
                note.draw(screen)
        pygame.draw.line(screen, (255, 0 , 0), (0, 500), (800, 500), 5)
        pygame.display.update()

        clock.tick(60)

if __name__ == "__main__":
    main()