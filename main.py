import turtle as tr


class GameBoard:

    def __init__(self):

        self.bricks = self.make_bricks()
        self.paddle = self.make_paddle()
        self.paddle_velocity = 0

        self.ball = self.make_ball()
        self.ball_velocity = [0, -7]

        self.walls = self.make_walls() 
        
        self.score = 0
        self.lives = 3
        self.score_board, self.lives_board = self.make_score_board()

        
    def make_bricks(self):

        tr.tracer(False)

        bricks = []
        colors = ["red", "orange", "yellow", "green", "blue"]
        for color_idx in range(len(colors)):
            for i in range(10):
                brick = tr.Turtle()
                brick.shape("square")
                brick.shapesize(1, 2.5, 1)
                brick.color(colors[color_idx])
                brick.penup()
                brick.goto(-275 + 60 * i, 200 - 25 * color_idx)
                bricks.append(brick)

        tr.tracer(True)

        return bricks

    def make_walls(self):

        tr.tracer(False)

        wall1 = tr.Turtle()
        wall2 = tr.Turtle()
        wall3 = tr.Turtle()

        wall1.shape("square")
        wall2.shape("square")
        wall3.shape("square")

        wall1.shapesize(1, 32, 1)
        wall2.shapesize(30, 1, 1)
        wall3.shapesize(30, 1, 1)

        wall1.color("white")
        wall2.color("white")
        wall3.color("white")

        wall1.penup()
        wall2.penup()
        wall3.penup()

        wall1.goto(-5, 310)
        wall2.goto(-315, 0)
        wall3.goto(305, 0)

        tr.tracer(True)
        return [wall1, wall2, wall3]
    
    def make_paddle(self):

        tr.tracer(False)

        paddle = tr.Turtle()
        paddle.shape("square")
        paddle.shapesize(1, 4, 1)
        paddle.color("white")
        paddle.penup()
        paddle.goto(0, -320)

        tr.tracer(True)

        return paddle
    
    def make_ball(self):

        tr.tracer(False)

        ball = tr.Turtle()
        ball.shape("circle")
        ball.color("white")
        ball.penup()
        ball.goto(0, -200)

        tr.tracer(True)

        return ball

    def make_score_board(self):

        tr.tracer(False)

        score_board = tr.Turtle()
        lives_board = tr.Turtle()

        score_board.hideturtle()
        score_board.penup()
        score_board.goto(-300, 350)
        score_board.color("white")
        score_board.write("Score: 0", align="left", font=("Arial", 24, "bold"))

        lives_board.hideturtle()
        lives_board.penup()
        lives_board.goto(300, 350)
        lives_board.color("white")
        lives_board.write("Lives: 3", align="right", font=("Arial", 24, "bold"))

        tr.tracer(True)

        return score_board, lives_board

    def update_score_board(self):

            self.score_board.clear()
            self.score_board.write("Score: " + str(game_board.score), align="left", font=("Arial", 24, "bold"))
            self.lives_board.clear()
            self.lives_board.write("Lives: " + str(game_board.lives), align="right", font=("Arial", 24, "bold"))

    def reset_paddle(self):

        tr.tracer(False)
        self.ball.goto(0, -200)
        self.ball_velocity = [0, -7]
        tr.tracer(True)



    def set_paddle_velocity_left(self):
        self.paddle_velocity = -10

    def set_paddle_velocity_right(self):
        self.paddle_velocity = 10

    def stop_paddle(self):
        self.paddle_velocity = 0

if __name__ == "__main__":
    tr.setup(650, 850)
    tr.title("Fake-Breakout")
    tr.bgcolor("black")
    
    game_board = GameBoard() 
    tr.speed(0)

    while game_board.lives > 0:

        # Move paddle
        tr.listen()
        tr.onkeypress(game_board.set_paddle_velocity_left, "Left")
        tr.onkeyrelease(game_board.stop_paddle, "Left")

        tr.onkeypress(game_board.set_paddle_velocity_right, "Right")
        tr.onkeyrelease(game_board.stop_paddle, "Right")

        game_board.paddle.goto(game_board.paddle.xcor() + game_board.paddle_velocity, game_board.paddle.ycor())

        # Move ball
        game_board.ball.penup()
        game_board.ball.goto(game_board.ball.xcor() + game_board.ball_velocity[0], game_board.ball.ycor() + game_board.ball_velocity[1])

        # Handle wall collisions
        if game_board.ball.xcor() > 290 or game_board.ball.xcor() < -300:
            game_board.ball_velocity[0] *= -1

        if game_board.ball.ycor() > 300:
            game_board.ball_velocity[1] *= -1

        # Handle paddle collisions
        ball_between_paddle_ends = game_board.paddle.xcor() - 40 < game_board.ball.xcor() < game_board.paddle.xcor() + 40
        ball_on_paddle_edge = game_board.ball.ycor() < -310 and ball_between_paddle_ends
        if ball_on_paddle_edge:
            game_board.ball_velocity[1] *= -1
            game_board.ball_velocity[0] = (game_board.ball.xcor() - game_board.paddle.xcor()) / 10 
        
        # Handle brick collisions
        for brick in game_board.bricks:
            ball_between_brick_ends = brick.xcor() - 30 < game_board.ball.xcor() < brick.xcor() + 30
            ball_on_brick_edge = brick.ycor() - 20 < game_board.ball.ycor() < brick.ycor() + 20 and ball_between_brick_ends
            if ball_on_brick_edge:
                game_board.ball_velocity[1] *= -1
                brick.hideturtle()
                game_board.bricks.remove(brick)
                game_board.score += 1
                game_board.update_score_board()
                break


        # Handle game over
        if game_board.ball.ycor() < -350:
            game_board.lives -= 1
            game_board.update_score_board()
            game_board.reset_paddle()

    if game_board.bricks is None:
        game_board.score_board.goto(0, 0)
        game_board.score_board.write("You win!", align="center", font=("Arial", 24, "bold"))
    else:
        game_board.score_board.goto(0, 0)
        game_board.score_board.write("You lose!", align="center", font=("Arial", 24, "bold"))

    tr.mainloop()
