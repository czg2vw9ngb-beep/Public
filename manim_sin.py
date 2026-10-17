"""Animate y = sin(x) with Manim Community.

Install: pip install manim
Render:  manim -pqh manim_sin.py SineWave
System dependencies: https://docs.manim.community/en/stable/installation.html
"""

import numpy as np
from manim import (
    Axes, BLUE, Create, Dot, FadeIn, GREEN, LEFT, PI,
    RIGHT, Scene, Text, TracedPath, UP, ValueTracker,
    VGroup, WHITE, YELLOW, always_redraw, linear,
)


class SineWave(Scene):
    def construct(self):
        self.camera.background_color = "#101827"
        title = Text("y = sin(x)", font_size=40).to_edge(UP)
        axes = Axes(
            x_range=[-2 * PI, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=11,
            y_length=4.5,
            tips=False,
            axis_config={"color": WHITE, "include_ticks": True},
        ).shift(0.35 * -UP)

        # Text labels avoid requiring a LaTeX installation.
        labels = VGroup()
        for x, label in [(-2 * PI, "-2π"), (-PI, "-π"), (0, "0"),
                         (PI, "π"), (2 * PI, "2π")]:
            labels.add(Text(label, font_size=22).next_to(axes.c2p(x, 0), -UP, buff=0.18))
        for y in [-1, 1]:
            labels.add(Text(str(y), font_size=22).next_to(axes.c2p(0, y), LEFT, buff=0.18))
        labels.add(Text("x", font_size=26).next_to(axes.x_axis, RIGHT))
        labels.add(Text("y", font_size=26).next_to(axes.y_axis, UP))

        position = ValueTracker(-2 * PI)
        point = always_redraw(lambda: Dot(
            axes.c2p(position.get_value(), np.sin(position.get_value())),
            color=YELLOW, radius=0.07,
        ))
        vertical = always_redraw(lambda: axes.get_vertical_line(
            axes.c2p(position.get_value(), np.sin(position.get_value())),
            color=BLUE,
        ))
        trace = TracedPath(point.get_center, stroke_color=GREEN, stroke_width=4)

        self.play(FadeIn(title), Create(axes), FadeIn(labels), run_time=1.5)
        self.add(trace, vertical, point)
        self.play(position.animate.set_value(2 * PI), run_time=8, rate_func=linear)
        # Replace the sampled trace with the exact complete curve at the end.
        curve = axes.plot(np.sin, x_range=[-2 * PI, 2 * PI], color=GREEN, stroke_width=4)
        self.remove(trace)
        self.add(curve)
        self.wait(2)
