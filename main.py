#2.1
import pygame
from sys import exit
from random import randint
import os

PATH = os.path.abspath(".") + "/"
pygame.init()

graphics = "graphics"

axolotl = False

with open(PATH+"Videogaim/save.txt") as save:
    bool_string = save.read()
    if bool_string == "True":
        axolotl = True


if axolotl:
    graphics = "axolotl_graphics"


class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(PATH+"Videogaim/"+graphics+"/spaceship_alt.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = (30,320))
        self.powerup = "default"

    def spaceship_input(self):
        mouse_x = pygame.mouse.get_pos()[0]
        pygame.event.get()
        touch = pygame.mouse.get_pressed()[0]
        if touch and mouse_x < 720:
            mouse_y = pygame.mouse.get_pos()[1]
            if abs(mouse_y - self.rect.y) < 15:
                self.rect.y = mouse_y
            elif mouse_y < self.rect.y and self.rect.top > 0:
                self.rect.y -= 15
            elif mouse_y > self.rect.y and self.rect.bottom < 720:
                self.rect.y += 15  
        if touch and mouse_x > 720:
            self.shoot()


    def shoot(self):
        if self.powerup == "default"  and len(projectiles.sprites()) < 1:
            projectiles.add(Laser(self.rect.center))
            laser_sound.play()

        elif self.powerup == "gattling":
            projectiles.add(GattlingLaser(self.rect.center))
            projectiles.add(GattlingLaser(self.rect.midbottom))
            projectiles.add(GattlingLaser(self.rect.midtop))
            if laser_sound.get_num_channels() >= 1:
                pass
            else:
                laser_sound.play()

        elif self.powerup == "enemy"  and len(obstacles.sprites()) < 1:
            obstacles.add(EnemyLaser(self.rect.center))
            laser_sound.play()

    def update(self):
        self.spaceship_input()  

class MirrorShip(Spaceship):
    def __init__(self, spaceship_y):
        super().__init__()
        self.image = pygame.image.load(PATH+"Videogaim/"+graphics+"/mirrorship.png").convert_alpha()
        self.rect = self.image.get_rect(midtop = (1360, spaceship_y))
        self.powerup = "enemy"


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(PATH+"Videogaim/"+graphics+"/laser.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = 20

    def movement(self):
        self.rect.x += self.speed
    
    def destroy(self):
        if self.rect.x >= 1460:
            self.kill()

    def update(self):
        self.movement()
        self.destroy()

class GattlingLaser(Laser):
    def __init__(self, pos):
        super().__init__(pos)
        self.speed = 40

class EnemyLaser(Laser):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.image.load(PATH+"Videogaim/"+graphics+"/enemylaser.png").convert_alpha()
        self.speed = -20
        

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(PATH+"Videogaim/"+graphics+"/Meteor_alt.png").convert_alpha()
        self.height = randint(120, 720)
        self.rect = self.image.get_rect(bottomleft = (1440,self.height))
        self.speed = randint(8, 20)

    def movement(self):
        if(self.rect.right > 0):
            self.rect.x -= self.speed

    def kill(self, no_suicide=True):
        super(Meteor, self).kill()
        if break_sound.get_num_channels() >= 1:
            pass
        elif no_suicide:
            break_sound.play()
          

    def update(self):
        self.movement()
        self.destroy()

    def destroy(self):
        if self.rect.right <= 0:
            self.kill(no_suicide=False) 

class StormMeteor(Meteor):
    def __init__(self):
        super().__init__()
        self.speed = randint(18,25)


#setting variables
lives = 3    
background = 0 
score = 0
angle = 0
game_active = False
bob_counter = 0
bob_direct = 0
pause = False
gameplay_event = "default"
boss_count = 0
meteorstorm_counter = 0

# -display & clock
screen = pygame.display.set_mode((1440,720), pygame.SCALED|pygame.FULLSCREEN)
pygame.display.set_caption("Shooty Shooty Rocks")
gameIcon = pygame.image.load(PATH+"Videogaim/graphics/icon.png")
pygame.display.set_icon(gameIcon)
clock = pygame.time.Clock()

darken = pygame.image.load(PATH+"Videogaim/graphics/darken.png").convert_alpha()

background_count = 0
nebula = pygame.image.load(PATH+"Videogaim/"+graphics+"/Nebula1.png").convert()
nebula_rect = nebula.get_rect(topleft = (background,0))
nebula2 = pygame.image.load(PATH+"Videogaim/"+graphics+"/Nebula1.png").convert()
nebula2_rect = nebula2.get_rect(topleft = (background,0))

text_font = pygame.font.Font(PATH+"Videogaim/Font/Pixeltype.ttf", 50)
pause_font = pygame.font.Font(PATH+"Videogaim/Font/Pixeltype.ttf", 120)

spaceship = pygame.sprite.GroupSingle()
spaceship.add(Spaceship())

obstacle_counter = 0
obstacle_interval = 120   #default = 120
obstacle_multiplier = 50
obstacles = pygame.sprite.Group()
obstacles.add(Meteor())

boss = pygame.sprite.GroupSingle()

projectiles = pygame.sprite.Group()

font_surface = text_font.render("Score: " + str(score), False, "white")
font_rect = font_surface.get_rect(topleft = (10,10))

lives_surface = text_font.render("Lives: " + str(lives), False, "white")
lives_rect = lives_surface.get_rect(topleft = font_rect.bottomleft)

pause_surface = pause_font.render("Paused", False, "white")
pause_rect = pause_surface.get_rect(center = (720,360))

menu_surface = pause_font.render("Shooty Shooty Rocks",False,"#ffffff")
menu_rect = menu_surface.get_rect(center = (720,190))
menu_sub_surface = text_font.render("Press to start",False,"#ffffff")
menu_sub_rect = menu_sub_surface.get_rect(center = (720,660))
menu_spaceship = pygame.image.load(PATH+"Videogaim/"+graphics+"/spaceship_alt.png").convert_alpha()
menu_spaceship = pygame.transform.rotozoom(menu_spaceship,90,2)
menu_spaceship_rect = menu_spaceship.get_rect(center = (720,380))

warning = pygame.image.load(PATH+"Videogaim/"+graphics+"/warning.png")
warning_rect = warning.get_rect(center = (1360, 380))

#sounds
laser_sound = pygame.mixer.Sound(PATH+"Videogaim/sounds/laser.mp3")
break_sound = pygame.mixer.Sound(PATH+"Videogaim/sounds/explosion.mp3")

#running loop
while True:
    #game loop
    while game_active:

        #pause loop            
        while pause:
            screen.blit(nebula,nebula_rect)
            screen.blit(nebula2,nebula2_rect)              
            obstacles.draw(screen)
            projectiles.draw(screen)
            boss.draw(screen)
            spaceship.draw(screen)
            screen.blit(darken,(0,0))
            screen.blit(pause_surface,pause_rect)   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause = False
                        pygame.mixer.unpause()      
            pygame.display.update()
            clock.tick(10)
        
        background_count += 1
        if background_count == 2:
            nebula_rect.x -= 1 
            nebula2_rect.x -= 1
            background_count = 0

        if nebula_rect.right == 1440:
            nebula2_rect.left = 1440
        if nebula2_rect.right == 1440:
            nebula_rect.left = 1440 

        if score > 10 and gameplay_event == "default":
            if randint(0, int((1000/(score/10))*1000) ) == 1:
                meteorstorm_counter = 0
                gameplay_event = "meteorstorm"
                spaceship.sprite.powerup = "gattling"

        if gameplay_event == "default":
            if score % obstacle_multiplier == 0 and score != 0:
                obstacle_interval /= 2
                obstacle_multiplier *= 2
            if obstacle_counter >= obstacle_interval:
                obstacles.add(Meteor())
                obstacle_counter = 0
            obstacle_counter += 1
        
        elif gameplay_event == "meteorstorm":
            meteorstorm_counter += 1
            if meteorstorm_counter < 200:
                pass
            else:
                obstacles.add(StormMeteor())
            if meteorstorm_counter >= 1200:
                gameplay_event = "default"
                spaceship.sprite.powerup = "default"

        elif gameplay_event == "mirrorboss":
            if boss_count < 1:
                boss.add(MirrorShip(spaceship.sprite.rect.y))
                boss_count += 1

        #collision
        for obstacle_index, obstacle in enumerate(obstacles.sprites()):
            #crashes without exception when obstacles group changes rapidly, basically brute forces code to work
            try:
                if pygame.sprite.spritecollide(obstacles.sprites()[obstacle_index], projectiles, True):
                    obstacles.sprites()[obstacle_index].kill()
                    if gameplay_event == "default" or gameplay_event == "meteorstorm":
                        obstacle_counter = obstacle_interval
                        score += 1
                        font_surface = text_font.render("Score: " + str(score), False, "white")
            except IndexError:
                pass

        if(pygame.sprite.spritecollide(spaceship.sprite, obstacles, True)):
            lives -= 1
            lives_surface = text_font.render("Lives: " + str(lives), False, "white")

        #background                                                                   
        screen.blit(nebula,nebula_rect)
        screen.blit(nebula2,nebula2_rect)
        #game objects               
        obstacles.draw(screen)
        obstacles.update()
        if len(projectiles.sprites()) >= 1:
            projectiles.draw(screen)
            projectiles.update()
        if meteorstorm_counter < 200 and gameplay_event == "meteorstorm":
            screen.blit(warning, warning_rect)
        if boss_count == 1:
            boss.draw(screen)
            boss.update()
        spaceship.draw(screen)
        spaceship.update()
        screen.blit(font_surface,font_rect)
        screen.blit(lives_surface,lives_rect)

        #death
        if lives == 0:
            game_active = False

        #allows user to quit    
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    pygame.mixer.pause()                
 
        pygame.display.update()
        clock.tick(30)

    #main menu loop and value resets   
    while game_active == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and menu_spaceship_rect.collidepoint(pygame.mouse.get_pos()):
                if axolotl:
                    with open(PATH+"Videogaim/save.txt", "w") as save:
                        save.write("False")
                else:
                    with open(PATH+"Videogaim/save.txt", "w") as save:
                        save.write("True")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_active = True
                #reset values
                lives = 3
                score = 0
                obstacles.empty()
                projectiles.empty()
                gameplay_event = "default"
                obstacle_interval = 120
                font_surface = text_font.render("Score: " + str(score), False, "white")
                lives_surface = text_font.render("Lives: " + str(lives), False, "white")
        screen.blit(nebula,nebula_rect)
        screen.blit(nebula2,nebula2_rect)
        screen.blit(darken,(0,0))
        screen.blit(menu_surface,menu_rect)
        screen.blit(menu_spaceship,menu_spaceship_rect)
        if bob_direct == 0:
            if bob_counter < 10:
                menu_spaceship_rect.y += 1
                bob_counter += 1
            elif bob_counter == 10:
                bob_direct += 1
        elif bob_direct == 1:
            if bob_counter > 0:
                menu_spaceship_rect.y -= 1
                bob_counter -= 1  
            elif bob_counter == 0:
                bob_direct -= 1                   
        screen.blit(menu_sub_surface,menu_sub_rect)
        pygame.display.update()
        clock.tick(30)       
             