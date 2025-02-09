
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create a blue circle
        circle = Circle(radius=1, color=BLUE)  # Changed LIGHT_BLUE to BLUE

        # Animation 1: Draw the blue circle
        self.play(Create(circle))
        
        # Animation 2: Scale the circle
        self.play(circle.animate.scale(1.5))
        
        # Animation 3: Fade out
        self.play(FadeOut(circle))
