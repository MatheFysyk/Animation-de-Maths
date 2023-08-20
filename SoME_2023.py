from objects import *
from colormap import rgb2hex
from scipy.ndimage import convolve
from PIL import Image, ImageFilter
from manim.opengl import *
from pyglet.window import key


# List of scenes :

# Introduction                          : h
# OldTheorems                           : h
# MorleysTheorem                        : h
# ConnesProofintro                      : h
# HowToStart                            : h
# ConwayProof                           : h
# ComplexNumbers1                       : h
# ComplexNumbers2                       : h
# ComplexNumbers3                       : h
# EquivalenceProof                      : h
# EquilateralTriangleSymetries          : h
# GroupVideoBy3b1b                      : h
# AlgebraicRelation                     : h
# AffineGroupR                          : h
# AffineGroupC                          : h
# CompositionOfTransformations          : h
# AffineRotations                       : h
# ProofSetup                            : h
# IdentityProof                         : h
# TrisectorsIntersectionsAsFixedPoints  : h
# MorleyTheoremProof                    : h
# Epilog                                : h
# Epilog2                               : h
# Epilog3                               : h
# Credits                               : h



class Introduction(Scene):
    def construct(self):
        group_of_thm_boxes = VGroup(*[TheoremObject(k, rgb_to_hex((0, k * 0.1, 1 - 2 * k * 0.1)), WHITE) for k in range(1, 6)]).add(MathTex(r"\vdots"))

        for k in range(len(group_of_thm_boxes) - 1):
            group_of_thm_boxes[k+1].next_to(group_of_thm_boxes[k], DOWN, buff=0.3)


        group_of_thm_boxes.move_to(ORIGIN).scale(0.9)

        for_specialists_text = Tex("For specialists !", color=RED).scale(2.5).rotate(-PI / 4)
        for_specialists_text.set_stroke(BLACK, width=2)

        list_of_fade_in_anim = [FadeIn(group_of_thm_boxes[k].text, shift=UP) for k in range(len(group_of_thm_boxes) - 1)]
        list_of_fade_in_anim.append(FadeIn(group_of_thm_boxes[-1], shift=UP))

        self.play(
            AnimationGroup(
                *list_of_fade_in_anim,
                run_time=3.5, lag_ratio=0.5
            ),
            AnimationGroup(
                *[DrawBorderThenFill(group_of_thm_boxes[k].rectangle) for k in range(len(group_of_thm_boxes) - 1)],
                run_time=3, lag_ratio=0.5
            )
        )
        
        self.wait(3)
        self.play(FadeIn(for_specialists_text, shift=100*Line(for_specialists_text.get_center(), np.array([0, 0, -1])).get_unit_vector()), run_time=2)
        self.wait(3)
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


class OldTheorems(MovingCameraScene):
    def construct(self):
        screen_1 = Rectangle(height=5.5 * config.frame_height / config.frame_width, width=5.5).set_fill(opacity=0).set_stroke(YELLOW, width=4)
        screen_1_label = Tex(r"old, well-known").next_to(screen_1, DOWN)
        screen_2 = screen_1.copy().next_to(screen_1, RIGHT, buff=1)
        screen_2_label = Tex(r"relatively unknown").next_to(screen_2, DOWN)
        VGroup(screen_1, screen_1_label, screen_2, screen_2_label).move_to(ORIGIN)
        question_marks = Tex("???").scale(2).move_to(screen_2)
        

        square = Polygon(ORIGIN, 3.5 * RIGHT, 3.5 * UR, 3.5 * UP, color=WHITE)
        triangle_1 = Polygon(ORIGIN, 2 * RIGHT, 1.5 * UP).set_fill(BLUE, opacity=1).set_stroke(width=0)
        triangle_2 = triangle_1.copy().rotate(PI / 2, about_point=ORIGIN).shift(3.5 * RIGHT)
        triangle_3 = triangle_2.copy().rotate(PI / 2, about_point=3.5 * RIGHT).shift(3.5 * UP)
        triangle_4 = triangle_3.copy().rotate(PI / 2, about_point=3.5 * UR).shift(3.5 * LEFT)
        c_squarred = MathTex(r"c^2").move_to(square)
        a_squarred = MathTex(r"a^2").move_to(2.75 * UR)
        b_squarred = MathTex(r"b^2").move_to(UR)
        pythagoras_thm = VGroup(square, triangle_1, triangle_2, triangle_3, triangle_4, c_squarred, a_squarred, b_squarred)
        pythagoras_thm.move_to(screen_1).scale(0.75 * screen_1.height / pythagoras_thm.height)
        triangle_1.shift(0.01 * UR)
        triangle_2.shift(0.01 * UL)
        triangle_3.shift(0.01 * DL)
        triangle_4.shift(0.01 * DR)

        square.set_z_index(VGroup(triangle_1, triangle_2, triangle_3, triangle_4).z_index + 1)
        #self.add(screen_1, screen_2, screen_1_label, screen_2_label, question_marks, pythagoras_thm)

        self.play(
            Create(screen_1),
            Create(square),
            AnimationGroup(*[DrawBorderThenFill(triangle) for triangle in VGroup(triangle_1, triangle_2, triangle_3, triangle_4)], lag_ratio=0.5),
            Write(screen_1_label),
            run_time=3
        )
        self.wait()
        self.play(Write(c_squarred))
        self.wait()
        a_length, b_length = triangle_1.get_vertices()[2][1] - triangle_1.get_vertices()[0][1] - 0.01, triangle_1.get_vertices()[1][0] - triangle_1.get_vertices()[0][0] - 0.01 
        c_length = np.sqrt(a_length ** 2 + b_length ** 2)
        c_vec = (b_length * RIGHT + a_length * DOWN) / np.linalg.norm(b_length * RIGHT + a_length * DOWN)

        self.play(
            triangle_1.animate.shift(b_length * UP),
            triangle_3.animate.shift(a_length * LEFT),
            triangle_4.animate.shift(c_length * c_vec),
            FadeOut(c_squarred),
            run_time=2
        )
        self.wait()
        self.play(
            Write(a_squarred),
            Write(b_squarred)
        )
        self.wait()
        self.play(
            Create(screen_2),
            Write(screen_2_label),
            Write(question_marks),
            run_time=3
        )
        self.wait()
        self.play(
            self.camera.frame.animate.move_to(screen_2).scale((screen_2.height - 0.05) / config.frame_height),
            FadeOut(question_marks),
            run_time=2
        )
        self.wait()


class MorleysTheorem(Scene):
    def construct(self):
        z_1, z_2, z_3 = ComplexValueTracker(complex(0, 3)), ComplexValueTracker(complex(-1, -3)), ComplexValueTracker(complex(3, -3))
        morley_triangle = always_redraw(lambda: MorleyTriangle([z_1.get_value(), z_2.get_value(), z_3.get_value()]))
        
        self.wait()
        self.play(
            AnimationGroup(*[Create(VGroup(side, dot)) for side, dot in zip(morley_triangle.outer_lines, morley_triangle.outer_dots)], lag_ratio=0.4, run_time=3),
            AnimationGroup(*[Write(label) for label in morley_triangle.outer_labels], lag_ratio=0.4, run_time=3)
        )
        self.wait()
        self.play(
            *[Create(angle) for angle in morley_triangle.outer_angle],
            *[Write(label) for label in morley_triangle.outer_angle_labels],
            run_time=2
        )
        self.wait()
        self.play(
            *[Create(trisector[0]) for trisector in morley_triangle.trisectors],
            *[Create(trisector[1]) for trisector in morley_triangle.trisectors],
            run_time=2
        )
        self.play(*[Create(morley_triangle.inner_lines)], run_time=2)
        self.play(FadeIn(morley_triangle.inner_dots), *[Write(morley_triangle.inner_labels)], run_time=1.5)
        self.wait(2)
        self.add(morley_triangle)
        self.remove(morley_triangle.outer_angle, morley_triangle.outer_angle_labels, morley_triangle.outer_dots, morley_triangle.outer_lines, morley_triangle.outer_labels, morley_triangle.inner_dots, morley_triangle.inner_lines, morley_triangle.inner_labels)
        self.play(z_1.animate.set_value(complex(2, 3)), run_time=2)
        self.wait()
        self.play(z_1.animate.set_value(complex(3, 1)), z_2.animate.set_value(complex(-3, 1)), z_3.animate.set_value(complex(0, -2)), run_time=2)
        self.wait()
        self.play(z_3.animate.set_value(complex(-2, -2)), run_time=2)
        self.play(z_3.animate.set_value(complex(2, -2)), run_time=2)
        self.wait(3)
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


class ConnesProofIntro(Scene):
    def construct(self):
        morley_svg = SVGMobject("Frank_Morley.svg").scale(3)
        morley_border = SurroundingRectangle(morley_svg, buff=0)
        morley_label = Tex(r"Frank \textsc{Morley}").next_to(morley_svg, DOWN)
        
        connes_svg = SVGMobject("Alain_Connes.svg").scale(3)
        connes_border = SurroundingRectangle(connes_svg, buff=0)
        connes_label = Tex(r"Alain \textsc{Connes}").next_to(connes_svg, DOWN)

        morley = Group(morley_svg, morley_border, morley_label)
        connes = Group(connes_svg, connes_border, connes_label).next_to(morley, RIGHT, buff=0.5)

        Group(morley, connes).move_to(ORIGIN)

        self.wait()
        self.play(
            AnimationGroup(*[FadeIn(morley_part) for morley_part in morley_svg], run_time=5, lag_ratio=0.3),
            AnimationGroup(*[FadeIn(connes_part) for connes_part in connes_svg], run_time=5, lag_ratio=0.3),
            Create(morley_border), Create(connes_border), Write(morley_label), Write(connes_label), run_time=5
        )
        self.wait(10)
        self.play(FadeIn(CoveringRectangle()))


class HowToStart(Scene):
    def construct(self):
        tex_1 = Tex(
            r"Groups \\ Complex numbers \\ Symetries \\ Linear maps",
            tex_environment="flushleft" 
        ).scale(2)
        tex_2 = Tex("How to start ?").scale(3)

        mt = MorleyTriangle(vertices=[complex(3, 3), complex(-2, 1), complex(0, -3)]).scale(0.5)
        general_framework = Rectangle(color=RED).scale(1.25).next_to(mt, RIGHT, buff=3)
        general_framework_label = Tex("Field and group theory", color=RED).next_to(general_framework, UP)
        VGroup(mt, general_framework, general_framework_label).move_to(ORIGIN)
        arrow = Arrow(
            mt.get_center() + 1.25 * mt.width / 2 * RIGHT,
            general_framework.get_center() + 1.25 * general_framework.width / 2 * LEFT,
            color=YELLOW        
        )
        arrow_label = Tex(r"Alain \textsc{Connes}' \\ proof").scale(0.65).next_to(arrow, UP)

        self.wait()
        self.play(Write(tex_1), run_time=5)
        self.wait()
        self.play(FadeOut(tex_1))
        self.wait(2)
        self.play(Write(tex_2), run_time=2)
        self.wait(3)
        self.play(ReplacementTransform(tex_2, mt))
        self.wait()
        self.play(
            AnimationGroup(
                AnimationGroup(
                    GrowArrow(arrow), Write(arrow_label), lag_ratio=0
                ),
                AnimationGroup(
                    Create(general_framework), Write(general_framework_label), lag_ratio=0
                ), lag_ratio=0.5
            ), run_time=3
        )
        self.play(
            ReplacementTransform(mt.copy(), Tex(r"Generalized \textsc{Morley}' \\ theorem").move_to(general_framework).scale(0.9)),
            run_time=1.5
        )
        self.wait(2)
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


class ConwayProof(Scene):
    def construct(self):
        svg = SVGMobject("Conway_proof.svg").scale(2.55)
        channel_name = Tex("video by Exponentielle Hippie").scale(0.9).next_to(svg, DOWN, buff=0.5)
        border = SurroundingRectangle(svg, buff=0)

        Group(svg, channel_name, border).move_to(ORIGIN)

        triangle_shape = Triangle().scale(2).rotate(PI / 4)
        vertices = triangle_shape.get_vertices()
        angles = VGroup(
            Angle(Line(vertices[0], vertices[1]), Line(vertices[0], vertices[2])),
            Angle(Line(vertices[1], vertices[2]), Line(vertices[1], vertices[0])),
            Angle(Line(vertices[2], vertices[0]), Line(vertices[2], vertices[1]))
        )
        triangle = VGroup(triangle_shape, angles)

        equivalent_sign = MathTex(r"\iff").scale(3).next_to(triangle, RIGHT, buff=0.5)
        dots = MathTex(r"\hdots").scale(3).next_to(equivalent_sign, RIGHT, buff=0.5)

        VGroup(triangle, equivalent_sign, dots).move_to(ORIGIN)

        self.wait()
        self.play(FadeIn(svg), Create(border), Write(channel_name), run_time=2)
        self.wait(4)
        self.play(FadeOut(*[part for part in svg], border), Unwrite(channel_name))
        self.wait(4)
        self.play(
            AnimationGroup(Create(triangle), Write(equivalent_sign), Write(dots), lag_ratio=0.4, run_time=3)
        )
        #self.add(triangle, equivalent_sign, dots) 
        self.wait(2)
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


