import pygame
import time
import random

pygame.init()

white = (255,255,255)
black = (0,0,0)
green = (0,150,0)
red = (255,0,0)
display_width = 800
display_height = 600
snake_list = []


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake On')

icon = pygame.image.load('./apple2.jpg')
pygame.display.set_icon(icon)

img = pygame.image.load('./snakehead2.jpeg')
appleimg = pygame.image.load('./apple2.jpg')

appleThickness = 30
block_size = 20
FPS = 10

direction = "right"

smallfont = pygame.font.SysFont("comicsansms" , 25)
medfont = pygame.font.SysFont("comicsansms" , 45)
largefont = pygame.font.SysFont("comicsansms" , 65)

clock = pygame.time.Clock()

def pause():
	paused = True
	message_to_screen("Paused",black,-100,size="large")
	message_to_screen("Press c to continue , q to quit",black,25)
	pygame.display.update()
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False

				elif event.key == pygame.K_q:
					pygame.quit()
					quit()
		#gameDisplay.fill(white)
		clock.tick(5)				

def score(score):
	text = smallfont.render("Score: "+str(score),True,black)
	gameDisplay.blit(text,[0,0])

def randapplegen():
	randapplex = random.randrange(0,display_width - appleThickness)
	randappley = random.randrange(0,display_height - appleThickness)
	randapplex = round(randapplex)#/10) * 10
	randappley = round(randappley)#/10) * 10
	return randapplex,randappley

randapplex,randappley = randapplegen()

def game_intro():

	intro = True

	while intro:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					intro = False
				if event.key == pygame.K_q:
					pygame.quit()
					quit()		


		gameDisplay.fill(white)
		message_to_screen("Welcome to Snake On",green,-100,"large")
		message_to_screen("The objective of the game is to eat apple as much as you can",black,-30)
		message_to_screen("More you eat , more you score",black,10)
		message_to_screen("Running in snake itself or edge will get you lose",black,50)
		message_to_screen("Press c to play again ,Press p to pause or q to quit",black,90,size = "medium")
		pygame.display.update()
		clock.tick(10)

def snake(snake_list,block_size):

	if direction == "right":
		head = pygame.transform.rotate(img,270)

	if direction == "left":
		head = pygame.transform.rotate(img,90)

	if direction == "up":
		head = img
		
	if direction == "down":
		head = pygame.transform.rotate(img,180)
				
	gameDisplay.blit(head, (snake_list[-1][0],snake_list[-1][1]))

	for xny in snake_list[:-1]:
		pygame.draw.rect(gameDisplay,green, [xny[0],xny[1],block_size,block_size])

def text_objects(text,color,size):
	if size == "small":
		textSurface = smallfont.render(text , True , color)
	elif size == "medium":
		textSurface = medfont.render(text , True , color)	
	elif size == "large":
		textSurface = largefont.render(text , True , color)	
	return textSurface , textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size = "small"):
	textSurf, textRect = text_objects(msg,color,size)
	textRect.center = (display_width/2) , ((display_height/2) + y_displace)
	gameDisplay.blit(textSurf,textRect)
	#pygame.display.update();

def gameLoop():
	global direction
	direction = "right"
	gameExit = False
	gameOver = False
	lead_x = display_width/2
	lead_y = display_height/2
	lead_x_change = 10
	lead_y_change = 0
	snakeLength = 1
	randapplex,randappley = randapplegen()
	while not gameExit:

		if gameOver == True:
			message_to_screen("Game Over",red,y_displace=-50,size = "large")
			message_to_screen("Press c to play again ,Press q to quit",black,50,size ="medium" )
			pygame.display.update()

		while gameOver == True:
			#gameDisplay.fill(white)
			

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOver = False
					gameExit = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					if event.key == pygame.K_c:
						gameLoop()	



		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					direction = "left"
					lead_x_change -= block_size
					lead_y_change = 0
				elif event.key == pygame.K_RIGHT:
					direction = "right"
					lead_x_change += block_size
					lead_y_change = 0
				elif event.key == pygame.K_UP:
					direction = "up"
					lead_y_change -= block_size
					lead_x_change = 0
				elif event.key == pygame.K_DOWN:
					direction = "down"
					lead_y_change += block_size
					lead_x_change = 0
				elif event.key == pygame.K_p:
					pause()			
			if lead_x >= display_width or lead_x <= 0 or lead_y >= display_height or lead_y <= 0:
				gameOver = True		
						
		lead_x+=lead_x_change
		lead_y+=lead_y_change

		gameDisplay.fill(white)
		#pygame.draw.rect(gameDisplay,red,[randapplex,randappley,appleThickness,appleThickness])
		
		gameDisplay.blit(appleimg, (randapplex,randappley))

		snake_head = []
		snake_head.append(lead_x)
		snake_head.append(lead_y)
		snake_list.append(snake_head)

		if len(snake_list) > snakeLength:
			del snake_list[0]

			for eachSegment in snake_list[:-1]:
				if eachSegment == snake_head:
					gameOver = True
			
		snake(snake_list,block_size)
		score(snakeLength-1)

		pygame.display.update()					
		
		if lead_x > randapplex and lead_x < randapplex + appleThickness or lead_x + block_size > randapplex and lead_x + block_size < randapplex + appleThickness:	

			if lead_y > randappley and lead_y < randappley + appleThickness or lead_y + block_size > randappley and lead_y + block_size < randappley + appleThickness:	
				randapplex,randappley = randapplegen()
				snakeLength += 1

			elif lead_y + block_size > randappley and lead_y + block_size < randappley + appleThickness:
				randapplex,randappley = randapplegen() 
				snakeLength += 1


		clock.tick(FPS)

	pygame.quit()
	quit()
game_intro()
gameLoop()	
