import pyxel
import enum
from ball import Ball
from paddle import Paddle


class GameState(enum.Enum):
    READY = 0
    RUNNING = 1
    DROPPED = 2
    GAME_OVER = 3
    WIN = 4


class App:
    def __init__(self):
        pyxel.init(width=384, height=300, display_scale=3, title="Breakout", fps=60)
        pyxel.load("assets/resources.pyxres")
        self.paddle = Paddle()
        self.ball = Ball()
        self.reset_ball()
        self.current_game_state = GameState.READY
        pyxel.run(self.update, self.draw)

    def reset_ball(self):
        self.ball.x = self.paddle.x + self.paddle.w / 2 + 10
        self.ball.y = self.paddle.y - self.ball.r
        self.ball.speedX = self.paddle.deflect_force(self.ball.x)
        self.ball.speedY = -2.5
        self.ball.out_of_bounds = False

    def update(self):
        self.paddle.update()
        if self.current_game_state == GameState.READY:
            # Update the ball X position: it should be stuck to the paddle
            self.ball.x = self.paddle.x + self.paddle.w / 2 + 10
        if self.current_game_state == GameState.RUNNING:
            self.ball.update()
            self.check_collision()
            if self.ball.out_of_bounds:
                self.current_game_state = GameState.DROPPED

    def check_collision(self):
        # Ball vs Paddle
        collision = self.ball.detect_collision(self.paddle, paddle=True)
        if collision:
            pass

    def draw(self):
        pyxel.cls(0)
        self.paddle.draw()
        self.ball.draw()


# Kickstart our app
App()