class ComplexNumbers1(ZoomedScene):
    def construct(self):
        plane = ComplexPlane(background_line_style={"stroke_opacity": 0.5}).add_coordinates()

        triangle = Triangle()
        triangle.match_height(Line(plane.c2p(0, 0), plane.c2p(0, 1.5))).move_to(plane.c2p(0, 0)).shift(1 / 4 * plane.c2p(1, 0)).rotate(-PI / 2)

        labels = VGroup(
            MathTex("a").rotate(-PI / 12).move_to(triangle.get_vertices()[0] + 0.3 * RIGHT),
            MathTex("b").rotate(-PI / 12).move_to(triangle.get_vertices()[1] + 0.3 * np.array([-1/2, np.sqrt(3)/2, 0])),
            MathTex("c").rotate(-PI / 12).move_to(triangle.get_vertices()[2] + 0.3 * np.array([-1/2, -np.sqrt(3)/2, 0]))
        )
        VGroup(triangle, labels).rotate(PI / 12).scale(1.4).shift(2.2 * UP + 3 * RIGHT)

        j = Dot(plane.c2p(-1/2, np.sqrt(3)/2), color=YELLOW).set_z_index(plane.z_index + 4)
        j_label = MathTex(r"j = -\frac{1}{2} + i\frac{\sqrt{3}}{2}", color=BLUE).scale(0.75).next_to(j, UL, buff=MED_SMALL_BUFF).shift(0.25 * DOWN)
        j_label_bis = MathTex(r"= ", r"e^{\frac{2i\pi}{3}}", color=BLUE).scale(0.75)
        j_label_bis[0].next_to(j_label[0][1], DOWN, buff=0.75)
        j_label_bis[1].next_to(j_label_bis[0], RIGHT).shift(0.1 * UP)
        j_label_background = BackgroundRectangle(j_label, buff=SMALL_BUFF).set_z_index(plane.z_index + 2)
        j_label_background_bis = BackgroundRectangle(VGroup(j_label, j_label_bis), buff=SMALL_BUFF).set_z_index(plane.z_index + 2)
        VGroup(j_label, j_label_bis).set_z_index(j_label_background.z_index + 1)
        dashed_lines = VGroup(
            DashedLine(start=plane.c2p(-1/2, 0), end=plane.c2p(-1/2, np.sqrt(3)/2), color=BLUE),
            DashedLine(start=plane.c2p(0, np.sqrt(3)/2), end=plane.c2p(-1/2, np.sqrt(3)/2), color=BLUE)
        )
        j.set_z_index(plane.z_index + 3)

        equation = MathTex("a + bj + cj^2 = 0")
        equation_background = BackgroundRectangle(equation, fill_opacity=0.75, buff=SMALL_BUFF)
        equation.set_z_index(equation_background.z_index + 1)
        VGroup(equation, equation_background).move_to(plane.c2p(-3.5, -2)).scale(1.5)

        link_arrow = CurvedDoubleArrow(equation.get_center() + 3.25 * RIGHT, triangle.get_center() + 1.5 * DOWN, color=YELLOW)
        link_text = Tex(r"geometry -- algebra \\ link").next_to(link_arrow.point_from_proportion(0.5), DR)
        link_text_background = BackgroundRectangle(link_text, fill_opacity=0.75, buff=SMALL_BUFF)
        link_text.set_z_index(link_text_background.z_index + 1)

        #self.add(plane, triangle, labels, j, j_label, j_label_background, dashed_lines, equation, equation_background, link_arrow, link_text, link_text_background)
        self.wait()
        self.play(FadeIn(plane))
        self.wait(2)
        self.play(AnimationGroup(Create(triangle), AnimationGroup(*[Write(label) for label in labels], lag_ratio=0), lag_ratio=0.3, run_time=3))
        self.wait(2)
        self.play(AnimationGroup(*[Wiggle(label, scale_value=1.25, rotation_angle=0.02 * TAU) for label in labels], lag_ratio=0.5, run_time=4))
        self.wait(2)
        self.play(Write(equation), FadeIn(equation_background), run_time=2)
        self.wait(2)
        self.play(FadeIn(j), Write(j_label), FadeIn(j_label_background), Create(dashed_lines), run_time=2)
        self.wait(5)
        self.play(Create(link_arrow), run_time=2)
        self.play(Write(link_text), FadeIn(link_text_background), run_time=2)
        self.wait(2)
        self.play(FadeOut(triangle, *labels, equation, equation_background, link_arrow, link_text, link_text_background))
        self.wait(6)

        self.play(self.camera.frame.animate.scale(.5).shift(0.4 * UP))
        self.wait(2)
        self.play(
            Wiggle(dashed_lines[0], scale_value=1.25, rotation_angle=0.02 * TAU),
            Wiggle(dashed_lines[1], scale_value=1.25, rotation_angle=0.02 * TAU)
        )
        
        theta = ValueTracker(0.01)
        exponential_form = always_redraw(lambda: Dot(plane.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())), color=YELLOW).set_z_index(plane.z_index + 4))
        
        module_line = always_redraw(lambda: Line(plane.c2p(0, 0), plane.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())), color=BLUE).set_z_index(plane.z_index + 3))
        module_line_label = MathTex("|j|", color=BLUE).scale(0.6).add_updater(
            lambda label: label.move_to(
                plane.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())) / 2 + 0.25 * np.array([-np.sin(theta.get_value()), np.cos(theta.get_value()), 0.])
            ), call_updater=True
        )
        module_line_label_background = BackgroundRectangle(module_line_label, fill_opacity=0.75)
        module_line_label.set_z_index(module_line_label_background.z_index + 1)
        module_line_label_background.add_updater(
            lambda rect: rect.move_to(
                plane.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())) / 2 + 0.25 * np.array([-np.sin(theta.get_value()), np.cos(theta.get_value()), 0.])
            )
        )

        argument_angle = always_redraw(
            lambda: Angle(
                Line(plane.c2p(0, 0), plane.c2p(1, 0)),
                Line(plane.c2p(0, 0), plane.c2p(np.cos(theta.get_value()), np.sin(theta.get_value()))),
                color=YELLOW
            ).set_z_index(plane.z_index + 2) if theta.get_value() != 0 else Line().scale(0)
        )
        argument_angle_label = MathTex(r"\mathrm{arg}(j)", color=YELLOW).add_updater(
            lambda label: label.move_to(
                Angle(
                    Line(plane.c2p(0, 0), plane.c2p(1, 0)),
                    Line(plane.c2p(0, 0), plane.c2p(np.cos(theta.get_value()), np.sin(theta.get_value()))),
                    radius=0.4 + 0.25
                ).point_from_proportion(0.5)
            ).scale_to_fit_height(0.2 * 3 / (2 * PI) * theta.get_value()).set_z_index(plane.z_index + 3),
            call_updater=True
        )

        argument_angle_label_background = BackgroundRectangle(MathTex("arg(j)"), fill_opacity=0.75)
        argument_angle_label.set_z_index(argument_angle_label_background.z_index + 1)
        argument_angle_label_background.add_updater(
            lambda rect: rect.move_to(
                Angle(
                    Line(plane.c2p(0, 0), plane.c2p(1, 0)),
                    Line(plane.c2p(0, 0), plane.c2p(np.cos(theta.get_value()), np.sin(theta.get_value()))),
                    radius=0.4 + 0.25
                ).point_from_proportion(0.5)
            ).scale_to_fit_height(0.3 * 3 / (2 * PI) * theta.get_value()).set_z_index(plane.z_index + 2),
            call_updater=True
        )

        self.play(Create(module_line), FadeIn(exponential_form, shift=RIGHT), Write(module_line_label), FadeIn(module_line_label_background), run_time=2)
        self.wait()
        self.play(Wiggle(module_line, scale_value=1.25, rotation_angle=0.02 * TAU))
        self.wait()
        self.add(argument_angle, argument_angle_label)#, argument_angle_label_background)
        self.play(theta.animate.set_value(2 * PI / 3), run_time=2)
        self.wait()
        self.play(Wiggle(argument_angle, scale_value=1.25, rotation_angle=0.02 * TAU))
        self.wait()
        self.play(Write(j_label_bis), Transform(j_label_background, j_label_background_bis), run_time=1.5)
        self.wait(5)

        plane_copy = plane.copy().set_z_index(plane.z_index + 1)
        plane_copy.remove(plane_copy.coordinate_labels)

        self.play(Rotate(plane_copy, 2 * PI / 3, about_point=plane.c2p(0, 0)), plane.animate.set_opacity(0.5), run_time=2)
        self.wait()
        self.play(FadeIn(CoveringRectangle()))
        self.wait()

        
