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

        # play number plane animations
        self.play(Succession(
            Create(number_plane, run_time=3),
            DrawBorderThenFill(blocks),
            Write(labels),
            Write(x_ticks_labels),
            Write(y_ticks_labels)
        ))

        pc_x, pc_y = (1.5, 1.5)

        player_point = Dot(number_plane.c2p(pc_x, pc_y), color=WHITE)
        player_label_1 = MathTex("Player").scale(0.6).next_to(player_point, DOWN, buff=0.05)

        zero_deg_line = DashedLine(number_plane.c2p(pc_x, pc_y), number_plane.c2p(5, pc_y), dash_length=0.15)
        ray = Line(
            number_plane.c2p(pc_x, pc_y), number_plane.c2p(3.5, 4)
        ).add_tip(tip_length=0.2, tip_width=0.2)
        ray_angle = Angle(zero_deg_line, ray)
        ray_angle_label = MathTex(r"\theta").next_to(ray_angle, buff=0.1)
        ray_angle_label.set_y(ray_angle_label.get_y() + 0.2)

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

        p_x_brace = Brace(
            Line(number_plane.c2p(1, 1), number_plane.c2p(1.5, 1)),
            buff=0
        )
        p_x_brace_label = MathTex("p_x").scale(0.5).next_to(p_x_brace, direction=DOWN, buff=0.1)
        p_y_brace = Brace(
            Line(number_plane.c2p(1, 1), number_plane.c2p(1, 1.5)),
            buff=0,
            direction=LEFT
        )
        p_y_brace_label = MathTex("p_y").scale(0.5).next_to(p_y_brace, direction=LEFT, buff=0.1)

        # transform Player to P
        player_label_2 = MathTex("P").scale(0.6).next_to(player_point, DOWN, buff=0.05)
        self.play(Transform(player_label_1, player_label_2))

        # play brace and explanation animations
        group_explain = VGroup(
            MathTex(r"P \, (x+p_x, y+p_y)").move_to(RIGHT*3.5+UP*0.3),
            MathTex(r"\theta - \textrm{ray angle}").move_to(RIGHT*3.5+DOWN*0.3),
        )
        self.play(AnimationGroup(
            Create(p_x_brace),
            Write(p_x_brace_label),
            Create(p_y_brace),
            Write(p_y_brace_label),
            Write(group_explain)
        ))

        self.wait(5)

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
            triangle_x_1_move.animate.move_to(RIGHT*3.5+UP*1.25).scale(4.5),
            Write(title_text)
        ))

        # write labels for each edge of the triangle and draw angle
        vertices = triangle_x_1_move.get_vertices()
        hypotenuse_label = MathTex("c_1")
        center_coordinates = Line(vertices[0], vertices[1]).get_center()
        hypotenuse_label.move_to([center_coordinates[0]-0.3, center_coordinates[1]+0.3, center_coordinates[2]])

        edge_labels_and_angle = VGroup(
            hypotenuse_label,
            MathTex("1-p_y").next_to(Line(vertices[1], vertices[2])),
            MathTex("x_i").next_to(Line(vertices[2], vertices[0]), DOWN),
            Angle(
                Line(vertices[2], vertices[0]),
                Line(vertices[2], vertices[1]),
                elbow=True
            )
        )
        self.play(Write(edge_labels_and_angle))

        # write the proof
        proof = MathTex(
            r"""\sin{\theta} &= \frac{1 - p_y}{c_1} \Rightarrow c_1 = \frac{1-p_y}{\sin{\theta}} \\
                \cos{\theta} &= \frac{x_i}{c_1} \Rightarrow x_i = c_1 \cdot \cos{\theta} \\
                x_i &= \frac{(1-p_y)\cos{\theta}}{\sin{\theta}} = \frac{1-p_y}{\tan{\theta}}""",
            font_size=32
        ).move_to(RIGHT*3.5+DOWN*1.75)

        self.play(Write(proof, run_time=5))
        self.wait(10)

        # simplify proof
        formula = MathTex(r"x_i = \frac{1-p_y}{\tan{\theta}}").move_to(RIGHT*3.5+DOWN*1.75)
        self.play(Transform(proof, formula))

        self.wait(3)

        # delete this triangle and formula
        self.play(AnimationGroup(
            Unwrite(proof),
            Unwrite(edge_labels_and_angle),
            Uncreate(triangle_x_1_move)
        ))

        # move second triangle
        triangle_x_2_move = triangle_x_2.copy()
        self.play(triangle_x_2_move.animate.move_to(RIGHT*3.5+UP*1.25).scale(2))

        self.wait()

        # write labels and angle for this new triangle
        vertices = triangle_x_2_move.get_vertices()
        hypotenuse_label = MathTex("c_2")
        center_coordinates = Line(vertices[0], vertices[1]).get_center()
        hypotenuse_label.move_to([center_coordinates[0]-0.3, center_coordinates[1]+0.3, center_coordinates[2]])

        edge_labels_and_angle = VGroup(
            hypotenuse_label,
            MathTex("1").next_to(Line(vertices[1], vertices[2])),
            MathTex(r"\Delta x").next_to(Line(vertices[2], vertices[0]), DOWN),
            Angle(
                Line(vertices[2], vertices[0]),
                Line(vertices[2], vertices[1]),
                elbow=True
            )
        )
        self.play(Write(edge_labels_and_angle))

        # write proof
        proof = MathTex(
            r"""\sin{\theta} &= \frac{1}{c_2} \Rightarrow c_2 = \frac{1}{\sin{\theta}} \\
                \cos{\theta} &= \frac{\Delta x}{c_2} \Rightarrow \Delta x = c_2 \cdot \cos{\theta} \\
                \Delta x &= \frac{\cos{\theta}}{\sin{\theta}} = \frac{1}{\tan{\theta}}""",
            font_size=32
        ).move_to(RIGHT*3.5+DOWN*1.75)

        self.play(Write(proof, run_time=5))
        self.wait(10)

        # simplify proof
        formula = MathTex(r"\Delta x = \frac{1}{\tan{\theta}}").move_to(RIGHT*3.5+DOWN*1.75)
        self.play(Transform(proof, formula))

        self.wait(3)

        # delete this triangle and formula
        # uncreate triangles on number plane
        self.play(AnimationGroup(
            Unwrite(proof),
            Unwrite(edge_labels_and_angle),
            Uncreate(triangle_x_2_move),

            Uncreate(triangle_x_1),
            Uncreate(triangle_x_2)
        ))

        self.wait()

        # create two new triangles on number plane
        triangle_y_1 = Polygon(
            number_plane.c2p(1.5, 1.5),
            number_plane.c2p(2, 2.125),
            number_plane.c2p(2, 1.5),
            color=GREEN
        )
        triangle_y_2 = Polygon(
            number_plane.c2p(2, 2.125),
            number_plane.c2p(3, 3.375),
            number_plane.c2p(3, 2.125),
            color=BLUE
        )

        self.play(AnimationGroup(
            Transform(
                title_text,
                MathTex(r"\textrm{Vertical intersections}").move_to(title_text)
            ),
            Create(triangle_y_1),
            Create(triangle_y_2)
        ))

        self.wait()

        # move first triangle
        triangle_y_1_move = triangle_y_1.copy()
        self.play(triangle_y_1_move.animate.move_to(RIGHT*3.5+UP*1.25).scale(3.25))

        # write labels for each edge of the triangle and draw angle
        vertices = triangle_y_1_move.get_vertices()
        hypotenuse_label = MathTex("c_3")
        center_coordinates = Line(vertices[0], vertices[1]).get_center()
        hypotenuse_label.move_to([center_coordinates[0]-0.3, center_coordinates[1]+0.3, center_coordinates[2]])

        edge_labels_and_angle = VGroup(
            hypotenuse_label,
            MathTex("y_i").next_to(Line(vertices[1], vertices[2])),
            MathTex("1-p_x").next_to(Line(vertices[2], vertices[0]), DOWN),
            Angle(
                Line(vertices[2], vertices[0]),
                Line(vertices[2], vertices[1]),
                elbow=True
            )
        )
        self.play(Write(edge_labels_and_angle))

        # write the proof
        proof = MathTex(
            r"""\sin{\theta} &= \frac{y_i}{c_3} \Rightarrow y_i = c_3 \cdot \sin{\theta} \\
                \cos{\theta} &= \frac{1-p_x}{c_3} \Rightarrow c_3 = \frac{1-p_x}{\cos{\theta}} \\
                y_i &= \frac{(1-p_x)\sin{\theta}}{\cos{\theta}} = (1-p_x)\tan{\theta}""",
            font_size=32
        ).move_to(RIGHT*3.5+DOWN*1.75)

        self.play(Write(proof, run_time=5))
        self.wait(10)

        # simplify proof
        formula = MathTex(r"y_i = (1-p_x)\tan{\theta}").move_to(RIGHT*3.5+DOWN*1.75)
        self.play(Transform(proof, formula))

        self.wait(3)

        # delete this triangle and formula
        self.play(AnimationGroup(
            Unwrite(proof),
            Unwrite(edge_labels_and_angle),
            Uncreate(triangle_y_1_move)
        ))

        self.wait()

        # move triangle
        triangle_y_2_move = triangle_y_2.copy()
        self.play(triangle_y_2_move.animate.move_to(RIGHT*3.5+UP*1.25).scale(1.75))

        # write labels for each edge of the triangle and draw angle
        vertices = triangle_y_2_move.get_vertices()
        hypotenuse_label = MathTex("c_4")
        center_coordinates = Line(vertices[0], vertices[1]).get_center()
        hypotenuse_label.move_to([center_coordinates[0]-0.3, center_coordinates[1]+0.3, center_coordinates[2]])

        edge_labels_and_angle = VGroup(
            hypotenuse_label,
            MathTex(r"\Delta y").next_to(Line(vertices[1], vertices[2])),
            MathTex("1").next_to(Line(vertices[2], vertices[0]), DOWN),
            Angle(
                Line(vertices[2], vertices[0]),
                Line(vertices[2], vertices[1]),
                elbow=True
            )
        )
        self.play(Write(edge_labels_and_angle))

        # write the proof
        proof = MathTex(
            r"""\sin{\theta} &= \frac{\Delta y}{c_4} \Rightarrow \Delta y = c_4 \cdot \sin{\theta} \\
                \cos{\theta} &= \frac{1}{c_4} \Rightarrow c_4 = \frac{1}{\cos{\theta}} \\
                \Delta y &= \frac{\sin{\theta}}{\cos{\theta}} = \tan{\theta}""",
            font_size=32
        ).move_to(RIGHT*3.5+DOWN*1.75)

        self.play(Write(proof, run_time=5))
        self.wait(10)

        # simplify proof
        formula = MathTex(r"\Delta y = \tan{\theta}").move_to(RIGHT*3.5+DOWN*1.75)
        self.play(Transform(proof, formula))

        self.wait(3)

        # delete this triangle and everything
        self.play(AnimationGroup(
            FadeOut(proof),
            FadeOut(edge_labels_and_angle),
            FadeOut(triangle_y_2_move),
            FadeOut(title_text),
            FadeOut(number_plane),
            FadeOut(blocks),
            FadeOut(ray),
            FadeOut(triangle_y_1),
            FadeOut(triangle_y_2),
            FadeOut(player_point),
            FadeOut(p_x_brace),
            FadeOut(p_y_brace),
            FadeOut(p_x_brace_label),
            FadeOut(p_y_brace_label),
            FadeOut(labels),
            FadeOut(x_ticks_labels),
            FadeOut(y_ticks_labels),
            FadeOut(player_label_1)
        ))

        algorithm_text = MathTex(
            r"""& \textrm{Raycasting algorithm for ray facing } +x \textrm{ and } +y \textrm{:} \\
                & \textrm{1. Cast ray that "sees" horizontal intersections} \\
                & \textrm{1.1. } Ray \, (Player_x + x_i, Player_y + (1 - p_y)) \\
                & \textrm{1.2. Increment } Player_x \textrm{ by } \Delta x \textrm{ and } Player_y \textrm{ by } 1 \textrm{ until hit a wall} \\
                & \textrm{2. Cast ray that "sees" vertical intersections} \\
                & \textrm{2.1. } Ray \, (Player_x + (1-p_x), Player_y + y_i) \\
                & \textrm{2.2. Increment } Player_x \textrm{ by } 1 \textrm{ and } Player_y \textrm{ by } \Delta y \textrm{ until hit a wall} \\
                & \textrm{3. Choose which ray to use} \\
                & \textrm{3.1. Calculate ray lengths} \\
                & \textrm{3.2. Choose the ray that has shorter length} \\""",
            font_size=32
        )
        self.play(Write(algorithm_text, run_time=3))

        self.wait(7)

        self.play(FadeOut(algorithm_text))

        self.wait()
