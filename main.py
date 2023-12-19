import pyxel
from ball import Ball
from paddle import Paddle


class App:
    def __init__(self):
        pyxel.init(width=384, height=300, display_scale=3, title="Breakout", fps=60)
        pyxel.load("assets/resources.pyxres")
        self.paddle = Paddle()
        self.ball = Ball(100, 100)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.ball.update()

    def draw(self):
        pyxel.cls(0)
        self.paddle.draw()
        self.ball.draw()


# Kickstart our app
App()