class ComplexNumbers2(Scene):
    def construct(self):
        tex_env = TexTemplate().add_to_preamble(r"\usepackage{mathrsfs}")

        rightarrow_tex = MathTex(r"\longrightarrow")
        C_tex = MathTex(r"\mathbb{C}").next_to(rightarrow_tex, LEFT, buff=MED_LARGE_BUFF)
        direct_similitudes = MathTex(r"\mathscr{S}_{+}(\mathbb{C})", tex_template=tex_env).next_to(rightarrow_tex, RIGHT, buff=MED_LARGE_BUFF)
        tex_group = VGroup(rightarrow_tex, C_tex, direct_similitudes).scale(2)

        C_plane_left = NumberPlane(x_range=[-6.01, 6.01], y_range=[-4.01, 4.01]).scale(0.45).move_to(config.frame_width/4 * LEFT)
        C_plane_right = C_plane_left.copy().move_to(config.frame_width/4 * RIGHT)
        mapsto_tex_planes = MathTex(r"\longmapsto")
        tex_group.set_z_index(C_plane_left.z_index + 1)

        mapsto_tex = MathTex(r"\longmapsto").to_edge(DOWN, buff=0.75)
        z_tex = MathTex(r"z", color=YELLOW).next_to(C_plane_left, DOWN).to_edge(DOWN, buff=0.75)
        z_exp_tex = MathTex(r"|z|", r"e^{i\mathrm{arg}(z)}").move_to(z_tex).shift(0.1 * UP)
        z_exp_tex_bis = MathTex(r"r", r"e^{i\theta}").move_to(z_tex).shift(0.145 * UP + 0.3 * LEFT)
        z_exp_tex_bis[1][0:2].move_to(z_exp_tex[1][0:2])
        VGroup(z_exp_tex[0], z_exp_tex_bis[0]).set_color(BLUE)
        VGroup(z_exp_tex[1][2:], z_exp_tex_bis[1][2]).set_color(RED)
        z_exp_tex_bis_target = z_exp_tex_bis.copy()

        double_arrow_tex = MathTex(r"\leftrightarrow").next_to(z_exp_tex_bis_target, RIGHT)
        matrix_tex = MathTex(r"r\begin{pmatrix} \cos{(\theta)} & -\sin{(\theta)} \\ \sin{(\theta)} & \cos{(\theta)} \end{pmatrix}").scale(0.75)
        matrix_tex[0][0].set_color(BLUE).scale(1 / 0.75)
        VGroup(matrix_tex[0][6], matrix_tex[0][13], matrix_tex[0][19], matrix_tex[0][25]).set_color(RED)
        matrix_tex.next_to(double_arrow_tex, RIGHT)
        VGroup(z_exp_tex_bis_target, double_arrow_tex, matrix_tex).move_to(z_tex).to_edge(DOWN)
        z_exp_tex_bis_target.shift(0.1 * UP)
        re_it_copy = z_exp_tex_bis.copy()

        func_tex = MathTex(r"f_z : w \mapsto ", r"z", r"w").next_to(C_plane_right, DOWN).to_edge(DOWN, buff=0.75)
        func_tex_exp = MathTex(r"f_z : w \mapsto ", r"re^{i\theta}", r"w")
        VGroup(func_tex[0][1], func_tex[1], func_tex_exp[0][1]).set_color(YELLOW)
        func_tex_exp[1][0].set_color(BLUE)
        func_tex_exp[1][3].set_color(RED)
        func_tex_exp[0].move_to(func_tex[0])
        func_tex_exp[1].next_to(func_tex_exp[0], RIGHT)
        func_tex_exp[2].next_to(func_tex_exp[1], RIGHT, buff=SMALL_BUFF)   
        func_tex_exp[1].shift(0.1 * UP)     

        label_f_1 = MathTex("z = f_z(1)").scale(0.75).next_to(C_plane_right.c2p(1, 1), UR).set_z_index(C_plane_left.z_index + 2)
        label_f_1[0][0:4:3].set_color(YELLOW)
        label_f_1_rect = BackgroundRectangle(label_f_1, buff=SMALL_BUFF).set_z_index(label_f_1.z_index - 1)

        rectangle = SurroundingRectangle(C_plane_right, buff=0).stretch(0.863, 0)
        background = Difference(
            Rectangle(height=config.frame_height, width=config.frame_width), rectangle
        ).set_fill(BLACK, opacity=1).set_stroke(width=0).set_z_index(-1)

        z_1 = Dot(C_plane_left.c2p(1, 1), color=YELLOW)
        z_2 = Dot(C_plane_left.c2p(-0.5, 2), color=YELLOW)
        z_3 = Dot(C_plane_left.c2p(-2, -3), color=YELLOW)
        z_group = VGroup(z_1, z_2, z_3)
        z_1_copy = z_1.copy().set_z_index(C_plane_right.z_index + 2)
        z_2_copy = z_2.copy().set_z_index(C_plane_right.z_index + 2)
        z_3_copy = z_3.copy().set_z_index(C_plane_right.z_index + 2)

        plane_copy_group = []

        for z in z_group:
            plane = NumberPlane(x_range=[-10.01, 10.01], y_range=[-10.01, 10.01]).scale(0.45).move_to(config.frame_width/4 * RIGHT).set_z_index(background.z_index - 1)
            pos = C_plane_left.p2c(z.get_center())
            matrix = np.array([[pos[0], -pos[1]], [pos[1], pos[0]]])
            plane_copy_group.append((plane, matrix))
            if z == z_3:
                plane_copy_group.append((plane.copy(), np.sqrt(pos[0] ** 2 + pos[1] ** 2) * np.eye(2)))

        self.add(background)
        self.play(Write(tex_group), run_time=3)
        self.wait(5)
        self.play(
            C_tex.animate.scale(0.5).next_to(C_plane_left, DOWN).to_edge(UP, buff=0.75),
            rightarrow_tex.animate.scale(0.5).move_to(ORIGIN).to_edge(UP, buff=0.75),
            direct_similitudes.animate.scale(0.5).next_to(C_plane_right, UP).to_edge(UP, buff=0.75),
            Create(C_plane_left), Create(z_1), run_time=3
        )
        self.play(ReplacementTransform(z_1.copy(), z_tex))
        self.wait()
        self.play(Write(mapsto_tex_planes), Write(mapsto_tex))
        self.wait()
        self.play(z_1_copy.animate.move_to(C_plane_right.c2p(1, 0)), ReplacementTransform(C_plane_left.copy().set_z_index(z_1.z_index - 1), C_plane_right), run_time=2)
        
        z_1_copy.add_updater(lambda point: point.move_to(plane_copy_group[0][0].c2p(1, 0)))
        
        self.add(plane_copy_group[0][0])
        self.wait()
        self.play(
            C_plane_right.animate.set_opacity(0.25).set_z_index(background.z_index - 2),
            ApplyMatrix(plane_copy_group[0][1], plane_copy_group[0][0], about_point=C_plane_right.c2p(0, 0))
        )
        self.wait()
        self.play(ReplacementTransform(VGroup(C_plane_right.copy(), z_1_copy.copy()), func_tex), run_time=2)
        self.wait(2)        
        self.play(FadeIn(label_f_1_rect), Write(label_f_1), run_time=2)
        self.wait(4)
        self.play(FadeOut(z_1_copy, label_f_1, label_f_1_rect), plane_copy_group[0][0].animate.set_opacity(0), ReplacementTransform(z_1, z_2))
        self.wait(0.5)
        self.play(z_2_copy.animate.move_to(C_plane_right.c2p(1, 0)), FadeIn(plane_copy_group[1][0]))
        self.wait()
        
        z_2_copy.add_updater(lambda point: point.move_to(plane_copy_group[1][0].c2p(1, 0)))
        
        self.play(
            ApplyMatrix(plane_copy_group[1][1], plane_copy_group[1][0], about_point=C_plane_right.c2p(0, 0))
        )
        self.wait()
        self.play(FadeOut(z_2_copy), plane_copy_group[1][0].animate.set_opacity(0), ReplacementTransform(z_2, z_3))
        self.wait(0.5)
        self.play(z_3_copy.animate.move_to(C_plane_right.c2p(1, 0)), FadeIn(plane_copy_group[2][0]))
        self.wait()
        
        z_3_copy.add_updater(lambda point: point.move_to(plane_copy_group[2][0].c2p(1, 0)))
        
        self.play(
            ApplyMatrix(plane_copy_group[2][1], plane_copy_group[2][0], about_point=C_plane_right.c2p(0, 0))
        )
        self.wait()

        z_3_copy.clear_updaters()

        self.play(
            plane_copy_group[2][0].animate.set_opacity(0),
            FadeIn(plane_copy_group[3][0]),
            z_3_copy.animate.move_to(plane_copy_group[3][0].c2p(1, 0)),
            run_time=1.5
        )
        self.wait()
        
        z_3_copy.add_updater(lambda point: point.move_to(plane_copy_group[3][0].c2p(1, 0)))

        self.wait()
        self.play(ReplacementTransform(z_tex, z_exp_tex))
        self.wait(2)
        self.play(ReplacementTransform(z_exp_tex[0], z_exp_tex_bis[0]))
        self.wait()
        self.play(ReplacementTransform(z_exp_tex[1][2:], z_exp_tex_bis[1][2:]))
        self.remove(*z_exp_tex[1])
        self.add(z_exp_tex_bis[1])
        self.play(*[ReplacementTransform(part, part_exp) for part, part_exp in zip(func_tex, func_tex_exp)], re_it_copy.animate.move_to(func_tex_exp[1]))
        self.remove(re_it_copy)
        self.wait(3)
        self.play(FocusOn(func_tex_exp, opacity=0.4))
        self.play(Wiggle(func_tex_exp[1][1:], scale_value=1.5, rotation_angle=0.03 * TAU), run_time=2)
        self.wait()
        self.play(
            Rotate(plane_copy_group[3][0], np.arctan(3 / 2) + PI),
            run_time=2
        )
        self.wait()
        self.play(Wiggle(func_tex_exp[1][0], scale_value=1.5, rotation_angle=0.03 * TAU), run_time=2)
        self.wait()
        
        self.play(
            ApplyMatrix(plane_copy_group[3][1], plane_copy_group[3][0], about_point=C_plane_right.c2p(0, 0)),
            run_time=2
        )
        self.wait(5)
        
        self.play(
            ReplacementTransform(z_exp_tex_bis, z_exp_tex_bis_target),
            Write(VGroup(double_arrow_tex, matrix_tex)),
            run_time=3
        )
        self.wait(5)
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


class ComplexNumbers3(ZoomedScene):
    def construct(self):
        plane = ComplexPlane(y_range=[-6, 6], background_line_style={"stroke_opacity": 0.5}).add_coordinates()
        self.camera.frame.shift(UP)

        arg_j_jp1_tex = MathTex(r"\mathrm{arg}(j) &= ", r"\frac{2\pi}{3}", r"\\ \mathrm{arg}(1 + j) &=", r"\frac{\pi}{3}").shift(4 * LEFT + 0.5 * DOWN)
        arg_j_jp1_tex[0][4].set_color(BLUE)
        arg_j_jp1_tex[2][4:7].set_color(GREEN)
        arg_j_jp1_tex_rectangle = BackgroundRectangle(arg_j_jp1_tex, buff=MED_SMALL_BUFF)
        arg_j_jp1_tex.set_z_index(arg_j_jp1_tex_rectangle.z_index + 1)

        j = Dot(plane.c2p(-1/2, np.sqrt(3)/2), color=BLUE)
        j_label = MathTex(r"j", color=BLUE).scale(0.8).next_to(j, j.get_center() / np.linalg.norm(j.get_center()), buff=MED_SMALL_BUFF)
        j_label_rectangle = BackgroundRectangle(j_label, fill_opacity=0.5, buff=SMALL_BUFF).set_z_index(plane.z_index + 1)
        VGroup(j_label, j).set_z_index(j_label_rectangle.z_index + 1)

        jp1 = Dot(plane.c2p(1/2, np.sqrt(3)/2), color=GREEN)
        jp1_label = MathTex(r"j + 1", color=GREEN).scale(0.8).next_to(jp1, 2 * jp1.get_center() / np.linalg.norm(jp1.get_center()), buff=MED_SMALL_BUFF).shift(0.25 * DOWN)
        jp1_label_rectangle = BackgroundRectangle(jp1_label, fill_opacity=0.5, buff=SMALL_BUFF).set_z_index(plane.z_index + 1)
        VGroup(jp1_label, jp1).set_z_index(jp1_label_rectangle.z_index + 1)

        z = Dot(plane.n2p(3 + 1j), color=YELLOW)
        z_label = MathTex("z", color=YELLOW).next_to(z, z.get_center() / np.linalg.norm(z.get_center()), buff=MED_SMALL_BUFF)
        z_label_rectangle = BackgroundRectangle(z_label, fill_opacity=0.5, buff=SMALL_BUFF).set_z_index(plane.z_index + 1)
        z_label.set_z_index(z_label_rectangle.z_index + 1)

        jz = Dot(plane.n2p(complex(-1 / 2, np.sqrt(3) / 2) * (3 + 1j)), color=YELLOW)
        jz_label = MathTex("jz", color=YELLOW).next_to(jz, jz.get_center() / np.linalg.norm(jz.get_center()), buff=MED_SMALL_BUFF).set_z_index(z_label.z_index)
        jz_label[0][0].set_color(BLUE)
        jz_label_rectangle = BackgroundRectangle(jz_label, fill_opacity=0.5, buff=SMALL_BUFF).set_z_index(plane.z_index + 1)

        jp1z = Dot(plane.n2p(complex(1 / 2, np.sqrt(3) / 2) * (3 + 1j)), color=YELLOW)
        jp1z_label = MathTex("(1 + j)z", color=YELLOW).next_to(jp1z, 2 * jp1z.get_center() / np.linalg.norm(jp1z.get_center()), buff=MED_SMALL_BUFF).set_z_index(z_label.z_index)
        jp1z_label[0][0:5].set_color(GREEN)
        jp1z_label_rectangle = BackgroundRectangle(jp1z_label, fill_opacity=0.5, buff=SMALL_BUFF).set_z_index(plane.z_index + 1)

        z_copy = z.copy()
        z_label_copy = z_label.copy()
        z_label_rectangle_copy = z_label_rectangle.copy()
        z_copy_bis = z.copy()
        z_label_copy_bis = z_label.copy()
        z_label_rectangle_copy_bis = z_label_rectangle.copy()

        line = Line(plane.c2p(0, 0), z_copy.get_center())
        line_bis = always_redraw(lambda: Line(plane.c2p(0, 0), z_copy.get_center()))
        line_tiers = always_redraw(lambda: Line(plane.c2p(0, 0), z_copy_bis.get_center()))

        fixed_line_j = Line(plane.c2p(0, 0), jz.get_center())
        fixed_line_jp1 = Line(plane.c2p(0, 0), jp1z.get_center())

        angle_j = Angle(line, fixed_line_j, radius=0.5, color=BLUE).set_z_index(arg_j_jp1_tex_rectangle.z_index + 1)
        angle_jp1 = Angle(line, fixed_line_jp1, radius = 0.5, color=GREEN).set_z_index(arg_j_jp1_tex_rectangle.z_index + 1)

        self.play(FadeIn(plane, j_label_rectangle, j_label), Create(j))
        self.wait()
        self.play(Create(line), Create(z), Write(z_label), FadeIn(z_label_rectangle))
        self.add(line_bis)
        self.wait()
        self.play(
            ReplacementTransform(z_copy, jz, path_arc=2 * PI / 3),
            ReplacementTransform(z_label_copy, jz_label, path_arc=2 * PI / 3),
            ReplacementTransform(z_label_rectangle_copy, jz_label_rectangle, path_arc=2 * PI / 3),
            Create(angle_j),
            run_time=3
        )
        self.add(line_tiers)
        self.wait()
        self.play(Write(arg_j_jp1_tex[0]), FadeIn(arg_j_jp1_tex_rectangle))
        self.play(ReplacementTransform(angle_j, arg_j_jp1_tex[1]))
        self.wait(4)
        self.play(
            ReplacementTransform(j.copy(), jp1),
            ReplacementTransform(j_label.copy(), jp1_label),
            ReplacementTransform(j_label_rectangle.copy(), jp1_label_rectangle)
        )
        self.wait()
        self.play(
            ReplacementTransform(z_copy_bis, jp1z, path_arc=PI / 3),
            ReplacementTransform(z_label_copy_bis, jp1z_label, path_arc=PI / 3),
            ReplacementTransform(z_label_rectangle_copy_bis, jp1z_label_rectangle, path_arc=PI / 3),
            Create(angle_jp1),
            run_time=3
        )
        self.wait()
        self.play(Write(arg_j_jp1_tex[2]))
        self.play(ReplacementTransform(angle_jp1, arg_j_jp1_tex[3]))
        self.wait(2)

        rectangle = CoveringRectangle()
        ending_plane = plane.copy().set_z_index(rectangle.z_index + 1)
        self.play(FadeIn(rectangle, ending_plane))
        self.wait()
        

