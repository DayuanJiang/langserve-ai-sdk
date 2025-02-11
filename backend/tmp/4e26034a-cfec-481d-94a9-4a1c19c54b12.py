
from manim import *
class GeneratedScene(Scene):
    def construct(self):
        circle = Circle(color=BLUE).set_fill(color=BLUE).set_stroke(width=0)
        self.play(Create(circle))
        self.play(MoveAlongPath(circle, Line(start=LEFT, end=RIGHT)),run_time=4)
        self.play(FadeOut(circle),run_time=1)
