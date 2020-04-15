import pygame
import random
from pygame import mixer
# to initialize pygame
pygame.init()

#create screen
screen=pygame.display.set_mode((800,600))

#background
background=pygame.image.load("308.jpg")

#backgroung sound
mixer.music.load("kick.mp3")
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
 
#player
playerImg=pygame.image.load("ship.png")
playerX=370
playerY=480
playerX_change=0

#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("monster.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(30)

#bullet
bulletImg=pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"

#score
score_value=0
font=pygame.font.Font("freesansbold.ttf",32)
textX=10
textY=10

def show_score(x,y):
    score=font.render("score : "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

#gameove
game_over=pygame.font.Font("freesansbold.ttf",64)

def game_over_text():
    over_text=game_over.render("Game Over",True,(255,255,255))
    screen.blit(over_text,(200,250))


#drawing the stuf
def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

#collision of bullet with enemy:
def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance= ((enemyX-bulletX)**2+(enemyY-bulletY)**2)**.5   
    if distance < 27:
        return True
    else:
        return False
#to open the screen or game loop
running =True
while running:
    #screen of background
    screen.fill((1,1,1)) 
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        #if close button is presed
        if event.type == pygame.QUIT:
            running =False    
    # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_LEFT:
                playerX_change=-5
            if event.key ==pygame.K_RIGHT:  
                playerX_change=5
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    bullet_sound=mixer.Sound("bullet.wav")
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key ==pygame.K_LEFT or event.key ==pygame.K_RIGHT: 
                playerX_change=0
    playerX+=playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736 

    #enemy movement    
    for i in range(num_of_enemies):
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break

        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i] +=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-4
            enemyY[i] +=enemyY_change[i]
        #collision
        collision=iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explor_sound=mixer.Sound("Blast.wav")
            explor_sound.play()
            bulletY=480
            bullet_state="ready"
            score_value+=1
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)
        enemy(enemyX[i],enemyY[i],i)

    #bulletmovement
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    if bulletY<=0:
        bullet_state="ready"
        bulletY=480

    player(playerX,playerY)
    show_score(textX,textY)
    # to update the screen
    pygame.display.update()