class EquivalenceProof(ZoomedScene):
    def construct(self):
        plane = ComplexPlane(x_range=[-10, 10], y_range=[-6, 6], background_line_style={"stroke_opacity": 0.5}).add_coordinates()
        self.camera.frame.shift(UP)
        triangle = Triangle(color=RED)
        triangle.match_height(Line(plane.c2p(0, 0), plane.c2p(0, 1.5))).move_to(plane.c2p(0, 0)).shift(1 / 4 * plane.c2p(1, 0)).rotate(-PI / 2)

        labels = VGroup(
            MathTex("a").scale(1 / 1.4).rotate(-PI / 12).move_to(triangle.get_vertices()[0] + 0.4 * RIGHT),
            MathTex("b").scale(1 / 1.4).rotate(-PI / 12).move_to(triangle.get_vertices()[1] + 0.4 * np.array([-1/2, np.sqrt(3)/2, 0])),
            MathTex("c").scale(1 / 1.4).rotate(-PI / 12).move_to(triangle.get_vertices()[2] + 0.4 * np.array([-1/2, -np.sqrt(3)/2, 0]))
        )
        
        label_rectangles = VGroup(
            BackgroundRectangle(labels[0].copy().rotate(PI / 12), fill_opacity=0.5, buff=SMALL_BUFF).rotate(-PI / 12),
            BackgroundRectangle(labels[1].copy().rotate(PI / 12), fill_opacity=0.5, buff=SMALL_BUFF).rotate(-PI / 12),
            BackgroundRectangle(labels[2].copy().rotate(PI / 12), fill_opacity=0.5, buff=SMALL_BUFF).rotate(-PI / 12)
        )
        labels.set_z_index(label_rectangles.z_index + 1)

        centered_triangle = triangle.copy()
        centered_labels = VGroup(
            MathTex("a - c").rotate(-PI / 12).scale(1 / 1.4).move_to(triangle.get_vertices()[0] + 0.6 * RIGHT),
            MathTex("b - c").rotate(-PI / 12).scale(1 / 1.4).move_to(triangle.get_vertices()[1] + 0.4 * np.array([-1/2, np.sqrt(3)/2, 0])),
            MathTex("0").rotate(-PI / 12).scale(1 / 1.4).move_to(triangle.get_vertices()[2] + 0.3 * np.array([-1/2, -np.sqrt(3)/2, 0]))
        )
        centered_label_rectangles = VGroup(
            BackgroundRectangle(centered_labels[0].copy().rotate(PI / 12), fill_opacity=0.5, buff=SMALL_BUFF).rotate(-PI / 12),
            BackgroundRectangle(centered_labels[1].copy().rotate(PI / 12), fill_opacity=0.5, buff=SMALL_BUFF).rotate(-PI / 12),
            BackgroundRectangle(centered_labels[2].copy().rotate(PI / 12), fill_opacity=0.5, buff=SMALL_BUFF).rotate(-PI / 12)
        )
        centered_labels.set_z_index(centered_label_rectangles.z_index + 1)

        VGroup(triangle, labels, label_rectangles, centered_triangle, centered_labels, centered_label_rectangles).rotate(PI / 12).scale(1.4).shift(2.2 * UP + 3 * RIGHT)
        VGroup(centered_triangle, centered_labels, centered_label_rectangles).shift(-triangle.get_vertices()[2] + 0.01 * UP + 0.007 * RIGHT)
        
        conditions_tex = MathTex(r"\alpha &= ", r" \frac{\pi}{3}", r"\\|a-c| ", r" &= ", r" |b-c|").move_to(plane.c2p(0, 2.5)).to_edge(buff=0.75)
        conditions_tex_rectangle = BackgroundRectangle(conditions_tex, buff=MED_SMALL_BUFF)
        conditions_tex.set_z_index(conditions_tex_rectangle.z_index + 1)
        
        angle = Angle(Line(plane.c2p(0, 0), centered_triangle.get_vertices()[0]), Line(plane.c2p(0, 0), centered_triangle.get_vertices()[1]), radius=0.5).set_z_index(conditions_tex_rectangle.z_index + 1)
        centered_triangle.set_z_index(angle.z_index + 1)
        angle_label = MathTex(r"\alpha").move_to(Angle(*angle.get_lines(), radius=angle.radius + 0.3).point_from_proportion(0.5))
        angle_label_rectangle = BackgroundRectangle(angle_label, buff=SMALL_BUFF)
        angle_label.set_z_index(angle_label_rectangle.z_index + 1)
        centered_triangle.set_z_index(angle.z_index + 1)

        j_relation = MathTex("1 + j + j^2 = 0").next_to(conditions_tex, DOWN, buff=0.5)
        j_relation_rectangle = BackgroundRectangle(j_relation, buff=MED_LARGE_BUFF)
        j_relation.set_z_index(j_relation_rectangle.z_index + 1)

        iff_relation = MathTex(r"b-c = (1+j)(a-c)", r" \iff ", "a + bj + cj^2 = 0").move_to(plane.c2p(-2, -1.25))
        iff_relation_rectangle = BackgroundRectangle(iff_relation, buff=MED_SMALL_BUFF)
        iff_relation.set_z_index(j_relation_rectangle.z_index + 1)

        VGroup(j_relation[0][2], j_relation[0][4], iff_relation[2][3], iff_relation[2][6]).set_color(BLUE)
        VGroup(iff_relation[0][4:9]).set_color(GREEN)
        
        self.add(plane)
        self.wait(2)
        self.play(Create(triangle), *[Write(label) for label in labels], FadeIn(*label_rectangles), run_time=2)
        self.wait(2)
        self.play(
            ReplacementTransform(triangle, centered_triangle),
            *[ReplacementTransform(label, centered_label) for label, centered_label in zip(labels, centered_labels)],
            *[ReplacementTransform(rectangle, centered_rectangle) for rectangle, centered_rectangle in zip(label_rectangles, centered_label_rectangles)],
            run_time=2            
        )
        self.wait()
        self.play(FadeOut(centered_labels[2], centered_label_rectangles[2]), self.camera.frame.animate.shift(2 * LEFT).scale(0.8))
        self.wait(5)
        #self.add(conditions_tex, conditions_tex_rectangle, j_relation, j_relation_rectangle, iff_relation, iff_relation_rectangle)
        self.play(Write(conditions_tex[0]), Create(angle), FadeIn(conditions_tex_rectangle))
        self.play(ReplacementTransform(angle, conditions_tex[1]), run_time=2)
        self.wait()
        self.play(
            ReplacementTransform(Line(centered_triangle.get_vertices()[2], centered_triangle.get_vertices()[0], color=RED), conditions_tex[2]),
            ReplacementTransform(Line(centered_triangle.get_vertices()[2], centered_triangle.get_vertices()[1], color=RED), conditions_tex[4]),
            Write(conditions_tex[3]), run_time=2
        )
        self.wait(5)
        self.play(Write(iff_relation[0]), FadeIn(iff_relation_rectangle), run_time=2)
        self.wait(2)
        self.play(Write(j_relation), FadeIn(j_relation_rectangle), run_time=2)
        self.play(Circumscribe(j_relation))
        self.wait()
        self.play(Write(iff_relation[1:]), run_time=2)
        self.wait()
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


class EquilateralTriangleSymetries(Scene):
    def construct(self):
        relation_1 = MathTex("a + bj + cj^2 = 0")
        relation_2 = MathTex("aj + bj^2 + c", "j^3", "= 0").next_to(relation_1, DOWN, buff=LARGE_BUFF)
        relation_3 = MathTex("aj^2 + b + cj = 0").next_to(relation_2, DOWN, buff=LARGE_BUFF)
        VGroup(relation_1, relation_2, relation_3).move_to(ORIGIN)

        j_cubed_width = relation_2[1].width
        multiply_by_j_arrow = CurvedArrow(relation_1.get_center() - relation_1.height / 2.5 * UP, relation_2.get_center() + relation_2.height / 2.5 * UP, color=YELLOW).shift((0.3 + max(relation_1.width / 2, relation_2.width / 2)) * LEFT)
        multiply_by_j_label = MathTex(r"\times j").next_to(multiply_by_j_arrow, LEFT)
        multiply_by_j_label[0][1].set_color(BLUE)
        multiply_by_j_arrow_bis = CurvedArrow(relation_2.get_center() - relation_2.height / 2.5 * UP, relation_3.get_center() + relation_3.height / 2.5 * UP, color=YELLOW).shift((0.3 + max(relation_2.width / 2, relation_3.width / 2)) * LEFT)
        multiply_by_j_label_bis = multiply_by_j_label.copy().next_to(multiply_by_j_arrow_bis, LEFT)

        brace = Brace(relation_2[1], buff=SMALL_BUFF)
        brace_label = MathTex("= 1").scale(0.5).next_to(brace, DOWN, buff=SMALL_BUFF)
        screen = Rectangle(width=8, height=5).set_fill(BLACK, opacity=1).set_stroke(WHITE, 4, opacity=1)
        triangle = Triangle().scale(2).rotate(-PI / 2).move_to(screen).set_z_index(screen.z_index + 1)

        D_6 = MathTex("D_6").move_to(triangle.get_center() + 1 / 2 * LEFT).scale(2)

        self.wait()
        self.play(FadeIn(relation_1))
        self.wait()
        self.play(Create(multiply_by_j_arrow), Write(multiply_by_j_label), ReplacementTransform(relation_1.copy(), relation_2), run_time=2)
        self.wait(4)
        self.play(FadeIn(brace, brace_label))
        self.wait()
        self.play(FadeOut(brace, brace_label, relation_2[1]), relation_2[2].animate.shift(j_cubed_width * LEFT / 2), relation_2[0].animate.shift(j_cubed_width * RIGHT / 2))
        self.wait(4)
        self.play(Create(multiply_by_j_arrow_bis), Write(multiply_by_j_label_bis), ReplacementTransform(VGroup(relation_2[0], relation_2[2]).copy(), relation_3), run_time=2)
        self.wait(9)
        self.play(GrowFromCenter(screen))
        self.wait()
        self.play(FadeIn(triangle))
        self.wait()
        self.play(Rotate(triangle, 2 * PI / 3, about_point=1 / 2 * LEFT), run_time=1.5)
        self.wait()
        self.play(Rotate(triangle, 4 * PI / 3, about_point=1 / 2 * LEFT), run_time=1.5)
        self.wait(14)
        self.play(triangle.animate.flip(RIGHT), run_time=1.5)
        self.wait()
        self.play(triangle.animate.rotate(4 * PI / 3, about_point=1 / 2 * LEFT).flip(RIGHT).rotate(-4 * PI / 3, about_point=1 / 2 * LEFT), run_time=1.5)
        self.play(triangle.animate.rotate(2 * PI / 3, about_point=1 / 2 * LEFT).flip(RIGHT).rotate(-2 * PI / 3, about_point=1 / 2 * LEFT), run_time=1.5)
        self.wait(5)
        self.play(Write(D_6))
        self.wait(15)
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


class GroupVideoBy3b1b(Scene):
    def construct(self):
        img = ImageMobject("3b1b_video.png").scale(1.5)
        channel_name = Tex("video by 3Blue1Brown").scale(0.9).next_to(img, DOWN, buff=0.5)
        border = SurroundingRectangle(img, buff=0)

        Group(img, channel_name, border).move_to(ORIGIN)

        self.wait()
        self.play(FadeIn(img), Create(border), Write(channel_name), run_time=2)
        self.wait(4)
        self.play(FadeOut(img, border), Unwrite(channel_name))
        self.wait(4)


class AlgebraicRelation(Scene):
    def construct(self):
        relation = MathTex("P + Qj + Rj^2 = 0").scale(2)
        self.wait()
        self.play(FadeIn(relation), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(relation), run_time=1.5)
        self.wait()

 
class AffRWait(Scene):
    def construct(self):
        aff_group_R_tex = MathTex(r"\mathrm{Af~\hspace{-0.42em}f}(\mathbb{R})").scale(3)
        self.add(aff_group_R_tex)
        self.wait(10)


