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


class GameState:
	def __init__(self):
		self.spawn_count = 4
		self.game_over = False


class Player(Turtle):
	def __init__(self, x, y, color, screen, right_key, left_key, fire_key, bomb_key):
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
		self.bombs = []
		self.bomb_limit = 3

		self.st()
		screen.onkeypress(self.turn_left, left_key)
		screen.onkeypress(self.turn_right, right_key)
		screen.onkeypress(self.fire, fire_key)
		screen.onkeypress(self.drop_bomb, bomb_key)

	def fire(self):
		if self.alive and len(self.bullets) < 5:
			self.bullets.append(Bullet(self))

	def drop_bomb(self):
		if self.alive and len(self.bombs) < self.bomb_limit:
			self.bombs.append(Bomb(self))

	def turn_left(self):
		if self.alive:
			self.left(10)

	def turn_right(self):
		if self.alive:
			self.right(10)

	def move(self):
		if not self.alive:
			return

		self.forward(5)

		if self.xcor() > 240 or self.xcor() < -240:
			self.setheading(180 - self.heading())

		if self.ycor() > 240 or self.ycor() < -240:
			self.setheading(-self.heading())

	def die(self):
		self.alive = False
		self.hideturtle()


class Bullet(Turtle):
	def __init__(self, player):
		super().__init__()

		self.player = player
		self.ht()
		self.speed(0)
		self.shape("circle")
		self.color("yellow")
		self.penup()

		self.goto(player.xcor(), player.ycor())
		self.setheading(player.heading())
		self.st()

	def move(self):
		pass

	def die(self):
		pass


class Zombie(Turtle):
	def __init__(self, target):
		super().__init__()

		self.shape("circle")
		self.color("red")
		self.penup()

		self.target = target
		self.goto(randint(-240, 240), randint(-240, 240))

	def move(self):
		pass

	def die(self):
		pass


class Prize(Turtle):
	def __init__(self):
		super().__init__()

		self.shape("circle")
		self.color("gold")
		self.penup()

		self.relocate()

	def relocate(self):
		pass


class Bomb(Turtle):
	def __init__(self, player):
		super().__init__()

		self.player = player
		self.shape("circle")
		self.color("orange")
		self.penup()

		self.goto(player.xcor(), player.ycor())

	def explode(self):
		pass


class Score(Turtle):
	def __init__(self, x, y, label):
		super().__init__()
		self.hideturtle()
		self.penup()
		self.goto(x, y)
		self.score = 0
		self.label = label

	def update_score(self):
		pass

	def add_point(self):
		pass


#### DRIVER CODE ####
screen = Screen()
screen.bgcolor("black")

playing_area()
screen.listen()


screen.mainloop()




