from turtle import *
from random import randint, choice

#### CLASS AND FUNCTION DEFINITIONS #####
def playing_area():
	t = Turtle()
	t.speed(0)
	t.ht()
	t.pu()
	t.goto(-250,250)
	t.color("light blue")
	t.pd()
	t.begin_fill()
	for i in range(4):
		t.forward(500)
		t.right(90)
	t.end_fill()

'''
Player() Class

Constructor( def __init__(self)):
- player should be shaped like a turtle.
- will take in the x and y coordinates for where the player will initially appear.
- will take in a color for the player
- will take in keys to turn left, turn right and shoot bullets.
- player will have an attribute that is a list that stores bullets


move(self):
- moves object forward five pixels

fire(self):
- creates a Bullet object
- appends the Bullet object to the players's bullet list
'''
class Player(Turtle):
	def __init__(self, x, y, color, screen, right_key, left_key, fire_key):
		super().__init__()
		self.ht()
		self.speed(0)
		self.color(color)
		self.penup()
		self.goto(x, y)
		self.setheading(90)
		self.shape("turtle")
		
		self.alive = True
		self.bullets = []
		
		self.st()
		screen.onkeypress(self.turn_left, left_key)
		screen.onkeypress(self.turn_right, right_key)
		screen.onkeypress(self.fire, fire_key)
	
	def fire(self):
		if self.alive:
			self.bullets.append(Bullet(self))
	
	def turn_left(self):
		if self.alive:
			self.left(10)
	
	def turn_right(self):
		if self.alive:
			self.right(10)



'''
Bullet() Class
Constructor ( def __init__(self) ):
- Input: player object
- Attributes:
	- Position: same as player
	- Heading: same as player
	- Player: the player
 
move(self):
- move 15 or more pixels forward
- should call on the die() method when the bullet leaves the playing area

die()
- hides the object. 
- removes object from the player's bullet list
'''


#### DRIVER CODE ####
screen = Screen()
screen.bgcolor("black")

playing_area()


screen.mainloop()
