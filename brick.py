import pyxel

BrickType = {1: {"img": 0, "u": 16, "v": 0, "w": 32, "h": 8, "score": 1}}


class Brick:
    def __init__(self, x, y, brick_type):
        self.x = x
        self.y = y
        self.brick_type = brick_type
        self.w = BrickType[brick_type]["w"]
        self.h = BrickType[brick_type]["h"]
        self.score = BrickType[brick_type]["score"]

    def draw(self):
        pyxel.blt(
            self.x,
            self.y,
            BrickType[self.brick_type]["img"],
            BrickType[self.brick_type]["u"],
            BrickType[self.brick_type]["v"],
            BrickType[self.brick_type]["w"],
            BrickType[self.brick_type]["h"],
        )
