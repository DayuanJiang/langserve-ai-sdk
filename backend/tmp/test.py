
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Introduction: Start with a blank screen
        self.wait(1)

        # Draw the Circle
        circle = Circle(radius=1, color=RED)
        self.play(Create(circle))

        # Scale the Circle
        self.play(circle.animate.scale(1.5))

        # Fade Out
        self.play(FadeOut(circle))

        # End Scene: Leave the screen blank for a moment
        self.wait(1)