class AffineGroupR(Scene):
    def construct(self):
        aff_group_C_tex = MathTex(r"\mathrm{Af~\hspace{-0.42em}f}(\mathbb{C})").scale(3)
        aff_group_R_tex = MathTex(r"\mathrm{Af~\hspace{-0.42em}f}(\mathbb{R})").scale(3)

        affine_real_func_tex = MathTex(r"&x \mapsto ax + b\\", "&a \in \mathbb{R}^{\star}, b \in \mathbb{R}").scale(2)

        plane = NumberPlane(x_range=[-4.01, 4.01], y_range=[-3.01, 3.01]).scale(0.75).shift(0.5 * DOWN)
        plane_rect = SurroundingRectangle(plane, buff=0).set_z_index(plane.z_index + 1)

        a, b = ValueTracker(1), ValueTracker(0)
        graph = plane.plot(lambda x: a.get_value() * x + b.get_value(), x_range=[-3, 3], color=YELLOW).set_z_index(plane.z_index + 1)

        def graph_updater(graph):
            try:
                if a.get_value() >= 0:
                    graph.become(
                        plane.plot(
                            lambda x: a.get_value() * x + b.get_value(),
                            x_range=[max(-(3 + b.get_value()) / a.get_value(), -4), min((3 - b.get_value()) / a.get_value(), 4)],
                            color=YELLOW
                        )
                    )
                else:
                    graph.become(
                        plane.plot(
                            lambda x: a.get_value() * x + b.get_value(),
                            x_range=[max((3 - b.get_value()) / a.get_value(), -4), min(-(3 + b.get_value()) / a.get_value(), 4)],
                            color=YELLOW
                        )
                    )
            except ZeroDivisionError:
                graph.become(
                        plane.plot(
                            lambda x: a.get_value() * x + b.get_value(),
                            x_range=[-4, 4],
                            color=YELLOW
                        )
                    )
            graph.set_z_index(plane.z_index + 1)
    
        real_line = NumberLine(x_range=[-50, 50], include_numbers=[0, 1])
        transformation_list = [(2, 0), (-1, 2), (-3, -4), (-1/3, 2)]

        self.wait()
        self.play(Write(aff_group_C_tex), run_time=2)
        self.wait(3)
        self.play(FadeOut(aff_group_C_tex))
        self.wait()
        self.play(Write(aff_group_R_tex), run_time=2)
        self.wait()
        self.play(aff_group_R_tex.animate.scale(1 / 2).to_edge(UP, buff=0.75), Write(affine_real_func_tex), run_time=3)
        self.wait(3)
        self.play(FadeIn(plane), Create(plane_rect), ReplacementTransform(affine_real_func_tex, graph))
        graph.add_updater(graph_updater)
        self.wait()
        self.play(a.animate.set_value(4), b.animate.set_value(2), run_time=2)
        self.play(a.animate.set_value(-1/2), b.animate.set_value(-1), run_time=2)
        self.play(a.animate.set_value(1), b.animate.set_value(0), run_time=2)
        self.wait()
        self.play(FadeOut(plane, plane_rect), Uncreate(graph))
        self.wait(2)
        self.play(FadeIn(real_line))
        self.wait()

        for transformation in transformation_list:
            a, b = transformation
            new_line = NumberLine(x_range=[-50, 50], unit_size=a, include_numbers=[0, 1]).shift(b * RIGHT)
            self.play(Transform(real_line, new_line), run_time=2)
            self.wait()

        self.wait()
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


class AffineGroupC(Scene):
    def construct(self):
        scale_factor = 0.75

        aff_group_C_tex = MathTex(r"\mathrm{Af~\hspace{-0.42em}f}(\mathbb{C})").scale(3 / 2).to_edge(UP, buff=0.75)
        affine_complex_func_tex = MathTex(r"&z \mapsto az + b\\", "&a \in \mathbb{C}^{\star}, b \in \mathbb{C}").scale(2)
        plane = NumberPlane(x_range=[-4.01, 4.01], y_range=[-3.01, 3.01]).scale(0.75).shift(0.5 * DOWN)
        plane_copy = NumberPlane(x_range=[-50.01, 50.01], y_range=[-50.01, 50.01]).scale(scale_factor).shift(0.5 * DOWN)
        plane_rect = SurroundingRectangle(plane, buff=0)
        rectangle = Difference(
            Rectangle(width=20, height=20), Rectangle(width=plane_rect.width, height=plane_rect.height).move_to(plane)
        ).set_fill(BLACK, 1).set_stroke(width=0)
        plane_copy.set_z_index(rectangle.z_index - 1)
        VGroup(plane, aff_group_C_tex, affine_complex_func_tex).set_z_index(rectangle.z_index + 2)
        plane_rect.set_z_index(plane.z_index + 1)

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{mathrsfs}")

        translation_group = MathTex(r"\mathrm{T}(\mathbb{C})").move_to(plane).scale(4)
        similitude_group = MathTex(r"\mathscr{S}_{+}(\mathbb{C})", tex_template=tex_template).move_to(plane).scale(4)
        rotation_group = MathTex(r"\mathrm{SO}(\mathbb{C})").move_to(plane).scale(4)
        VGroup(translation_group, similitude_group, rotation_group).set_z_index(plane_copy.z_index + 2)

        a_1, b_1 = complex(-1, 2), complex(-1, 1)
        a_2, b_2 = 1, complex(2, 3)
        a_3, b_3 = complex(2, -1), 0
        a_4, b_4 = np.exp(2 * PI / 3 * complex(0, 1)), 0

        plane_center = complex(plane.c2p(0, 0)[0], plane.c2p(0, 0)[1])
        plane_copy_save = plane_copy.copy()

        self.add(rectangle)
        self.wait()
        self.play(Write(aff_group_C_tex), Write(affine_complex_func_tex), run_time=2)
        self.wait(3)
        self.play(ReplacementTransform(affine_complex_func_tex, plane), Create(plane_rect), run_time=2)
        self.add(plane_copy)
        self.wait(2)
        # Correct exp : lambda z: (a_1 * (z - plane_center) / scale_factor + b_1) * scale_factor + plane_center
        self.play(
            Rotate(plane_copy, np.arctan(2) + PI / 2),
            plane.animate.set_opacity(0.25), run_time=1.5
        )
        self.play(
            ApplyComplexFunction(lambda z: (np.sqrt(a_1.real ** 2 + a_1.imag ** 2) * (z - plane_center) / scale_factor) * scale_factor + plane_center, plane_copy),
            run_time=1.5
        )
        self.play(
            ApplyComplexFunction(lambda z: ((z - plane_center) / scale_factor + b_1) * scale_factor + plane_center, plane_copy),
            run_time=1.5
        )
        self.wait(2)
        self.play(Transform(plane_copy, plane_copy_save), run_time=1)
        self.wait(2)

        self.play(
            ApplyComplexFunction(lambda z: (a_2 * (z - plane_center) / scale_factor + b_2) * scale_factor + plane_center, plane_copy),
            run_time=2
        )
        self.wait(3)
        self.play(
            Transform(plane_copy, plane_copy_save),
            ReplacementTransform(plane_copy.copy(), translation_group), run_time=1
        )
        self.wait()
        self.play(FadeOut(translation_group))
        self.wait(2)
        
        self.play(
            ApplyComplexFunction(lambda z: (a_3 * (z - plane_center) / scale_factor + b_3) * scale_factor + plane_center, plane_copy),
            run_time=2
        )
        self.wait(3)
        self.play(
            Transform(plane_copy, plane_copy_save),
            ReplacementTransform(plane_copy.copy(), similitude_group), run_time=1
        )
        self.wait()
        self.play(FadeOut(similitude_group))
        self.wait(2)

        self.play(
            Rotate(plane_copy, 2 * PI / 3),
            run_time=2
        )
        self.wait(3)
        self.play(
            ReplacementTransform(plane_copy.copy(), rotation_group), run_time=1
        )
        self.wait()
        self.play(FadeOut(rotation_group))
        self.wait(2)
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


    def get_blurred_image(self, radius, iterations):
        current_image = self.camera.pixel_array
        blurred_image = Image.fromarray(current_image).filter(ImageFilter.GaussianBlur(radius=radius))

        for k in range(iterations - 1):
            temp_array = np.clip(np.asarray(blurred_image) + 2 * np.ones(np.asarray(blurred_image).shape, dtype=np.uint8), 0, 255, dtype=np.uint8)
            blurred_image = Image.fromarray(temp_array).filter(ImageFilter.GaussianBlur(radius=radius))

        new_image = ImageMobject(np.asarray(blurred_image))
        new_image.height = config.frame_height
        return new_image


class CompositionOfTransformations(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-4.01, 4.01], y_range=[-3.01, 3.01])
        plane_copy = NumberPlane(x_range=[-50.01, 50.01], y_range=[-50.01, 50.01])
        screen = BackgroundRectangle(plane, buff=0).set_fill(BLACK, 1)
        rectangle = Difference(
            Rectangle(width=20, height=20), Rectangle(width=screen.width, height=screen.height).move_to(plane)
        ).set_fill(BLACK, 1).set_stroke(width=0)

        couple_rep_tex = MathTex("(b, a)").scale(1.5)
        couple_rep_tex_copy = couple_rep_tex.copy().scale(1.5)
        couple_rep_tex_2 = MathTex("(d, c)").scale(1.5).next_to(couple_rep_tex, RIGHT)
        couple_rep_tex_3 = MathTex(" = (f, e)").scale(1.5).next_to(couple_rep_tex_2, RIGHT)
        e_tex = MathTex(r"e =", r"\varphi(a, b, c, d)", r"\overset{?}{=}", " ac").scale(1.5).to_edge()
        f_tex = MathTex(r"f =", r"\psi(a, b, c, d)", r"\overset{?}{=} ", " b + d", "ad + b").scale(1.5).next_to(e_tex, DOWN).to_edge().shift(0.1 * LEFT)
        VGroup(e_tex, f_tex).next_to(VGroup(couple_rep_tex, couple_rep_tex_2, couple_rep_tex_3), DOWN, buff=0.75)
        VGroup(couple_rep_tex, couple_rep_tex_2, couple_rep_tex_3, e_tex, f_tex).move_to(ORIGIN)
        VGroup(e_tex, f_tex).shift(RIGHT)
        eq_tex = MathTex("=").scale(1.5).move_to(f_tex[2])
        eq_tex_copy = MathTex("=").scale(1.5).move_to(e_tex[2]).shift(0.3 * DOWN)
        f_tex[-1].next_to(eq_tex, RIGHT)
        VGroup(eq_tex, f_tex[-1]).shift(0.2 * DOWN)
        eq_tex.shift(0.05 * DOWN)

        semi_direct_product = MathTex(
            r"\mathrm{Af~\hspace{-0.42em}f}(\mathbb{C}) = \mathbb{C} \rtimes \mathrm{GL}(\mathbb{C})"
        ).scale(1.5).next_to(VGroup(couple_rep_tex, couple_rep_tex_2, couple_rep_tex_3, e_tex, f_tex), DOWN, buff=0.75)
        action_tex = MathTex(r"z \in \mathrm{GL}(\mathbb{C}) \mapsto (w \mapsto zw) \in \mathrm{Aut}(\mathbb{C})").scale(1.5).next_to(semi_direct_product, DOWN)

        screen.set_z_index(VGroup(couple_rep_tex, couple_rep_tex_2, couple_rep_tex_3, e_tex, f_tex).z_index + 1)
        plane.set_z_index(screen.z_index + 1)
        plane_copy.set_z_index(plane.z_index + 1)
        rectangle.set_z_index(plane_copy.z_index + 1)

        c, d = complex(-1, 1), complex(1, 1)
        a, b = 2 * np.exp(-PI / 3 * complex(0, 1)), complex(-2, 3)

        zero_dot = always_redraw(lambda: Dot(plane_copy.c2p(0, 0), color=YELLOW).set_z_index(plane_copy.z_index + 1))
        dot_label_0 = MathTex("0").next_to(zero_dot, RIGHT)
        dot_label_d = MathTex("d").next_to(plane.c2p(d.real, d.imag), plane.c2p(d.real, d.imag) / np.linalg.norm(plane.c2p(d.real, d.imag)))
        dot_label_ad = MathTex("ad").next_to(plane.c2p((a*d).real, (a*d).imag), plane.c2p((a*d).real, (a*d).imag) / np.linalg.norm(plane.c2p((a*d).real, (a*d).imag)))
        dot_label_ad_b = MathTex("ad + b").next_to(plane.c2p((a*d+b).real, (a*d+b).imag), plane.c2p((a*d+b).real, (a*d+b).imag) / np.linalg.norm(plane.c2p((a*d+b).real, (a*d+b).imag)))
        dot_label_0_rectangle = BackgroundRectangle(dot_label_0, buff=SMALL_BUFF).set_z_index(plane_copy.z_index + 1)
        VGroup(dot_label_0, dot_label_d, dot_label_ad, dot_label_ad_b).set_z_index(dot_label_0_rectangle.z_index + 1)

        matrix = np.array([[1, -1], [1, 1]])
        cross = Cross(f_tex[2:4]).shift(0.15 * DOWN)

        self.wait()
        self.play(Write(couple_rep_tex_copy), run_time=1.5)
        self.wait(3)
        self.play(ApplyMatrix(matrix, couple_rep_tex_copy[0][3], about_point=couple_rep_tex_copy.get_center()), run_time=1)
        self.play(ApplyMatrix(np.linalg.inv(matrix), couple_rep_tex_copy[0][3], about_point=couple_rep_tex_copy.get_center()), run_time=1)
        self.wait()
        self.play(couple_rep_tex_copy[0][1].animate.shift(2 * RIGHT + UP), run_time=1)
        self.play(couple_rep_tex_copy[0][1].animate.shift(2 * LEFT + DOWN), run_time=1)
        self.wait()
        self.play(ReplacementTransform(couple_rep_tex_copy, couple_rep_tex))
        self.play(Write(couple_rep_tex_2))
        self.wait()
        self.play(ReplacementTransform(VGroup(couple_rep_tex.copy(), couple_rep_tex_2.copy()), couple_rep_tex_3))
        self.wait(2)
        self.play(Write(e_tex[0:2]), Write(f_tex[0:2]), run_time=2)
        """
        self.wait()
        self.play(Write(e_tex[2:]))
        self.play(Write(f_tex[2:4]))
        self.wait(2)
        self.play(GrowFromCenter(cross), Indicate(e_tex[2:], scale_factor=1.25, color=GREEN))
        self.wait()
        self.play(GrowFromCenter(VGroup(plane, screen)), run_time=1.5)
        self.add(plane_copy, rectangle)
        self.wait()
        self.play(Create(zero_dot), Write(dot_label_0), FadeIn(dot_label_0_rectangle), run_time=1.5)
        self.wait()
        self.play(ApplyComplexFunction(lambda z: c*z, plane_copy), run_time=2)
        self.play(
            ApplyComplexFunction(lambda z: z + d, plane_copy),
            ReplacementTransform(dot_label_0, dot_label_d),
            Transform(dot_label_0_rectangle, BackgroundRectangle(dot_label_d).set_z_index(dot_label_0_rectangle.z_index)), run_time=2
        )
        self.wait()
        self.play(
            ApplyComplexFunction(lambda z: a*z, plane_copy),
            ReplacementTransform(dot_label_d, dot_label_ad),
            Transform(dot_label_0_rectangle, BackgroundRectangle(dot_label_ad).set_z_index(dot_label_0_rectangle.z_index)), run_time=2
        )
        self.wait()
        self.play(
            ApplyComplexFunction(lambda z: z + b, plane_copy),
            ReplacementTransform(dot_label_ad, dot_label_ad_b),
            Transform(dot_label_0_rectangle, BackgroundRectangle(dot_label_ad_b).set_z_index(dot_label_0_rectangle.z_index)), run_time=2
        )
        self.wait(3)
        self.play(Indicate(dot_label_ad_b), cross.animate.set_opacity(0))
        self.wait(2)
        zero_dot.clear_updaters()
        self.play(
            ShrinkToCenter(VGroup(plane, screen, zero_dot, dot_label_ad_b, dot_label_0_rectangle)),
            plane_copy.animate.set_opacity(0), run_time=1.5
        )
        self.remove(rectangle)
        self.wait()
        self.play(
            ReplacementTransform(f_tex[3], f_tex[4]),
            ReplacementTransform(f_tex[2], eq_tex),
            ReplacementTransform(e_tex[2], eq_tex_copy), run_time=1.5
        )
        self.wait()
        self.play(Indicate(f_tex[4], scale_factor=1.25, color=GREEN), Indicate(e_tex[-1], color=GREEN))
        self.wait()
        VGroup(semi_direct_product, action_tex).set_opacity(0)
        self.play(
            VGroup(couple_rep_tex, couple_rep_tex_2, couple_rep_tex_3, e_tex, f_tex, semi_direct_product, action_tex).animate.move_to(ORIGIN),
            VGroup(eq_tex, eq_tex_copy).animate.set_opacity(0)
        )
        self.play(Write(semi_direct_product.copy().set_opacity(1)), run_time=3)
        self.play(Write(action_tex.copy().set_opacity(1)), run_time=3)
        self.wait(2)
        self.play(FadeIn(CoveringRectangle()))
        self.wait()
        """


