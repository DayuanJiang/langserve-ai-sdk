
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create axes
        axes = Axes(x_range=[-4, 4, 1], y_range=[0, 0.5, 0.1], axis_config={"color": DARK_GRAY})
        self.play(DrawBorderThenFill(axes))

        # Create normal distribution curve
        normal_curve = axes.plot(lambda x: np.exp(-x**2 / 2) / np.sqrt(2 * np.pi), color=BLUE_E, stroke_width=2)
        self.play(Create(normal_curve))

        # Create mean line
        mean_line = axes.get_vertical_line(axes.c2p(0, 0), color=RED, stroke_width=2)
        self.play(Create(mean_line))

        # Create standard deviation lines
        std_dev_left = axes.get_vertical_line(axes.c2p(-1, 0), color=GREEN, stroke_width=2)
        std_dev_right = axes.get_vertical_line(axes.c2p(1, 0), color=GREEN, stroke_width=2)

        # Create dashed lines for standard deviations
        dashed_std_dev_left = DashedLine(start=std_dev_left.get_start(), end=std_dev_left.get_end(), color=GREEN, stroke_width=2)
        dashed_std_dev_right = DashedLine(start=std_dev_right.get_start(), end=std_dev_right.get_end(), color=GREEN, stroke_width=2)

        self.play(Create(dashed_std_dev_left), Create(dashed_std_dev_right))

        # Create labels
        normal_dist_label = MathTex("Normal Distribution").scale(0.5).next_to(axes, UP)
        mean_label = MathTex("Mean (\\\\mu)").scale(0.3).next_to(mean_line, RIGHT)
        std_dev_label = MathTex("Standard Deviation (\\\\sigma)").scale(0.3).next_to(dashed_std_dev_left, LEFT)

        self.play(FadeIn(normal_dist_label))
        self.play(FadeIn(mean_label))
        self.play(FadeIn(std_dev_label))

        # Hold the final scene
        self.wait(3)
