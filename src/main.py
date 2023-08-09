from manim import *
import numpy as np

class TrigonometryProofsScene(Scene):
    def construct(self):
        # create the number plane
        number_plane = NumberPlane(
            x_range=(-1, 5, 1),
            y_range=(-1, 5, 1),
            axis_config={
                "include_tip": True,
                "tip_width": 0.2,
                "tip_height": 0.2,
                "include_ticks": True,
                "numbers_with_elongated_ticks": range(-5, 5),
            },
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.3
            }
        ).move_to(LEFT*3)

        # add axis labels
        labels = number_plane.get_axis_labels(x_label='x', y_label='y')

        # add x values
        x_ticks_labels = VGroup()
        x_values = [
            (1, "x"),
            (2, "x+1"),
            (3, "x+2"),
            (4, "x+3")
        ]
        for value, text in x_values:
            tex = MathTex(text).set_color(WHITE).scale(0.7).next_to(number_plane.c2p(value, 0), DOWN)
            x_ticks_labels.add(tex)

        # add y values
        y_ticks_labels = VGroup()
        y_values = [
            (1, "y"),
            (2, "y+1"),
            (3, "y+2"),
            (4, "y+3")
        ]
        for value, text in y_values:
            tex = MathTex(text).set_color(WHITE).scale(0.7).next_to(number_plane.c2p(0, value), LEFT)
            x_ticks_labels.add(tex)

        pc_x, pc_y = (1.5, 1.5)
        player_angle = np.radians(60)

        player_point = Dot(number_plane.c2p(pc_x, pc_y), color=WHITE)
        player_label_1 = MathTex("Player").scale(0.6).next_to(player_point, DOWN, buff=0.05)
        player_label_2 = MathTex("P").scale(0.6).next_to(player_point, DOWN, buff=0.05)

        zero_deg_line = DashedLine(number_plane.c2p(pc_x, pc_y), number_plane.c2p(5, pc_y), dash_length=0.15)
        ray = Line(
            number_plane.c2p(pc_x, pc_y), number_plane.c2p(5.6, pc_y)
        ).set_angle(player_angle).add_tip(tip_length=0.2, tip_width=0.2)
        ray_angle = Angle(zero_deg_line, ray)
        ray_angle_label = MathTex(r"\theta").next_to(ray_angle, buff=0.1)
        ray_angle_label.set_y(ray_angle_label.get_y() + 0.2)

        # play number plane animations
        self.play(Create(number_plane, run_time=3))
        self.play(Write(labels))
        self.play(Write(x_ticks_labels))
        self.play(Write(y_ticks_labels))

        self.play(Create(player_point, run_time=0.5))
        self.play(Create(zero_deg_line, run_time=1))
        self.play(Create(ray, run_time=1))
        self.play(Create(ray_angle, run_time=0.5))
        self.play(Write(player_label_1))
        self.play(Write(ray_angle_label))

        self.wait()

        self.play(Transform(player_label_1, player_label_2))
        player_label_3 = MathTex(r"P(x+px, y+py)")
        player_label_3.move_to([3, 3, 0]).scale(1.25)
        self.play(Create(player_label_3))

        self.wait()


