
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create a blue circle
        circle = Circle(color=BLUE)

        # Animation 1: Create the circle
        self.play(Create(circle))
        self.wait(0.5)

        # Animation 2 (alternative): Grow from center
        # self.play(GrowFromCenter(circle))
        # self.wait(0.5)
        
        # Animation 3 (Optional): Shift to the right
        self.play(circle.animate.shift(RIGHT))
        self.wait(0.5)

        # Animation 4 (Optional): Pulsing effect
        self.play(circle.animate.scale(1.2))
        self.wait(0.5)
        self.play(circle.animate.scale(0.8))
        self.wait(0.5)
