import sys
import pygame
import os
import random

pygame.init()

screen=pygame.display.set_mode((1100,600)) #寬1100，高600的視窗

running=[
    pygame.image.load(os.path.join("assets","Dino","Chrome Dino Run.png")),
    pygame.image.load(os.path.join("assets","Dino", "Chrome Dino Run 2.png"))
] #導入圖片
jumping=  pygame.image.load(os.path.join("assets","Dino","Dino Jump.png"))
ducking=[
    pygame.image.load(os.path.join("assets","Dino", "Dino Duck.png")),
    pygame.image.load(os.path.join("assets","Dino", "Dino Duck 2.png"))
]
cloud=pygame.image.load(os.path.join("assets","Other","Chrome Dinosaur Cloud.png"))
bg=pygame.image.load(os.path.join("assets","Other","Chrome Dinosaur Track.png"))
small_cactus=[
    pygame.image.load(os.path.join("assets","Cactus","Chrome Dinosaur Small Cactus.png")),
    pygame.image.load(os.path.join("assets","Cactus","Chrome Dinosaur Small Cactus (1).png")),
    pygame.image.load(os.path.join("assets","Cactus","Chrome Dinosaur Small Cactus (2).png"))
]
large_cactus=[
    pygame.image.load(os.path.join("assets","Cactus","Chrome Dinosaur Large Cactus.png")),
    pygame.image.load(os.path.join("assets","Cactus","Chrome Dinosaur Large Cactus (1).png")),
    pygame.image.load(os.path.join("assets","Cactus","Chrome Dinosaur Large Cactus (2).png"))
]
bird=[
    pygame.image.load(os.path.join("assets","Bird","Chrome Dinosaur Bird1.png")),
    pygame.image.load(os.path.join("assets", "Bird", "Chrome Dinosaur Bird2.png"))
]
class Dino:
    X_pos = 80 #x座標
    Y_pos = 310
    Y_pos_duck = 340 #蹲下時座標向下
    set_jump_vel = 8.5 #跳躍高度

    def __init__(self): #初始化物件的屬性
        self.duck_img = ducking
        self.run_img = running
        self.jump_img = jumping

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False #開始時是跑步狀態

        self.step_index = 0
        self.jump_vel = self.set_jump_vel
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect() #.get_rect() 取得圖片寬高及位置
        self.dino_rect.x = self.X_pos
        self.dino_rect.y = self.Y_pos

    def update(self, userInput) : #更新恐龍控制狀態 ##userInput 玩家輸入狀態
        if self.dino_duck:
                self.duck()  #self.dino_duck為True時 執行對應動作
        if self.dino_run:
                self.run()
        if self.dino_jump:
                self.jump()

        if self.step_index >= 10:
                self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
                self.dino_duck = False
                self.dino_run = True
                self.dino_jump = False

    def duck(self):
            self.image = self.duck_img[self.step_index // 5 ]
            #//表無條件捨去 index <= 9  只有0or1的可能
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_pos
            self.dino_rect.y = self.Y_pos_duck
            self.step_index += 1
            self.dino_rect.width = self.dino_rect.width - 33

    def run(self):
            self.image = self.run_img[self.step_index // 5 ]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_pos
            self.dino_rect.y = self.Y_pos
            self.dino_rect.width = self.dino_rect.width - 30  ### 縮小更多寬度
            self.step_index += 1

    def jump(self):
            self.image = self.jump_img
            if self.dino_jump:
                self.dino_rect.y -= self.jump_vel * 5
                self.jump_vel -= 0.85
            if self.jump_vel < -self.set_jump_vel:
                self.dino_jump = False
                self.jump_vel = self.set_jump_vel

    def draw(self, SCREEN):  #將圖片畫到畫面上
            SCREEN.blit(self.image, (self.dino_rect.x,self.dino_rect.y))
            #pygame.draw.rect(SCREEN, (255, 0, 0), self.dino_rect, 2) ###


class Cloud:
    def __init__(self):
        self.x = 1100 + random.randint(500,2000)
        #random.randint 產生指定範圍內的隨機整數 ##x座標在螢幕寬度(前面設定的1100)加上500~2000間的隨機數值
        self.y = random.randint(50,200)
        self.image = cloud
        self.width = self.image.get_width() #self.width 讀取雲朵的寬度

    def update(self):
        self.x -= game_speed
        if self.x < -self.width: #雲朵完全移動到螢幕外
            self.x = 1100 + random.randint(500,1500)
            self.y = random.randint(50,200)

    def draw (self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obs:
    def __init__(self,image,type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = 1100 #(螢幕寬度)
        self.rect.y = 0
        self.x_pos = float(self.rect.x)


    def update(self):
        self.rect.x = int(self.rect.x - game_speed)
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type],self.rect)
        ###pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)  # 畫出碰撞框，確認對齊


class SmallCactus(Obs):
    def __init__(self,image):
        self.type = random.randint (0,2) #隨機選擇0or1or2
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obs):
    def __init__(self,image):
        self.type = random.randint (0,2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obs):
    def __init__(self,image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 10:
            self.index = 0
        SCREEN.blit(self.image[self.index//5],self.rect)
        self.index += 1

def main(): #main函式執行遊戲
    run = True
    clock = pygame.time.Clock() #Clock管理遊戲更新速度與時間間隔
    player = Dino()
    clouds = Cloud()
    global game_speed, x_pos_bg, y_pos_bg, obstacles, points
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    obstacles = []
    death_count = 0
    points = 0
    font = pygame.font.Font(os.path.join("assets","font","ARCADECLASSIC.TTF"), 30)

    def background():
        global x_pos_bg , y_pos_bg
        image_width = bg.get_width()
        bg_rect = bg.get_rect()
        screen.blit(bg, (x_pos_bg,y_pos_bg))
        screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg=0
        x_pos_bg -= game_speed
        bg_rect.x = x_pos_bg

    def score():
        global points, game_speed
        points +=1
        if points % 100 == 0: #每100分加1點速度
            game_speed += 1

        text = font.render(str(points), True, (94, 94, 94))
        textRect = text.get_rect()
        textRect.center = (1000, 60)
        screen.blit(text, textRect)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((255,255,255)) #設定畫布顏色
        background()
        userInput = pygame.key.get_pressed()

        if len(obstacles) == 0 :
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(small_cactus))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(large_cactus))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(bird))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect): #.colliderect 檢測物件碰撞
                ###pygame.draw.rect(screen, (255, 0, 0), player.dino_rect, 2)  # 紅色框表示恐龍
                ###pygame.draw.rect(screen, (0, 255, 0), obstacle.rect , 2)  # 綠色框表示障礙物
                ###pygame.display.update()  # 更新畫面以顯示矩形
                death_count += 1
                #pygame.time.wait(5000)
                menu(death_count)


        player.draw(screen)
        clouds.draw(screen)
        player.update(userInput)
        clouds.update()
        score()

        clock.tick(30) #畫面更新每秒30次
        pygame.display.update()

def menu(death_count):

    global points
    run = True
    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(os.path.join("assets","font","ARCADECLASSIC.TTF"), 30)
        if death_count == 0 :
            text = font.render("Press any key to start", True,(94, 94, 94))
        elif death_count > 0 :
            text = font.render("Press any key to start", True,(94, 94, 94))
            score_text = font.render(f"Your Score  {points}" , True, (94, 94, 94))
            scoreRect = score_text.get_rect()
            scoreRect.center = (1100 // 2, 600 // 2+50 )
            screen.blit(score_text, scoreRect)

        textRect = text.get_rect()
        textRect.center = (1100 // 2, 600//2)
        screen.blit(text, textRect)
        screen.blit(running[0], (1100 // 2 -20, 600 // 2-140))

        pygame.display.update()
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :
                main()

menu(death_count=0)