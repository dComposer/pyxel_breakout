import pyxel
import enum
from ball import Ball
from paddle import Paddle
from brick import check_levels, load_level
from hud import draw_hud, draw_dropped, draw_game_over, draw_win


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
        self.levels = check_levels()
        self.paddle = Paddle()
        self.ball = Ball()
        self.reset_ball()
        self.live = None
        self.score = None
        self.bricks = None
        self.current_level = None
        self.current_game_state = None
        self.start_new_game()
        pyxel.run(self.update, self.draw)

    def start_new_game(self):
        self.lives = 3
        self.current_level = 1
        self.score = 0
        self.bricks = load_level(self.levels[self.current_level - 1])
        self.reset_ball()
        self.current_game_state = GameState.READY

    def reset_ball(self):
        self.ball.x = self.paddle.x + self.paddle.w / 2 + 10
        self.ball.y = self.paddle.y - self.ball.r
        self.ball.speedX = self.paddle.deflect_force(self.ball.x)
        self.ball.speedY = -2.5
        self.ball.out_of_bounds = False

    def start_next_level(self):
        self.current_level += 1
        self.bricks = load_level(self.levels[self.current_level - 1])
        self.current_game_state = GameState.READY
        self.reset_ball()

    def update(self):
        self.check_input()
        self.paddle.update()
        if self.current_game_state == GameState.READY:
            # Update the ball X position: it should be stuck to the paddle
            self.ball.x = self.paddle.x + self.paddle.w / 2 + 10
        if self.current_game_state == GameState.RUNNING:
            self.ball.update()
            self.check_collision()
            if self.ball.out_of_bounds:
                self.lives -= 1
                if self.lives > 0:
                    self.current_game_state = GameState.DROPPED
                else:
                    self.current_game_state = GameState.GAME_OVER

    def check_collision(self):
        # Ball vs Paddle
        collision, _ = self.ball.detect_collision(self.paddle, paddle=True)
        if collision:
            pass
        # Ball vs Bricks
        for i in reversed(range(len(self.bricks))):
            b = self.bricks[i]
            collision, score = self.ball.detect_collision(b)
            if collision:
                self.score += score
                del self.bricks[i]
                self.check_level_complete()
                break

    def check_level_complete(self):
        if len(self.bricks) == 0:
            if len(self.levels) > self.current_level:
                self.start_next_level()
            else:
                self.current_game_state = GameState.WIN

    def check_input(self):
        if self.current_game_state == GameState.READY:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE):
                # Launch the ball and set the game running
                self.current_game_state = GameState.RUNNING
        if self.current_game_state == GameState.DROPPED:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_ball()
                self.current_game_state = GameState.READY
        if (
            self.current_game_state == GameState.GAME_OVER
            or self.current_game_state == GameState.WIN
        ):
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.start_new_game()

    def draw(self):
        pyxel.cls(0)
        self.paddle.draw()
        for b in self.bricks:
            b.draw()
        self.ball.draw()
        draw_hud(score=self.score, lives=self.lives)
        if self.current_game_state == GameState.DROPPED:
            draw_dropped()
        if self.current_game_state == GameState.GAME_OVER:
            draw_game_over(score=self.score)
        if self.current_game_state == GameState.WIN:
            draw_win(score=self.score)
        pyxel.text(10, pyxel.height - 20, str(self.current_game_state), 7)
        pyxel.text(10, pyxel.height - 10, str(self.score), 7)


# Kickstart our app
App()
