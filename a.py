import pygame
from pygame.locals import *
import sys

def event():
    # イベント処理
    for event in pygame.event.get():  # イベントを取得
        if event.type == QUIT:        # 閉じるボタンが押されたら
            pygame.quit()             
            sys.exit()                # 終了


pygame.init()                                 # Pygameの初期化
screen = pygame.display.set_mode((800, 600))  # 800*600の画面
px=120
py=100
while True:
    screen.fill((255,255,255))                                     # 背景を白に
    pygame.draw.circle(screen,(10,10,10),(px,py),50)               # ●
    px += 1
    pygame.display.update()                                        # 画面更新
    event()