class CompositionOfTransformationsWait(Scene):
    def construct(self):
        im = ImageMobject("CompositionOfTransformationsWait.png")
        self.add(im)
        self.wait(2.5)


class AffineRotations(Scene):
    def construct(self):
        scale_factor = 0.8
        plane = NumberPlane(x_range=[-4.01, 4.01], y_range=[-3.01, 3.01]).scale(scale_factor).shift(0.75 * UP)
        plane_copy = NumberPlane(x_range=[-50.01, 50.01], y_range=[-50.01, 50.01]).scale(scale_factor).shift(0.75 * UP)
        screen = BackgroundRectangle(plane, buff=0).set_fill(BLACK, 1)
        rectangle = Difference(
            Rectangle(width=20, height=20), Rectangle(width=screen.width, height=screen.height).move_to(plane)
        ).set_fill(BLACK, 1).set_stroke(width=0)
        plane_center = complex(plane.c2p(0, 0)[0], plane.c2p(0, 0)[1])
        plane_center_array = plane.c2p(0, 0)

        plane_copy.set_z_index(plane.z_index + 1)
        rectangle.set_z_index(plane_copy.z_index + 1)

        a_tex = MathTex(r"a = e^{i\theta}").scale(1.25).next_to(plane, DOWN, buff=0.75)
        func_tex = MathTex(r"z \mapsto e^{i\theta}(z-c) + c = e^{i\theta}z + (1 - e^{i\theta})c").next_to(plane, DOWN, buff=0.75).scale(1.25)
        VGroup(a_tex, func_tex).set_z_index(rectangle.z_index + 1)

        c = complex(1, 1)
        c_dot = always_redraw(lambda: Dot(plane_copy.c2p(c.real, c.imag)).set_z_index(plane_copy.z_index + 1))
        c_label = MathTex("c").next_to(plane.c2p(1, 1), plane.c2p(1, 1) / np.linalg.norm(plane.c2p(1, 1)))
        c_label_rectangle = BackgroundRectangle(c_label, buff=SMALL_BUFF).set_z_index(plane_copy.z_index + 1)
        zero_label = MathTex("0").next_to(plane.c2p(0, 0), plane.c2p(0, 0) / np.linalg.norm(plane.c2p(0, 0))).set_z_index(plane_copy.z_index + 1)
        zero_label_rectangle = BackgroundRectangle(zero_label, buff=SMALL_BUFF).set_z_index(plane_copy.z_index + 1)
        VGroup(c_label, zero_label_rectangle).set_z_index(c_label_rectangle.z_index + 1)

        c_label_copy = c_label.copy()
        c_label_rectangle_copy = c_label_rectangle.copy()

        self.add(rectangle)
        self.wait()
        self.play(FadeIn(plane_copy))
        self.wait()
        self.play(Write(a_tex))
        self.play(Wiggle(a_tex[0][-1], scale_value=1.25, rotation_angle=0.02 * TAU))
        self.wait()
        self.play(Create(c_dot), Write(c_label), FadeIn(c_label_rectangle))
        self.wait()
        self.play(
            ApplyComplexFunction(lambda z: (((z - plane_center)/ scale_factor) - c + plane_center) * scale_factor, plane_copy),
            Transform(c_label, zero_label.copy()),
            Transform(c_label_rectangle, zero_label_rectangle.copy()), run_time=2
        )
        self.wait()
        self.play(Rotate(plane_copy, PI / 3, about_point=plane_center_array), run_time=2)
        self.wait()
        self.play(
            ApplyComplexFunction(lambda z: (((z - plane_center)/ scale_factor) + c + plane_center) * scale_factor, plane_copy),
            Transform(c_label, c_label_copy),
            Transform(c_label_rectangle, c_label_rectangle_copy), run_time=2
        )
        self.wait(2)
        self.play(ReplacementTransform(a_tex, func_tex), run_time=2)
        self.wait()
        self.play(Rotate(plane_copy, PI / 3, about_point=c_dot.get_center()), run_time=2)
        self.wait(2)
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


class ProofSetup(Scene):
    def construct(self):
        triangle = MorleyTriangle([complex(-3, 1), complex(3, 2), complex(0, -2)], direct=False)
        triangle_copy = triangle.copy()
        cross = Cross(VGroup(triangle.outer_lines, triangle.outer_dots).copy().scale(1.5), stroke_width=16)

        g_A = MathTex("g_A")
        g_B = MathTex("g_B").next_to(g_A, DOWN, buff=0.75)
        g_C = MathTex("g_C").next_to(g_B, DOWN, buff=0.75)
        VGroup(g_A, g_B, g_C).move_to(ORIGIN).to_edge(buff=1)

        g_A_cube = MathTex("g_A^3")
        g_B_cube = MathTex("g_B^3").next_to(g_A_cube, DOWN, buff=0.75)
        g_C_cube = MathTex("g_C^3").next_to(g_B_cube, DOWN, buff=0.75)
        i_tex = MathTex("i = g_A^3g_B^3g_C^3").next_to(g_C_cube, DOWN, buff=0.75)
        VGroup(g_A_cube, g_B_cube, g_C_cube, i_tex).move_to(ORIGIN).to_edge(RIGHT, buff=1)
        
        self.wait()
        self.play(DrawBorderThenFill(triangle), run_time=3)
        self.play(FadeIn(triangle_copy))
        triangle_copy.set_opacity(0.25)
        triangle_copy.outer_angle.set_fill(opacity=0).set_stroke(opacity=0.25)
        self.wait(2)
        self.play(Rotate(VGroup(*[part for part in triangle.subvmobjects if part != triangle.A_label]), 2 / 3 * triangle.BAC_angle_value, about_point=triangle.A.get_center()), run_time=1)
        self.play(Rotate(VGroup(*[part for part in triangle.subvmobjects if part != triangle.A_label]), -2 / 3 * triangle.BAC_angle_value, about_point=triangle.A.get_center()), run_time=1)
        self.wait()
        self.play(Rotate(VGroup(*[part for part in triangle.subvmobjects if part != triangle.B_label]), 2 / 3 * triangle.CBA_angle_value, about_point=triangle.B.get_center()), run_time=1)
        self.play(Rotate(VGroup(*[part for part in triangle.subvmobjects if part != triangle.B_label]), -2 / 3 * triangle.CBA_angle_value, about_point=triangle.B.get_center()), run_time=1)
        self.wait()
        self.play(Rotate(VGroup(*[part for part in triangle.subvmobjects if part != triangle.C_label]), 2 / 3 * triangle.ACB_angle_value, about_point=triangle.C.get_center()), run_time=1)
        self.play(Rotate(VGroup(*[part for part in triangle.subvmobjects if part != triangle.C_label]), -2 / 3 * triangle.ACB_angle_value, about_point=triangle.C.get_center()), run_time=1)
        self.wait(2)
        self.play(AnimationGroup(Write(g_A), Write(g_B), Write(g_C), lag_ratio=0.3))
        self.wait()
        self.play(Rotate(VGroup(*[part for part in triangle.subvmobjects if part != triangle.A_label]), 2 * triangle.BAC_angle_value, about_point=triangle.A.get_center()), Write(g_A_cube), run_time=1)
        self.play(Rotate(VGroup(*[part for part in triangle.subvmobjects if part != triangle.A_label]), -2 * triangle.BAC_angle_value, about_point=triangle.A.get_center()), run_time=1)
        self.wait()
        self.play(AnimationGroup(Write(g_B_cube), Write(g_C_cube), lag_ratio=0.3))
        self.wait(3)
        self.play(ScaleInPlace(triangle, 1.5))
        self.play(GrowFromCenter(cross))
        self.wait()
        self.play(ScaleInPlace(triangle, 1 / 1.5), FadeOut(triangle_copy, cross))
        self.wait()
        self.play(Write(i_tex), triangle.animate.scale(0.7).shift(1.75 * UP + 0.75 * RIGHT))
        self.wait()


