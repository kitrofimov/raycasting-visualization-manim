from manim import *

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
                "numbers_with_elongated_ticks": range(0, 5),
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

        blocks = VGroup()
        block_positions = [
            (2, 4),
            (3, 4),
            (4, 4),
            (4, 3)
        ]
        for block_position in block_positions:
            block_origin = number_plane.c2p(block_position[0], block_position[1])
            block_vertices = [
                block_origin,
                [block_origin[0]+1, block_origin[1], 0],
                [block_origin[0]+1, block_origin[1]+1, 0],
                [block_origin[0], block_origin[1]+1, 0]
            ]
            blocks.add(Polygon(
                *block_vertices,
                color=BLUE,
                fill_color=BLUE,
                fill_opacity=0.5
            ))

        pc_x, pc_y = (1.5, 1.5)

        player_point = Dot(number_plane.c2p(pc_x, pc_y), color=WHITE)
        player_label_1 = MathTex("Player").scale(0.6).next_to(player_point, DOWN, buff=0.05)
        player_label_2 = MathTex("P").scale(0.6).next_to(player_point, DOWN, buff=0.05)

        zero_deg_line = DashedLine(number_plane.c2p(pc_x, pc_y), number_plane.c2p(5, pc_y), dash_length=0.15)
        ray = Line(
            number_plane.c2p(pc_x, pc_y), number_plane.c2p(3.5, 4)
        ).add_tip(tip_length=0.2, tip_width=0.2)
        ray_angle = Angle(zero_deg_line, ray)
        ray_angle_label = MathTex(r"\theta").next_to(ray_angle, buff=0.1)
        ray_angle_label.set_y(ray_angle_label.get_y() + 0.2)

        px_brace = Brace(
            Line(number_plane.c2p(1, 1), number_plane.c2p(1.5, 1)),
            buff=0
        )
        px_brace_label = MathTex("px").scale(0.5).next_to(px_brace, direction=DOWN, buff=0.1)
        py_brace = Brace(
            Line(number_plane.c2p(1, 1), number_plane.c2p(1, 1.5)),
            buff=0,
            direction=LEFT
        )
        py_brace_label = MathTex("py").scale(0.5).next_to(py_brace, direction=LEFT, buff=0.1)

        # play number plane animations
        self.play(Succession(
            Create(number_plane, run_time=3),
            DrawBorderThenFill(blocks),
            Write(labels),
            Write(x_ticks_labels),
            Write(y_ticks_labels)
        ))

        # play ray animations
        self.play(Succession(
            Create(player_point, run_time=0.25),
            Create(zero_deg_line, run_time=1),
            Create(ray, run_time=1),
            Create(ray_angle, run_time=0.5),
            Write(player_label_1),
            Write(ray_angle_label)
        ))

        self.wait(2)

        # play brace animations
        self.play(Transform(player_label_1, player_label_2))
        self.play(AnimationGroup(
            Create(px_brace),
            Write(px_brace_label),
            Create(py_brace),
            Write(py_brace_label)
        ))

        # play P and theta explanation animation
        group_explain = VGroup(
            MathTex(r"P(x+px, y+py)").move_to(RIGHT*3.5+UP*0.5),
            MathTex(r"\theta \textrm{ is ray angle}").move_to(RIGHT*3.5+DOWN*0.5),
        )
        self.play(Write(group_explain))

        self.wait(3)

        # uncreate useless things
        group = VGroup(zero_deg_line, ray_angle)
        self.play(AnimationGroup(
            Uncreate(group),
            Unwrite(group_explain),
            Unwrite(ray_angle_label)
        ))

        self.wait()

        # create x triangles
        triangle_x_1 = Polygon(
            number_plane.c2p(1.5, 1.5),
            number_plane.c2p(1.9, 2),
            number_plane.c2p(1.9, 1.5),
            color=RED
        )
        triangle_x_2 = Polygon(
            number_plane.c2p(1.9, 2),
            number_plane.c2p(2.7, 3),
            number_plane.c2p(2.7, 2),
            color=YELLOW
        )
        triangles_x = VGroup(triangle_x_1, triangle_x_2)
        self.play(Create(triangles_x))

        self.wait()

        # move first triangle and write title text
        triangle_x_1_move = triangle_x_1.copy()
        title_text = MathTex(r"\textrm{Horizontal intersections}").move_to(RIGHT*3.5+UP*3)
        self.play(AnimationGroup(
            triangle_x_1_move.animate.move_to(RIGHT*3.5+UP*1.25).scale(5),
            Write(title_text)
        ))

        # write labels for each edge of the triangle and draw angle
        vertices = triangle_x_1_move.get_vertices()
        hypotenuse_label = MathTex("c")
        center_coordinates = Line(vertices[0], vertices[1]).get_center()
        hypotenuse_label.move_to([center_coordinates[0]-0.3, center_coordinates[1]+0.3, center_coordinates[2]])

        edge_labels_and_angle = VGroup(
            hypotenuse_label,
            MathTex("1-py").next_to(Line(vertices[1], vertices[2])),
            MathTex("x_i").next_to(Line(vertices[2], vertices[0]), DOWN),
            Angle(
                Line(vertices[2], vertices[0]),
                Line(vertices[2], vertices[1]),
                elbow=True
            )
        )
        self.play(Write(edge_labels_and_angle, run_time=1))

        # write the proof
        proof_x = MathTex(
            r"""\sin{\theta} &= \frac{1 - py}{c} \Rightarrow c = \frac{1-py}{\sin{\theta}} \\
                \cos{\theta} &= \frac{x_i}{c} \Rightarrow x_i = c \cdot \cos{\theta} \\
                x_i &= \frac{(1-py)\cos{\theta}}{\sin{\theta}} = \frac{1-py}{\tan{\theta}}""",
            font_size=32
        ).move_to(RIGHT*3.5+DOWN*1.75)

        self.play(Write(proof_x, run_time=5))
        self.wait(5)

        # simplify proof
        xi_formula = MathTex(r"x_i = \frac{1-py}{\tan{\theta}}").move_to(RIGHT*3.5+DOWN*1.75)
        self.play(Transform(proof_x, xi_formula))

        self.wait()

        # delete this triangle and formula
        self.play(AnimationGroup(
            Unwrite(proof_x),
            Unwrite(edge_labels_and_angle),
            Uncreate(triangle_x_1_move)
        ))

        # move second triangle
        triangle_x_2_move = triangle_x_2.copy()
        self.play(triangle_x_2_move.animate.move_to(RIGHT*3.5+UP*1.10).scale(3))

        self.wait()
