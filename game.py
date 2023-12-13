import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite:
    vertVelocity = 1.2
    rightFacing = True
    frameCounter = 0
    def update(self):
        pass
    def isPipe(self):
        return False
    def isGoomba(self):
        return False
    def isFireball(self):
        return False
    def removeable(self):
        return False
    
class Fireball(Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 37
        self.w = 37
        self.horzVelocity = 15
        self.fireball_image = pygame.image.load("fireball.png")
        
    def draw(self, screen, scrollPos):
        screen.blit(self.fireball_image, (self.x - scrollPos, self.y))
    
    def Bounce(self):
        #frame counter less than 5
        if(self.frameCounter < 5):
            self.vertVelocity -= 26

    def update(self):
        self.vertVelocity += 3 #this is gravity
        self.y += self.vertVelocity #update position
        self.x += self.horzVelocity

        self.frameCounter += 1

        if(self.y  > 513):
            self.vertVelocity = 0
            self.y = 513; #snap back to the ground
            self.frameCounter = 0
            self.Bounce()

    def isFireball(self):
        return True
    
class Goomba(Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 45
        self.w = 37
        self.direction = -1
        self.speed = 5
        self.burnFrames = 0
        self.onFire = False
        self.goomba_image = pygame.image.load("goomba.png")
        self.goombaFire_image = pygame.image.load("goomba_fire.png")
    
    def draw(self, screen, scrollPos):
        if self.onFire:
            screen.blit(self.goombaFire_image, (self.x - scrollPos, self.y))
        else:
            screen.blit(self.goomba_image, (self.x - scrollPos, self.y))
    
    def setPreviousPosition(self):
        self.prev_x = self.x
        self.prev_y = self.y
        
    def getOutOfPipe(self, pipe):
        #Goomba is coming from the left, moving to the right
        if(self.x + self.w >= pipe.x and self.prev_x + self.w <= pipe.x):
            #Goomba's right = pipes left
            self.x = pipe.x - self.w
            self.direction *= -1
        #Goomba is coming from the right, moving to the left
        if(self.prev_x >= pipe.x + pipe.w):
            #Goomba's right = pipes left
            self.x = pipe.x + pipe.w
            self.direction *= -1
        #if Goomba is coming from the air, moving down
        if(self.prev_y + self.h <= pipe.y):
            #Goomba's toes = pipe's top
            self.y = pipe.y - self.h
            self.vertVelocity = 0
        #coming from the ground, moving up 
        if(self.prev_y >= pipe.y + pipe.h):
            #Goomba's head = Pipe's bottom
            self.y = pipe.y + pipe.h
            self.vertVelocity = 0
    
    def update(self):
        self.vertVelocity += 5.5 #this is gravity
        self.y += self.vertVelocity #update position
        
        if not self.onFire:
            self.x += self.direction * self.speed
        else:
            self.burnFrames += 1

        if(self.y > 505):
            self.vertVelocity = 0
            self.y = 505 # snap back to the ground
    
    def removeable(self):
        if(self.burnFrames > 25):
            return True
        else:
            return False
   
    def isGoomba(self):
    	return True
    
class Pipe(Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 400
        self.w = 55
        self.pipe_image = pygame.image.load("pipe.png")
    
    def draw(self, screen, scrollPos):
        screen.blit(self.pipe_image, (self.x - scrollPos, self.y))
    
    def isPipe(self):
        return True
    
        
class Mario(Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 95
        self.w = 60
        self.currentImage = 0
        self.frameCounter = 0
        self.mario_images = []
        for x in range(1, 6):
            image = "mario" + str(x) + ".png"
            self.mario_images.append(pygame.image.load(image))
    
    def changeImageState(self):
        self.currentImage += 1
        if(self.currentImage >= len(self.mario_images)):
            self.currentImage = 0
            
    def setPreviousPosition(self):
        self.prev_x = self.x
        self.prev_y = self.y
    
    def Jump(self):
        #frame counter less than 5 AND the space bar is pressed
        if(self.frameCounter < 5):
            self.vertVelocity -= 15
            
    def draw(self, screen, scrollPos):
        if self.rightFacing:
            screen.blit(self.mario_images[self.currentImage], (self.x - scrollPos, self.y))
        else:
            screen.blit(pygame.transform.flip(self.mario_images[self.currentImage], True, False), (self.x - scrollPos, self.y))
    
    def getOutOfPipe(self, pipe):
        #Mario is coming from the left, moving to the right
        if(self.prev_x + self.w <= pipe.x):
            #mario's right = pipes left
            self.x = pipe.x - self.w

        #Mario is coming from the right, moving to the left
        if(self.prev_x >= pipe.x + pipe.w):
            #mario's right = pipes left
            self.x = pipe.x + pipe.w

        #if Mario is coming from the air, moving down
        if(self.prev_y + self.h <= pipe.y):
            #Mario's toes = pipe's top
            self.y = pipe.y - self.h
            self.vertVelocity = 0
            self.frameCounter = 0

        #coming from the ground, moving up 
        if(self.prev_y >= pipe.y + pipe.h):
            #Mario's head = Pipe's bottom
            self.y = pipe.y + pipe.h
            self.vertVelocity = 0
    
    def update(self):
        self.vertVelocity += 5.5; #this is gravity
        self.y += self.vertVelocity; #update position
        self.frameCounter += 1

        if(self.y > 455):
            self.vertVelocity = 0
            self.y = 455; #snap back to the ground
            self.frameCounter = 0

class Model():
    
	def __init__(self):
		self.sprites = []
		self.mario = Mario(100, 455)
		self.sprites.append(self.mario)
		self.sprites.append(Pipe(4, 150))
		#self.sprites.append(Pipe(150, 0)) #for testing head bump
		self.sprites.append(Pipe(280, 331))
		self.sprites.append(Pipe(456, 250))
		self.sprites.append(Pipe(738, 200))
		self.sprites.append(Pipe(970, 312))
		self.sprites.append(Pipe(1766, 374))
		self.sprites.append(Goomba(360, 455))
		self.sprites.append(Goomba(620, 455))
		self.sprites.append(Goomba(888, 455))
		self.sprites.append(Goomba(1360, 455))
		self.sprites.append(Goomba(1280, 455))
		self.sprites.append(Goomba(1215, 455))

	def addFireball(self, x, y):
		self.sprites.append(Fireball(x, y))
                           
	def checkCollision(self, a, b):
		#sprite's left > sprite right  not colliding
		if(b.x > (a.x + a.w)):
			return False
		#sprite's right < sprite's left  not colliding 
		if((b.x + b.w) < a.x):
			return False
		#sprite's bottom < sprite's top
		if((b.y + b.h) < a.y):
			return False
		#sprite's top > sprite's bottom 
		if(b.y > (a.y + a.h)):
			return False

		#if colliding 
		return True

	def update(self):
		removeFireball = []
		removeGoomba = []
		for sprite in self.sprites:
			sprite.update()
			if sprite.isPipe():
				check = self.checkCollision(sprite, self.mario)
				if check:
					self.mario.getOutOfPipe(sprite)
			if sprite.isGoomba():
				for sprite2 in self.sprites:
					if sprite2.isPipe():
						check = self.checkCollision(sprite2, sprite)
						if check:
							sprite.getOutOfPipe(sprite2)
					if sprite2.isFireball():
						if sprite2.x > self.sprites[0].x + 1000:
							removeFireball.append(sprite2)
						check = self.checkCollision(sprite2, sprite)
						if check:
							sprite.onFire = True
							removeFireball.append(sprite2)
				if sprite.removeable():
					removeGoomba.append(sprite)
		self.sprites = [i for i in self.sprites if i not in removeGoomba and i not in removeFireball]

class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.ground_image = pygame.image.load("ground.png")
		self.model = model
		self.scrollPos = 0

	def update(self):
		self.scrollPos = self.model.mario.x - 100
		self.screen.fill([152,245,255])
		self.screen.blit(self.ground_image, (0 - self.scrollPos, 550))
		self.screen.blit(self.ground_image, (2010 - self.scrollPos, 550))
		for sprite in self.model.sprites:
			sprite.draw(self.screen, self.scrollPos)
		pygame.display.flip()

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
		self.model.sprites[0].setPreviousPosition()
		for i in range(len(self.model.sprites)):
			if self.model.sprites[i].isGoomba():
				self.model.sprites[i].setPreviousPosition()

		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					self.keep_going = False
				if event.key == K_LCTRL:
					self.model.addFireball(self.model.mario.x, self.model.mario.y + 50)
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.mario.x -= 10
			self.model.mario.changeImageState()
			self.model.mario.rightFacing = False
		if keys[K_RIGHT]:
			self.model.mario.x += 10
			self.model.mario.changeImageState()
			self.model.mario.rightFacing = True
		if keys[K_SPACE]:
			self.model.mario.Jump()

print("Use the arrow keys to move and ctrl to throw fireballs. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")