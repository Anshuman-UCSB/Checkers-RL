import pygame
from pygame.locals import (
    MOUSEBUTTONUP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
sq_size = 80

SCREEN_WIDTH = sq_size*8
SCREEN_HEIGHT = sq_size*8

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Checkers - Reinforcement Learning")

running = True
white = (240,217,181)
black = (181,136,99)

imgs = {
	"white": pygame.image.load("assets/white.png"),
	"black": pygame.image.load("assets/black.png"),
	"white_king": pygame.image.load("assets/white_king.png"),
	"black_king": pygame.image.load("assets/black_king.png"),
}

pieces = [None, imgs['white'], imgs['black'], imgs['white_king'], imgs['black_king']]
board = [[0]*8 for _ in range(8)]
for i in range(8):
	for j in range(8):
		if i < 3 and (i+j) % 2 == 1:
			board[i][j] = 1
		elif i > 4 and (i+j) % 2 == 1:
			board[i][j] = 2

def inBounds(x,y):
	return 0<=x<8 and 0<=y<8
def isWhite(x,y):
	return board[y][x]%2==1
def isEmpty(x,y):
	return board[y][x]==0
def getMove(x,y):
	forwards = isWhite(x,y)
	enemy = not forwards
	isKing = board[y][x]>2
	dy = 1 if forwards else -1
	moves = []
	for dx in (-1,1):
		if inBounds(x+dx,y+dy) and isEmpty(x+dx,y+dy):
			print(x,y,"move",x+dx,y+dy)
			moves.append((x+dx,y+dy))
		if isKing and inBounds(x+dx,y-dy) and isEmpty(x+dx,y-dy):
			print(x,y,"move",x+dx,y-dy)
			moves.append((x+dx,y-dy))
		if inBounds(x+dx,y+dy) and not isEmpty(x+dx,y+dy) and isWhite(x+dx,y+dy)==enemy:
			if inBounds(x+2*dx,y+2*dy) and isEmpty(x+2*dx,y+2*dy):
				moves.append((x+2*dx,y+2*dy))
	print(x,y,"move")
	return moves

color = True
highlights = []
selected = None
while running:
	for y in range(8):
		for x in range(8):
			if (x,y) in highlights or (x,y) == selected:
				screen.fill((239,94,63),(x*sq_size,y*sq_size,sq_size,sq_size))
			else:
				screen.fill(white if color else black,(x*sq_size,y*sq_size,sq_size,sq_size))
			if board[y][x]:
				screen.blit(pieces[board[y][x]],(x*sq_size,y*sq_size))
			color = not color
		color = not color
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			running = False
		if event.type == MOUSEBUTTONUP:
			x,y=event.pos
			x//=sq_size
			y//=sq_size
			if highlights == []:
				if not isEmpty(x,y) and not isWhite(x,y):
					highlights = getMove(x,y)
					selected = (x,y)
			else:
				if (x,y) in highlights:
					board[selected[1]][selected[0]],board[y][x]=board[y][x],board[selected[1]][selected[0]]
					
				highlights = []
				selected = None
				
pygame.quit()