
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create a red circle
        circle = Circle(radius=1, color=RED)
        
        # Step 1: Draw the red circle
        self.play(Create(circle))
        
        # Step 2: Scale the circle
        self.play(circle.animate.scale(1.5))
        
        # Step 3: Move the circle to the right
        self.play(circle.animate.move_to(RIGHT * 3))
        
        # Step 4: Fade out the circle
        self.play(FadeOut(circle))