class IdentityProof(Scene):
    def construct(self):
        triangle = MorleyTriangle([complex(-3, 1), complex(3, 2), complex(0, -2)], direct=False)
        triangle.save_state()
        triangle.scale(0.7).shift(1.75 * UP + 0.75 * RIGHT)
        triangle_C = triangle.copy()
        triangle_C.remove(triangle_C.C_label)
        triangle_B = triangle.copy()
        triangle_B.remove(triangle_B.B_label, triangle_B.A_label)
        triangle_A = triangle.copy()
        triangle_A.remove(triangle_A.C_label, triangle_A.B_label, triangle_A.A_label)

        g_A = MathTex("g_A")
        g_B = MathTex("g_B").next_to(g_A, DOWN, buff=0.75)
        g_C = MathTex("g_C").next_to(g_B, DOWN, buff=0.75)
        VGroup(g_A, g_B, g_C).move_to(ORIGIN).to_edge(buff=1)

        g_A_cube = MathTex("g_A^3")
        g_B_cube = MathTex("g_B^3").next_to(g_A_cube, DOWN, buff=0.75)
        g_C_cube = MathTex("g_C^3").next_to(g_B_cube, DOWN, buff=0.75)
        i_tex = MathTex("i = g_A^3g_B^3g_C^3")
        i_tex.next_to(g_C_cube, DOWN, buff=0.75)
        VGroup(g_A_cube, g_B_cube, g_C_cube, i_tex).move_to(ORIGIN).to_edge(RIGHT, buff=1)

        i_exp = MathTex("i = ", "r_{CA}", "r_{AB}", "r_{AB}", "r_{BC}", "r_{BC}", "r_{CA}").to_edge(DOWN, buff=0.6)
        VGroup(i_exp[1], i_exp[6]).set_color(PURE_GREEN)
        i_exp[2:4].set_color(PURE_RED)
        i_exp[4:6].set_color(PURPLE_E)
        id_tex = MathTex(r"\mathrm{id}").next_to(i_exp[0], RIGHT)

        self.add(triangle, g_A, g_B, g_C, g_A_cube, g_B_cube, g_C_cube, i_tex)
        self.wait(2)
        self.play(Rotate(VGroup(triangle_C, triangle_B, triangle_A), 2 * triangle_C.ACB_angle_value, about_point=triangle_C.C.get_center()), run_time=2)
        self.play(Rotate(VGroup(triangle_B, triangle_A), 2 * triangle.CBA_angle_value, about_point=triangle_B.B.get_center()), run_time=2)
        self.play(Rotate(triangle_A, 2 * triangle.BAC_angle_value, about_point=triangle_A.A.get_center()), run_time=2)
        
        triangle_A.remove(
            triangle_A.P_label, triangle_A.Q_label, triangle_A.R_label,
            triangle_A.ACB_angle_label, triangle_A.BAC_angle_label, triangle_A.CBA_angle_label
        )
        
        self.wait(3)
        self.play(*[Wiggle(line, scale_value=1.2, rotation_angle=0.015 * TAU) for line in VGroup(triangle.AB_line, triangle_A.AB_line, triangle_B.AB_line, triangle_C.AB_line)])
        self.play(*[line.animate.set_color(PURE_RED) for line in VGroup(triangle.AB_line, triangle_A.AB_line, triangle_B.AB_line, triangle_C.AB_line)], run_time=0.5)
        self.play(*[Wiggle(line, scale_value=1.2, rotation_angle=0.015 * TAU) for line in VGroup(triangle.BC_line, triangle_A.BC_line, triangle_B.BC_line, triangle_C.BC_line)])
        self.play(*[line.animate.set_color(PURPLE_E) for line in VGroup(triangle.AB_line, triangle_A.BC_line, triangle_B.BC_line, triangle_C.BC_line)], run_time=0.5)
        self.play(*[Wiggle(line, scale_value=1.2, rotation_angle=0.015 * TAU) for line in VGroup(triangle.CA_line, triangle_A.CA_line, triangle_B.CA_line, triangle_C.CA_line)])
        self.play(*[line.animate.set_color(PURE_GREEN) for line in VGroup(triangle.CA_line, triangle_A.CA_line, triangle_B.CA_line, triangle_C.CA_line)], run_time=0.5)
        self.wait(3)
        self.play(Indicate(
                VGroup(
                    triangle.CA_line, triangle.A, triangle.C,
                    triangle_A.CA_line, triangle_A.A, triangle_A.C,
                    triangle_B.AB_line, triangle_B.A, triangle_B.B,
                    triangle_C.BC_line, triangle_C.B, triangle_C.C
                ), color=None 
            ), run_time=2
        )
        self.wait()
        self.play(Rotate(triangle_A, PI, axis=triangle.CA_line.get_vector(), about_point=triangle.A.get_center()), run_time=1.5)
        self.play(Rotate(triangle_A, PI, axis=triangle.CA_line.get_vector(), about_point=triangle.A.get_center()), run_time=1.5)
        self.wait(3)

        self.play(
            Rotate(triangle_A, PI, axis=triangle.CA_line.get_vector(), about_point=triangle.A.get_center()),
            Write(VGroup(i_exp[0], i_exp[6])),
            run_time=1.5
        )
        self.play(
            Rotate(triangle_A, PI, axis=triangle_C.BC_line.get_vector(), about_point=triangle_C.C.get_center()),
            Write(i_exp[5]),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(
            Rotate(triangle_A, PI, axis=triangle_C.BC_line.get_vector(), about_point=triangle_C.C.get_center()),
            Write(i_exp[4]),
            run_time=1.5
        )
        self.play(
            Rotate(triangle_A, PI, axis=triangle_B.AB_line.get_vector(), about_point=triangle_B.B.get_center()),
            Write(i_exp[3]),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(
            Rotate(triangle_A, PI, axis=triangle_B.AB_line.get_vector(), about_point=triangle_B.B.get_center()),
            Write(i_exp[2]),
            run_time=1.5
        )
        self.play(
            Rotate(triangle_A, PI, axis=triangle.CA_line.get_vector(), about_point=triangle.A.get_center()),
            Write(i_exp[1]),
            run_time=1.5
        )
        self.wait(2)

        self.play(Wiggle(i_exp[2:4], scale_value=1.25))
        self.play(FadeOut(i_exp[2:4]), i_exp[4:].animate.shift(i_exp[2:4].width * LEFT))

        self.play(Wiggle(i_exp[4:6], scale_value=1.25))
        self.play(FadeOut(i_exp[4:6]), i_exp[6:].animate.shift(i_exp[4:6].width * LEFT))

        self.play(Wiggle(VGroup(i_exp[1], i_exp[6]), scale_value=1.25))
        self.play(ReplacementTransform(VGroup(i_exp[1], i_exp[6]), id_tex))
        self.wait(2)
        self.play(FadeOut(i_exp[0], id_tex, triangle_A, triangle_B, triangle_C), triangle.animate.restore())
        self.wait()


class TrisectorsIntersectionsAsFixedPoints(Scene):
    def construct(self):
        triangle = MorleyTriangle([complex(-3, 1), complex(3, 2), complex(0, -2)], direct=False)
        triangle_copy = triangle.copy().set_opacity(0.2)
        VGroup(triangle_copy.R, triangle_copy.R_label).set_opacity(1)
        VGroup(triangle_copy.BAC_angle, triangle_copy.ACB_angle, triangle_copy.CBA_angle).set_fill(opacity=0).set_stroke(opacity=0.2)

        R_copy = triangle.R.copy()
        trisector_from_A_copy = triangle.trisectors_from_A[0].copy().rotate(2 / 3 * triangle.BAC_angle_value, about_point=triangle.A.get_center())
        trisector_from_B_copy = triangle.trisectors_from_B[1].copy().rotate(-2 / 3 * triangle.CBA_angle_value, about_point=triangle.B.get_center())
        A_trisector_angle = Angle(triangle.AB_line, trisector_from_A_copy, radius=triangle.BAC_angle.radius, color=triangle.BAC_angle.color).set_z_index(triangle.AB_line.z_index - 1)
        B_trisector_angle = Angle(trisector_from_B_copy, Line(triangle.B.get_center(), triangle.A.get_center()), radius=triangle.CBA_angle.radius, color=triangle.CBA_angle.color).set_z_index(triangle.AB_line.z_index - 1)
        A_trisector_angle_label = triangle.BAC_angle_label[0][1].copy().move_to(Angle(triangle.AB_line, trisector_from_A_copy, radius=triangle.BAC_angle.radius + 0.4).point_from_proportion(0.5))
        B_trisector_angle_label = triangle.CBA_angle_label[0][1].copy().move_to(Angle(trisector_from_B_copy, Line(triangle.B.get_center(), triangle.A.get_center()), radius=triangle.CBA_angle.radius + 0.4).point_from_proportion(0.25))
        R_copy.set_z_index(trisector_from_B_copy.z_index + 1)

        g_A = MathTex("g_A")
        g_B = MathTex("g_B").next_to(g_A, DOWN, buff=0.75)
        g_C = MathTex("g_C").next_to(g_B, DOWN, buff=0.75)
        VGroup(g_A, g_B, g_C).move_to(ORIGIN).to_edge(buff=1)

        g_A_cube = MathTex("g_A^3")
        g_B_cube = MathTex("g_B^3").next_to(g_A_cube, DOWN, buff=0.75)
        g_C_cube = MathTex("g_C^3").next_to(g_B_cube, DOWN, buff=0.75)
        i_tex = MathTex("i = g_A^3g_B^3g_C^3")
        i_tex.next_to(g_C_cube, DOWN, buff=0.75)
        VGroup(g_A_cube, g_B_cube, g_C_cube, i_tex).move_to(ORIGIN).to_edge(RIGHT, buff=1)

        g_B_g_A = MathTex("g_Bg_A").move_to(g_A_cube)
        g_C_g_B = MathTex("g_Cg_B").move_to(g_B_cube)
        g_A_g_C = MathTex("g_Ag_C").move_to(g_C_cube)
        rectangle_2 = BackgroundRectangle(VGroup(g_B_g_A, g_C_g_B, g_A_g_C), buff=SMALL_BUFF).set_z_index(VGroup(g_B_g_A, g_C_g_B, g_A_g_C).z_index - 1)

        fixed_point = MathTex("g_Ag_B(R) = R").to_edge(DOWN, buff=0.75).move_to(i_tex).to_edge(buff=1)

        self.add(triangle, g_A, g_B, g_C, g_A_cube, g_B_cube, g_C_cube, i_tex, rectangle_2)
        self.wait(2)
        self.play(ReplacementTransform(g_A_cube, g_B_g_A))
        self.play(ReplacementTransform(g_B_cube, g_C_g_B))
        self.play(ReplacementTransform(g_C_cube, g_A_g_C))
        self.wait(2)
        self.play(Wiggle(VGroup(triangle.R, triangle.R_label)))
        self.wait(2)
        self.play(
            g_A.animate.move_to(g_B_g_A).to_edge(buff=1),
            g_B.animate.move_to(g_C_g_B).to_edge(buff=1),
            g_C.animate.move_to(g_A_g_C).to_edge(buff=1),
            Write(fixed_point)
        )

        rectangle_1 = BackgroundRectangle(VGroup(g_A, g_B, g_C), buff=SMALL_BUFF).set_z_index(VGroup(g_A, g_B, g_C).z_index - 1)
        rectangle_3 = BackgroundRectangle(fixed_point, buff=SMALL_BUFF).set_z_index(fixed_point.z_index - 1)
        self.add(rectangle_1, rectangle_3, R_copy)

        start = triangle.A.get_center() + 10 * (triangle.B.get_center() - triangle.A.get_center())
        end = triangle.A.get_center() - 10 * (triangle.B.get_center() - triangle.A.get_center())
        AB_line = DashedLine(start=start, end=end).set_z_index(min([triangle.AB_line.z_index - 1, rectangle_1.z_index - 1, rectangle_2.z_index - 1, rectangle_3.z_index - 1]))

        self.play(FadeIn(AB_line))
        self.wait()

        self.play(Rotate(R_copy, PI, triangle.AB_line.get_vector(), triangle.A.get_center()), run_time=1.5)
        self.wait()
        self.play(Create(trisector_from_A_copy), Create(A_trisector_angle), Write(A_trisector_angle_label), run_time=1.5)
        self.play(Wiggle(VGroup(A_trisector_angle, A_trisector_angle_label)))
        self.wait()
        self.play(Rotate(triangle_copy, 2 / 3 * triangle.BAC_angle_value, about_point=triangle.A.get_center()), run_time=2)
        self.wait()

        self.play(
            Rotate(R_copy, PI, triangle.AB_line.get_vector(), triangle.A.get_center()),
            Create(trisector_from_B_copy),
            Create(B_trisector_angle),
            Write(B_trisector_angle_label), run_time=1.5
        )
        self.wait()
        self.play(Wiggle(VGroup(B_trisector_angle, B_trisector_angle_label)))
        self.wait()
        self.play(Rotate(triangle_copy, 2 / 3 * triangle.CBA_angle_value, about_point=triangle.B.get_center()), run_time=2)
        self.wait()

        self.play(Circumscribe(fixed_point))
        self.wait()

        p_qj_rj2 = MathTex("P + Qj + Rj^2 = 0").to_edge(DOWN, buff=0.5)

        self.play(Write(p_qj_rj2), run_time=3)
        self.play(Circumscribe(p_qj_rj2))
        self.wait(3)
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


class MorleyTheoremProof(Scene):
    def construct(self):
        g_A_tex = MathTex("g_A = (", "t_A, ", r"s_A = e^{2i\alpha})")
        g_B_tex = MathTex(r"g_B = (t_B, s_B = e^{2i\beta})").next_to(g_A_tex, DOWN)
        g_C_tex = MathTex(r"g_C = (t_C, s_C = e^{2i\gamma})").next_to(g_B_tex, DOWN)
        j_tex = MathTex(r"j = s_As_Bs_C = e^{2i(\alpha + \beta + \gamma)}").next_to(g_C_tex, DOWN, buff=0.75)
        VGroup(g_A_tex, g_B_tex, g_C_tex, j_tex).move_to(ORIGIN).scale(1.25)

        #self.add(VGroup(g_A_tex, g_B_tex, g_C_tex, j_tex))

        i_tex = MathTex("i = g_A^3g_B^3g_C^3 = (t_i, s_i)", " = (0, 1)")
        t_i_exp = MathTex("-js_A^2s_B", "(s_A-j)", "(s_B-j)", "(s_C-j)", "(S + Tj + Uj^2)", " = 0").next_to(i_tex, DOWN, buff=0.75)
        P_exp = MathTex(r"S = \frac{s_Ct_B + t_C}{1-s_Cs_B}").scale(0.8).next_to(t_i_exp, DOWN, buff=1.25)
        Q_exp = MathTex(r"T = \frac{s_At_C + t_A}{1-s_As_C}").scale(0.8).next_to(P_exp, DOWN)
        R_exp = MathTex(r"U = \frac{s_Bt_A + t_B}{1-s_Bs_A}").scale(0.8).next_to(Q_exp, DOWN)
        rectangle = SurroundingRectangle(VGroup(P_exp, Q_exp, R_exp), buff=MED_SMALL_BUFF)
        brace = Brace(t_i_exp[0], buff=0)
        brace_label = always_redraw(lambda: MathTex(r"\neq 0").scale(0.8).next_to(brace, DOWN))

        VGroup(i_tex, t_i_exp, P_exp, Q_exp, R_exp, rectangle, brace, brace_label).move_to(ORIGIN)
        Q_tex_y_pos = Q_exp.get_center()[1]
        composition_formula = MathTex("(t_A, s_A)(t_B, s_B) = (s_At_B + t_A, s_As_B)").next_to(i_tex, DOWN, buff=0.75)

        PQR_exp_copy = VGroup(P_exp, Q_exp, R_exp, rectangle).copy()

        #self.add(VGroup(i_tex, t_i_exp, P_exp, Q_exp, R_exp, rectangle, brace, brace_label))
        implications = MathTex("s_A", " = ", "j =", " s_A", "s_Bs_C", r"\implies", " g_Cg_B = (1, t_{CB})")
        P_fixed_point = MathTex("g_Cg_B(S) = S")
        Q_fixed_point = MathTex("g_Ag_C(T) = T").next_to(P_fixed_point, DOWN)
        R_fixed_point = MathTex("g_Bg_A(U) = U").next_to(Q_fixed_point, DOWN)
        rectangle_2 = SurroundingRectangle(VGroup(P_fixed_point, Q_fixed_point, R_fixed_point), buff=MED_SMALL_BUFF)
        VGroup(P_fixed_point, Q_fixed_point, R_fixed_point, rectangle_2).next_to(PQR_exp_copy, RIGHT, buff=1)
        VGroup(P_fixed_point, Q_fixed_point, R_fixed_point, rectangle_2, PQR_exp_copy).move_to(ORIGIN).shift(Q_tex_y_pos * UP)
        implications.next_to(PQR_exp_copy[1], RIGHT, buff=1).shift(2 * LEFT)
        cross = Cross(implications[6])

        self.wait(2)
        self.play(Write(g_A_tex[0]))
        self.wait()
        self.play(Write(g_A_tex[1]))
        self.wait()
        self.play(Write(g_A_tex[2]))
        self.play(Write(g_B_tex), Write(g_C_tex), run_time=2)
        self.wait(3)
        self.play(Write(j_tex), run_time=2)
        self.wait(2)
        self.play(Transform(j_tex[0][12:], MathTex(r"\frac{\pi}{3}").scale(0.75).next_to(j_tex[0][11], RIGHT, buff=0.1)))
        self.wait(2)
        self.play(FadeOut(g_A_tex, g_B_tex, g_C_tex, j_tex))
        self.wait(3)
        self.play(Write(i_tex[0]), run_time=3)
        self.wait(2)
        self.play(Write(composition_formula), run_time=3)
        self.play(Circumscribe(composition_formula))
        self.wait(3)
        self.play(FadeOut(composition_formula))
        self.wait(6)
        self.play(Write(t_i_exp[0:5]), run_time=5)
        self.wait()
        self.play(Write(P_exp), run_time=2)
        self.play(Write(Q_exp), run_time=2)
        self.play(Write(R_exp), run_time=2)
        self.play(Create(rectangle))
        self.wait(2)
        self.play(Write(i_tex[1]))
        self.play(ReplacementTransform(i_tex[1].copy(), t_i_exp[5]))
        self.wait(3)
        self.play(FadeIn(brace), Write(brace_label), run_time=2)
        self.wait(3)
        self.play(Transform(brace, Brace(t_i_exp[1], buff=0)), run_time=1.5)
        self.wait()
        self.play(
            VGroup(P_exp, Q_exp, R_exp, rectangle).animate.to_edge(buff=1.5),
            ReplacementTransform(t_i_exp[1].copy(), implications[0:5]), run_time=2
        )
        self.wait(3)
        self.play(
            Transform(implications[0], MathTex("1").move_to(implications[0]).shift(0.05 * UP)),
            FadeOut(implications[2:4]),
            implications[4].animate.shift(implications[2:4].width * LEFT)
        )
        VGroup(implications[5:7], cross).shift(implications[2:4].width * LEFT)
        self.wait(3)
        self.play(Write(implications[5:7]), run_time=2)
        self.wait(2)
        self.play(GrowFromCenter(cross))
        self.wait()
        self.play(FadeOut(implications[0], implications[1], implications[4], implications[5:7], cross))
        self.wait()
        self.play(Transform(brace, Brace(t_i_exp[2], buff=0)), run_time=1)
        self.play(Transform(brace, Brace(t_i_exp[3], buff=0)), run_time=1)
        self.wait()

        new_brace = Brace(t_i_exp[4], buff=0)
        brace_label.clear_updaters()
        brace_label_eq_0 = MathTex("= 0").scale(0.8).next_to(new_brace, DOWN)
        self.play(ReplacementTransform(brace, new_brace), ReplacementTransform(brace_label, brace_label_eq_0))
        self.wait()
        self.play(
            FadeOut(new_brace, brace_label_eq_0, t_i_exp[0:4], t_i_exp[4][0], t_i_exp[4][-1]),
            t_i_exp[4][1:9].animate.shift(VGroup(t_i_exp[4][1:9], t_i_exp[5]).get_center()[0] * LEFT),
            t_i_exp[5].animate.shift((VGroup(t_i_exp[4][1:9], t_i_exp[5]).get_center()[0] + 0.25) * LEFT), run_time=2
        )
        self.wait()
        self.play(
            VGroup(P_exp, Q_exp, R_exp, rectangle).animate.move_to(PQR_exp_copy),
            Write(P_fixed_point), Write(Q_fixed_point), Write(R_fixed_point), run_time=2
        )
        self.play(Create(rectangle_2))
        self.wait(3)
        self.play(
            Transform(t_i_exp[4][1], MathTex("P").move_to(t_i_exp[4][1])),
            Transform(t_i_exp[4][3], MathTex("Q").move_to(t_i_exp[4][3])),
            Transform(t_i_exp[4][6], MathTex("R").move_to(t_i_exp[4][6]))
        )
        self.wait(3)
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


class Epilog(ThreeDScene):
    def construct(self):
        radius = 3
        sphere = OpenGLSurface(
            lambda u, v: radius * np.array([np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)]),
            u_range=(0, TAU),
            v_range=(0, PI),
            color=BLUE
        )
        self.set_camera_orientation(65 * DEGREES, 40 * DEGREES)

        A = OpenGLSurface(
            lambda u, v: DEFAULT_DOT_RADIUS * np.array([np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)]),
            u_range=(0, TAU),
            v_range=(0, PI),
            resolution=(20, 20),
            color=WHITE
        ).move_to(np.array([0, 0, 3]))
        B = OpenGLSurface(
            lambda u, v: DEFAULT_DOT_RADIUS * np.array([np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)]),
            u_range=(0, TAU),
            v_range=(0, PI),
            resolution=(20, 20),
            color=WHITE
        ).move_to(np.array([0, -3, 0]))
        C = OpenGLSurface(
            lambda u, v: DEFAULT_DOT_RADIUS * np.array([np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)]),
            u_range=(0, TAU),
            v_range=(0, PI),
            resolution=(20, 20),
            color=WHITE
        ).move_to(np.array([3, 0, 0]))

        AB = ArcBetweenPoints(A.get_center(), B.get_center()).rotate(PI, B.get_center() - A.get_center(), A.get_center())
        BC = ArcBetweenPoints(B.get_center(), C.get_center(), radius=radius)
        CA = ArcBetweenPoints(A.get_center(), C.get_center(), radius=radius)#.rotate(PI / 2, C.get_center() - A.get_center(), A.get_center())

        angle_radius = 0.5

        B_angle = VGroup(
            ArcBetweenPoints(
                AB.point_from_proportion(1 - angle_radius / AB.get_arc_length()),
                self.rotation_matrix(angle_radius / radius) @ AB.point_from_proportion(1 - angle_radius / AB.get_arc_length()), radius=radius
            ),#.set_stroke(width=2),
            ArcBetweenPoints(
                BC.point_from_proportion(angle_radius / BC.get_arc_length()),
                self.rotation_matrix(angle_radius / radius) @ AB.point_from_proportion(1 - angle_radius / AB.get_arc_length()), radius=radius
            ).rotate(PI / 2 + PI / 6, BC.point_from_proportion(angle_radius / BC.get_arc_length()) - self.rotation_matrix(angle_radius / radius) @ AB.point_from_proportion(1 - angle_radius / AB.get_arc_length()), about_point=BC.point_from_proportion(angle_radius / BC.get_arc_length()))
        ).set_color(GREEN)

        C_angle = VGroup(
            ArcBetweenPoints(
                BC.point_from_proportion(1 - angle_radius / BC.get_arc_length()),
                self.rotation_matrix(-angle_radius / radius) @ CA.point_from_proportion(1 - angle_radius / CA.get_arc_length()), radius=radius
            ).rotate(PI / 2 + PI / 6, BC.point_from_proportion(1 - angle_radius / BC.get_arc_length()) - self.rotation_matrix(-angle_radius / radius) @ CA.point_from_proportion(1 - angle_radius / CA.get_arc_length()), about_point=BC.point_from_proportion(1 - angle_radius / BC.get_arc_length())),
            ArcBetweenPoints(
                CA.point_from_proportion(1 - angle_radius / CA.get_arc_length()),
                self.rotation_matrix(-angle_radius / radius) @ CA.point_from_proportion(1 - angle_radius / CA.get_arc_length()), radius=radius
            ).rotate(PI, CA.point_from_proportion(1 - angle_radius / CA.get_arc_length()) - self.rotation_matrix(-angle_radius / radius) @ CA.point_from_proportion(1 - angle_radius / CA.get_arc_length()), about_point=CA.point_from_proportion(1 - angle_radius / CA.get_arc_length()))
        ).set_color(GREEN)

        A_angle = VGroup(
            B_angle[0].copy().rotate(2 * B_angle[1].get_arc_length() / radius - PI / 2, C.get_center(), C.get_center()),
            B_angle[1].copy().rotate(B_angle[0].get_arc_length() / radius - PI / 2, C.get_center(), C.get_center())
        )

        self.wait()
        self.play(Create(sphere), run_time=2)
        self.wait(8)
        self.play(FadeIn(A_angle, B_angle, C_angle, AB, BC, CA, A, B, C))
        self.wait(30)
    

    def rotation_matrix(self, angle):
        return np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])


