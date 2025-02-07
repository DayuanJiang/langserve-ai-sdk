
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create a red circle
        circle = Circle(radius=1, color=RED)

        # Step 1: Fade in the circle
        self.play(FadeIn(circle, run_time=1))
        
        # Step 2: Scale up the circle
        self.play(circle.animate.scale(1.5), run_time=1)
        
        # Step 3: Move the circle to the right
        self.play(circle.animate.shift(RIGHT * 3), run_time=2)
        
        # Step 4: Scale down the circle
        self.play(circle.animate.scale(1/1.5), run_time=1)
        
        # Step 5: Fade out the circle
        self.play(FadeOut(circle, run_time=1))
