#PARTICLE GAME
#BY ALEXANDER VINCENT-HILL

#MODULES
import pygame, pygame.font
import random
import math
import sys

#KEYPRESSCODE
from pygame.locals import *

#CONSTANTS
background_color = (0,0,0)
(width, height) = (1000, 1000)
elasticity = 0.9852
drag = 0.9999
gravitationalconstant=0.01
numberofparticles=50
particlesize=10
randomsizes = False
attraction = False
directionofgravity = 1 #GRAVITY DOWN AS DEFAULT

#FUNCTIONS
def addVectors(angle1, length1, angle2, length2):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)
    return (angle, length)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

def checkOverlap(p1,p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dist = math.hypot(dx, dy)
    if dist <= (p1.size + p2.size)*1.01:
        return True
    else:
        return False

#TO DO: MAKE ATTRACTION AND COLLISION PHYSICAL
def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent
        angle1 = 2*tangent - p1.angle
        angle2 = 2*tangent - p2.angle
        speed1 = p2.speed*elasticity
        speed2 = p1.speed*elasticity
        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)
        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)
        
def attract(p1,p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    adist = math.hypot(dx, dy)
    if adist < 2*p1.size + 2*p2.size:
        atangent = math.atan2(dy, dx)
        (p1.angle, p1.speed) = (atangent-math.pi/2, p1.speed)
        (p2.angle, p2.speed) = (atangent+math.pi/2, p2.speed)

#TO DO: ADD ORBIT MECHANIC
#TO DO: ADD CHAIN REACTION MECHANIC
#TO DO: ADD CHEMICAL REACTION MECHANIC
        
#PARTICLE CLASS
class Particle:
    def __init__(self, x, y, size, color = (0,0,0), thickness=1):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.thickness = size
        self.speed = 0
        self.angle = 0
        
    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors(self.angle, self.speed, math.pi*directionofgravity, gravitationalconstant)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

#SCREEN SETTINGS
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('PARTICLE GAME')

#PARTICLE CHARACTERISTICS
my_particles1 = []

for z in range(numberofparticles):
    if randomsizes == True:
        size = random.randint(4,15)
    else:
        size = particlesize
    x = random.randint(size, width - size)
    y = random.randint(size, height - size)
    particle = Particle(x, y, size)
    particle.speed = random.uniform(0,.5)
    particle.angle = random.uniform(0,math.pi*2)
    my_particles1.append(particle)

#EXECUTION
selected_particle = None
running = True
while running:
    screen.fill(background_color)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles1, mouseX, mouseY)

        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

        elif event.type == pygame.KEYDOWN:
            if event.key == K_DOWN:
                directionofgravity=1
                gravitationalconstant=0.01
            if event.key == K_SPACE:
                gravitationalconstant=0.00
            if event.key == K_UP:
                gravitationalconstant=0.01
                directionofgravity=2
            if event.key == K_RIGHT:
                gravitationalconstant=0.01
                directionofgravity=0.5
            if event.key == K_LEFT:
                gravitationalconstant=0.01
                directionofgravity=1.5
            if event.key == K_a:
                attraction = not attraction

#ESCAPING PYGAME WINDOW
            if event.key == K_ESCAPE:
                pygame.display.quit()
                sys.exit()

#ELASTICITY ADJUSTMENT
    keys = pygame.key.get_pressed()
    if keys[K_LSHIFT]:
        if elasticity<2.0000:
                elasticity+=.0001
    if keys[K_LCTRL]:
        if elasticity>0.0000:
                elasticity-=.0001

#PICKING UP A PARTICLE
    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1

#CREATES PARTICLES
    for i, particle in enumerate(my_particles1):
        particle.move()
        particle.bounce()

#IMPLEMENT PARTICLE ATTRACTION AND COLLISION
        for particle2 in my_particles1[i+1:]:
            collide(particle, particle2)

        #for particle2 in my_particles1[i+1:]:
            #if checkOverlap(particle, particle2):
                #print("bang")
            
        if attraction == True:    
            for particle2 in my_particles1[i+1:]:
                attract(particle, particle2)

        particle.display()
        y=150 #colorscalefactor
        if particle.speed*y <= 255:
            particle.color = (255, particle.speed*y, particle.speed*y)
        else:
            particle.color = (255, 255, 255)

#DISPLAYS TEXT ON SCREEN
    pygame.font.init()
    myfont = pygame.font.SysFont("monospace", 15)
    line1 = myfont.render("Press Esc to quit", 1, (255,255,255))
    screen.blit(line1, (5, 5))
    line2 = myfont.render("Arrow keys and spacebar control gravity", 1, (255,255,255))
    screen.blit(line2, (5, 20))
    line3 = myfont.render("LShift/LCtrl keys control elasticity (+/-)", 1, (255,255,255))
    screen.blit(line3, (5, 35))
    line4 = myfont.render("Elasticity = " + str(elasticity), 1, (255,255,255))
    screen.blit(line4, (5, 50))
    line5 = myfont.render("Press a to toggle interparticle attraction", 1, (255,255,255))
    screen.blit(line5, (5, 65))

    pygame.display.flip()