class Epilog2(ThreeDScene):
    def construct(self):
        hyperbolic_surface = OpenGLSurface(
            lambda u, v: np.array([u, v, 1 / 2 * (u**2 - v**2)]),
            u_range=(-2, 2),
            v_range=(-2, 2),
            color=BLUE
        ).scale(1.25).shift(0.5 * np.array([0, 0, 1]))

        self.set_camera_orientation(65 * DEGREES, 20 * DEGREES)

        self.wait()
        self.begin_ambient_camera_rotation()
        self.play(Create(hyperbolic_surface), run_time=2)
        self.wait(40)


class Epilog3(Scene):
    def construct(self):
        double_arrow = DoubleArrow(LEFT, 2 * RIGHT, color=YELLOW)
        double_arrow_label = Tex("link ?").next_to(double_arrow, UP)

        equilateral_triangle = Triangle().scale(1.5).rotate(PI / 5).next_to(double_arrow, RIGHT, buff=1.25)
        isoceles_triangle = Triangle().stretch(1.4, 1).scale(1.5).next_to(double_arrow, RIGHT, buff=1.25)
        right_triangle = Polygon(ORIGIN, UP, 2 * RIGHT).scale(1.5).next_to(double_arrow, RIGHT, buff=1.25)

        self.wait()
        self.play(GrowArrow(double_arrow), Write(double_arrow_label), run_time=1.5)
        self.wait()
        self.play(Create(equilateral_triangle))
        self.wait(10)
        self.play(Transform(equilateral_triangle, isoceles_triangle))
        self.wait(2)
        self.play(Transform(equilateral_triangle, right_triangle))
        self.wait(5)
        self.play(FadeIn(CoveringRectangle()))
        self.wait()


class Credits(Scene):
    def construct(self):
        credits_tex = Tex(r"Animations made with Manim CE").scale(1.5)
        music_credits = Tex(r"Musics : 'Odyssey' by Kevin \textsc{MacLeod}").scale(1.5)
        proof_credits = Tex(r"Proof : Alain \textsc{Connes}'s article \\ 'A new proof of \textsc{Morley}'s theorem'").scale(1.5)
        self.wait()
        self.play(FadeIn(credits_tex))
        self.wait(2)
        self.play(FadeOut(credits_tex))
        self.wait()
        self.play(FadeIn(music_credits))
        self.wait(2)
        self.play(FadeOut(music_credits))
        self.wait()
        self.play(FadeIn(proof_credits))
        self.wait(4)
        self.play(FadeOut(proof_credits))
        self.wait()



