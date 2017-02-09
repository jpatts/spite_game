# sample_ball.py
#
# A sample program consisting of an animated ball which bounces off of the edges of the screen.
#
# B. Bird - 01/27/2016

import sys, os, platform
#Set up import paths for the SDL2 libraries
if platform.system() == 'Linux':
	os.environ['PYSDL2_DLL_PATH'] = os.path.join(os.getcwd(),'lib_linux')
elif platform.system() == 'Darwin':
	os.environ['PYSDL2_DLL_PATH'] = os.path.join(os.getcwd(),'lib_osx')
elif platform.system() == 'Windows':
	os.environ['PYSDL2_DLL_PATH'] = os.path.join(os.getcwd(),'lib_windows')
  
import sdl2
import sdl2.ext
from sdl2 import *
import sdl2.sdlgfx
import time
import math
from point import Vector2d
from random import *


def rotate_vector( v, angle_degrees ):
	rot_x, rot_y = math.cos(angle_degrees*math.pi/180), math.sin(angle_degrees*math.pi/180)
	return Vector2d( v.x*rot_x - v.y*rot_y, rot_x*v.y+rot_y*v.x )

class A2Canvas:
	CANVAS_SIZE_X = 800
	CANVAS_SIZE_Y = 700
	BALL_RADIUS = 15
	BALL_VELOCITY = 150
	BALL_COLOURS = ( 
					(0,0,0),
					(255,0,0),
					(0,255,0),
					(0,0,255),
					(0,255,255),
					(255,0,255),
					(255,255,0)
				   )
	
	def __init__(self):
		#Initialization
		self.ball_position = Vector2d(self.CANVAS_SIZE_X/2, self.CANVAS_SIZE_Y/2)
		self.ball_direction = rotate_vector( Vector2d( 0, 0 ), 0)
		self.ball_colour_idx = 0
		#f character
		self.f_velocity = 1
		self.f_position = Vector2d(400, 300)
		self.f_position2 = Vector2d(430, 300)
		self.f_position3 = Vector2d(400, 320)
		self.f_position4 = Vector2d(430, 320)
		self.f_position5 = Vector2d(400, 360)
		self.score = 0
		#enemy / pear
		self.x = randint(0, 535)
		self.enemy_position = Vector2d(799, self.x + 29)
		self.enemy_position2 = Vector2d(799, self.x + 45)
		self.enemy_position3 = Vector2d(800, self.x + 10)
		self.enemy_position4 = Vector2d(798, self.x)	
		self.enemy_velocity = 1
		self.enemy_hit = False
		#timers
		self.keys_down = set()
		self.enemy_timer = 0
		self.a_timer = 0
		self.d_timer = 0
		self.w_timer = 0
		self.s_timer = 0
		self.SPACE_timer = 0
		self.shoot_timer = 0
		self.respawn_timer = 0
		self.pillar_timer = 10
		self.pillar2_timer = 5
		self.immune_timer = 0
		#shoot
		self.shoot = Vector2d(self.f_position3.x, self.f_position3.y)
		self.shoot2 = Vector2d(self.f_position4.x, self.f_position4.y)
		self.shoot_velocity = 1
		self.shooted = False
		#pillar1
		self.p1 = uniform(.001, .009)
		self.i = randint(100, 280)
		self.pillar = Vector2d(799, 0)
		self.pillar2 = Vector2d(840, self.i)
		#pillar2
		self.p2 = uniform(.001, .009)
		self.j = randint(320, 500)
		self.pillar3 = Vector2d(799, 600)
		self.pillar4 = Vector2d(840, self.j)
		#UI
		self.life = 3
		self.immune = False
		f = open('output.txt', 'r')
		self.highScore = f.read()
		f.close()
		#power up dp
		self.double_penetration = False
		self.zy = randint(15, 585)
		self.zx = 800
		z = randint(3, 5)
		self.z_timer = time.time() + z
		#power up shield
		self.shield_up = False
		self.sy = randint(15, 585)
		self.sx = 800
		s = randint(1, 3)
		self.shield_timer = time.time() + s
		#title screen / tutorial
		self.new_game = False
		self.continue_game = False
		self.play_game = False
		self.play_game_new = False
		self.play_tutorial = False
		self.play_tutorial2 = False
		self.play_tutorial3 = False
		self.new_delay = time.time()
		self.new_delay2 = time.time()
		self.new_delay3 = time.time()
		#the bird is the word
		self.bird_timer = 0
		self.bird1 = Vector2d(625, 300)
		self.bird2 = Vector2d(650, 350)
		self.bird3 = Vector2d(595, 250)
		self.bird_left = False
		self.bird_right = False
		self.bird_up = False
		self.bird_down = False
		self.attack_timer = 0
		self.bird1_attack = Vector2d(self.bird1.x, self.bird1.y)
		self.bird2_attack = Vector2d(self.bird2.x, self.bird2.y)
		self.bird3_attack = Vector2d(self.bird3.x, self.bird3.y)
		self.attack = False
		self.up_right = False
		self.down_right = False
		self.up_left = False
		self.down_left = False
		self.attack_speed = 0
		self.enemy_life = 15
	
	def title_screen(self):
		#sdl2.sdlgfx.gfxPrimitivesSetFont('', 160, 160)
		sdl2.sdlgfx.stringRGBA(renderer, 390, 300, 'SPITE', 0, 0, 0, 255)
		sdl2.sdlgfx.stringRGBA(renderer, 380, 400, 'NEW GAME', 0, 0, 0, 255)
		if int(self.highScore) > 0:
			sdl2.sdlgfx.stringRGBA(renderer, 380, 500, 'CONTINUE', 0, 0, 0, 255)
		else:
			sdl2.sdlgfx.stringRGBA(renderer, 380, 500, 'CONTINUE', 0, 0, 0, 64)
		if self.new_game == True:
			sdl2.sdlgfx.thickLineRGBA(renderer, 350, 402, 360, 402, 3, 255, 255, 255, 255)
			sdl2.sdlgfx.filledTrigonRGBA(renderer, 360, 392, 360, 412, 370, 402, 255, 255, 255, 255)
		if self.continue_game == True:
			sdl2.sdlgfx.thickLineRGBA(renderer, 350, 502, 360, 502, 3, 255, 255, 255, 255)
			sdl2.sdlgfx.filledTrigonRGBA(renderer, 360, 492, 360, 512, 370, 502, 255, 255, 255, 255)
		
	def intro(self):
		#sdl2.sdlgfx.gfxPrimitivesSetFont('', 160, 160)
		sdl2.sdlgfx.stringRGBA(renderer, 300, 300, 'Hello, and Welcome to Spite.', 0, 0, 0, 255)
		sdl2.sdlgfx.stringRGBA(renderer, 300, 400, 'The Game is Simple:', 0, 0, 0, 255)
		sdl2.sdlgfx.stringRGBA(renderer, 300, 420, 'KILL THE PEARS AND DONT DIE', 255, 0, 0, 128)
		
	def tutorial(self):
		sdl2.sdlgfx.stringRGBA(renderer, 200, 200, 'Use the Keys WASD to Move UP, LEFT, DOWN, and RIGHT', 0, 0, 0, 255)
		sdl2.sdlgfx.boxRGBA(renderer, 250, 270, 290, 310, 255, 0, 0, 128)
		sdl2.sdlgfx.characterRGBA(renderer, 267, 289, 'W', 255, 255, 255, 255)
		sdl2.sdlgfx.boxRGBA(renderer, 200, 320, 240, 360, 255, 0, 0, 128)
		sdl2.sdlgfx.characterRGBA(renderer, 217, 339, 'A', 255, 255, 255, 255)
		sdl2.sdlgfx.boxRGBA(renderer, 250, 320, 290, 360, 255, 0, 0, 128)
		sdl2.sdlgfx.characterRGBA(renderer, 267, 339, 'S', 255, 255, 255, 255)
		sdl2.sdlgfx.boxRGBA(renderer, 300, 320, 340, 360, 255, 0, 0, 128)
		sdl2.sdlgfx.characterRGBA(renderer, 317, 339, 'D', 255, 255, 255, 255)
		sdl2.sdlgfx.stringRGBA(renderer, 200, 400, 'Press the SPACE Key to Shoot', 0, 0, 0, 255)
		sdl2.sdlgfx.boxRGBA(renderer, 200, 460, 400, 500, 255, 0, 0, 128)
		sdl2.sdlgfx.stringRGBA(renderer, 280, 478, 'SPACE', 255, 255, 255, 255)
	
	def tutorial2(self):
		sdl2.sdlgfx.stringRGBA(renderer, 200, 200, 'The Enemies are Walls and Pears', 0, 0, 0, 255)
		sdl2.sdlgfx.filledCircleRGBA(renderer, 249, 329, 15, 0, 255, 0, 255)
		sdl2.sdlgfx.filledCircleRGBA(renderer, 249, 345, 20, 0, 255, 0, 255)
		sdl2.sdlgfx.lineRGBA(renderer, 250, 310, 248, 300, 255, 0, 0, 255)
		sdl2.sdlgfx.boxRGBA(renderer, 350, 250, 380, 400, 0, 0, 0, 255)
		sdl2.sdlgfx.stringRGBA(renderer, 180, 450, 'Shoot the Pears for Points and Glory!!', 0, 0, 0, 255)
		sdl2.sdlgfx.filledCircleRGBA(renderer, 449, 529, 15, 0, 255, 0, 255)
		sdl2.sdlgfx.filledCircleRGBA(renderer, 449, 545, 20, 0, 255, 0, 255)
		sdl2.sdlgfx.lineRGBA(renderer, 450, 510, 448, 500, 255, 0, 0, 255)
		sdl2.sdlgfx.thickLineRGBA(renderer, 349, 530, 369, 530, 3, 255, 0, 0, 255)
		sdl2.sdlgfx.stringRGBA(renderer, 250, 510, 'Die Pear!', 0, 0, 0, 255)
		sdl2.sdlgfx.stringRGBA(renderer, 530, 550, 'why?', 0, 0, 0, 255)
	
	def tutorial3(self):
		sdl2.sdlgfx.stringRGBA(renderer, 200, 200, 'On Your Adventure You May Encounter Strange Objects', 0, 0, 0, 255)
		sdl2.sdlgfx.filledCircleRGBA(renderer, 300, 300, 15, 0, 0, 255, 255)
		sdl2.sdlgfx.characterRGBA(renderer, 298, 298, "P", 255, 255, 255, 255)
		sdl2.sdlgfx.filledCircleRGBA(renderer, 500, 300, 15, 0, 255, 0, 255)
		sdl2.sdlgfx.characterRGBA(renderer, 498, 298, "P", 255, 255, 255, 255)
		sdl2.sdlgfx.stringRGBA(renderer, 260, 400, 'Collect them for Mysterious Rewards', 0, 0, 0, 255)
		sdl2.sdlgfx.stringRGBA(renderer, 320, 500, 'Press SPACE to Start', 255, 0, 0, 128)
	
	def pear(self):
		if self.enemy_hit == False:
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.enemy_position.x, self.enemy_position.y, 15, 0, 255, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.enemy_position2.x, self.enemy_position2.y, 20, 0, 255, 0, 255)
			sdl2.sdlgfx.lineRGBA(renderer, self.enemy_position3.x, self.enemy_position3.y, self.enemy_position4.x, self.enemy_position4.y, 255, 0, 0, 255)
	
	def f(self):
		if self.immune == False:
			sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position.x, self.f_position.y, self.f_position2.x, self.f_position2.y, 3, 255, 0, 0, 255)
			sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position3.x, self.f_position3.y, self.f_position4.x, self.f_position4.y, 3, 255, 0, 0, 255)
			sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position.x, self.f_position.y, self.f_position5.x, self.f_position5.y, 3, 255, 0, 0, 255)
		if self.immune == True:
			sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position.x, self.f_position.y, self.f_position2.x, self.f_position2.y, 3, 255, 0, 0, 10)
			sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position3.x, self.f_position3.y, self.f_position4.x, self.f_position4.y, 3, 255, 0, 0, 10)
			sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position.x, self.f_position.y, self.f_position5.x, self.f_position5.y, 3, 255, 0, 0, 10)
		#sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position2.x - 10, self.f_position5.y - 15, self.f_position2.x + 5, self.f_position5.y - 15, 3, 255, 0, 0, 255)
		if self.shooted == True:
			sdl2.sdlgfx.thickLineRGBA(renderer, self.shoot.x, self.shoot.y, self.shoot2.x, self.shoot2.y, 3, 255, 0, 0, 255)
	
	def c(self):
		if self.immune == False:
			sdl2.sdlgfx.arcRGBA(renderer, self.f_position2.x, self.f_position2.y, 30, 70, 280, 255, 255, 0, 255)
			sdl2.sdlgfx.arcRGBA(renderer, self.f_position2.x + 1, self.f_position2.y, 31, 70, 280, 255, 255, 0, 255)
		if self.immune == True:
			sdl2.sdlgfx.arcRGBA(renderer, self.f_position2.x, self.f_position2.y, 30, 70, 280, 255, 255, 0, 64)
		if self.shooted == True:
			sdl2.sdlgfx.thickLineRGBA(renderer, self.shoot.x, self.shoot.y - 20, self.shoot2.x, self.shoot2.y - 20, 3, 255, 0, 0, 255)
	
	def b(self):
		if self.immune == False:
			sdl2.sdlgfx.lineRGBA(renderer, self.f_position.x - 10, self.f_position.y, self.f_position5.x - 10, self.f_position5.y + 20, 0, 255, 0, 255)
			sdl2.sdlgfx.arcRGBA(renderer, self.f_position3.x - 5, self.f_position3.y, 20, -100, -260, 0, 255, 0, 255)
			sdl2.sdlgfx.arcRGBA(renderer, self.f_position3.x - 5, self.f_position3.y + 40, 20, -100, -260, 0, 255, 0, 255)
		if self.immune == True:
			sdl2.sdlgfx.lineRGBA(renderer, self.f_position.x - 10, self.f_position.y, self.f_position5.x - 10, self.f_position5.y + 20, 0, 255, 0, 64)
			sdl2.sdlgfx.arcRGBA(renderer, self.f_position3.x - 5, self.f_position3.y, 20, -100, -260, 0, 255, 0, 64)
			sdl2.sdlgfx.arcRGBA(renderer, self.f_position3.x - 5, self.f_position3.y + 40, 20, -100, -260, 0, 255, 0, 64)
		if self.shooted == True:
			sdl2.sdlgfx.thickLineRGBA(renderer, self.shoot.x, self.shoot.y + 20, self.shoot2.x, self.shoot2.y + 20, 3, 255, 0, 0, 255)
		
	def a(self):
		if self.immune == False:
			sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position5.x, self.f_position5.y, self.f_position.x + 20, self.f_position.y, 3, 255, 0, 0, 255)
			sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position5.x + 40, self.f_position5.y, self.f_position.x + 20, self.f_position.y, 3, 255, 0, 0, 255)
			sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position.x + 12, self.f_position.y + 25, self.f_position2.x - 2, self.f_position2.y + 25, 2, 255, 0, 0, 255)
		if self.immune == True:
			sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position5.x, self.f_position5.y, self.f_position.x + 20, self.f_position.y, 3, 255, 0, 0, 10)
			sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position5.x + 40, self.f_position5.y, self.f_position.x + 20, self.f_position.y, 3, 255, 0, 0, 10)
			sdl2.sdlgfx.thickLineRGBA(renderer, self.f_position.x + 12, self.f_position.y + 25, self.f_position2.x - 2, self.f_position2.y + 25, 2, 255, 0, 0, 10)
		if self.shooted == True:
			sdl2.sdlgfx.thickLineRGBA(renderer, self.shoot.x, self.shoot.y + 5, self.shoot2.x, self.shoot2.y + 5, 3, 255, 0, 0, 255)
	
	def ui(self):
		sdl2.sdlgfx.boxRGBA(renderer, 0, 600, 800, 700, 0, 0, 0, 255)
		if self.life >= 1:
			sdl2.sdlgfx.filledTrigonRGBA(renderer, 78, 650, 122, 650, 100, 680, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, 90, 640, 15, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, 110, 640, 15, 255, 0, 0, 255)
		if self.life >= 2:
			sdl2.sdlgfx.filledTrigonRGBA(renderer, 178, 650, 222, 650, 200, 680, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, 190, 640, 15, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, 210, 640, 15, 255, 0, 0, 255)
		if self.life == 3:
			sdl2.sdlgfx.filledTrigonRGBA(renderer, 278, 650, 322, 650, 300, 680, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, 290, 640, 15, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, 310, 640, 15, 255, 0, 0, 255)
	
	def bird(self):
		#sdl2.ext.load_image("paper_mario-shadow.bmp")
		sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird1.x, self.bird1.y, 25, 255, 0, 0, 255)
		sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird2.x, self.bird2.y, 25, 255, 0, 0, 255)
		sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird3.x, self.bird3.y, 25, 255, 0, 0, 255)
	
	def bird_attack(self):
		if self.up_right == True:
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird1_attack.x, self.bird1_attack.y, 25, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird2_attack.x, self.bird2_attack.y, 25, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird3_attack.x, self.bird3_attack.y, 25, 255, 0, 0, 255)
		if self.down_right == True:
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird1_attack.x, self.bird1_attack.y, 25, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird2_attack.x, self.bird3_attack.y, 25, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird3_attack.x, self.bird2_attack.y, 25, 255, 0, 0, 255)
		if self.up_left == True:
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird1_attack.x, self.bird1_attack.y, 25, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird2_attack.x, self.bird3_attack.y, 25, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird3_attack.x, self.bird2_attack.y, 25, 255, 0, 0, 255)
		if self.down_left == True:
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird1_attack.x, self.bird1_attack.y, 25, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird2_attack.x, self.bird2_attack.y, 25, 255, 0, 0, 255)
			sdl2.sdlgfx.filledCircleRGBA(renderer, self.bird3_attack.x, self.bird3_attack.y, 25, 255, 0, 0, 255)
	
	def total_score(self):
		#sdl2.sdlgfx.gfxPrimitivesSetFont('', 160, 160)
		sdl2.sdlgfx.stringRGBA(renderer, 550, 650, 'SCORE:', 255, 255, 255, 255)
		x = str(self.score)
		sdl2.sdlgfx.stringRGBA(renderer, 600, 650, x, 255, 255, 255, 255)
		sdl2.sdlgfx.stringRGBA(renderer, 510, 675, 'HIGH SCORE:', 255, 255, 255, 255)
		y = str(self.highScore)
		sdl2.sdlgfx.stringRGBA(renderer, 600, 675, y, 255, 255, 255, 255)

	def dp(self):
		sdl2.sdlgfx.filledCircleRGBA(renderer, self.zx, self.zy, 15, 0, 0, 255, 255)
		sdl2.sdlgfx.characterRGBA(renderer, self.zx - 2, self.zy - 2, "P", 255, 255, 255, 255)
	
	def shield(self):
		sdl2.sdlgfx.filledCircleRGBA(renderer, self.sx, self.sy, 15, 0, 255, 0, 255)
		sdl2.sdlgfx.characterRGBA(renderer, self.sx - 2, self.sy - 2, "P", 255, 255, 255, 255)
	
	def shield_draw(self):
		if self.score <= 30:
			sdl2.sdlgfx.circleRGBA(renderer, self.f_position3.x + 10, self.f_position3.y + 5, 40, 0, 0, 255, 128)
		if 60 >= self.score > 30:
			sdl2.sdlgfx.circleRGBA(renderer, self.f_position2.x, self.f_position2.y, 40, 0, 0, 255, 128)
		if 90 >= self.score > 60:
			sdl2.sdlgfx.circleRGBA(renderer, self.f_position3.x, self.f_position3.y + 20, 45, 0, 0, 255, 128)
		if 90 < self.score:
			sdl2.sdlgfx.circleRGBA(renderer, self.f_position5.x + 18, self.f_position5.y - 25, 40, 0, 0, 255, 128)
		
	def draw_pillar(self):
		sdl2.sdlgfx.boxRGBA(renderer, self.pillar.x, self.pillar.y, self.pillar2.x, self.pillar2.y, 0, 0, 0, 255)
	
	def draw_pillar2(self):
		sdl2.sdlgfx.boxRGBA(renderer, self.pillar3.x, self.pillar3.y, self.pillar4.x, self.pillar4.y, 0, 0, 0, 255)
	
	def draw(self, renderer, frame_delta_seconds):
		
		sdl2.SDL_SetRenderDrawColor(renderer, 128, 128, 128, 255);
		sdl2.SDL_RenderClear(renderer);
		
		if self.play_game == True and self.score != 30:
		
			current_frame = time.time()
			
			if self.immune == True:
				if self.immune_timer < current_frame:
					self.immune = False
					
			#basic collision detection
			if self.enemy_position.x < 0:
				self.enemy_hit = True
				self.x = randint(0, 535)
				self.enemy_position = Vector2d(799, self.x + 29)
				self.enemy_position2 = Vector2d(799, self.x + 45)
				self.enemy_position3 = Vector2d(800, self.x + 10)
				self.enemy_position4 = Vector2d(798, self.x)
			
			if self.pillar.x < 0:
				self.i = randint(100, 280)
				self.pillar = Vector2d(799, 0)
				self.pillar2 = Vector2d(840, self.i)
				self.p1 = uniform(.001, .009)
			
			if self.pillar3.x < 0:
				self.j = randint(320, 500)
				self.pillar3 = Vector2d(799, 600)
				self.pillar4 = Vector2d(840, self.j)
				self.p2 = uniform(.001, .008)

			if self.enemy_position.x > 800:
				self.enemy_velocity = -1 * self.enemy_velocity
			
			
			if self.enemy_position.x - 15 < self.shoot2.x < self.enemy_position.x + 20 and self.enemy_position4.y - 15 < self.shoot2.y < self.enemy_position2.y + 40 and self.shooted == True:
				self.enemy_hit = True
				if self.double_penetration == False:
					self.shooted = False
					self.shoot = Vector2d(self.f_position3.x, self.f_position3.y)
					self.shoot2 = Vector2d(self.f_position4.x, self.f_position4.y)
					self.shoot_timer = 0
				self.score = self.score + 1
				self.x = randint(0, 535)
				self.enemy_position = Vector2d(799, self.x + 29)
				self.enemy_position2 = Vector2d(799, self.x + 45)
				self.enemy_position3 = Vector2d(800, self.x + 10)
				self.enemy_position4 = Vector2d(798, self.x)
			
			if self.pillar.x < self.shoot2.x < self.pillar2.x and self.pillar.y < self.shoot2.y < self.pillar2.y and self.shooted == True:
				if self.double_penetration == False:
					self.shooted = False
					self.shoot = Vector2d(self.f_position3.x, self.f_position3.y)
					self.shoot2 = Vector2d(self.f_position4.x, self.f_position4.y)
					self.shoot_timer = 0
			
			if self.pillar3.x < self.shoot2.x < self.pillar4.x and self.pillar3.y > self.shoot2.y > self.pillar4.y and self.shooted == True:
				if self.double_penetration == False:
					self.shooted = False
					self.shoot = Vector2d(self.f_position3.x, self.f_position3.y)
					self.shoot2 = Vector2d(self.f_position4.x, self.f_position4.y)
					self.shoot_timer = 0
			
			if self.score < 30 and self.immune == False:
				#double penetration
				if (self.zx - 25 < self.f_position.x < self.zx + 25 and self.zy - 25 < self.f_position5.y < self.zy + 25) or (self.zx - 25 < self.f_position2.x < self.zx + 25 and self.zy - 25 < self.f_position.y < self.zy + 25):
					self.double_penetration = True
					self.zx = -10
					
				#shield
				if (self.sx - 25 < self.f_position.x < self.sx + 25 and self.sy - 25 < self.f_position5.y < self.sy + 25) or (self.sx - 25 < self.f_position2.x < self.sx + 25 and self.sy - 25 < self.f_position.y < self.sy + 25):
					self.shield_up = True
					self.sx = -10
					
				if (self.pillar.x < self.f_position2.x < self.pillar2.x or self.pillar.x < self.f_position.x < self.pillar2.x) and self.pillar.y < self.f_position.y < self.pillar2.y:
					if self.shield_up == False:
						self.life = self.life - 1
					self.shield_up = False
					self.double_penetration = False
					self.immune = True
					self.immune_timer = current_frame + 1
			
				if (self.pillar3.x < self.f_position2.x < self.pillar4.x or self.pillar3.x < self.f_position.x < self.pillar4.x) and self.pillar3.y > self.f_position5.y > self.pillar4.y:
					if self.shield_up == False:
						self.life = self.life - 1
					self.shield_up = False
					self.double_penetration = False
					self.immune = True
					self.immune_timer = current_frame + 1
			
				if (self.enemy_position.x - 15 < self.f_position.x < self.enemy_position.x + 20 and self.enemy_position4.y - 15 < self.f_position5.y < self.enemy_position2.y + 20) or (self.enemy_position.x - 15 < self.f_position2.x < self.enemy_position.x + 20 and self.enemy_position4.y - 15 < self.f_position.y < self.enemy_position2.y + 20):
					if self.shield_up == False:
						self.life = self.life - 1
					self.shield_up = False
					self.double_penetration = False
					self.immune = True
					self.immune_timer = current_frame + 1
			
			if 30 <= self.score <= 60 and self.immune == False:
				#double penetration
				if (self.zx - 25 < self.f_position2.x + 5 < self.zx + 25 and self.zy - 25 < self.f_position2.y + 30 < self.zy + 25) or (self.zx - 25 < self.f_position2.x + 5 < self.zx + 25 and self.zy - 25 < self.f_position2.y - 30 < self.zy + 25) or (self.zx - 25 < self.f_position2.x - 30 < self.zx + 25 and self.zy - 25 < self.f_position2.y < self.zy + 25):
					self.double_penetration = True
					self.zx = -10
					
				#shield
				if (self.sx - 25 < self.f_position2.x + 5 < self.sx + 25 and self.sy - 25 < self.f_position2.y + 30 < self.sy + 25) or (self.sx - 25 < self.f_position2.x + 5 < self.sx + 25 and self.sy - 25 < self.f_position2.y - 30 < self.sy + 25) or (self.sx - 25 < self.f_position2.x - 30 < self.sx + 25 and self.sy - 25 < self.f_position2.y < self.sy + 25):
					self.shield_up = True
					self.sx = -10
					
				if (self.pillar.x < self.f_position2.x + 5 < self.pillar2.x or self.pillar.x < self.f_position2.x - 30 < self.pillar2.x) and self.pillar.y < self.f_position2.y - 30 < self.pillar2.y:
					if self.shield_up == False:
						self.life = self.life - 1
					self.shield_up = False
					self.double_penetration = False
					self.immune = True
					self.immune_timer = current_frame + 1
					
				if (self.pillar3.x < self.f_position2.x + 5 < self.pillar4.x or self.pillar3.x < self.f_position2.x - 30 < self.pillar4.x) and self.pillar3.y > self.f_position2.y + 30 > self.pillar4.y:
					if self.shield_up == False:
						self.life = self.life - 1
					self.shield_up = False
					self.double_penetration = False
					self.immune = True
					self.immune_timer = current_frame + 1
					
				if (self.enemy_position.x - 15 < self.f_position2.x + 5 < self.enemy_position.x + 20 and self.enemy_position4.y - 15 < self.f_position2.y + 30 < self.enemy_position2.y + 20) or (self.enemy_position.x - 15 < self.f_position2.x + 5 < self.enemy_position.x + 20 and self.enemy_position4.y - 15 < self.f_position2.y - 30 < self.enemy_position2.y + 20) or (self.enemy_position.x - 15 < self.f_position2.x - 30 < self.enemy_position.x + 20 and self.enemy_position4.y - 15 < self.f_position2.y < self.enemy_position2.y + 20):
					if self.shield_up == False:
						self.life = self.life - 1
					self.shield_up = False
					self.double_penetration = False
					self.immune = True
					self.immune_timer = current_frame + 1
			
			if 60 < self.score <= 90 and self.immune == False:
				#double penetration
				if (self.zx - 25 < self.f_position.x - 10 < self.zx + 25 and self.zy - 25 < self.f_position.y < self.zy + 25) or (self.zx - 25 < self.f_position3.x + 10 < self.zx + 25 and self.zy - 25 < self.f_position.y < self.zy + 25) or (self.zx - 25 < self.f_position3.x < self.zx + 25 and self.zy - 25 < self.f_position3.y + 40 < self.zy + 25):
					self.double_penetration = True
					self.zx = -10
					
				#shield
				if (self.sx - 25 < self.f_position2.x - 10 < self.sx + 25 and self.sy - 25 < self.f_position.y < self.sy + 25) or (self.sx - 25 < self.f_position3.x + 10 < self.sx + 25 and self.sy - 25 < self.f_position.y < self.sy + 25) or (self.sx - 25 < self.f_position3.x < self.sx + 25 and self.sy - 25 < self.f_position3.y + 40 < self.sy + 25):
					self.shield_up = True
					self.sx = -10
					
				if (self.pillar.x < self.f_position.x - 10 < self.pillar2.x or self.pillar.x < self.f_position3.x + 15 < self.pillar2.x) and self.pillar.y < self.f_position.y < self.pillar2.y:
					if self.shield_up == False:
						self.life = self.life - 1
					self.shield_up = False
					self.double_penetration = False
					self.immune = True
					self.immune_timer = current_frame + 1
					
				if (self.pillar3.x < self.f_position.x - 10 < self.pillar4.x or self.pillar3.x < self.f_position3.x + 15 < self.pillar4.x) and self.pillar3.y > self.f_position5.y + 15 > self.pillar4.y:
					if self.shield_up == False:
						self.life = self.life - 1
					self.shield_up = False
					self.double_penetration = False
					self.immune = True
					self.immune_timer = current_frame + 1
					
				if (self.enemy_position.x - 15 < self.f_position.x - 10 < self.enemy_position.x + 20 and self.enemy_position4.y - 15 < self.f_position.y < self.enemy_position2.y + 20) or (self.enemy_position.x - 15 < self.f_position3.x + 10 < self.enemy_position.x + 20 and self.enemy_position4.y - 15 < self.f_position.y < self.enemy_position2.y + 20) or (self.enemy_position.x - 15 < self.f_position3.x < self.enemy_position.x + 20 and self.enemy_position4.y - 15 < self.f_position3.y + 40 < self.enemy_position2.y + 20):
					if self.shield_up == False:
						self.life = self.life - 1
					self.shield_up = False
					self.double_penetration = False
					self.immune = True
					self.immune_timer = current_frame + 1

			if 90 < self.score and self.immune == False:
				#double penetration
				if (self.zx - 25 < self.f_position5.x < self.zx + 25 and self.zy - 25 < self.f_position5.y < self.zy + 25) or (self.zx - 25 < self.f_position.x + 20 < self.zx + 25 and self.zy - 25 < self.f_position.y < self.zy + 25) or (self.zx - 25 < self.f_position5.x + 40 < self.zx + 25 and self.zy - 25 < self.f_position5.y < self.zy + 25) or (self.zx - 25 < self.f_position.x + 30 < self.zx + 25 and self.zy - 25 < self.f_position.y + 20 < self.zy + 25):
					self.double_penetration = True
					self.zx = -10
					
				#shield
				if (self.sx - 25 < self.f_position5.x < self.sx + 25 and self.sy - 25 < self.f_position5.y < self.sy + 25) or (self.sx - 25 < self.f_position.x + 20 < self.sx + 25 and self.sy - 25 < self.f_position.y < self.sy + 25) or (self.sx - 25 < self.f_position5.x + 40 < self.sx + 25 and self.sy - 25 < self.f_position5.y < self.sy + 25) or (self.sx - 25 < self.f_position.x + 30 < self.sx + 25 and self.sy - 25 < self.f_position.y + 20 < self.sy + 25):
					self.shield_up = True
					self.sx = -10
					
				if (self.pillar.x < self.f_position5.x < self.pillar2.x and self.pillar.y < self.f_position5.y < self.pillar2.y) or (self.pillar.x < self.f_position.x + 20 < self.pillar2.x and self.pillar.y < self.f_position.y < self.pillar2.y) or (self.pillar.x < self.f_position5.x + 40 < self.pillar2.x and self.pillar.y < self.f_position5.y < self.pillar2.y) or (self.pillar.x < self.f_position.x + 30 < self.pillar2.x and self.pillar.y < self.f_position.y + 20 < self.pillar2.y):
					if self.shield_up == False:
						self.life = self.life - 1
					self.shield_up = False
					self.double_penetration = False
					self.immune = True
					self.immune_timer = current_frame + 1
					
				if (self.pillar3.x < self.f_position5.x + 40 < self.pillar4.x or self.pillar3.x < self.f_position5.x < self.pillar4.x) and self.pillar3.y > self.f_position5.y > self.pillar4.y:
					if self.shield_up == False:
						self.life = self.life - 1
					self.shield_up = False
					self.double_penetration = False
					self.immune = True
					self.immune_timer = current_frame + 1
					
				if (self.enemy_position.x - 15 < self.f_position5.x < self.enemy_position.x + 20 and self.enemy_position4.y < self.f_position5.y < self.enemy_position2.y + 20) or (self.enemy_position.x - 15 < self.f_position.x + 20 < self.enemy_position.x + 20 and self.enemy_position4.y < self.f_position.y < self.enemy_position2.y + 20) or (self.enemy_position.x - 15 < self.f_position5.x + 40 < self.enemy_position.x + 20 and self.enemy_position4.y < self.f_position5.y < self.enemy_position2.y + 20) or (self.enemy_position.x - 15 < self.f_position.x + 30 < self.enemy_position.x + 20 and self.enemy_position4.y < self.f_position.y + 20 < self.enemy_position2.y + 20):
					if self.shield_up == False:
						self.life = self.life - 1
					self.shield_up = False
					self.double_penetration = False
					self.immune = True
					self.immune_timer = current_frame + 1
			
			#delays movement to appropriate speed
			if current_frame > self.enemy_timer:
				self.enemy_timer = current_frame + .003
				self.enemy_position.x = self.enemy_position.x - self.enemy_velocity
				self.enemy_position2.x = self.enemy_position2.x - self.enemy_velocity
				self.enemy_position3.x = self.enemy_position3.x - self.enemy_velocity
				self.enemy_position4.x = self.enemy_position4.x - self.enemy_velocity
			if current_frame > self.pillar_timer:
				self.pillar_timer = current_frame + self.p1
				self.pillar.x = self.pillar.x - self.enemy_velocity
				self.pillar2.x = self.pillar2.x - self.enemy_velocity
			if current_frame > self.pillar2_timer:
				self.pillar2_timer = current_frame + self.p2
				self.pillar3.x = self.pillar3.x - self.enemy_velocity
				self.pillar4.x = self.pillar4.x - self.enemy_velocity
			
			#delays bullet to appropriate speed
			if current_frame > self.shoot_timer:
				self.shoot_timer = current_frame
				if self.shooted == True:
					self.shoot.x = self.shoot.x + self.shoot_velocity
					self.shoot2.x = self.shoot2.x + self.shoot_velocity
			
			#Deletes / resets bullet
			if self.shoot.x > 800:
				self.shooted = False
				self.shoot = Vector2d(self.f_position3.x, self.f_position3.y)
				self.shoot2 = Vector2d(self.f_position4.x, self.f_position4.y)
				self.shoot_timer = 0
			
			self.pear()
			self.draw_pillar()
			self.draw_pillar2()
			
			if self.score < 30:
				self.f()
			if 30 < self.score <= 60:
				self.c()
			if 60 < self.score <= 90:
				self.b()
			if 90 < self.score:
				self.a()
			
			if self.life == 0:
				if self.score > int(self.highScore):
					file = open("output.txt", "w")
					file.write(str(self.score))
					file.close()
					
				self.ball_position = Vector2d(self.CANVAS_SIZE_X/2, self.CANVAS_SIZE_Y/2)
				self.ball_direction = rotate_vector( Vector2d( 0, 0 ), 0)
				self.ball_colour_idx = 0
				#f character
				self.f_velocity = 1
				self.f_position = Vector2d(400, 300)
				self.f_position2 = Vector2d(430, 300)
				self.f_position3 = Vector2d(400, 320)
				self.f_position4 = Vector2d(430, 320)
				self.f_position5 = Vector2d(400, 360)
				self.score = 0
				#enemy / pear
				self.x = randint(0, 535)
				self.enemy_position = Vector2d(799, self.x + 29)
				self.enemy_position2 = Vector2d(799, self.x + 45)
				self.enemy_position3 = Vector2d(800, self.x + 10)
				self.enemy_position4 = Vector2d(798, self.x)	
				self.enemy_velocity = 1
				self.enemy_hit = False
				#timers
				self.keys_down = set()
				self.enemy_timer = 0
				self.a_timer = 0
				self.d_timer = 0
				self.w_timer = 0
				self.s_timer = 0
				self.SPACE_timer = 0
				self.shoot_timer = 0
				self.respawn_timer = 0
				self.pillar_timer = 10
				self.pillar2_timer = 5
				self.immune_timer = 0
				#shoot
				self.shoot = Vector2d(self.f_position3.x, self.f_position3.y)
				self.shoot2 = Vector2d(self.f_position4.x, self.f_position4.y)
				self.shoot_velocity = 1
				self.shooted = False
				#pillar1
				self.p1 = uniform(.001, .009)
				self.i = randint(100, 280)
				self.pillar = Vector2d(799, 0)
				self.pillar2 = Vector2d(840, self.i)
				#pillar2
				self.p2 = uniform(.001, .009)
				self.j = randint(320, 500)
				self.pillar3 = Vector2d(799, 600)
				self.pillar4 = Vector2d(840, self.j)
				#UI
				self.life = 3
				self.immune = False
				f = open('output.txt', 'r')
				self.highScore = f.read()
				f.close()
				#power up dp
				self.double_penetration = False
				self.zy = randint(15, 585)
				self.zx = 800
				z = randint(30, 50)
				self.z_timer = time.time() + z
				#power up shield
				self.shield_up = False
				self.sy = randint(15, 585)
				self.sx = 800
				s = randint(10, 30)
				self.shield_timer = time.time() + s
				#title screen / tutorial
				self.new_game = False
				self.continue_game = False
				self.play_game = False
				self.play_game_new = False
				self.play_tutorial = False
				self.play_tutorial2 = False
				self.play_tutorial3 = False
				self.new_delay = time.time()
				self.new_delay2 = time.time()
				self.new_delay3 = time.time()
				
			
			#double penetration
			if self.zx < 800:
				self.dp()
			if current_frame > self.z_timer:
				self.z_timer = current_frame + 0.005
				self.zx = self.zx - self.enemy_velocity
			if self.zx < 0 and self.double_penetration == False:
				self.zx = 800
				self.zy = randint(15, 585)
				z = randint(30, 50)
				self.z_timer = current_frame + z
			
			#shield
			if self.sx < 800:
				self.shield()
			if current_frame > self.shield_timer:
				self.shield_timer = current_frame + 0.002
				self.sx = self.sx - self.enemy_velocity
			if self.sx < 0 and self.shield_up == False:
				self.sx = 800
				self.sy = randint(15, 585)
				s = randint(10, 30)
				self.shield_timer = current_frame + s
			if self.shield_up == True:
				self.shield_draw()
				
			self.ui()
			self.total_score()		
			
			if current_frame > self.respawn_timer:
				self.enemy_hit = False
				self.respawn_timer = self.respawn_timer + 3
		
		if self.play_game == True and self.score == 30:
			if self.immune == True:
				if self.immune_timer < time.time():
					self.immune = False
			self.bird()
			self.ui()
			self.total_score()
			if self.score == 30:
				self.f()
			if self.score == 60:
				self.c()
			if self.score == 90:
				self.b()
			#delays bullet to appropriate speed
			if time.time() > self.shoot_timer:
				self.shoot_timer = time.time()
				if self.shooted == True:
					self.shoot.x = self.shoot.x + self.shoot_velocity
					self.shoot2.x = self.shoot2.x + self.shoot_velocity
			if self.bird_timer < time.time():
				self.bird_timer = time.time() + 0.008
				if self.bird_left == True and self.bird1.x - 50 > 0 and self.bird1.x > self.f_position.x:
					self.bird1.x = self.bird1.x - self.enemy_velocity
					self.bird2.x = self.bird2.x - self.enemy_velocity
					self.bird3.x = self.bird3.x - self.enemy_velocity
				elif self.bird_left == True and self.bird1.x + 50 < 800 and self.bird1.x < self.f_position.x:
					self.bird1.x = self.bird1.x + self.enemy_velocity
					self.bird2.x = self.bird2.x + self.enemy_velocity
					self.bird3.x = self.bird3.x + self.enemy_velocity
				if self.bird_right == True and self.bird1.x + 50 < 800 and self.bird1.x < self.f_position.x:
					self.bird1.x = self.bird1.x + self.enemy_velocity
					self.bird2.x = self.bird2.x + self.enemy_velocity
					self.bird3.x = self.bird3.x + self.enemy_velocity
				elif self.bird_right == True and self.bird1.x - 50 > 0 and self.bird1.x > self.f_position.x:
					self.bird1.x = self.bird1.x - self.enemy_velocity
					self.bird2.x = self.bird2.x - self.enemy_velocity
					self.bird3.x = self.bird3.x - self.enemy_velocity
				if self.bird_up == True and self.bird1.y - 80 > 0 and self.bird1.y > self.f_position.y:
					self.bird1.y = self.bird1.y - self.enemy_velocity
					self.bird2.y = self.bird2.y - self.enemy_velocity
					self.bird3.y = self.bird3.y - self.enemy_velocity
				elif self.bird_up == True and self.bird1.y + 80 < 600 and self.bird1.y < self.f_position.y:
					self.bird1.y = self.bird1.y + self.enemy_velocity
					self.bird2.y = self.bird2.y + self.enemy_velocity
					self.bird3.y = self.bird3.y + self.enemy_velocity
				if self.bird_down == True and self.bird1.y + 80 < 600 and self.bird1.y < self.f_position.y:
					self.bird1.y = self.bird1.y + self.enemy_velocity
					self.bird2.y = self.bird2.y + self.enemy_velocity
					self.bird3.y = self.bird3.y + self.enemy_velocity
				elif self.bird_down == True and self.bird1.y - 80 > 0 and self.bird1.y > self.f_position.y:
					self.bird1.y = self.bird1.y - self.enemy_velocity
					self.bird2.y = self.bird2.y - self.enemy_velocity
					self.bird3.y = self.bird3.y - self.enemy_velocity
			if self.attack_timer < time.time():
				self.attack = True
				self.attack_timer = time.time() + 1
				if 400 <= self.f_position.x <= 800 and 0 <= self.f_position.y < 300:
					self.up_right = True
				elif 400 <= self.f_position.x <= 800 and 600 >= self.f_position.y > 300:
					self.down_right = True
				elif 0 <= self.f_position.x < 400 and 0 <= self.f_position.y < 300:
					self.up_left = True
				elif 0 <= self.f_position.x < 400 and 600 >= self.f_position.y > 300:
					self.down_left = True
			if self.attack == True and self.attack_speed < time.time():
				self.attack_speed = time.time() + 0.003
				if self.up_right == True:
					self.bird1_attack.x = self.bird1_attack.x + self.enemy_velocity
					self.bird2_attack.x = self.bird2_attack.x + self.enemy_velocity
					self.bird3_attack.x = self.bird3_attack.x + self.enemy_velocity
					self.bird1_attack.y = self.bird1_attack.y - self.enemy_velocity
					self.bird2_attack.y = self.bird2_attack.y - self.enemy_velocity
					self.bird3_attack.y = self.bird3_attack.y - self.enemy_velocity
				if self.down_right == True:
					self.bird1_attack.x = self.bird1_attack.x + self.enemy_velocity
					self.bird2_attack.x = self.bird2_attack.x + self.enemy_velocity
					self.bird3_attack.x = self.bird3_attack.x + self.enemy_velocity
					self.bird1_attack.y = self.bird1_attack.y + self.enemy_velocity
					self.bird2_attack.y = self.bird2_attack.y + self.enemy_velocity
					self.bird3_attack.y = self.bird3_attack.y + self.enemy_velocity
				if self.up_left == True:
					self.bird1_attack.x = self.bird1_attack.x - self.enemy_velocity
					self.bird2_attack.x = self.bird2_attack.x - self.enemy_velocity
					self.bird3_attack.x = self.bird3_attack.x - self.enemy_velocity
					self.bird1_attack.y = self.bird1_attack.y - self.enemy_velocity
					self.bird2_attack.y = self.bird2_attack.y - self.enemy_velocity
					self.bird3_attack.y = self.bird3_attack.y - self.enemy_velocity
				if self.down_left == True:
					self.bird1_attack.x = self.bird1_attack.x - self.enemy_velocity
					self.bird2_attack.x = self.bird2_attack.x - self.enemy_velocity
					self.bird3_attack.x = self.bird3_attack.x - self.enemy_velocity
					self.bird1_attack.y = self.bird1_attack.y + self.enemy_velocity
					self.bird2_attack.y = self.bird2_attack.y + self.enemy_velocity
					self.bird3_attack.y = self.bird3_attack.y + self.enemy_velocity
					
			if self.attack == False:
				self.bird1_attack = Vector2d(self.bird1.x, self.bird1.y)
				self.bird2_attack = Vector2d(self.bird2.x, self.bird2.y)
				self.bird3_attack = Vector2d(self.bird3.x, self.bird3.y)
				self.up_right = False
				self.down_right = False
				self.up_left = False
				self.down_left = False
			
			if self.attack == True:
				self.bird_attack()
				if self.bird1_attack.x < 0:
					self.attack = False
				if self.bird1_attack.x > 800:
					self.attack = False
				if self.bird1_attack.y < 0:
					self.attack = False
				if self.bird1_attack.y > 600:
					self.attack = False
				
			if self.immune == False:
				if (self.bird1.x - 25 < self.f_position.x < self.bird1.x + 25 and self.bird1.y - 25 < self.f_position5.y < self.bird1.y + 25) or (self.bird2.x - 25 < self.f_position.x < self.bird2.x + 25 and self.bird2.y - 25 < self.f_position5.y < self.bird2.y + 25) or (self.bird3.x - 25 < self.f_position.x < self.bird3.x + 25 and self.bird3.y - 25 < self.f_position5.y < self.bird3.y + 25) or (self.bird1.x - 25 < self.f_position2.x < self.bird1.x + 25 and self.bird1.y - 25 < self.f_position.y < self.bird1.y + 25) or (self.bird2.x - 25 < self.f_position2.x < self.bird2.x + 25 and self.bird2.y - 25 < self.f_position.y < self.bird2.y + 25) or (self.bird3.x - 25 < self.f_position2.x < self.bird3.x + 25 and self.bird3.y - 25 < self.f_position.y < self.bird3.y + 25):
						if self.shield_up == False:
							self.life = self.life - 1
						self.shield_up = False
						self.double_penetration = False
						self.immune = True
						self.immune_timer = time.time() + 1
				if self.attack == True and (self.up_right == True or self.down_left == True):
					if (self.bird1_attack.x - 25 < self.f_position.x < self.bird1_attack.x + 25 and self.bird1_attack.y - 25 < self.f_position5.y < self.bird1_attack.y + 25) or (self.bird2_attack.x - 25 < self.f_position.x < self.bird2_attack.x + 25 and self.bird2_attack.y - 25 < self.f_position5.y < self.bird2_attack.y + 25) or (self.bird3_attack.x - 25 < self.f_position.x < self.bird3_attack.x + 25 and self.bird3_attack.y - 25 < self.f_position5.y < self.bird3_attack.y + 25) or (self.bird1_attack.x - 25 < self.f_position2.x < self.bird1_attack.x + 25 and self.bird1_attack.y - 25 < self.f_position.y < self.bird1_attack.y + 25) or (self.bird2_attack.x - 25 < self.f_position2.x < self.bird2.x + 25 and self.bird2_attack.y - 25 < self.f_position.y < self.bird2_attack.y + 25) or (self.bird3_attack.x - 25 < self.f_position2.x < self.bird3_attack.x + 25 and self.bird3_attack.y - 25 < self.f_position.y < self.bird3_attack.y + 25):
						if self.shield_up == False:
							self.life = self.life - 1
						self.shield_up = False
						self.double_penetration = False
						self.immune = True
						self.immune_timer = time.time() + 1
				if self.attack == True and (self.up_left == True or self.down_right == True):
					if (self.bird1_attack.x - 25 < self.f_position.x < self.bird1_attack.x + 25 and self.bird1_attack.y - 25 < self.f_position5.y < self.bird1_attack.y + 25) or (self.bird2_attack.x - 25 < self.f_position.x < self.bird2_attack.x + 25 and self.bird3_attack.y - 25 < self.f_position5.y < self.bird3_attack.y + 25) or (self.bird3_attack.x - 25 < self.f_position.x < self.bird3_attack.x + 25 and self.bird2_attack.y - 25 < self.f_position5.y < self.bird2_attack.y + 25) or (self.bird1_attack.x - 25 < self.f_position2.x < self.bird1_attack.x + 25 and self.bird1_attack.y - 25 < self.f_position.y < self.bird1_attack.y + 25) or (self.bird2_attack.x - 25 < self.f_position2.x < self.bird2.x + 25 and self.bird3_attack.y - 25 < self.f_position.y < self.bird3_attack.y + 25) or (self.bird3_attack.x - 25 < self.f_position2.x < self.bird3_attack.x + 25 and self.bird2_attack.y - 25 < self.f_position.y < self.bird2_attack.y + 25):
						if self.shield_up == False:
							self.life = self.life - 1
						self.shield_up = False
						self.double_penetration = False
						self.immune = True
						self.immune_timer = time.time() + 1
			
			if (self.bird3.x - 25 < self.shoot2.x < self.bird3.x + 25 and self.bird3.y - 25 < self.shoot2.y < self.bird3.y + 25) or (self.bird2.x - 25 < self.shoot2.x < self.bird2.x + 25 and self.bird2.y - 25 < self.shoot2.y < self.bird2.y + 25) or (self.bird1.x - 25 < self.shoot2.x < self.bird1.x + 25 and self.bird1.y - 25 < self.shoot2.y < self.bird1.y + 25)and self.shooted == True:
				self.enemy_life = self.enemy_life - 1
				self.shooted = False
				self.shoot = Vector2d(self.f_position3.x, self.f_position3.y)
				self.shoot2 = Vector2d(self.f_position4.x, self.f_position4.y)
				self.shoot_timer = 0
			
			if self.enemy_life == 0:
				self.score = self.score + 1
			
			if self.life == 0:
				if self.score > int(self.highScore):
					file = open("output.txt", "w")
					file.write(str(self.score))
					file.close()
					
				self.ball_position = Vector2d(self.CANVAS_SIZE_X/2, self.CANVAS_SIZE_Y/2)
				self.ball_direction = rotate_vector( Vector2d( 0, 0 ), 0)
				self.ball_colour_idx = 0
				#f character
				self.f_velocity = 1
				self.f_position = Vector2d(400, 300)
				self.f_position2 = Vector2d(430, 300)
				self.f_position3 = Vector2d(400, 320)
				self.f_position4 = Vector2d(430, 320)
				self.f_position5 = Vector2d(400, 360)
				self.score = 0
				#enemy / pear
				self.x = randint(0, 535)
				self.enemy_position = Vector2d(799, self.x + 29)
				self.enemy_position2 = Vector2d(799, self.x + 45)
				self.enemy_position3 = Vector2d(800, self.x + 10)
				self.enemy_position4 = Vector2d(798, self.x)	
				self.enemy_velocity = 1
				self.enemy_hit = False
				#timers
				self.keys_down = set()
				self.enemy_timer = 0
				self.a_timer = 0
				self.d_timer = 0
				self.w_timer = 0
				self.s_timer = 0
				self.SPACE_timer = 0
				self.shoot_timer = 0
				self.respawn_timer = 0
				self.pillar_timer = 10
				self.pillar2_timer = 5
				self.immune_timer = 0
				#shoot
				self.shoot = Vector2d(self.f_position3.x, self.f_position3.y)
				self.shoot2 = Vector2d(self.f_position4.x, self.f_position4.y)
				self.shoot_velocity = 1
				self.shooted = False
				#pillar1
				self.p1 = uniform(.001, .009)
				self.i = randint(100, 280)
				self.pillar = Vector2d(799, 0)
				self.pillar2 = Vector2d(840, self.i)
				#pillar2
				self.p2 = uniform(.001, .009)
				self.j = randint(320, 500)
				self.pillar3 = Vector2d(799, 600)
				self.pillar4 = Vector2d(840, self.j)
				#UI
				self.life = 3
				self.immune = False
				f = open('output.txt', 'r')
				self.highScore = f.read()
				f.close()
				#power up dp
				self.double_penetration = False
				self.zy = randint(15, 585)
				self.zx = 800
				z = randint(30, 50)
				self.z_timer = time.time() + z
				#power up shield
				self.shield_up = False
				self.sy = randint(15, 585)
				self.sx = 800
				s = randint(10, 30)
				self.shield_timer = time.time() + s
				#title screen / tutorial
				self.new_game = False
				self.continue_game = False
				self.play_game = False
				self.play_game_new = False
				self.play_tutorial = False
				self.play_tutorial2 = False
				self.play_tutorial3 = False
				self.new_delay = time.time()
				self.new_delay2 = time.time()
				self.new_delay3 = time.time()
					
		if self.play_game == False:
			if self.play_game_new == False:
				self.title_screen()
		
			if self.play_game_new == True and self.play_tutorial == False:
				self.intro()
			
			if self.play_tutorial == True and self.play_tutorial2 == False:
				self.tutorial()
			
			if self.play_tutorial2 == True and self.play_tutorial3 == False:
				self.tutorial2()
				
			if self.play_tutorial3 == True:
				self.tutorial3()
			
		sdl2.SDL_RenderPresent(renderer)
		
	def frame_loop(self,renderer):
		last_frame = time.time()
		print 'frame loop'
		while True:
			current_frame = time.time()
			frame_time = current_frame-last_frame
			all_events = sdl2.ext.get_events()
			for event in all_events:
				if event.type == sdl2.SDL_QUIT:
					return
				elif event.type == sdl2.SDL_KEYDOWN:
					#print 'KeyDown: key code ', SDL_GetKeyName(event.key.keysym.sym)
					key_code = event.key.keysym.sym
					self.keys_down.add(key_code)
				elif event.type == sdl2.SDL_KEYUP:
					key_code = event.key.keysym.sym
					self.keys_down.remove(key_code)
				elif event.type == sdl2.SDL_MOUSEMOTION:
					#print 'MouseMotion: ',event.motion.x, event.motion.y
					pass
				elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
					#print 'MouseDown: ', event.button.button, event.button.x, event.button.y	
					pass
				elif event.type == sdl2.SDL_MOUSEBUTTONUP:
					#print 'MouseUp: ', event.button.button, event.button.x, event.button.y
					pass
			if self.play_game == True:
				#move left
				if sdl2.SDLK_a in self.keys_down:
					self.bird_left = True
					self.bird_right = False
					if current_frame > self.a_timer and self.f_position.x > 0:
						self.a_timer = current_frame + .002
						self.f_position.x = self.f_position.x - self.f_velocity
						self.f_position2.x = self.f_position2.x - self.f_velocity
						self.f_position3.x = self.f_position3.x - self.f_velocity
						self.f_position4.x = self.f_position4.x - self.f_velocity
						self.f_position5.x = self.f_position5.x - self.f_velocity
				#move right
				if sdl2.SDLK_d in self.keys_down:
					self.bird_right = True
					self.bird_left = False
					if current_frame > self.d_timer and self.f_position2.x < 800 and self.score <= 60:
						self.d_timer = current_frame + .002
						self.f_position.x = self.f_position.x + self.f_velocity
						self.f_position2.x = self.f_position2.x + self.f_velocity
						self.f_position3.x = self.f_position3.x + self.f_velocity
						self.f_position4.x = self.f_position4.x + self.f_velocity
						self.f_position5.x = self.f_position5.x + self.f_velocity
					elif current_frame > self.d_timer and self.f_position3.x + 15 < 800 and 90 >= self.score > 60:
						self.d_timer = current_frame + .002
						self.f_position.x = self.f_position.x + self.f_velocity
						self.f_position2.x = self.f_position2.x + self.f_velocity
						self.f_position3.x = self.f_position3.x + self.f_velocity
						self.f_position4.x = self.f_position4.x + self.f_velocity
						self.f_position5.x = self.f_position5.x + self.f_velocity
					elif current_frame > self.d_timer and self.f_position2.x + 10 < 800 and self.score > 90:
						self.d_timer = current_frame + .002
						self.f_position.x = self.f_position.x + self.f_velocity
						self.f_position2.x = self.f_position2.x + self.f_velocity
						self.f_position3.x = self.f_position3.x + self.f_velocity
						self.f_position4.x = self.f_position4.x + self.f_velocity
						self.f_position5.x = self.f_position5.x + self.f_velocity
				#move up
				if sdl2.SDLK_w in self.keys_down:
					self.bird_up = True
					self.bird_down = False
					if current_frame > self.w_timer and self.f_position.y > 0 and (self.score <= 30 or self.score > 60):
						self.w_timer = current_frame + .002
						self.f_position.y = self.f_position.y - self.f_velocity
						self.f_position2.y = self.f_position2.y - self.f_velocity
						self.f_position3.y = self.f_position3.y - self.f_velocity
						self.f_position4.y = self.f_position4.y - self.f_velocity
						self.f_position5.y = self.f_position5.y - self.f_velocity
					elif current_frame > self.w_timer and self.f_position2.y - 30 > 0 and 30 < self.score <= 60:
						self.w_timer = current_frame + .002
						self.f_position.y = self.f_position.y - self.f_velocity
						self.f_position2.y = self.f_position2.y - self.f_velocity
						self.f_position3.y = self.f_position3.y - self.f_velocity
						self.f_position4.y = self.f_position4.y - self.f_velocity
						self.f_position5.y = self.f_position5.y - self.f_velocity
				#move down
				if sdl2.SDLK_s in self.keys_down:
					self.bird_down = True
					self.bird_up = False
					if current_frame > self.s_timer and self.f_position5.y < 600 and (self.score <= 30 or self.score > 90):
						self.s_timer = current_frame + .002
						self.f_position.y = self.f_position.y + self.f_velocity
						self.f_position2.y = self.f_position2.y + self.f_velocity
						self.f_position3.y = self.f_position3.y + self.f_velocity
						self.f_position4.y = self.f_position4.y + self.f_velocity
						self.f_position5.y = self.f_position5.y + self.f_velocity
					elif current_frame > self.s_timer and self.f_position2.y + 30 < 600 and 30 < self.score <= 60:
						self.s_timer = current_frame + .002
						self.f_position.y = self.f_position.y + self.f_velocity
						self.f_position2.y = self.f_position2.y + self.f_velocity
						self.f_position3.y = self.f_position3.y + self.f_velocity
						self.f_position4.y = self.f_position4.y + self.f_velocity
						self.f_position5.y = self.f_position5.y + self.f_velocity
					elif current_frame > self.s_timer and self.f_position5.y + 20 < 600 and 60 < self.score <= 90:
						self.s_timer = current_frame + .002
						self.f_position.y = self.f_position.y + self.f_velocity
						self.f_position2.y = self.f_position2.y + self.f_velocity
						self.f_position3.y = self.f_position3.y + self.f_velocity
						self.f_position4.y = self.f_position4.y + self.f_velocity
						self.f_position5.y = self.f_position5.y + self.f_velocity
				#shoot
				if sdl2.SDLK_SPACE in self.keys_down:
					if current_frame > self.SPACE_timer:
						self.SPACE_timer = current_frame + 0.5
						self.shooted = True
						self.shoot = Vector2d(self.f_position3.x, self.f_position3.y)
						self.shoot2 = Vector2d(self.f_position4.x, self.f_position4.y)
				
				if sdl2.SDLK_ESCAPE in self.keys_down:
					self.life = 0
				
			#Navigate Title Screen
			if self.play_game == False:
				if self.play_tutorial == False and self.play_game_new == False:
					if sdl2.SDLK_w in self.keys_down:
						self.new_game = True
						self.continue_game = False
					if int(self.highScore) > 0:
						if sdl2.SDLK_s in self.keys_down:
							self.new_game = False
							self.continue_game = True
					if sdl2.SDLK_SPACE in self.keys_down:
						if self.new_game == True:
							self.play_game_new = True
							self.new_delay = time.time() + 1
						if self.continue_game == True:
							self.play_game = True
				if self.play_game_new == True and self.play_tutorial == False and self.new_delay < time.time():
					if sdl2.SDLK_SPACE in self.keys_down:
						self.play_tutorial = True
						self.new_delay = time.time() + 1
				if self.play_tutorial == True and self.play_tutorial2 == False and self.new_delay < time.time():
					if sdl2.SDLK_SPACE in self.keys_down:
						self.play_tutorial2 = True
						self.new_delay = time.time() + 1
				if self.play_tutorial2 == True and self.play_tutorial3 == False and self.new_delay < time.time():
					if sdl2.SDLK_SPACE in self.keys_down:
						self.play_tutorial3 = True
						self.new_delay = time.time() + 1
				if self.play_tutorial3 == True and self.new_delay < time.time():
					if sdl2.SDLK_SPACE in self.keys_down:
						file = open("output.txt", "w")
						file.write(str(0))
						file.close()
						f = open('output.txt', 'r')
						self.highScore = f.read()
						f.close()
						self.play_game = True
					
			self.draw(renderer,frame_time)
			last_frame = current_frame
		

sdl2.ext.init()

window = sdl2.ext.Window("CSC 205 A2", size=(A2Canvas.CANVAS_SIZE_X, A2Canvas.CANVAS_SIZE_Y))
window.show()

renderer = sdl2.SDL_CreateRenderer(window.window, -1,0)# sdl2.SDL_RENDERER_PRESENTVSYNC | sdl2.SDL_RENDERER_ACCELERATED);


sdl2.SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255)
sdl2.SDL_RenderClear(renderer)
sdl2.SDL_RenderPresent(renderer)

canvas = A2Canvas()		
canvas.frame_loop(renderer)
		
sdl2.SDL_DestroyRenderer(renderer)
