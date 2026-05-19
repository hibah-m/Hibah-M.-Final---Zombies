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
		self.prize_lock = False


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
		self.bombs_used = 0

		self.st()

		screen.onkeypress(self.turn_left, left_key)
		screen.onkeypress(self.turn_right, right_key)
		screen.onkeypress(self.fire, fire_key)
		screen.onkeypress(self.drop_bomb, bomb_key)

	def fire(self):
		if self.alive and len(self.bullets) < 5:
			self.bullets.append(Bullet(self))

	def drop_bomb(self):
		if self.alive and self.bombs_used < self.bomb_limit:
			self.bombs.append(Bomb(self))
			self.bombs_used += 1

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

		x = self.xcor()
		y = self.ycor()

		if x > 240 or x < -240:
			self.setheading(180 - self.heading())

		if y > 240 or y < -240:
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

		self.shape("triangle")
		self.shapesize(0.3, 0.6)
		self.color("white")
		self.penup()

		self.goto(player.xcor(), player.ycor())
		self.setheading(player.heading())
		self.forward(10)
		self.st()

	def move(self):
		self.forward(15)

		# NO abs() version
		if self.xcor() > 250 or self.xcor() < -250 or self.ycor() > 250 or self.ycor() < -250:
			self.die()
			return True

		return False

	def die(self):
		self.hideturtle()


class Zombie(Turtle):
	def __init__(self, target):
		super().__init__()
		self.shape("turtle")
		self.color("green")
		self.penup()
		self.target = target
		self.goto(randint(-240, 240), randint(-240, 240))

	def move(self):
		if self.target.alive:
			self.setheading(self.towards(self.target))
			self.forward(2)

	def die(self):
		self.hideturtle()


class Prize(Turtle):
	def __init__(self):
		super().__init__()
		self.shape("circle")
		self.color("yellow")
		self.shapesize(1.2, 1.2)
		self.penup()
		self.relocate()

	def relocate(self):
		self.goto(randint(-230, 230), randint(-230, 230))


class Bomb(Turtle):
	def __init__(self, player):
		super().__init__()

		self.player = player
		self.shape("circle")
		self.color("orange")
		self.penup()
		self.goto(player.xcor(), player.ycor())

		ontimer(self.explode, 1000)

	def explode(self):

		explosion = Turtle()
		explosion.hideturtle()
		explosion.penup()
		explosion.color("red")
		explosion.goto(self.xcor(), self.ycor())
		explosion.pendown()
		explosion.circle(100)

		ontimer(explosion.hideturtle, 200)

		to_remove = []

		for z in zombies:

			if self.distance(z) < 100:

				z.die()
				to_remove.append(z)

				if self.player == p1:
					score1.add_point()
				else:
					score2.add_point()

		for z in to_remove:

			if z in zombies:
				zombies.remove(z)

		self.hideturtle()

		if self in self.player.bombs:
			self.player.bombs.remove(self)


class Score(Turtle):
	def __init__(self, x, y, label):
		super().__init__()
		self.hideturtle()
		self.penup()
		self.goto(x, y)
		self.score = 0
		self.label = label
		self.color("white")
		self.update_score()

	def update_score(self):
		self.clear()
		self.write(f"{self.label}: {self.score}", font=("Arial", 14, "normal"))

	def add_point(self):
		self.score += 1
		self.update_score()


#### DRIVER CODE #####

screen = Screen()
screen.bgcolor("black")

playing_area()
screen.listen()

state = GameState()

p1 = Player(-100, 0, "red", screen, "d", "a", "w", "s")
p2 = Player(100, 0, "blue", screen, "Right", "Left", "Up", "Down")

players = [p1, p2]
zombies = []

prize = Prize()

score1 = Score(-200, 260, "Player 1")
score2 = Score(100, 260, "Player 2")

writer = Turtle()
writer.hideturtle()
writer.penup()
writer.color("white")


def unlock_prize():
	state.prize_lock = False


def spawn_zombies():

	for i in range(state.spawn_count // 2):
		zombies.append(Zombie(p1))

	for i in range(state.spawn_count // 2):
		zombies.append(Zombie(p2))

	state.spawn_count += 2


def game_loop():

	if state.game_over:
		return

	for player in players:
		player.move()

	for zombie in zombies:
		zombie.move()

	zombies_to_remove = []

	for player in players:

		new_bullet_list = []

		for bullet in player.bullets:

			keep_bullet = True
			offscreen = bullet.move()

			if offscreen:

				keep_bullet = False

			else:

				hit = False

				for zombie in zombies:

					if bullet.distance(zombie) < 20:

						if hit == False:

							bullet.die()
							zombie.die()

							zombies_to_remove.append(zombie)

							if player == p1:
								score1.add_point()
							else:
								score2.add_point()

							hit = True

				if hit == True:
					keep_bullet = False

			if keep_bullet:
				new_bullet_list.append(bullet)

		player.bullets = new_bullet_list

	for z in zombies_to_remove:

		if z in zombies:
			zombies.remove(z)

	for player in players:

		if not state.prize_lock and player.distance(prize) < 20:

			state.prize_lock = True
			prize.relocate()
			spawn_zombies()

			ontimer(unlock_prize, 300)

	for zombie in zombies:

		for player in players:

			if zombie.distance(player) < 20:

				player.die()
				state.game_over = True

				if player == p1:
					winner = "Player 2"
				else:
					winner = "Player 1"

				writer.goto(0, 0)
				writer.write(f"{winner} Wins!", align="center", font=("Arial", 24, "bold"))

	screen.ontimer(game_loop, 20)


game_loop()
screen.mainloop()
