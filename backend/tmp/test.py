
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create a blue circle with a thick black border
        circle = Circle(radius=2, color=BLUE, fill_opacity=1).set_stroke(BLACK, 2)

        # Add the circle to the scene
        self.add(circle)

        # Fade in the circle
        self.play(FadeIn(circle))

        # Grow the circle to a radius of 3 units
        self.play(circle.animate.scale(1.5), run_time=2)

        # Rotate the circle 360 degrees around its center
        self.play(Rotate(circle, angle=TAU), run_time=3)

        # Shrink the circle back to its original size
        self.play(circle.animate.scale(2/3), run_time=2)

        # End of the scene
        self.wait(1)
