from manim import *
from functions import *
from scipy.integrate import odeint
from HEX.objects import *
import itertools as it
import random as rd




#scenes list :

#Introduction               : not done yet
#BrouwerIntroAnimation      : k
#BrouwerHistory             : k
#DefFixedPoints             : k
#BrouwerDim1Proof           : k
#FixedPointsThmList         : not done by manim
#CauchyLipschitzThm         : k
#BrouwersThm                : k
#BrouwersThmIllustration1   : k
#BrouwersThmIllustration2   : k
#CoffeeCup                  : not done by manim
#HexHistory                 : k
#HexGame                    : k
#HexThmProof                : k
#Requirements               : k
#BrouwersThmProof1          : k
#BrouwersThmProof2          : k
#BrouwersThmProof3          : k
#BrouwersThmProof4          : k





### Introduction


class Introduction(Scene):
    def construct(self):
        pass


class BrouwerIntroAnimation(MovingCameraScene):
    def construct(self):
        plane = NumberPlane(
            x_axis_config = {"stroke_width": 0.5},
            y_axis_config = {"stroke_width": 0.5},
            background_line_style={"stroke_width": 0.5}
        )
        unit_circle = Circle(1, color=RED)

        a = np.array([0.2, -0.3, 0])

        vector_field = ArrowVectorField(
            lambda pos: (fixed_point_func(pos, a) - pos) * (np.linalg.norm(pos) <= 1),
            x_range=[-1, 1, 0.15],
            y_range=[-1, 1, 0.15],
            vector_config={"stroke_width": 0.3}
        )
        
        for vector in vector_field:
            vec_array = vector.get_end() - vector.get_start()
            vector.tip.scale(0.3, about_point=vector.get_start() + vec_array/2)
            vector.tip.shift(0.1 * vec_array)
        
        dot_list = VGroup()

        for vector in vector_field:
            dot = Dot(vector.get_start(), radius=DEFAULT_SMALL_DOT_RADIUS/5)
            dot_list += dot

        fixed_point_dot = Dot(a, radius=DEFAULT_SMALL_DOT_RADIUS/5)

        self.play(AnimationGroup(Create(plane), Create(unit_circle), lag_ratio=0.5), run_time=3)
        self.play(
            self.camera.frame.animate.set(width=5),
            unit_circle.animate.set(stroke_width=1),
            run_time=3
        )
        self.play(*[GrowArrow(vector) for vector in vector_field], run_time=3)
        self.wait(0.5)

        self.play(
            *[FadeIn(dot) for dot in dot_list if np.linalg.norm(dot.get_center()) <= 1 and np.linalg.norm(dot.get_center() - a) >= 0.05],
            FadeIn(fixed_point_dot),
            vector_field.animate.set_opacity(0.5)
        )
        self.wait(0.5)
        self.play(
            *[dot.animate.shift(vector.get_end() - vector.get_start()) for dot, vector in zip(dot_list, vector_field) if np.linalg.norm(dot.get_center()) <= 1],
            fixed_point_dot.animate.move_to(fixed_point_func(fixed_point_dot.get_center(), a)),
            run_time=3
        )
        self.play(Flash(fixed_point_dot, line_length=0.05, flash_radius=3 * fixed_point_dot.radius, line_stroke_width=1))
        self.wait()
        self.play(
            FadeOut(
                vector_field,
                *[dot for dot in dot_list if np.linalg.norm(dot.get_center()) <= 1],
                fixed_point_dot, unit_circle, plane
            )
        )


class BrouwerHistory(Scene):
    def construct(self):
        image = SVGMobject("brouwer.svg")
        image.height = config.frame_height/1.2
        image_rectangle = SurroundingRectangle(image, buff=0)
        caption = Tex("Luitzen Egbertus Jan \\textsc{Brouwer}").next_to(image_rectangle, DOWN)
        Group(image, image_rectangle, caption).move_to(ORIGIN)
        
        self.play(
            AnimationGroup(
                AnimationGroup(
                    Create(image_rectangle),
                    Write(caption),
                    lag_ratio=0, run_time=5
                ),
                AnimationGroup(
                    *[FadeIn(sub_image) for sub_image in image],
                    lag_ratio=0.5, run_time=15
                )
            )            
        )
        self.wait(10)
        self.play(FadeOut(image, image_rectangle, caption), run_time=5)
        self.wait()
        title = Tex("Chapter 1 : Fixed Points")
        underline = Underline(title).set_opacity([0, 1, 1, 0])
        title_group = VGroup(title, underline).scale(1.5)
        self.play(FadeIn(title_group), run_time=3)
        self.play(FadeOut(title_group), run_time=2)
        self.wait()
        





### Points fixes


class DefFixedPoints(Scene):
    def construct(self):
        tex_scale_factor = 0.7
        f = lambda x: 0.3 * x**3 + 0.5 * x**2 - x - 0.5
        fixed_point = dichotomie(lambda x: f(x) - x, -1, 2)

        axes = Axes(x_range=[-1.2, 2.2], y_range=[-1.2, 2.2], x_length=6, y_length=6, tips=False)
        axes_labels = axes.get_axis_labels()

        v_dashed_line = DashedLine(axes.c2p(fixed_point, fixed_point), axes.c2p(fixed_point, 0), color=WHITE)
        h_dashed_line = DashedLine(axes.c2p(fixed_point, fixed_point), axes.c2p(0, fixed_point), color=WHITE)

        f_curve = axes.plot(f, x_range=[-1, 2])
        f_label = MathTex("f").scale(tex_scale_factor).next_to(f_curve.get_end(), RIGHT)
        id_curve = axes.plot(lambda x: x, x_range=[-1, 2], color=RED)
        id_label = Tex("Id", color=RED).scale(tex_scale_factor).next_to(id_curve.get_end(), UP)
        
        x_label = MathTex("x").scale(0.8).next_to(axes.c2p(fixed_point, 0), UP)
        y_label = MathTex("f(x) = x").scale(tex_scale_factor).next_to(axes.c2p(0, fixed_point), RIGHT)

        x_dot = Dot(axes.c2p(fixed_point, 0), color=YELLOW)
        y_dot = Dot(axes.c2p(0, fixed_point), color=YELLOW)
        intersection_point = Dot(axes.c2p(fixed_point, fixed_point), color=YELLOW)

        f_m_id_curve = axes.plot(lambda x: f(x) - x, x_range=[-1, 2]).set_z_index(f_curve.z_index)
        f_m_id_label = MathTex("f - \\mathrm{Id}").scale(tex_scale_factor).next_to(f_m_id_curve.get_end(), RIGHT)

        self.play(Create(axes), Write(axes_labels), run_time=2)
        self.wait(0.5)
        self.play(Create(f_curve), Create(id_curve), Write(f_label), Write(id_label), run_time=2)
        self.wait(0.5)
        self.play(Create(intersection_point), Flash(intersection_point), run_time=1.5)
        self.wait(0.5)
        self.play(Create(v_dashed_line), Create(h_dashed_line), Create(x_dot), Create(y_dot), run_time=1.5)
        self.play(Write(x_label), Write(y_label))
        self.wait()

        self.play(Transform(f_curve, f_m_id_curve), Transform(f_label, f_m_id_label), run_time=3)
        self.wait()

        self.play(
            AnimationGroup(
                FadeOut(f_curve, id_curve, f_label, id_label),
                FadeOut(axes, axes_labels, x_dot, x_label, y_dot, y_label, h_dashed_line, v_dashed_line, intersection_point),
                lag_ratio=0.3
            )
        )
        self.wait()


class BrouwerDim1Proof(Scene):
    def construct(self):
        thm = Tex(
            "$f : [0, 1] \\to [0, 1], \\hspace{0.15cm} \\mathcal{C}^0 \\implies \\exists x \\in [0, 1], \\hspace{0.15cm} f(x)=x$",
            tex_environment=TexTemplate().add_to_preamble("\\usepackage{mathrsfs}")
        ).scale(1.25)

        tex_scale_factor = 0.7

        axes = Axes(
            x_range=[-0.2, 1.2, 0.25], y_range=[-0.7, 1.2, 0.25],
            x_length=4.5, y_length=5.5,
            tips=False,
            x_axis_config={"include_numbers": True, "numbers_to_include": [0, 1], "decimal_number_config": {"num_decimal_places": 0}},
            y_axis_config={"include_numbers": True, "numbers_to_include": [0, 1], "decimal_number_config": {"num_decimal_places": 0}}
        ).to_edge(DOWN, buff=0.75).shift(2 * LEFT)
        axes_labels = axes.get_axis_labels()

        f = lambda x: 0.8 * np.sin(2.5*x) + 0.1
        g = lambda x: f(x) - x
        fixed_point = dichotomie(lambda x: f(x) - x, 0, 1)

        f_curve = axes.plot(f, x_range=[0, 1])
        f_curve_copy = f_curve.generate_target()
        f_label = MathTex("f").scale(tex_scale_factor).next_to(f_curve.get_end(), RIGHT)
        f_label_copy = f_label.generate_target()
        id_curve = axes.plot(lambda x: x, x_range=[0, 1], color=RED)
        id_label = Tex("Id", color=RED).scale(tex_scale_factor).next_to(id_curve.get_end(), RIGHT)
        g_curve = axes.plot(g, x_range=[0, 1], color=ORANGE)
        g_label = MathTex("g = f - \\mathrm{Id}", color=ORANGE).scale(tex_scale_factor).next_to(g_curve.get_end(), RIGHT)
        g_def = MathTex("g : [0, 1] &\\to [0, 1] \\\\ x &\\mapsto f(x) - x").scale(0.85).to_edge(RIGHT, buff=1.5)

        dot_0 = Dot(axes.c2p(0, g(0)), color=YELLOW).set_z_index(g_curve.z_index + 2)
        dot_1 = Dot(axes.c2p(1, g(1)), color=YELLOW).set_z_index(g_curve.z_index + 2)
        moving_dot_left = dot_0.generate_target().set_color(RED).set_z_index(g_curve.z_index + 1)
        moving_dot_right = dot_1.generate_target().set_color(RED).set_z_index(g_curve.z_index + 1)

        distance_conversion = np.linalg.norm(axes.c2p(1, 0) - axes.c2p(0, 0))
        curve_continuity_text = Tex("continious")
        curve_continuity_text.scale(0.75/curve_continuity_text.width).move_to(0.34 * RIGHT).apply_function(lambda pos: np.array([pos[0], pos[1] + g(pos[0]), 0]))
        curve_continuity_text.scale(0.35 * distance_conversion).stretch(2, 0).next_to(axes.c2p(3/8, g(3/8)), UP, buff=-0.25).stretch(1.25, 1)

        self.play(Write(thm), run_time=5)
        self.wait()

        self.play(thm.animate.scale(0.6).to_edge(UP), Create(axes), Write(axes_labels), run_time=3.25)
        self.play(Create(f_curve), Create(id_curve), Write(f_label), Write(id_label), run_time=2)
        self.wait()
        self.play(
            Write(g_def),
            Transform(f_curve_copy, g_curve),
            Transform(f_label_copy, g_label),
            id_curve.animate.set_stroke(opacity=0.25),
            f_curve.animate.set_stroke(opacity=0.25),
            run_time=3)
        self.wait()
        self.play(
            AnimationGroup(
                AnimationGroup(Create(dot_0), Flash(dot_0), lag_ratio=0),
                AnimationGroup(Create(dot_1), Flash(dot_1), lag_ratio=0),
                lag_ratio=0.75
            ), run_time=4
        )
        self.wait()
        self.play(
            MoveAlongPath(moving_dot_left, axes.plot(g, x_range=[0, fixed_point])),
            MoveAlongPath(moving_dot_right, axes.plot(g, x_range=[fixed_point, 1]).reverse_direction()),
            Write(curve_continuity_text),
            run_time=4
        )
        self.play(
            id_curve.animate.set_stroke(opacity=1),
            f_curve.animate.set_stroke(opacity=1),
            moving_dot_left.animate.move_to(axes.c2p(fixed_point, fixed_point)),
            run_time=2
        )
        self.wait()
        """
        self.play(
            AnimationGroup(
                FadeOut(f_curve, id_curve, f_label, id_label, f_curve_copy, f_label_copy, g_def),
                FadeOut(axes, axes_labels, moving_dot_right, moving_dot_left, dot_0, dot_1, thm),
                lag_ratio=0.3
            )
        )
        self.wait()
        """


class FixedPointsThmList(Scene):
    def construct(self):
        title = Tex("Chapter 2 : \\textsc{Brouwer}'s theorem")
        underline = Underline(title).set_opacity([0, 1, 1, 0])
        title_group = VGroup(title, underline).scale(1.5)
        self.play(FadeIn(title_group), run_time=3)
        self.play(FadeOut(title_group), run_time=2)
        self.wait()


class CauchyLipschitzThm(Scene):
    def construct(self):
        plane = NumberPlane(
            x_axis_config={"stroke_width": 1, "stroke_opacity": 0.8},
            y_axis_config={"stroke_width": 1, "stroke_opacity": 0.8},
            background_line_style={"stroke_width": 1, "stroke_opacity": 0.8}
        )

        x_values = np.linspace(-8, 7.15, 1000)

        def diff_eq(y, x):
            return 0.05 * y - np.sin(y) / 10

        curves = []

        for init_height in np.arange(-4, 4.25, 0.25):
            solution = odeint(diff_eq, init_height, x_values)
            curve = plane.plot_line_graph(x_values, solution[:, 0], add_vertex_dots=False, line_color= interpolate_color(RED, BLUE, init_height / 8 + 1 / 2))
            curves.append(curve)

        diff_eq_tex = MathTex(
            "\\begin{cases} \\displaystyle \\frac{\\mathrm{d}y}{\\mathrm{d}x} = \\frac{y - 2\\sin{(y)}}{20} \\\\ y(-8) \\in [-4, 4] \\end{cases}"
        ).scale(0.8).to_edge(DOWN, buff=0.5)
        rectangle_diff_eq = SurroundingRectangle(diff_eq_tex, color=BLACK, fill_opacity=0.6, stroke_opacity=0)
        diff_eq_tex.set_z_index(rectangle_diff_eq.z_index + 1)

        cauchy_lipschitz_thm_tex = Tex(
            "Let $E$ be a \\textsc{Banach} space, $\\Omega$ an open set of $\\mathbb{R} \\times E$ and $f : \\Omega \\to E$ a continuous function. If $f$ is \\textit{locally lipschitzian}, $$\\begin{cases} \\displaystyle \\frac{\\mathrm{d}y}{\\mathrm{d}x} = f(x, y) \\\\ y(x_0 \\in \\mathbb{R}) = y_0 \\in E\\end{cases}$$ has a unique maximal solution.",
            tex_environment="flushleft" 
        ).scale(0.7).to_edge(UP, buff=0.5)
        rectangle_cl = SurroundingRectangle(cauchy_lipschitz_thm_tex, color=BLACK, fill_opacity=0.6, stroke_opacity=0)
        cauchy_lipschitz_thm_tex.set_z_index(rectangle_cl.z_index + 1)

        hex_image = ImageMobject("hex_image.jpg").set_z_index(31)
        hex_image.height = 0.8 * config.frame_height


        self.play(FadeIn(plane))
        self.play(
            AnimationGroup(
                AnimationGroup(
                    *[Create(curve) for curve in curves],
                    lag_ratio=0.5,
                    run_time=6
                ),
                AnimationGroup(
                    Write(diff_eq_tex),
                    Write(cauchy_lipschitz_thm_tex),
                    FadeIn(rectangle_diff_eq, rectangle_cl),
                    lag_ratio=0,
                    run_time=4
                ),
                lag_ratio=1/6,
            )
        )
        self.wait()
        self.play(FadeIn(Rectangle(width=30, height=30, fill_color=BLACK, fill_opacity=1).set_z_index(30)), run_time=1.5)
        self.wait()
        self.play(FadeIn(hex_image), run_time=1.5)
        self.wait()
        self.play(FadeOut(hex_image), run_time=1.5)
        self.wait()





### Thm Brouwer


class BrouwersThm(Scene):
    def construct(self):

        thm = Tex(
            "Brouwer's theorem :\\\\",
            "Let $(E, ||\\cdot||)$ be a finite-dimensional normed vector space, \\\\$K$ a non-empty convex compact subset of E and",
            "$$f : K \\to K$$",
            "a continuous map. Then $f$ has a fixed point.",
            tex_environment="flushleft"        
        ).scale(0.9)
        thm[0].move_to(ORIGIN).shift(2 * UP).scale(1/0.9)
        thm[1:4].move_to(ORIGIN).shift(0.5 * DOWN)
        thm[2].shift(2 * LEFT)
        underline = Underline(thm[0]).set_opacity([0, 1, 0])
        self.play(Write(thm), Create(underline), run_time=10)
        self.wait()
        self.play(FadeOut(thm, underline))
        self.wait()


class BrouwersThmIllustration1(MovingCameraScene):
    def construct(self):
        plane = NumberPlane(
            x_axis_config = {"stroke_width": 0.5},
            y_axis_config = {"stroke_width": 0.5},
            background_line_style={"stroke_width": 0.5}
        )
        unit_circle = Circle(1, color=RED)

        tex_scale_factor = 0.3
        tex_buff = 0.1

        a = np.array([0.4, 0.6, 0])
        theta = PI / 6

        vector_field = ArrowVectorField(
            lambda pos: (rotation(theta) @ pos - pos) * (np.linalg.norm(pos) <= 1),
            x_range=[-1, 1, 0.25],
            y_range=[-1, 1, 0.25],
            vector_config={"stroke_width": 1},
            length_func=lambda norm: norm
        )
        vector_field_with_too_many_arrows = ArrowVectorField(
            lambda pos: (rotation(theta) @ pos - pos) * (np.linalg.norm(pos) <= 1),
            x_range=[-1, 1, 0.1],
            y_range=[-1, 1, 0.1],
            vector_config={"stroke_width": 1},
            length_func=lambda norm: norm
        )
        vector_field_bis = ArrowVectorField(
            lambda pos: (fixed_point_func(pos, a) - pos) * (np.linalg.norm(pos) <= 1),
            x_range=[-1, 1, 0.2],
            y_range=[-1, 1, 0.2],
            vector_config={"stroke_width": 0.8},
            length_func=lambda norm: 6 * 0.45 * sigmoid(norm)
        )
        for vector in vector_field_bis:
            vector.scale(1 / 6, scale_tips=True, about_point=vector.get_start())
        
        vector_field.move_to(ORIGIN)
        vector_field_bis.remove(vector_field_bis[85])

        arrow_ex_index = 42

        ex_dot = Dot(vector_field[arrow_ex_index].get_start(), radius=DEFAULT_SMALL_DOT_RADIUS / 2)
        ex_dot_copy = ex_dot.generate_target().move_to(vector_field[arrow_ex_index].get_end())
        ex_image_dot = Dot(ex_dot.get_center(), radius=DEFAULT_SMALL_DOT_RADIUS / 2)
        ex_arrow = vector_field[arrow_ex_index]
        ex_arrow_array = ex_arrow.get_end() - ex_arrow.get_start()

        VGroup(ex_dot, ex_image_dot, ex_dot_copy, ex_image_dot).set_z_index(ex_arrow.z_index + 1)

        ex_dot_label = MathTex("x").scale(tex_scale_factor).next_to(ex_dot, -ex_arrow_array/np.linalg.norm(ex_arrow_array), buff=tex_buff)
        ex_arrow_label = MathTex("f(x) - x").scale(tex_scale_factor / 2).move_to(ex_arrow).rotate(ex_arrow.get_slope()).shift(-0.35 * np.array([-ex_arrow_array[1], ex_arrow_array[0], 0]))
        ex_image_dot_label = MathTex("f(x)").scale(tex_scale_factor).next_to(ex_dot_copy, ex_arrow_array/np.linalg.norm(ex_arrow_array), buff=tex_buff)
        rectangles = VGroup(
            SurroundingRectangle(ex_dot_label, color=BLACK, stroke_opacity=0, fill_opacity=0.75, buff=0.025),
            SurroundingRectangle(ex_arrow_label, color=BLACK, stroke_opacity=0, fill_opacity=0.75, buff=0.025),
            SurroundingRectangle(ex_image_dot_label, color=BLACK, stroke_opacity=0, fill_opacity=0.75, buff=0.025)
        ).set_z_index(vector_field.z_index + 1)
        VGroup(ex_dot_label, ex_arrow_label, ex_image_dot_label, vector_field[arrow_ex_index]).set_z_index(vector_field.z_index + 2)
        VGroup(ex_dot, ex_image_dot).set_z_index(vector_field[arrow_ex_index].z_index + 1)

        x_tex = MathTex("x = \\begin{pmatrix} x_1 \\\\ x_2 \\end{pmatrix}").shift(1.6 * RIGHT).scale(tex_scale_factor).set_z_index(plane.z_index + 2)
        f_x_tex = MathTex("\\mapsto f(x) = \\begin{pmatrix} f_1(x_1) \\\\ f_2(x_2) \\end{pmatrix}").scale(tex_scale_factor).next_to(x_tex, RIGHT, buff=tex_buff).set_z_index(plane.z_index + 2)

        rectangle_tex = SurroundingRectangle(VGroup(x_tex, f_x_tex), color=BLACK, stroke_opacity=0, fill_opacity=0.9).set_z_index(x_tex.z_index - 1)

        self.play(Create(plane), Create(unit_circle), run_time=2)

        self.play(
            self.camera.frame.animate.set(width=5).shift(RIGHT),
            unit_circle.animate.set(stroke_width=1),
            run_time=3
        )
        self.wait()
        self.play(
            Create(ex_dot),
            FadeIn(x_tex, ex_dot_label, rectangle_tex)
        )
        self.wait()
        self.play(
            Transform(ex_image_dot, ex_dot_copy),
            GrowArrow(ex_arrow),
            FadeIn(ex_image_dot_label, f_x_tex, ex_arrow_label),
            run_time=2
        )
        self.wait()
        self.play(
            *[GrowArrow(vector_field[k]) for k in range(len(vector_field)) if k != 42],
            FadeIn(rectangles),
            run_time=1.5
        )
        self.wait()
        self.play(FadeOut(ex_dot, ex_image_dot, ex_dot_label, ex_image_dot_label, ex_arrow_label, rectangles))
        self.wait()

        dot_list = VGroup(*[Dot(vector.get_start(), radius=DEFAULT_SMALL_DOT_RADIUS / 2) for vector in vector_field if np.linalg.norm(vector.get_end()) <= 1 and np.linalg.norm(vector.get_start()) <= 1])
        vector_field[arrow_ex_index].set_z_index(vector_field[0].z_index)

        self.play(FadeIn(dot_list))
        self.play(*[dot.animate.shift(rotation(theta) @ dot.get_center() - dot.get_center()) for dot in dot_list])
        self.wait()
        self.play(FadeOut(dot_list))
        self.wait()

        self.play(*[GrowArrow(vector) for vector in vector_field_with_too_many_arrows])
        self.wait()
        self.play(*[GrowArrow(vector, reverse_rate_function=True) for vector in vector_field_with_too_many_arrows])
        self.wait()

        not_valid_index = 69

        self.play(vector_field[not_valid_index].animate.rotate(-PI / 3, about_point=vector_field[not_valid_index].get_start()))
        self.wait()

        cross = Cross(vector_field[not_valid_index], stroke_width=2)

        self.play(GrowFromCenter(cross))
        self.wait()

        self.play(
            AnimationGroup(
                FadeOut(cross),
                vector_field[not_valid_index].animate.rotate(PI / 3, about_point=vector_field[not_valid_index].get_start()),
                lag_ratio=0
            )   
        )
        self.wait()

        moving_dot = Dot(vector_field[69].get_start(), radius=DEFAULT_SMALL_DOT_RADIUS / 2).set_z_index(vector_field[0].z_index + 2)
        dot_pos = moving_dot.get_center()
        moving_arrow = always_redraw(lambda: vector_field.get_vector(moving_dot.get_center()))

        self.play(
            vector_field.animate.set_opacity(0.25),
            Create(VGroup(moving_dot, moving_arrow))
        )
        self.wait()
        self.play(moving_dot.animate.shift(0.05 * RIGHT), run_time=2)
        self.play(MoveAlongPath(moving_dot, Circle(0.05).move_to(dot_pos)), run_time=4)
        self.play(moving_dot.animate.shift(0.05 * LEFT), run_time=2)
        self.play(
            FadeOut(moving_dot, moving_arrow),
            vector_field.animate.set_opacity(1),
            VGroup(x_tex, f_x_tex, rectangle_tex).animate.shift(0.75 * UP)
        )
        self.wait()

        not_continuous_vector_field = ArrowVectorField(
            lambda pos: np.exp(-1/(1 - pos[0]**2 - pos[1]**2)) * ((1 + pos[0]) * RIGHT * (pos[0] >= 0) + (1 - pos[0]) * LEFT * (pos[0] < 0)) * (np.linalg.norm(pos) <= 1),
            x_range=[-1, 1, 0.15],
            y_range=[-1, 1, 0.15],
            vector_config={"stroke_width": 1},
            length_func=lambda norm: norm
        ).set_opacity(0.5)

        moving_dot_bis = Dot(np.array([0.05, 0.05, 0]), radius=DEFAULT_SMALL_DOT_RADIUS / 2).set_z_index(not_continuous_vector_field[0].z_index + 2)
        dot_pos_bis = moving_dot_bis.get_center()
        moving_arrow_bis = always_redraw(lambda: not_continuous_vector_field.get_vector(moving_dot_bis.get_center()))
        oceane = MathTex(
            "f : \\begin{pmatrix} x_1 \\\\ x_2 \\end{pmatrix}", "\\mapsto e^{-\\frac{1}{1 - x_1^2 - x_2^2}} \\displaystyle \\begin{pmatrix} 1 + \\text{sign}(x_1) x_1 \\\\ 0 \\end{pmatrix}"
        ).scale(tex_scale_factor / 1.25).shift(2.25 * RIGHT)
        camille = SurroundingRectangle(oceane, stroke_width=0, color=BLACK, fill_opacity=0.9)
        oceane.set_z_index(camille.z_index + 1)

        self.play(
            ReplacementTransform(vector_field, not_continuous_vector_field),
            FadeIn(oceane, camille)
        )
        self.play(
            FadeIn(moving_dot_bis, moving_arrow_bis)
        )
        self.wait()
        
        self.play(moving_dot_bis.animate.move_to(np.array([-0.05, 0.05, 0])))
        self.play(moving_dot_bis.animate.move_to(np.array([-0.05, -0.05, 0])))
        self.play(moving_dot_bis.animate.move_to(np.array([-0.05, 0, 0])))
        self.play(moving_dot_bis.animate.move_to(dot_pos_bis))
        self.wait()
        self.play(
            FadeOut(moving_dot_bis, moving_arrow_bis),
            ReplacementTransform(not_continuous_vector_field, vector_field_bis),
            VGroup(x_tex, f_x_tex, rectangle_tex).animate.shift(0.75 * DOWN),
            FadeOut(oceane, camille, x_tex, f_x_tex, rectangle_tex),
            self.camera.frame.animate.shift(LEFT),
            run_time=2
        )
        self.wait()


class BrouwersThmIllustration2(MovingCameraScene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-config.frame_width, config.frame_width, 1],
            y_range=[-config.frame_height, config.frame_height, 1],
            x_length=2 * config.frame_width,
            y_length=2 * config.frame_height,
            x_axis_config = {"stroke_width": 0.5},
            y_axis_config = {"stroke_width": 0.5},
            background_line_style={"stroke_width": 0.5}
        )
        unit_circle = Circle(1, color=RED, stroke_width=1)
        self.camera.frame.width = 5

        a = np.array([0.4, 0.6, 0])

        vector_field = ArrowVectorField(
            lambda pos: (fixed_point_func(pos, a) - pos) * (np.linalg.norm(pos) <= 1),
            x_range=[-1, 1, 0.2],
            y_range=[-1, 1, 0.2],
            vector_config={"stroke_width": 0.8},
            length_func=lambda norm: 6 * 0.45 * sigmoid(norm)
        )
        for vector in vector_field:
            vector.scale(1 / 6, scale_tips=True, about_point=vector.get_start())
        
        vector_field.move_to(ORIGIN)
        vector_field.remove(vector_field[85])

        vector_field_model = ArrowVectorField(
            lambda pos: (fixed_point_func(pos, a) - pos) * (np.linalg.norm(pos) <= 1),
            x_range=[-1, 1, 0.2],
            y_range=[-1, 1, 0.2],
            vector_config={"stroke_width": 0.8}
        )

        fixed_point = Dot(a, radius=DEFAULT_SMALL_DOT_RADIUS / 2, color=RED)
        dots_list = VGroup(
            *[Dot(vector.get_start(), radius=DEFAULT_SMALL_DOT_RADIUS / 3, color=YELLOW) for vector in vector_field_model]
        ).sort(submob_func=lambda pos: -pos.get_center()[1])

        self.add(plane, unit_circle, vector_field)
        self.wait()
        self.play(
            AnimationGroup(
                *[FadeIn(dot, shift=Line(dot.get_center(), np.array([0, 0, -4])).get_unit_vector()) for dot in dots_list if np.linalg.norm(dot.get_center()) <= 1 and np.linalg.norm(dot.get_center() - fixed_point.get_center()) >= 0.1],
                lag_ratio=0.05
            ),
            vector_field.animate.set_opacity(0.5),
            run_time=3
        )
        self.wait()
        self.play(FocusOn(fixed_point))
        self.play(
            FadeIn(fixed_point),
            Flash(fixed_point, line_length=0.1, flash_radius=2.5 * fixed_point.radius, line_stroke_width=1, color=RED),
            run_time=1.5
        )
        self.play(
            *[dot.animate.shift(vector_field_model.get_vector(dot.get_center()).get_vector()) for dot in dots_list if np.linalg.norm(dot.get_center()) <= 1 and np.linalg.norm(dot.get_center() - fixed_point.get_center()) >= 0.1],
            fixed_point.animate.shift(vector_field_model.func(fixed_point.get_center())),
            run_time=2
        )
        self.wait()


        compact_convex = SVGMobject("potato_2.svg").set_color(RED).move_to(ORIGIN)
        compact_convex_curve = VMobject(stroke_width=1).start_new_path(compact_convex.get_all_points()[0])
        compact_convex_curve.add_points_as_corners(compact_convex.get_all_points()[1:])
        width, height = compact_convex_curve.width, compact_convex_curve.height
        compact_convex_curve.scale(2 / max(width, height)).stretch(0.95, 0)
        compact_convex.scale(2 / max(width, height), about_point=compact_convex.get_center()).set_stroke(width=1)
        compact_convex.scale(1.5).shift(5 * UR)

        
        self.play(
            self.camera.frame.animate.move_to(compact_convex).scale(1.5),
            Create(compact_convex),
            run_time=2
        )
        self.wait()

        
        a_2 = np.array([0.3, -0.4, 0])

        vector_field_2 = ArrowVectorField(
            lambda pos: (fixed_point_func(pos, a_2) - pos) * (len(Intersection(compact_convex_curve, Dot(pos, radius=DEFAULT_SMALL_DOT_RADIUS / 2)).points) == len(Intersection(compact_convex_curve, Dot(compact_convex_curve.get_center(), radius=DEFAULT_SMALL_DOT_RADIUS / 2)).points)),
            x_range=[-1, 1, 0.15],
            y_range=[-1, 1, 0.15],
            vector_config={"stroke_width": 1},
            length_func=lambda norm: 6 * 0.35 * sigmoid(norm)
        )
        for vector in vector_field_2:
            vector.scale(1/6, scale_tips=True, about_point=vector.get_start())
        
        vector_field_2.scale(1.5).shift(5 * UR).shift(0.1 * RIGHT)
        vector_field_2.remove(*[vector for vector in vector_field_2 if np.linalg.norm(vector.get_vector()) == 0])
        vector_field_2.remove(vector_field_2[8], vector_field_2[48], vector_field_2[75])

        fixed_point_2 = Dot(5 * UR + 1.5 * a_2 + 0.1 * RIGHT + 0.04 * DOWN, radius=1.5 * DEFAULT_SMALL_DOT_RADIUS / 2, color=RED)
        dots_list_2 = VGroup(*[Dot(vector.get_start(), radius=1.5 * DEFAULT_SMALL_DOT_RADIUS / 3, color=YELLOW) for vector in vector_field_2])#.sort(submob_func=lambda pos: -pos.get_center()[1])

        compact_convex.set_z_index(dots_list_2[0].z_index + 1)


        self.play(
            *[GrowArrow(vector) for vector in vector_field_2],
            run_time=1.5
        )
        self.wait()
        self.play(
            AnimationGroup(
                *[FadeIn(dot, shift=Line(dot.get_center(), compact_convex.get_center() - np.array([0, 0, 4])).get_unit_vector()) for dot in dots_list_2],
                lag_ratio=0
            ),
            vector_field_2.animate.set_opacity(0.5),
            run_time=1.5
        )
        self.wait()
        self.play(FocusOn(fixed_point_2))
        self.play(
            FadeIn(fixed_point_2),
            Flash(fixed_point_2, line_length=1.5 * 0.1, flash_radius=1.5 * 2.5 * fixed_point.radius, line_stroke_width=1.5 * 1, color=RED),
            run_time=1.5
        )
        
        self.play(
            *[dots_list_2[k].animate.shift(vector_field_2[k].get_vector()) for k in range(len(dots_list_2))],
            fixed_point_2.animate.shift(vector_field_2.func(fixed_point_2.get_center())),
            run_time=2
        )
        self.wait()
        self.play(FadeIn(Rectangle(width=50, height=50, fill_color=BLACK, fill_opacity=1).set_z_index(100)), run_time=1.5)
        self.wait()





class CoffeeCup(Scene):
    def construct(self):
        pass





### Jeu de Hex


class HexHistory(Scene):
    def construct(self):
        title = Tex("Chapter 3 : \\textsc{Hex} game")
        underline = Underline(title).set_opacity([0, 1, 1, 0])
        title_group = VGroup(title, underline).scale(1.5)
        self.play(FadeIn(title_group), run_time=3)
        self.play(FadeOut(title_group), run_time=2)
        self.wait()

        image_nash, image_hein = SVGMobject("nash.svg"), SVGMobject("hein.svg")
        image_nash.height = config.frame_height/1.25
        image_hein.height = config.frame_height/1.25
        image_nash_rectangle = SurroundingRectangle(image_nash, buff=0).set_z_index(image_nash.z_index + 1)
        image_hein_rectangle = SurroundingRectangle(image_hein, buff=0).set_z_index(image_hein.z_index + 1).next_to(image_nash_rectangle, RIGHT)
        image_hein.move_to(image_hein_rectangle)
        caption_nash = Tex("John Forbes \\textsc{Nash}").next_to(image_nash_rectangle, DOWN)
        caption_hein = Tex("Piet \\textsc{Hein}").next_to(image_hein_rectangle, DOWN)
        Group(image_nash, image_nash_rectangle, caption_nash, image_hein, image_hein_rectangle, caption_hein).move_to(ORIGIN)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Create(image_nash_rectangle),
                    Create(image_hein_rectangle),
                    Write(caption_nash),
                    Write(caption_hein),
                    lag_ratio=0, run_time=5
                ),
                AnimationGroup(
                    *[FadeIn(sub_image) for sub_image in image_nash],   
                    lag_ratio=0.5, run_time=15
                ),
                AnimationGroup(
                    *[FadeIn(sub_image) for sub_image in image_hein],
                    lag_ratio=0.5, run_time=15
                )
            )            
        )
        self.wait(10)
        self.play(FadeOut(image_nash, image_nash_rectangle, caption_nash, image_hein, image_hein_rectangle, caption_hein), run_time=5)
        self.wait()


class HexGame(Scene):
    def construct(self):
        board_image = BoardImage(hexagon_stroke_color=WHITE, sides_stroke_color=WHITE).scale(0.75)
        board_hexagons = board_image[:-4]
        board_sides = board_image[-4:]
        board = Board()

        pawn_radius = 0.8 * board_image.side_length / 2

        h_arrow = DoubleArrow(
            start=board_hexagons[0][0].get_center(), end=board_hexagons[0][-1].get_center(), color=YELLOW
        ).shift(0.75 * UP).stretch(1.15, 0)
        v_arrow = DoubleArrow(
            start=board_hexagons[0][-1].get_center(), end=board_hexagons[-1][-1].get_center(), color=YELLOW
        ).rotate(PI / 3).stretch(1.15, 0).rotate(-PI / 3).shift(0.75 * (np.sqrt(3) / 2 * RIGHT + 1 / 2 * UP))
        h_arrow_label, v_arrow_label = MathTex("11").next_to(h_arrow, UP, buff=0.1), MathTex("11").next_to(v_arrow.get_center(), np.sqrt(3) / 2 * UP + 1 / 2 * RIGHT, buff=0.25)
        
        game_1_w = [(0, 0), (0, 1), (0, 5), (0, 6), (0, 8), (0, 9), (1, 0), (1, 1), (1, 4), (1, 5), (1, 7), (1, 8), (1, 10), (2, 0), (2, 3), (2, 4), (2, 5), (2, 6), (2, 8), (3, 9), (3, 10), (4, 1), (4, 3), (4, 4), (4, 6), (4, 10), (5, 2), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (6, 0), (6, 2), (6, 3), (6, 4), (6, 6), (6, 7), (6, 8), (7, 2), (7, 6), (7, 9), (7, 10), (8, 0), (8, 1), (8, 2), (8, 4), (8, 5), (9, 0), (9, 1), (9, 2), (9, 6), (9, 10), (10, 0), (10, 1), (10, 3), (10, 6), (10, 7), (7, 7)]
        game_1_b = [(k, l) for k in range(11) for l in range(11)]
        for pos in game_1_w:
            game_1_b.remove(pos)
        game_1_b.append((0, 2))
        
        blacks_winning_path = [(5, 0), (5, 1), (4, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (2, 9), (2, 10)]
        white_winning_path = [(0, 9), (1, 8), (2, 8), (2, 9), (3, 9), (3, 10), (4, 10), (5, 9), (5, 8), (5, 7), (5, 6), (5, 5), (5, 4), (6, 3), (7, 2), (8, 2), (9, 2), (10, 1)]

        blacks_winning_pawns = VGroup(*[Dot(board_hexagons[pos[0]][pos[1]].get_center(), color=BLACK, radius=pawn_radius).set_z_index(board_hexagons[0][0].z_index + 1) for pos in blacks_winning_path])
        whites_winning_pawns = VGroup(*[Dot(board_hexagons[pos[0]][pos[1]].get_center(), color=WHITE, radius=pawn_radius).set_z_index(board_hexagons[0][0].z_index + 1) for pos in white_winning_path])

        w_pawns = VGroup(*[Dot(board_hexagons[pos[0]][pos[1]].get_center(), color=WHITE, radius=pawn_radius).set_z_index(board_hexagons[0][0].z_index + 1) for pos in game_1_w])
        b_pawns = VGroup(*[Dot(board_hexagons[pos[0]][pos[1]].get_center(), color=BLACK, radius=pawn_radius).set_z_index(board_hexagons[0][0].z_index + 1) for pos in game_1_b])

        w_pawns_copy, b_pawns_copy = w_pawns.copy(), b_pawns.copy()

        b_pawns_copy[12].set_color(WHITE)
        w_pawns_copy[37].set_color(BLACK)
        #(2, 9) (12) <-> (6, 3) (37)

        rd.shuffle(w_pawns)
        rd.shuffle(b_pawns)

        self.play(
            AnimationGroup(
                *[FadeIn(hexagon, shift=-Line(hexagon.get_center(), np.array([0, 0, -6])).get_unit_vector()) for hexagon in board_hexagons],
                lag_ratio=0.1
                ), run_time=3
        )
        self.wait()
        self.play(*[DrawBorderThenFill(side) for side in board_sides])
        self.wait()
        self.play(
            DrawBorderThenFill(VGroup(h_arrow, v_arrow)),
            Write(VGroup(v_arrow_label, h_arrow_label))
        )
        self.wait()
        self.play(
            FadeOut(h_arrow, v_arrow),
            Unwrite(VGroup(v_arrow_label, h_arrow_label))
        )
        self.wait()

        self.play(FadeIn(w_pawns[0]), run_time=0.5)
        self.wait()
        self.play(FadeIn(b_pawns[0]), run_time=0.5)
        self.wait()
        
        self.add(*[hexagon for hexagon in board_hexagons], w_pawns[0], b_pawns[0])

        self.play(
            AnimationGroup(
                *[AnimationGroup(FadeIn(w_pawns[k]), FadeIn(b_pawns[k]), lag_ratio=0.5) for k in range(1, len(w_pawns))],
                lag_ratio=0.5
            ), run_time=10
        )
        self.wait()

        self.play(
            AnimationGroup(
                *[Indicate(blacks_winning_pawns[k]) for k in range(len(blacks_winning_pawns))],
                lag_ratio=0.2
            ), run_time=2.5
        )
        self.remove(*[blacks_winning_pawns[k] for k in range(len(blacks_winning_pawns))])
        self.wait()
        
        self.play(
            Transform(b_pawns, b_pawns_copy),
            Transform(w_pawns, w_pawns_copy)
        )
        self.wait()

        b_pawns.save_state()
        w_pawns.save_state()
        
        self.play(
            AnimationGroup(
                *[Indicate(whites_winning_pawns[k]) for k in range(len(whites_winning_pawns))],
                lag_ratio=0.2
            ), run_time=2.5
        )
        self.remove(*[pawn for pawn in whites_winning_pawns])
        self.wait()
        self.play(
            AnimationGroup(
                AnimationGroup(
                    b_pawns[12].animate.set_color(BLACK),
                    w_pawns[37].animate.set_color(WHITE),
                    lag_ratio=0
                ),
                AnimationGroup(
                    *[Transform(pawn, board_hexagons[0][0].copy().set_color(BLUE).move_to(pawn)) for pawn in w_pawns]
                ), lag_ratio=1
            )  
        )
        self.play(
            AnimationGroup(
                *[Transform(pawn, board_hexagons[0][0].copy().set_color(DARK_BROWN).move_to(pawn)) for pawn in b_pawns]
            )
        )

        bonhomme = SVGMobject("bonhomme.svg").scale(0.25).set_z_index(w_pawns[0].z_index + 1).move_to(blacks_winning_pawns[0])
        blacks_winning_path_line = VMobject().add(
            *[Line(blacks_winning_pawns[k].get_center(), blacks_winning_pawns[k+1].get_center()) for k in range(len(blacks_winning_pawns) - 1)]
        )
        points_b = []
        for sub in blacks_winning_path_line:
            for point in sub.points:
                points_b.append(point)
        blacks_winning_path_line = blacks_winning_path_line.set_points_as_corners(points_b)

        whites_winning_path_line = VMobject().add(
            *[Line(whites_winning_pawns[k].get_center(), whites_winning_pawns[k+1].get_center()) for k in range(len(whites_winning_pawns) - 1)]
        )
        points_w = []
        for sub in whites_winning_path_line:
            for point in sub.points:
                points_w.append(point)
        whites_winning_path_line = whites_winning_path_line.set_points_as_corners(points_w)

        self.wait()
        self.play(FadeIn(bonhomme))
        self.wait()
        self.play(MoveAlongPath(bonhomme, blacks_winning_path_line), run_time=3)
        self.wait()
        self.play(
            b_pawns[12].animate.set_color(BLUE).set_z_index(b_pawns[0][0].z_index - 1),
            w_pawns[37].animate.set_color(DARK_BROWN),
            bonhomme.animate.move_to(whites_winning_pawns[0])
        )
        self.wait()
        self.play(MoveAlongPath(bonhomme, whites_winning_path_line), run_time=3)
        self.wait()
        self.play(
            b_pawns.animate.restore(),
            w_pawns.animate.restore(),
            FadeOut(bonhomme)
        )


class HexThmProof(Scene):
    def construct(self):
        board_image = BoardImage(hexagon_stroke_color=WHITE, sides_stroke_color=WHITE).scale(0.75)
        board_hexagons = board_image[:-4]
        board_sides = board_image[-4:]

        pawn_radius = 0.8 * board_image.side_length / 2

        game_1_w = [(0, 0), (0, 1), (0, 5), (0, 6), (0, 8), (0, 9), (1, 0), (1, 1), (1, 4), (1, 5), (1, 7), (1, 8), (1, 10), (2, 0), (2, 3), (2, 4), (2, 5), (2, 6), (2, 8), (2, 9), (3, 9), (3, 10), (4, 1), (4, 3), (4, 4), (4, 6), (4, 10), (5, 2), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (6, 0), (6, 2), (6, 3), (6, 6), (6, 7), (6, 8), (7, 2), (7, 6), (7, 7), (7, 9), (7, 10), (8, 0), (8, 1), (8, 2), (8, 4), (8, 5), (9, 0), (9, 1), (9, 2), (9, 6), (9, 10), (10, 0), (10, 1), (10, 3), (10, 6), (10, 7)]
        game_1_b = [(k, l) for k in range(11) for l in range(11)]
        for pos in game_1_w:
            game_1_b.remove(pos)
        game_1_b.append((0, 2))
        
        blacks_winning_path = [(3, 0), (2, 1), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (2, 9), (1, 9), (0, 10)]
        white_winning_path = [(0, 9), (1, 8), (2, 8), (2, 9), (3, 9), (3, 10), (4, 10), (5, 9), (5, 8), (5, 7), (5, 6), (5, 5), (5, 4), (6, 3), (7, 2), (8, 2), (9, 2), (10, 1)]

        blacks_winning_pawns = VGroup(*[Dot(board_hexagons[pos[0]][pos[1]].get_center(), color=BLACK, radius=pawn_radius).set_z_index(board_hexagons[0][0].z_index + 1) for pos in blacks_winning_path])
        whites_winning_pawns = VGroup(*[Dot(board_hexagons[pos[0]][pos[1]].get_center(), color=WHITE, radius=pawn_radius).set_z_index(board_hexagons[0][0].z_index + 1) for pos in white_winning_path])

        w_pawns = VGroup(*[Dot(board_hexagons[pos[0]][pos[1]].get_center(), color=WHITE, radius=pawn_radius).set_z_index(board_hexagons[0][0].z_index + 1) for pos in game_1_w])
        b_pawns = VGroup(*[Dot(board_hexagons[pos[0]][pos[1]].get_center(), color=BLACK, radius=pawn_radius).set_z_index(board_hexagons[0][0].z_index + 1) for pos in game_1_b])
        

        label_1 = MathTex("1").move_to(board_sides[0]).shift(0.75 * UP)
        label_2 = MathTex("2").move_to(board_sides[3]).shift(0.75 * (0.5 * UP + np.sqrt(3)/2 * RIGHT))
        label_3 = MathTex("3").move_to(board_sides[1]).shift(0.75 * DOWN)
        label_4 = MathTex("4").move_to(board_sides[2]).shift(0.75 * (0.5 * DOWN + np.sqrt(3)/2 * LEFT))
        sides_labels = VGroup(label_1, label_2, label_3, label_4)

        cross = Cross(w_pawns[19]).set_z_index(w_pawns[0].z_index + 1)

        self.add(board_hexagons, board_sides, w_pawns, b_pawns)
        self.wait()
        self.play(
            AnimationGroup(
                *[Write(label) for label in sides_labels],
                lag_ratio=0.5
            )
        )
        self.wait()
        self.play(
            AnimationGroup(
                Indicate(VGroup(label_1, label_3), scale_factor=1.05), Indicate(VGroup(label_2, label_4), scale_factor=1.05), lag_ratio=1
            ), run_time=3
        )
        non_relied_to_1_pawns_1 = VGroup(*b_pawns, w_pawns[22], w_pawns[35], w_pawns[44], w_pawns[45], w_pawns[54], w_pawns[55], w_pawns[58], w_pawns[59], w_pawns[60])
        non_relied_to_1_pawns_2 = VGroup(*w_pawns[19:], b_pawns[37], w_pawns[12]).remove(*[pawn for pawn in non_relied_to_1_pawns_1 if pawn in w_pawns])

        self.wait()
        self.play(FadeOut(non_relied_to_1_pawns_1), run_time=2)
        self.wait()
        self.play(
            AnimationGroup(
                *[Indicate(whites_winning_pawns[k]) for k in range(len(whites_winning_pawns))],
                lag_ratio=0.2
            ), run_time=2.5
        )
        self.remove(*whites_winning_pawns)
        b_pawns[37].set_color(WHITE)
        self.wait()
        self.play(
            w_pawns[19].animate.set_color(BLACK),
            FadeIn(b_pawns[37])
        )
        self.play(FadeIn(cross, shift=np.array([0, 0, -1])))
        self.wait()
        self.play(
            FadeOut(cross),
            FadeOut(non_relied_to_1_pawns_2)
        )
        self.wait()
        b_adjacent_boxes = VGroup(*b_pawns[:22], w_pawns[19]).remove(*[b_pawns[1], b_pawns[12], b_pawns[14]])
        board_hexagons[0][2].set_z_index(board_hexagons[0][2].z_index + 1)
        self.play(Indicate(board_hexagons[0][2]), run_time=1.5)
        board_hexagons[0][2].set_z_index(board_hexagons[0][2].z_index - 1)
        self.wait()
        self.play(FadeIn(b_adjacent_boxes[0]))
        self.wait()
        self.play(FadeIn(*[b_adjacent_boxes[k] for k in range(1, len(b_adjacent_boxes))]), run_time=2)
        self.wait()
        self.play(
            AnimationGroup(
                *[Indicate(blacks_winning_pawns[k]) for k in range(len(blacks_winning_pawns))],
                lag_ratio=0.2
            ), run_time=2.5
        )
        self.remove(*blacks_winning_pawns)
        self.wait()
        self.play(FadeOut(b_adjacent_boxes[3]), w_pawns[5].animate.set_color(BLACK))
        self.wait()
        self.play(Indicate(board_sides[0]))
        self.wait()
        self.play(FadeIn(b_pawns[1], b_adjacent_boxes[3]))
        self.wait()
        blacks_winning_path_2 = [pawn for pawn in blacks_winning_path]
        blacks_winning_path_2.append((0, 10))
        blacks_winning_path_2[-2] = 0, 9
        blacks_winning_pawns_2 = VGroup(*[Dot(board_hexagons[pos[0]][pos[1]].get_center(), color=BLACK, radius=pawn_radius).set_z_index(board_hexagons[0][0].z_index + 1) for pos in blacks_winning_path_2])
        self.play(
            AnimationGroup(
                *[Indicate(blacks_winning_pawns[k]) for k in range(len(blacks_winning_pawns))],
                lag_ratio=0.2
            ), run_time=2.5
        )
        rectangle = SurroundingRectangle(board_image, color=BLACK, fill_color=BLACK, fill_opacity=1).set_z_index(w_pawns[0].z_index + 1)
        self.wait()
        self.play(blacks_winning_pawns_2.animate.set_color(YELLOW))
        self.wait()
        self.play(
            AnimationGroup(
                Unwrite(VGroup(label_1, label_2, label_3, label_4)),
                FadeIn(rectangle),
                lag_ratio=0.5
            )
        )
        hex_thm_recap = MathTex(
            "&\\forall B, W \\subset \\mathcal{B}_k,", "\\hspace{0.075cm} \\mathcal{B}_k \\subset B \\cup W, \\\\",
            "&\\exists \\text{path} \\subset B, \\hspace{0.1cm} \\text{path connects} \\hspace{0.1cm} B \\hspace{0.1cm} \\text{edges or} \\\\",
            "&\\exists \\text{path} \\subset W, \\hspace{0.1cm} \\text{path connects} \\hspace{0.1cm} W \\hspace{0.1cm} \\text{edges}."
        ).scale(1.25).set_z_index(rectangle.z_index + 1)
        VGroup(hex_thm_recap[0][1], hex_thm_recap[1][3], hex_thm_recap[2][6], hex_thm_recap[2][20]).set_color(BLACK).set_stroke(color=WHITE, width=0.75)

        self.play(FadeIn(hex_thm_recap[0]))
        self.wait()
        self.play(FadeIn(hex_thm_recap[1]))
        self.wait()
        self.play(FadeIn(hex_thm_recap[2]))
        self.wait()
        self.play(FadeIn(hex_thm_recap[3]))
        self.wait()
        self.play(FadeOut(*hex_thm_recap))
        self.wait()
        title = Tex(
            "Chapter 4 : \\textsc{Brouwer}'s theorem proof"
        ).set_z_index(rectangle.z_index + 1).scale(0.9)
        underline = Underline(title).set_opacity([0, 1, 1, 0]).set_z_index(title.z_index)
        title_group = VGroup(title, underline).scale(1.5)
        self.play(FadeIn(title_group), run_time=3)
        self.play(FadeOut(title_group), run_time=2)
        self.wait()
        




### Démo Brouwer


class Requirements(Scene):
    def construct(self):
        list = Tex(
            "\\begin{itemize} \\item Uniform Continuity \\item Heine's theorem \\item Boundedness theorem \\end{itemize}"
        ).scale(1.5)
        self.wait()
        self.play(FadeIn(list))
        self.wait(3)
        self.play(FadeOut(list))
        self.wait()


a = np.array([-0.45, 0.35, 0])

#Ajouter champ de vecteurs sur la patate
class BrouwersThmProof1(MovingCameraScene):
    def construct(self):
        scale_factor = 2.5
        plane = NumberPlane(
            x_range = [-config["frame_x_radius"],config["frame_x_radius"], 0.5],
            y_range =[-config["frame_y_radius"], config["frame_y_radius"], 0.5],
            background_line_style={"stroke_opacity": 0.5}
        ).scale(scale_factor).shift(3 * LEFT)
        unit_circle = Square(color=RED).move_to(plane.c2p(0, 0)).scale(scale_factor)
        compact_convex = SVGMobject("potato.svg").flip().set_color(RED)
        width, height = compact_convex.width, compact_convex.height
        proportion_x, proportion_y = 2 / width, 1 / height
        compact_convex.scale(2 / width)
        compact_convex_curve = VMobject().start_new_path(compact_convex.get_all_points()[0])
        compact_convex_curve.add_points_as_corners(compact_convex.get_all_points()[1:])

        compact_convex.scale(2.5 * width / 2).shift(13 * LEFT + 5 * UP)

        compact_convex_for_transform = compact_convex.generate_target().set_z_index(compact_convex.z_index + 1)

        vector_field = ArrowVectorField(
            lambda pos: fixed_point_func(pos, a) - pos,
            x_range=[-1, 1, 0.25],
            y_range=[-1, 1, 0.25],
            vector_config={"stroke_width": 1},
            length_func=lambda norm: 6 * 0.55 * sigmoid(norm)
        ).scale(scale_factor).shift(3 * LEFT)

        for vector in vector_field:
            vector.scale(1/6, scale_tips=True, about_point=vector.get_start())

        vector_field.move_to(plane.c2p(0, 0))

        vector_field_in_compact_convex = ArrowVectorField(
            lambda pos: (fixed_point_func(pos, (proportion_x * LEFT + proportion_y * UP)/2.5) - pos) * (len(Intersection(compact_convex_curve, Dot(pos, radius=DEFAULT_SMALL_DOT_RADIUS)).points) == len(Intersection(compact_convex_curve, Dot((proportion_x * LEFT + proportion_y * UP)/2.5, radius=DEFAULT_SMALL_DOT_RADIUS)).points)),
            x_range=[-1, 1, 0.17],
            y_range=[-1, 1, 0.12],
            vector_config={"stroke_width": 1},
            length_func=lambda norm: 12 * 0.45 * sigmoid(norm)
        ).scale(2.5 * width / 2).shift(13 * LEFT + 5 * UP).set_z_index(plane.z_index + 1)

        for vector in vector_field_in_compact_convex:
            vector.scale(1 / 12, scale_tips=True, about_point=vector.get_start())

        vector_field_in_compact_convex.move_to(compact_convex.get_center())
        vector_field_in_compact_convex_for_transform = vector_field_in_compact_convex.copy()

        compact_convex_label = MathTex("K'", color=RED).next_to(compact_convex, UR, buff=-0.15).shift(0.35 * DL).shift(0.1 * DOWN)
        unit_circle_label = MathTex("K", color=RED).next_to(unit_circle, UL)
        arrow_K_p_K = CurvedArrow(plane.c2p(-2.25, 2.75), plane.c2p(0, 1.35), color=YELLOW)
        arrow_K_p_K.flip(arrow_K_p_K.get_end() - arrow_K_p_K.get_start())
        arrow_K_p_K_label = MathTex(
            "\\varphi", color=YELLOW
        ).move_to(arrow_K_p_K.point_from_proportion(0.5)).shift(0.3 * UP + 0.6 * RIGHT)

        fixed_dot = Dot(plane.c2p(*a), color=GREEN).set_z_index(vector_field[0].z_index + 2)
        fixed_dot_label = MathTex(
            "f(","x", ") = ", "x"
        ).scale(0.9).next_to(fixed_dot, UR).set_z_index(vector_field[0].z_index + 2)
        fixed_dot_label[1:5:2].set_color(GREEN)
        rectangle_fixed_dot = SurroundingRectangle(
            VGroup(fixed_dot, fixed_dot_label), color=BLACK, stroke_opacity=0, fill_opacity=0.8, buff=0.2
        ).set_z_index(vector_field[0].z_index + 1)

        fixed_dot_in_compact_convex = Dot(compact_convex.get_center() + 1.15 *  LEFT + 0.85 * UP, color=YELLOW).set_z_index(vector_field_in_compact_convex.z_index + 1)
        fixed_dot_in_compact_convex_label = MathTex(
            "g(", "\\varphi^{-1}", "(", "x", ")) = ", "\\varphi^{-1}", "(", "x", ")"
        ).next_to(fixed_dot_in_compact_convex, UP).set_z_index(compact_convex.z_index + 2)
        rectangle_compact_convex_fixed_dot = SurroundingRectangle(
            fixed_dot_in_compact_convex_label, color=BLACK, stroke_opacity=0, fill_opacity=0.8
        ).set_z_index(compact_convex.z_index + 1)
        fixed_dot_in_compact_convex_label[1:9:4].set_color(YELLOW)
        fixed_dot_in_compact_convex_label[3:11:4].set_color(GREEN)

        arrow_fixed_points = CurvedArrow(plane.c2p(-1.25, 0), plane.c2p(-3, 0.8), color=YELLOW).set_z_index(rectangle_fixed_dot.z_index + 1).shift(0.25 * DOWN)
        arrow_fixed_points.flip(arrow_fixed_points.get_end() - arrow_fixed_points.get_start())
        arrow_fixed_points_label = MathTex(
            "\\varphi^{-1}", color=YELLOW
        ).move_to(arrow_fixed_points.point_from_proportion(0.5)).shift(0.4 * DOWN + 0.6 * LEFT)

        self.camera.frame.save_state()

        tex_f = MathTex("f : ", "K", " \\to", " K ", "\hspace{0.2cm} \\text{continuous}")
        tex_f[-1].set_color(BLUE)
        tex_f[1:5:2].set_color(RED)
        tex_K = MathTex(
            "K", " = \\mathcal{B}_{||\\cdot||_{\\infty}}(0, 1) =  \\{u \\in \\mathbb{R}^2, ||u||_{\\infty} = 1\\}"
        ).next_to(tex_f, DOWN, buff=0.5)
        tex_inf_norm = MathTex("||x = (x_1, x_2)||_{\\infty} = \\max{(|x_1|, |x_2|)}").next_to(tex_K, DOWN, buff=0.5)
        tex_K[0].set_color(RED)
        tex_convex_compact = Tex(
            "$K' \\subset \\mathbb{R}^2$ non-empty convex compact \\\\ \\vspace{0.1cm} $\\downarrow$ \\vspace{0.1cm} \\\\ $\\exists$",
            "$\\varphi$ ", "$ : $", " $ K' $", " $ \\to $", " $ K $ ", " an ", "\\emph{homeomorphism}"
        ).next_to(tex_inf_norm, DOWN, buff=0.75)
        VGroup(tex_convex_compact[0][0:2], *tex_convex_compact[3:5:2], tex_convex_compact[5]).set_color(RED)
        tex_convex_compact[1].set_color(YELLOW)
        
        tex_fixed_point = Tex(
            "$g : $", " $ K' $ ", " $ \\to $ ", " $ K'$", ", \\hspace{0.05cm} $f = \\varphi \\circ g \\circ \\varphi^{-1}$",
            "\\\\ \\vspace{0.1cm} $\\downarrow$ \\vspace{0.1cm} \\\\ $f(x) = x \\iff g(\\varphi^{-1}(x)) = \\varphi^{-1}(x)$"
        ).next_to(tex_convex_compact, DOWN, buff=0.75)
        tex_fixed_point[1:5:2].set_color(RED)
        VGroup(tex_fixed_point[4][3], tex_fixed_point[4][7:10]).set_color(YELLOW)
        VGroup(tex_fixed_point[5][11:13], tex_fixed_point[5][19:22]).set_color(YELLOW)
        VGroup(tex_fixed_point[5][3:9:3], tex_fixed_point[5][15:31:8]).set_color(GREEN)
        tex_group = VGroup(tex_f, tex_K, tex_convex_compact, tex_fixed_point, tex_inf_norm).scale(0.75).move_to(plane.c2p(0, 0)).to_edge(RIGHT).set_z_index(plane.z_index + 3)
        tex_group_rectangle = SurroundingRectangle(tex_group, color=BLACK, stroke_opacity=0, fill_opacity=0.8, buff=0.2).set_z_index(plane.z_index + 2)

        self.play(
            FadeIn(plane),
            Create(unit_circle),
            Write(unit_circle_label),
            run_time=2
        )
        self.wait()
        self.play(
            Write(tex_f),
            FadeIn(tex_group_rectangle),
            *[GrowArrow(vector) for vector in vector_field], run_time=2
        )
        self.play(Write(tex_K), run_time=3)
        self.play(Write(tex_inf_norm), run_time=2.5)
        self.wait()
        self.play(Write(tex_convex_compact), run_time=4)
        self.wait()
        self.play(Indicate(tex_convex_compact[-1]), run_time=2)
        self.wait()
        self.play(self.camera.frame.animate.scale(2).shift(2 * UP + 5 * LEFT), run_time=2)
        self.wait()
        self.play(
            Create(compact_convex),
            Write(compact_convex_label), run_time=3
        )
        self.wait()
        self.play(
            *[GrowArrow(vector) for vector in vector_field_in_compact_convex], run_time=2
        )
        self.wait()
        self.play(
            Transform(compact_convex_for_transform, unit_circle),
            Transform(vector_field_in_compact_convex_for_transform, vector_field),
            Create(arrow_K_p_K, ),
            Write(arrow_K_p_K_label),
            compact_convex.animate.set_stroke_opacity(0.5),
            run_time=3
        )
        self.wait()
        self.play(self.camera.frame.animate.restore(), run_time=2)
        self.camera.frame.save_state()
        self.wait()
        self.play(Write(tex_fixed_point[:-1]), run_time=4)
        self.wait()
        self.play(Write(tex_fixed_point[-1]), run_time=4)
        self.play(Create(fixed_dot), Write(fixed_dot_label), FadeIn(rectangle_fixed_dot), run_time=2)
        self.wait()
        self.play(
            self.camera.frame.animate.scale(2).shift(2 * UP + 5 * LEFT),
            Create(arrow_fixed_points),
            Write(arrow_fixed_points_label),
            run_time=2
        )
        self.play(
            Create(fixed_dot_in_compact_convex),
            Write(fixed_dot_in_compact_convex_label),
            FadeIn(rectangle_compact_convex_fixed_dot), 
            run_time=2
        )
        self.wait()
        self.play(
            self.camera.frame.animate.restore(),
            AnimationGroup(
                FadeOut(fixed_dot_in_compact_convex, fixed_dot_in_compact_convex_label, rectangle_compact_convex_fixed_dot),
                FadeOut(
                    compact_convex, arrow_fixed_points, arrow_fixed_points_label, arrow_K_p_K, arrow_K_p_K_label, fixed_dot,
                    fixed_dot_label, tex_group, tex_group_rectangle, rectangle_fixed_dot, vector_field_in_compact_convex
                ), lag_ratio=0.1
            ), run_time=2
        )
               

class BrouwersThmProof2(MovingCameraScene):
    def construct(self):
        scale_factor = 2.5
        plane = NumberPlane(
            x_range = [-config["frame_x_radius"],config["frame_x_radius"], 0.5],
            y_range =[-config["frame_y_radius"], config["frame_y_radius"], 0.5],
            background_line_style={"stroke_opacity": 0.5}
        ).scale(scale_factor).shift(3 * LEFT)
        unit_circle = Square(color=RED).move_to(plane.c2p(0, 0)).scale(scale_factor)
        unit_circle_label = MathTex("K", color=RED).next_to(unit_circle, UL)   

        vector_field = ArrowVectorField(
            lambda pos: fixed_point_func(pos, a) - pos,
            x_range=[-1, 1, 0.25],
            y_range=[-1, 1, 0.25],
            vector_config={"stroke_width": 1},
            length_func=lambda norm: 6 * 0.55 * sigmoid(norm)
        )
        vector_field.scale(scale_factor).shift(3 * LEFT)

        for vector in vector_field:
            vector.scale(1/6, scale_tips=True, about_point=vector.get_start())

        vector_field.move_to(plane.c2p(0, 0))

        heine_thm = Tex("\\textsc{Heine}'s thm \\\\", "$\\downarrow$ \\\\", " $f$ is uniformly continuous over ", " $K$").scale(0.9)
        heine_thm[-1].set_color(RED)
        uc_tex = MathTex(
            "\\forall \\varepsilon > 0, \\exists \\delta > 0, \\forall x, y \\in ",
            "K \\\\",
            "||x-y||_{\\infty} \\leqslant \\delta \\implies ||f(x)-f(y)||_{\\infty} \\leqslant \\varepsilon"
        )
        uc_tex[1].set_color(RED)
        uc_tex[0:2].scale(0.9).next_to(heine_thm, DOWN, buff=1)
        uc_tex[-1].scale(0.75).next_to(uc_tex[0:2], DOWN, buff=0.3)
        tex_group = VGroup(heine_thm, uc_tex).move_to(ORIGIN).to_edge(RIGHT).set_z_index(plane.z_index + 2) 
        tex_rectangle = SurroundingRectangle(tex_group, color=BLACK, fill_opacity=0.8, stroke_width=0, buff=0.2).set_z_index(plane.z_index + 1)

        self.add(plane, unit_circle, unit_circle_label, vector_field)
        self.wait()
        self.play(Write(heine_thm), FadeIn(tex_rectangle), run_time=3)
        self.wait()
        self.play(Write(uc_tex), run_time=6)
        self.wait()

        window = Rectangle(
            fill_color=BLACK, fill_opacity=0.9, height=0.8 * 8, width=0.8 * 14
        ).set_z_index(tex_group.z_index + 1)
        axes = Axes(
            x_range=[0, 4], y_range=[0, 4], x_length=0.75 * window.height, y_length=0.8 * window.height, tips=False
        ).set_z_index(window.z_index + 1)
        inv_curve = axes.plot(lambda x: 1/x, x_range=[1 / 4, 4, 0.01], color=RED).set_z_index(axes.z_index + 1)
        inv_label = MathTex("\\frac{1}{\\cdot}", color=RED).scale(0.8).next_to(inv_curve.get_end(), RIGHT).set_z_index(window.z_index + 1)
        root_curve = axes.plot(np.sqrt, x_range=[0, 4, 0.01], color=BLUE).set_z_index(axes.z_index + 1)
        root_label = MathTex("\\sqrt{\\cdot}", color=BLUE).scale(0.8).next_to(root_curve.get_end(), RIGHT).set_z_index(window.z_index + 1)

        x = ValueTracker(0.5)
        epsilon = ValueTracker(0.4)

        class UniformContinuityWindow(VMobject):
            def __init__(
                self,
                x: float,
                epsilon: float,
                delta: float,
                axes: Axes,
                function: Callable[[float], float],
                curve: ParametricFunction,
                add_labels: bool = False,
                **kwargs
            ):
                self.x = x
                self.epsilon = epsilon
                self.delta = delta
                self.axes = axes
                self.f = function
                self.curve = curve
                self.up_line, self.down_line = self.get_lines()
                super().__init__(**kwargs)
                self.add(*self.get_lines())
                self.add(Polygon(
                        self.up_line.get_start(), self.up_line.get_end(), self.down_line.get_end(), self.down_line.get_start(),
                        color=self.curve.color, fill_opacity=0.5, stroke_width=0
                    )
                )
                self.set_z_index(self.curve.z_index + 1)
                if add_labels:
                    self.add(*self.get_labels())
            
            def get_lines(self):
                up_line = Line(
                    self.axes.c2p(0, 0), self.axes.c2p(0.8 * 2 * self.delta, 0), color=self.curve.color
                ).move_to(self.axes.c2p(self.x, self.f(self.x) + self.epsilon))
                down_line = Line(
                    self.axes.c2p(0, 0), self.axes.c2p(0.8 * 2 * self.delta, 0), color=self.curve.color
                ).move_to(self.axes.c2p(self.x, self.f(self.x) - self.epsilon))
                return up_line, down_line

            def get_labels(self):
                return VGroup(*self.get_epsilon_label(), *self.get_delta_label())
                
            def get_epsilon_label(self):
                self.epsilon_brace = Brace(Line(self.up_line.get_start(), self.down_line.get_start()), direction=LEFT, buff=0.1)
                self.epsilon_brace_label = MathTex("2\\varepsilon").scale(0.65).next_to(self.epsilon_brace, LEFT, buff=0.15)
                self.epsilon_label = VGroup(self.epsilon_brace, self.epsilon_brace_label).set_z_index(self.z_index + 1)
                self.epsilon_rectangle = SurroundingRectangle(self.epsilon_label, color=BLACK, fill_opacity=0.5, stroke_width=0, buff=0.05).set_z_index(self.z_index)
                self.epsilon_label.add(self.epsilon_rectangle)
                return self.epsilon_label

            def get_delta_label(self):
                self.delta_brace = Brace(self.down_line, direction=DOWN, buff=0.1)
                self.delta_brace_label = MathTex("< 2\\delta").scale(0.65).next_to(self.delta_brace, DOWN, buff=0.15)
                self.delta_label = VGroup(self.delta_brace, self.delta_brace_label).set_z_index(self.z_index + 1)
                self.delta_rectangle = SurroundingRectangle(self.delta_label, color=BLACK, fill_opacity=0.5, stroke_width=0, buff=0.05).set_z_index(self.z_index)
                self.delta_label.add(self.delta_rectangle)
                return self.delta_label
                
        root_window = always_redraw(lambda: UniformContinuityWindow(x.get_value(), epsilon.get_value(), epsilon.get_value()**2, axes, np.sqrt, root_curve, add_labels=True))
        x_dot = Dot().set_z_index(root_window.z_index + 1).add_updater(lambda dot: dot.move_to(axes.c2p(x.get_value(), np.sqrt(x.get_value()))))

        self.play(GrowFromCenter(window), run_time=1.5)
        self.play(FadeIn(axes))
        self.wait()
        self.play(Create(root_curve), Write(root_label), run_time=1.5)
        self.wait()
        self.play(FadeIn(root_window, x_dot))
        self.wait()
        self.play(x.animate.set_value(4), run_time=4)
        self.wait()
        self.play(epsilon.animate.set_value(0.25))
        self.play(x.animate.set_value(0), run_time=2)
        self.play(x.animate.set_value(4), run_time=2)
        self.play(epsilon.animate.set_value(0.5))
        self.wait()

        root_window.clear_updaters()
        x_dot.clear_updaters()

        inv_window = always_redraw(lambda: UniformContinuityWindow(x.get_value(), epsilon.get_value(), epsilon.get_value()**2, axes, lambda x: 1 / x, inv_curve, add_labels=True))

        self.play(
            Transform(root_window, inv_window.generate_target()),
            ReplacementTransform(root_curve, inv_curve),
            ReplacementTransform(root_label, inv_label),
            x_dot.animate.move_to(axes.c2p(x.get_value(), 1 / x.get_value()))
        )
        self.wait()
        self.remove(root_window)
        self.add(inv_window)
        
        x_dot.add_updater(lambda dot: dot.move_to(axes.c2p(x.get_value(), 1 / x.get_value())))

        self.play(x.animate.set_value(0.6), run_time=4)
        self.wait()
        self.play(epsilon.animate.set_value(0.25))
        self.wait()
        self.play(x.animate.set_value(0.28))
        self.wait()
        self.play(FadeOut(inv_curve, inv_label, x_dot, inv_window, axes))
        self.play(GrowFromCenter(window), reverse_rate_function=True)
        self.wait()


class BrouwersThmProof3(MovingCameraScene):
    def construct(self):
        scale_factor = 2.5
        plane = NumberPlane(
            x_range = [-config["frame_x_radius"],config["frame_x_radius"], 0.5],
            y_range =[-config["frame_y_radius"], config["frame_y_radius"], 0.5],
            background_line_style={"stroke_opacity": 0.5}
        ).scale(scale_factor).shift(3 * LEFT)
        unit_distance_conversion = np.linalg.norm(plane.c2p(1, 0) - plane.c2p(0, 0))

        unit_circle = Square(color=RED).move_to(plane.c2p(0, 0)).scale(scale_factor)
        unit_circle_label = MathTex("K", color=RED).next_to(unit_circle, UL)   

        vector_field = ArrowVectorField(
            lambda pos: fixed_point_func(pos, a) - pos,
            x_range=[-1, 1, 0.25],
            y_range=[-1, 1, 0.25],
            vector_config={"stroke_width": 1},
            length_func=lambda norm: 6 * 0.55 * sigmoid(norm)
        )
        vector_field_target = vector_field.generate_target()
        vector_field_target.length_func = lambda norm: 0.55 * sigmoid(norm)
        
        vector_field.scale(scale_factor).shift(3 * LEFT)

        for vector in vector_field:
            vector.scale(1/6, scale_tips=True, about_point=vector.get_start())

        vector_field.move_to(plane.c2p(0, 0))  

        def get_delta(epsilon: float, dx: float, plane: NumberPlane, vector_field: ArrowVectorField) -> float:
            delta_list = []

            for x in it.product(np.arange(-1 + dx, 1, dx), np.arange(-1 + dx, 1, dx)):
                x = np.hstack((x, 0))
                delta_x = 0
                f_x = vector_field.get_vector(x).get_end()

                for ring_size in np.arange(dx / 4, dx + dx / 4, dx / 4):
                    ring = Square(side_length=2 * ring_size * unit_distance_conversion).move_to(plane.c2p(x[0], x[1]))
                    points = [ring.point_from_proportion(k/ring_size) for k in np.arange(0, ring_size, ring_size / 5)]
                    for y in points:
                        f_y = vector_field.get_vector(np.hstack((plane.p2c(y), 0))).get_end()
                        if inf_norm(f_x - f_y) <= epsilon:
                            delta_x = inf_norm(x - y)
           
                delta_list.append(delta_x)
            return min(delta_list)

        heine_thm = Tex("\\textsc{Heine}'s thm \\\\", "$\\downarrow$ \\\\", " $f$ is uniformly continuous over ", " $K$").scale(0.9)
        heine_thm[-1].set_color(RED)
        uc_tex = MathTex(
            "\\forall \\varepsilon > 0, \\exists \\delta > 0, \\forall x, y \\in ",
            "K \\\\",
            "||x-y||_{\\infty} \\leqslant \\delta \\implies ||f(x)-f(y)||_{\\infty} \\leqslant \\varepsilon"
        )
        uc_tex[1].set_color(RED)
        uc_tex[0:2].scale(0.9).next_to(heine_thm, DOWN, buff=1)
        uc_tex[-1].scale(0.75).next_to(uc_tex[0:2], DOWN, buff=0.3)
        tex_group = VGroup(heine_thm, uc_tex).move_to(ORIGIN).to_edge(RIGHT).set_z_index(plane.z_index + 2) 
        tex_rectangle = SurroundingRectangle(tex_group, color=BLACK, fill_opacity=0.8, stroke_width=0, buff=0.2).set_z_index(plane.z_index + 1)

        self.add(plane, unit_circle, unit_circle_label, vector_field, tex_group, tex_rectangle)
        self.wait()

        epsilon = 0.20
        delta = 0.27#min(get_delta(epsilon, 0.1, plane, vector_field_target), 0.2)
        board_size = int(np.ceil(2/delta))

        class UniformContinuityBoxes(VMobject):
            def __init__(self, point: np.ndarray, side_length: float, color: str, label: str, brace_position: str = 'UP', **kwargs):
                super().__init__(**kwargs)
                self.point = point
                self.side_length = side_length
                self.color = color
                self.label = label
                self.brace_position = brace_position
                self.box = Square(self.side_length * unit_distance_conversion, color=self.color).move_to(plane.c2p(*self.point))
                self.brace = Brace(
                    Line(
                        plane.c2p(point[0], point[1] + int(((self.brace_position == 'UP') - (self.brace_position == 'DOWN'))) * self.side_length / 2),
                        plane.c2p(point[0] + self.side_length / 2, point[1] + int(((self.brace_position == 'UP') - (self.brace_position == 'DOWN'))) * self.side_length / 2)
                    ), UP * (self.brace_position == 'UP') + DOWN * (self.brace_position == 'DOWN'), buff=0, color=self.color
                )
                self.brace_label = MathTex(
                    self.label, color=self.color
                ).scale(0.6).next_to(self.brace, UP * (self.brace_position == 'UP') + DOWN * (self.brace_position == 'DOWN'), buff=0.15)
                self.brace_label_rectangle = SurroundingRectangle(
                    VGroup(self.brace, self.brace_label), color=BLACK, fill_opacity=0.75, stroke_width=0, buff=0.05
                )
                self.add(self.box, self.brace, self.brace_label, self.brace_label_rectangle)
                self.set_z_index(vector_field.z_index + 1)
                VGroup(self.brace, self.brace_label, self.box).set_z_index(self.z_index + 1)
        
        delta_box_init = UniformContinuityBoxes(np.array([0.3, 0.2, 0]), delta, GREEN, "\\delta", brace_position='DOWN')
        epsilon_box_init = UniformContinuityBoxes(
            vector_field_target.get_vector(np.hstack((plane.p2c(delta_box_init.box.get_center()), 0))).get_end(),
            epsilon, PURPLE, "\\varepsilon"
        )

        self.play(
            Indicate(uc_tex[0][1], scale_factor=1.5, color=PURPLE),
            Indicate(uc_tex[0][6], scale_factor=1.5, color=GREEN),
            run_time=1.5
        )
        self.play(
            GrowFromCenter(epsilon_box_init.box), GrowFromCenter(delta_box_init.box),
            Write(VGroup(delta_box_init.brace, delta_box_init.brace_label, epsilon_box_init.brace, epsilon_box_init.brace_label)),
            FadeIn(delta_box_init.brace_label_rectangle), FadeIn(epsilon_box_init.brace_label_rectangle),
            uc_tex[0][1].animate.set_color(PURPLE),
            uc_tex[0][6].animate.set_color(GREEN),
            run_time=2
        )

        delta_box = UniformContinuityBoxes(np.array([0.3, 0.2, 0]), delta, GREEN, "\\delta", brace_position='DOWN')
        epsilon_box = always_redraw(
            lambda: UniformContinuityBoxes(
                vector_field_target.get_vector(np.hstack((plane.p2c(delta_box.box.get_center()), 0))).get_end(),
                epsilon, PURPLE, "\\varepsilon"
            )
        )

        self.add(delta_box, epsilon_box)
        self.remove(*delta_box_init, *epsilon_box_init)

        self.wait()
        self.play(delta_box.animate.shift(LEFT))
        self.play(delta_box.animate.shift(UL), run_time=2)
        self.play(delta_box.animate.move_to(plane.c2p(-0.7, -0.8)), run_time=2)
        self.play(delta_box.animate.shift(3 * RIGHT + UP))
        self.wait()
        self.play(FadeOut(delta_box, epsilon_box, tex_group, tex_rectangle))
        self.wait()


class BrouwersThmProof4(MovingCameraScene):
    def construct(self):
        scale_factor = 2.5

        epsilon = 0.31
        delta = 0.3
        board_size = 10

        plane = NumberPlane(
            x_range = [-config["frame_x_radius"],config["frame_x_radius"], 0.5],
            y_range =[-config["frame_y_radius"], config["frame_y_radius"], 0.5],
            background_line_style={"stroke_opacity": 0.5}
        ).scale(scale_factor).shift(3 * LEFT)
        unit_distance_conversion = np.linalg.norm(plane.c2p(1, 0) - plane.c2p(0, 0))

        unit_circle = Square(color=RED).move_to(plane.c2p(0, 0)).scale(scale_factor)
        unit_circle_label = MathTex("K", color=RED).next_to(unit_circle, UL)   

        vector_field = ArrowVectorField(
            lambda pos: fixed_point_func(pos, a) - pos,
            x_range=[-1, 1, 0.25],
            y_range=[-1, 1, 0.25],
            vector_config={"stroke_width": 1},
            length_func=lambda norm: 6 * 0.55 * sigmoid(norm)
        ).set_z_index(plane.z_index + 3)
        vector_field_target = vector_field.generate_target()
        vector_field.scale(scale_factor).shift(3 * LEFT)

        for vector in vector_field:
            vector.scale(1/6, scale_tips=True, about_point=vector.get_start())

        vector_field.move_to(plane.c2p(0, 0))


        self.add(plane, vector_field, unit_circle, unit_circle_label)
        self.wait()


        def get_vector_in_vector_field(point: np.ndarray, plane: NumberPlane, vector_field: ArrowVectorField) -> Vector:
            scale_factor = np.linalg.norm(plane.c2p(1, 0) - plane.c2p(0, 0))
            shift = plane.get_center()
            return vector_field.get_vector(point).apply_function(lambda vector: scale_factor * vector).shift(shift)
        
        board = BoardImage(
            board_size=board_size + 1, board_color=YELLOW, hexagon_stroke_color=WHITE, sides_stroke_color=WHITE
        ).set_opacity(0.5)
        board[board_size + 1 : board_size + 5].set_opacity(0)
        

        epsilon_delta_tex = MathTex("\\varepsilon > 0, \\hspace{0.1cm} 0 < \\delta \\leqslant \\varepsilon").scale(0.8)
        epsilon_delta_tex[0][0:20:10].set_color(PURPLE)
        epsilon_delta_tex[0][6:10:2].set_color(GREEN)
        k_tex = MathTex("\\mathbb{N} \\ni k > \\frac{2}{\\delta}").scale(0.8).next_to(epsilon_delta_tex, DOWN, buff=0.65)
        k_tex[0][6].set_color(GREEN)
        B_k_tex = MathTex(
            "B_k = \\left\\{ \\left( -1 + \\frac{2u}{k} , -1 + \\frac{2v}{k} \\right), (u, v) \\in [\\![ 0, k ]\\!] \\right\\}"
        ).scale(0.6).next_to(k_tex, DOWN, buff=0.65)
        B_k_label = MathTex("B_k", color=ORANGE).next_to(unit_circle, UR, buff=0.45)
        B_k_tex[0][0:2].set_color(ORANGE)
        RLUD_tex = MathTex(
            "&R = \\{ z = (z_1, z_2) \\in B_k \\hspace{0.1cm} | \\hspace{0.1cm} f_1(z) - z_1 > \\varepsilon\\} \\\\",
            "&L = \\{ z = (z_1, z_2) \\in B_k \\hspace{0.1cm} | \\hspace{0.1cm} z_1 - f_1(z) > \\varepsilon\\} \\\\",
            "&U = \\{ z = (z_1, z_2) \\in B_k \\hspace{0.1cm} | \\hspace{0.1cm} f_2(z) - z_2 > \\varepsilon\\} \\\\",
            "&D = \\{ z = (z_1, z_2) \\in B_k \\hspace{0.1cm} | \\hspace{0.1cm} z_2 - f_2(z) > \\varepsilon\\}"
        ).scale(0.7).next_to(B_k_tex, DOWN, buff=0.65)
        RLUD_tex[0][0].set_color(RED)
        RLUD_tex[1][0].set_color(PURE_RED)
        RLUD_tex[2][0].set_color("#0000BB")
        RLUD_tex[3][0].set_color(PURE_BLUE)
        VGroup(RLUD_tex[0][-2], RLUD_tex[1][-2], RLUD_tex[2][-2], RLUD_tex[3][-2]).set_color(PURPLE)
        tex_group = VGroup(epsilon_delta_tex, k_tex, B_k_tex, RLUD_tex)
        tex_group.move_to(ORIGIN).to_edge(RIGHT, buff=0.5)
        tex_rectangle = SurroundingRectangle(tex_group, color=BLACK, fill_opacity=0.9, stroke_width=0)
        tex_group.set_z_index(tex_rectangle.z_index + 1)

        epsilon_brace = Brace(Line(plane.c2p(0, 0), plane.c2p(epsilon, 0)), DOWN, color=PURPLE, buff=0.1)
        epsilon_brace_label = MathTex("\\varepsilon", color=PURPLE).scale(0.8).next_to(epsilon_brace, DOWN, buff=0.15)
        epsilon_brace_rectangle = SurroundingRectangle(VGroup(epsilon_brace, epsilon_brace_label), color=BLACK, fill_opacity=1, stroke_width=0)
        VGroup(epsilon_brace, epsilon_brace_label).set_z_index(vector_field.z_index + 2)
        epsilon_brace_rectangle.set_z_index(vector_field.z_index + 1)

        class UniformContinuityBoxes(VMobject):
            def __init__(self, point: np.ndarray, side_length: float, color: str, label: str, brace_position: str = 'UP', **kwargs):
                super().__init__(**kwargs)
                self.point = point
                self.side_length = side_length
                self.color = color
                self.label = label
                self.brace_position = brace_position
                self.box = Square(self.side_length * unit_distance_conversion, color=self.color).move_to(plane.c2p(*self.point))
                self.brace = Brace(
                    Line(
                        plane.c2p(point[0], point[1] + int(((self.brace_position == 'UP') - (self.brace_position == 'DOWN'))) * self.side_length / 2),
                        plane.c2p(point[0] + self.side_length / 2, point[1] + int(((self.brace_position == 'UP') - (self.brace_position == 'DOWN'))) * self.side_length / 2)
                    ), UP * (self.brace_position == 'UP') + DOWN * (self.brace_position == 'DOWN'), buff=0, color=self.color
                )
                self.brace_label = MathTex(
                    self.label, color=self.color
                ).scale(0.6).next_to(self.brace, UP * (self.brace_position == 'UP') + DOWN * (self.brace_position == 'DOWN'), buff=0.15)
                self.brace_label_rectangle = SurroundingRectangle(
                    VGroup(self.brace, self.brace_label), color=BLACK, fill_opacity=0.75, stroke_width=0, buff=0.05
                )
                self.add(self.box, self.brace, self.brace_label, self.brace_label_rectangle)
                self.set_z_index(vector_field.z_index + 1)
                VGroup(self.brace, self.brace_label, self.box).set_z_index(self.z_index + 1)


        self.play(Write(epsilon_delta_tex), FadeIn(tex_rectangle), run_time=1.5)
        self.wait()
        self.play(FocusOn(epsilon_brace_rectangle))
        self.play(FadeIn(epsilon_brace, epsilon_brace_label, epsilon_brace_rectangle))
        self.wait()
        self.play(FadeOut(epsilon_brace, epsilon_brace_label, epsilon_brace_rectangle))
        self.wait()
        self.play(Write(k_tex), run_time=1.5)
        self.wait()
        self.play(Create(board), run_time=3)
        self.wait()
        self.play(
            board.animate.apply_matrix(np.array([[1, 0.58], [0, 1]])).move_to(plane.c2p(0, 0)).stretch(1.16, 1).match_height(Square().scale(1.2 * scale_factor)),
            run_time=3
        )

        
        B_k = []
        for line in range(board_size + 1):
            for row in range(board_size + 1):
                B_k.append(np.hstack((plane.p2c(board[line][row].get_center()), 0)))

        B_k_dots = VGroup(*[Dot(plane.c2p(*pos), radius=1.5 * DEFAULT_SMALL_DOT_RADIUS, color=RED) for pos in B_k])

        vector_field_for_board = vector_field.copy()
        vector_field_for_board.remove(*vector_field_for_board)
        vector_field_for_board.add(*[get_vector_in_vector_field(point, plane, vector_field_target) for point in B_k])
        vector_field_for_board[3 * (board_size + 1) + 3] = Vector(
            plane.c2p(*a) - board[3][3].get_center()
        ).set_color(BLUE).shift(board[3][3].get_center())
        vector_field_for_board.set_z_index(vector_field.z_index + 5)


        for vector in vector_field_for_board:
            vector.scale(1/6, scale_tips=True, about_point=vector.get_start())
        

        vector_2_1 = vector_field_for_board[2 * (board_size + 1) + 1].copy()
        vector_3_2 = vector_field_for_board[3 * (board_size + 1) + 2].copy()
        vector_3_4 = vector_field_for_board[3 * (board_size + 1) + 4].copy()
        
        VGroup(vector_3_2, vector_3_4).set_color(WHITE)
        vector_3_4.set_stroke(BLACK, width=1)
        vector_3_2.set_stroke(BLACK, width=1)

        vector_field_for_board.move_to(plane.c2p(0, 0))


        self.wait()
        self.play(ReplacementTransform(vector_field, vector_field_for_board), run_time=2)
        self.wait()
        self.play(FadeOut(vector_field_for_board))


        delta_box = UniformContinuityBoxes(B_k[3 * (board_size + 1) + 2], delta, BLACK, "\\frac{\\delta}{2}").set_z_index(board.z_index + 3)
        VGroup(delta_box.brace, delta_box.brace_label).shift(0.035 * UP)
        delta_box.brace_label.set_stroke(width=1.5)
        delta_box.brace_label_rectangle.set_opacity(0)


        self.wait()
        self.play(FadeIn(delta_box))
        self.wait()
        self.play(FadeOut(delta_box))
        self.wait()
        self.play(Write(B_k_tex), run_time=3)
        self.wait()
        self.play(FadeIn(B_k_dots), Write(B_k_label))
        self.wait()
        self.play(
            FadeOut(B_k_dots, B_k_label), 
            board[0 : board_size + 1].animate.set_opacity(0.65),
            board[3][3].animate.set_z_index(vector_field_for_board.z_index - 2).set_opacity(0.65)
        )
        self.wait()

        self.play(Write(RLUD_tex[0]), run_time=3)
        self.wait()
        self.play(
            AnimationGroup(
                *[
                    board[index // (board_size + 1)][index % (board_size + 1)].animate.set_color(RED)
                    for index in range(len(vector_field_for_board))
                    if (vector_field_for_board[index].get_end() - vector_field_for_board[index].get_start())[0] / unit_distance_conversion > epsilon
                ], lag_ratio=0.25
            ), run_time=2
        )
        self.wait()
        

        z_dot = Dot(plane.c2p(*B_k[2 * (board_size + 1) + 1]), radius=1.5 * DEFAULT_SMALL_DOT_RADIUS, color=BLACK).set_z_index(vector_field_for_board.z_index + 2)
        z_dot_label = MathTex("z", color=BLACK, stroke_width=1.5).scale(0.8).next_to(z_dot, LEFT, buff=0.15).set_z_index(z_dot.z_index)
        f_z_dot = Dot(vector_field_for_board[2 * (board_size + 1) + 1].get_end(), radius=1.5 * DEFAULT_SMALL_DOT_RADIUS, color=BLACK).set_z_index(z_dot.z_index)
        f_z_dot_label = MathTex("f(z)", color=BLACK, stroke_width=1.5).scale(0.8).next_to(f_z_dot, RIGHT, buff=0.15).set_z_index(z_dot.z_index)

        f_z_array = vector_field_for_board[2 * (board_size + 1) + 1].get_end() - vector_field_for_board[2 * (board_size + 1) + 1].get_start()
        f_z_brace = Brace(Line(z_dot.get_center(), z_dot.get_center() + f_z_array[0] * RIGHT), UP, buff=0, color=BLACK).set_z_index(z_dot.z_index - 1)
        f_z_brace_label = MathTex("f_1(z) - z_1", "> \\varepsilon", color=BLACK, stroke_width=2).scale(0.8).set_z_index(z_dot.z_index - 1)
        f_z_brace_label[0].next_to(f_z_brace, UP, buff=0.15)
        f_z_brace_label[1].next_to(f_z_brace_label[0], RIGHT)

        VGroup(epsilon_brace, epsilon_brace_label).next_to(Line(z_dot.get_center(), z_dot.get_center() + epsilon * unit_distance_conversion * RIGHT), DOWN, buff=0).set_z_index(z_dot.z_index - 1)
        epsilon_brace_label.shift(0.09 * UP).set_stroke(width=1.75)


        self.play(Create(z_dot), Write(z_dot_label), FadeIn(vector_2_1))
        self.wait()
        self.play(z_dot.animate.shift(f_z_array), Write(f_z_dot_label))
        self.wait()
        self.play(Write(VGroup(f_z_brace, f_z_brace_label[0])))
        self.wait()
        self.play(FadeIn(epsilon_brace, epsilon_brace_label), Write(f_z_brace_label[1]))
        self.wait()
        self.play(FadeOut(vector_2_1, z_dot, z_dot_label, f_z_dot_label, f_z_brace, f_z_brace_label[0], f_z_brace_label[1], epsilon_brace, epsilon_brace_label))
        self.wait()

        self.play(
            Write(RLUD_tex[1]),
            AnimationGroup(
                *[
                    board[index // (board_size + 1)][index % (board_size + 1)].animate.set_color(PURE_RED)
                    for index in range(len(vector_field_for_board))
                    if -(vector_field_for_board[index].get_end() - vector_field_for_board[index].get_start())[0] / unit_distance_conversion > epsilon
                ], lag_ratio=0
            ), run_time=2
        )
        self.wait()
        self.play(
            Write(RLUD_tex[2]),
            AnimationGroup(
                *[
                    board[index // (board_size + 1)][index % (board_size + 1)].animate.set_stroke("#0000BB")
                    for index in range(len(vector_field_for_board))
                    if (vector_field_for_board[index].get_end() - vector_field_for_board[index].get_start())[1] / unit_distance_conversion > epsilon
                ], lag_ratio=0
            ), run_time=2
        )
        self.wait()
        self.play(
            Write(RLUD_tex[3]),
            AnimationGroup(
                *[
                    board[index // (board_size + 1)][index % (board_size + 1)].animate.set_stroke(PURE_BLUE)
                    for index in range(len(vector_field_for_board))
                    if -(vector_field_for_board[index].get_end() - vector_field_for_board[index].get_start())[1] / unit_distance_conversion > epsilon
                ], lag_ratio=0
            ), run_time=2
        )
        self.wait()


        z_R_dot = Dot(vector_3_2.get_start(), radius=DEFAULT_SMALL_DOT_RADIUS, color=BLACK).set_z_index(vector_field_for_board.z_index + 2)
        z_L_dot = Dot(vector_3_4.get_start(), radius=DEFAULT_SMALL_DOT_RADIUS, color=BLACK).set_z_index(z_R_dot.z_index)
        z_R_dot_label = MathTex("z_R", color=BLACK, stroke_width=1.5).scale(0.7).next_to(z_R_dot, LEFT, buff=0.15).set_z_index(z_R_dot.z_index)
        z_L_dot_label = MathTex("z_L", color=BLACK, stroke_width=1.5).scale(0.7).next_to(z_L_dot, RIGHT, buff=0.15).set_z_index(z_R_dot.z_index)

        R_line = Line(ORIGIN, (vector_3_2.get_end() - vector_3_2.get_start())[0] * RIGHT, color=BLACK).shift(z_R_dot.get_center() + 0.5 * UP).set_z_index(z_R_dot.z_index)
        L_line = Line(ORIGIN, -(vector_3_4.get_end() - vector_3_4.get_start())[0] * RIGHT, color=BLACK).shift(R_line.get_end()).set_z_index(z_R_dot.z_index)

        R_line_brace = Brace(R_line, UP, buff=0, color=BLACK).set_z_index(z_R_dot.z_index)

        RL_lines_brace = Brace(VGroup(R_line, L_line), UP, buff=0, color=BLACK).set_z_index(z_R_dot.z_index)
        RL_lines_brace_label = MathTex("f_1(z_R) - z_{R, 1}", "+ z_{L, 1} - f_1(z_L)", color=BLACK, stroke_width=1.6).scale(0.5).set_z_index(z_R_dot.z_index)
        RL_lines_brace_label_target = RL_lines_brace_label.generate_target().next_to(RL_lines_brace, UP, buff=0.1)
        RL_lines_brace_label[0].next_to(R_line_brace, UP, buff=0.1)
        RL_lines_brace_label[1].move_to(RL_lines_brace_label_target[1])
        g_2_epsilon_tex = MathTex("> 2\\varepsilon", color=BLACK, stroke_width=1.6).scale(0.5).next_to(RL_lines_brace_label_target, RIGHT, buff=0.1).set_z_index(z_R_dot.z_index)

        two_epsilon_brace = Brace(Line(R_line.get_start(), R_line.get_start() + 2 * epsilon * unit_distance_conversion * RIGHT), DOWN, buff=0, color=PURPLE).set_z_index(z_R_dot.z_index)
        two_epsilon_brace_label = MathTex("2\\varepsilon", color=PURPLE, stroke_width=1.75).scale(0.8).next_to(two_epsilon_brace, DOWN, buff=0.1).set_z_index(z_R_dot.z_index)


        self.play(
            FadeOut(k_tex, B_k_tex, *RLUD_tex[2::]),
            RLUD_tex[:2].animate.next_to(epsilon_delta_tex, DOWN, buff=0.5),
            run_time=1.5
        )
        self.wait()


        RL_not_connected_tex = Tex("$R$ and $L$ are not connected.").scale(0.8).next_to(RLUD_tex[1], DOWN, buff=0.5)
        RL_not_connected_tex[0][0].set_color(RED)
        RL_not_connected_tex[0][4].set_color(PURE_RED)

        UD_not_connected_tex = Tex("Same for $U$ and $D$.").next_to(RL_not_connected_tex, DOWN, buff=0.5)
        UD_not_connected_tex[0][7].set_color("#0000BB")
        UD_not_connected_tex[0][11].set_color(PURE_BLUE)

        z_R_z_L_tex = Tex("$z_R \\in R, z_L \\in L$  in adjacents hexagons").scale(0.7).next_to(RL_not_connected_tex, DOWN, buff=0.5)
        z_R_z_L_tex[0][3].set_color(RED)
        z_R_z_L_tex[0][8].set_color(PURE_RED)

        z_R_z_L_cond_tex = MathTex("z_{L, 1} - z_{R, 1} \\leqslant ||z_L - z_R||_{\\infty} \\leqslant", "\\delta").scale(0.8).next_to(z_R_z_L_tex, DOWN, buff=0.5)
        z_R_z_L_cond_tex[-1].set_color(GREEN)
        z_R_z_L_cond_tex_rectangle = SurroundingRectangle(z_R_z_L_cond_tex, buff=0.2)

        #for line in board[0 : board_size + 1]:
        #    self.remove(*line)


        self.play(Write(RL_not_connected_tex), run_time=2)
        self.wait()
        self.play(Write(z_R_z_L_tex), run_time=3)
        self.wait()
        self.play(
            board[0 : board_size + 1].animate.set_opacity(0.5),
            FadeIn(z_R_dot, z_L_dot, vector_3_2, vector_3_4),
            Write(VGroup(z_R_dot_label, z_L_dot_label))
        )
        self.wait()
        self.play(Write(z_R_z_L_cond_tex), run_time=2)
        self.play(Create(z_R_z_L_cond_tex_rectangle), run_time=1.5)
        self.wait()
        self.play(
            ReplacementTransform(vector_3_2.copy(), R_line),
            FadeIn(R_line_brace, RL_lines_brace_label[0])
        )
        self.wait()
        self.play(
            ReplacementTransform(vector_3_4.copy(), L_line),
            ReplacementTransform(R_line_brace, RL_lines_brace),
            FadeIn(RL_lines_brace_label[1]),
            RL_lines_brace_label[0].animate.move_to(RL_lines_brace_label_target[0])
        )
        self.wait()
        self.play(FadeIn(two_epsilon_brace, two_epsilon_brace_label), Write(g_2_epsilon_tex))
        self.wait()
        self.play(FadeOut(two_epsilon_brace, two_epsilon_brace_label))
        self.wait()

        
        formula_z_f_z = VGroup(RL_lines_brace_label.copy(), g_2_epsilon_tex.copy())

        formula_z_f_z_tex = MathTex(
            "f_1(z_R) ",  " - ", " z_{R, 1} ", " + ", " z_{L, 1} ", " - ", " f_1(z_L) ", " > ", " 2 ", " \\varepsilon "
        ).scale(0.7).next_to(z_R_z_L_cond_tex_rectangle, DOWN, buff=0.5)
        formula_z_f_z_tex_2 = formula_z_f_z_tex.copy()
        formula_z_f_z_tex_2[5:].next_to(formula_z_f_z_tex_2[0], RIGHT, buff=0.15)
        formula_z_f_z_tex_2[1:5].next_to(formula_z_f_z_tex_2[-1], RIGHT, buff=0.15)
        m_sine = formula_z_f_z_tex_2[1].get_center()
        formula_z_f_z_tex_2[1].move_to(formula_z_f_z_tex_2[3])
        formula_z_f_z_tex_2[3].move_to(m_sine)

        self.play(ReplacementTransform(formula_z_f_z, formula_z_f_z_tex))
        self.wait()
        self.play(*[formula_z_f_z_tex[k].animate.move_to(formula_z_f_z_tex_2[k]) for k in range(len(formula_z_f_z_tex))])
        
        brace_g_delta_epsilon = Brace(formula_z_f_z_tex[1:5], DOWN)
        brace_g_delta_epsilon_label = MathTex("\\geqslant", "-\\delta", "\\geqslant", "-\\varepsilon").scale(0.7).next_to(brace_g_delta_epsilon, DOWN, buff=0.15)

        self.wait()
        self.play(Write(VGroup(brace_g_delta_epsilon, brace_g_delta_epsilon_label)), run_time=2)
        self.wait()
        self.play(
            FadeOut(formula_z_f_z_tex[1:5], brace_g_delta_epsilon, brace_g_delta_epsilon_label[:3]),
            brace_g_delta_epsilon_label[3].animate.next_to(formula_z_f_z_tex[-1], RIGHT, buff=0.15)
        )
        self.play(
            formula_z_f_z_tex[-1].animate.move_to(formula_z_f_z_tex[-2]).shift(0.03 * DOWN),
            FadeOut(formula_z_f_z_tex[-2], brace_g_delta_epsilon_label[3])
        )
        self.wait()
        remaining_tex = VGroup(formula_z_f_z_tex[0], formula_z_f_z_tex[5:8], formula_z_f_z_tex[-1])
        cross = Cross(remaining_tex)


        self.play(GrowFromCenter(cross))
        self.wait()
        self.play(
            FadeOut(
                remaining_tex, cross, z_L_dot, z_L_dot_label, z_R_dot, z_R_dot_label, vector_3_2, vector_3_4, RL_lines_brace,
                *RL_lines_brace_label, R_line, L_line, z_R_z_L_cond_tex, z_R_z_L_cond_tex_rectangle, z_R_z_L_tex, g_2_epsilon_tex,
                epsilon_delta_tex, *RLUD_tex[0:2]
            ),
            RL_not_connected_tex.animate.shift(2 * UP)
        )
        self.wait()


        UD_not_connected_tex.scale(0.8).next_to(RL_not_connected_tex, DOWN, buff=0.3)

        R_not_connected_right_edge_tex = Tex("R isn't connected to the right edge.").scale(0.75).next_to(UD_not_connected_tex, DOWN, buff=0.5)
        R_not_connected_right_edge_tex[0][0].set_color(RED)
        
        LUD_not_connected_edges_tex = Tex("Same for $L$, $U$ and $D$.").scale(0.8).next_to(R_not_connected_right_edge_tex, DOWN, buff=0.3)
        LUD_not_connected_edges_tex[0][7].set_color(PURE_RED)
        LUD_not_connected_edges_tex[0][9].set_color("#0000BB")
        LUD_not_connected_edges_tex[0][13].set_color(PURE_BLUE)
        
        hex_thm_contrapositive_tex = Tex(
            "$\\nexists$ \\hspace{0.05cm} red path from r.e to l.e and \\\\ $\\nexists$ \\hspace{0.05cm} blue path from u.e to d.e \\\\",
            "$\\implies$ \\\\", "$B_k \\not \\subset R \\cup L \\cup U \\cup D$"
        ).scale(0.75).next_to(LUD_not_connected_edges_tex, DOWN, buff=0.5)
        hex_thm_contrapositive_tex[-1][4].set_color(RED)
        hex_thm_contrapositive_tex[-1][6].set_color(PURE_RED)
        hex_thm_contrapositive_tex[-1][8].set_color("#0000BB")
        hex_thm_contrapositive_tex[-1][10].set_color(PURE_BLUE)
        hex_thm_contrapositive_tex[1].rotate(-PI/2).scale(0.8 / 0.75)
        hex_thm_contrapositive_tex[1:].shift(0.2 * DOWN)
        hex_thm_contrapositive_tex[2].shift(0.2 * DOWN)
        hex_thm_contrapositive_tex_2 = Tex(
            "\\textsc{Hex} theorem contrapositive"
        ).scale(0.35).set_z_index(hex_thm_contrapositive_tex.z_index + 2).move_to(hex_thm_contrapositive_tex[1])
        hex_thm_contrapositive_tex_2_rectangle = SurroundingRectangle(
            hex_thm_contrapositive_tex_2, color=BLACK, fill_opacity=0.8, stroke_width=0, buff=0.1
        ).set_z_index(hex_thm_contrapositive_tex.z_index + 1)
        hex_thm_contrapositive_tex     

        right_edge_vectors = vector_field_for_board[board_size:(board_size + 2)**2 - 1:board_size + 1].copy()

        
        self.play(Write(UD_not_connected_tex), run_time=2)
        self.wait()
        self.play(Write(R_not_connected_right_edge_tex, run_rime=2.5))
        self.wait()
        self.play(
            AnimationGroup(
                *[GrowArrow(vector) for vector in right_edge_vectors],
                lag_ratio=0.25
            ), run_time=2.5
        )
        self.wait()
        self.play(FadeOut(*right_edge_vectors))
        self.wait()
        self.play(Write(LUD_not_connected_edges_tex), run_time=2)
        self.wait()
        self.play(Write(hex_thm_contrapositive_tex[0], run_time=5))
        self.wait()
        self.play(Write(hex_thm_contrapositive_tex[1]))
        self.play(FadeIn(hex_thm_contrapositive_tex_2_rectangle), Write(hex_thm_contrapositive_tex_2), run_time=1.5)
        self.play(Write(hex_thm_contrapositive_tex[2]), run_time=2)
        self.wait()
        self.play(
            FadeOut(UD_not_connected_tex, LUD_not_connected_edges_tex, R_not_connected_right_edge_tex, RL_not_connected_tex),
            VGroup(hex_thm_contrapositive_tex, hex_thm_contrapositive_tex_2, hex_thm_contrapositive_tex_2_rectangle).animate.shift(3 * UP),
            run_time=1.5            
        )
        self.wait()


        exists_fixed_hex_tex = MathTex("\\forall \\varepsilon > 0, \\exists z_{\\varepsilon} \\in B_k \\\\ ||f(z_{\\varepsilon}) - z_{\\varepsilon}||_{\\infty} \\leqslant \\varepsilon").scale(0.8).next_to(hex_thm_contrapositive_tex, DOWN, buff=0.5)
        inf_f_m_id_tex = MathTex("\\inf_K ||f - \\mathrm{Id}||_{\\infty} = 0").scale(0.8).next_to(exists_fixed_hex_tex, DOWN, buff=0.5)
        target_start, target_end = Dot().next_to(exists_fixed_hex_tex, UL).get_center(), Dot().next_to(board[3][3], UR).shift(0.2 * DOWN).get_center()
        arrow_indication = CurvedArrow(target_start, target_end, color=YELLOW).set_z_index(vector_field.z_index + 2)

        self.play(
            Write(exists_fixed_hex_tex),
            run_time=3
        )
        self.play(Create(arrow_indication), run_time=1.5)
        self.play(Indicate(board[3][3], scale_factor=1.5), run_time=2)
        
        self.wait()
        self.play(Write(inf_f_m_id_tex), FadeOut(arrow_indication), run_time=1.5)
        self.wait()
        self.play(
            FadeOut(hex_thm_contrapositive_tex, hex_thm_contrapositive_tex_2, hex_thm_contrapositive_tex_2_rectangle, exists_fixed_hex_tex),
            inf_f_m_id_tex.animate.shift(4 * UP),
            run_time=1.5
        )
        self.wait()


        conclusion_1 = Tex(
            "$||f - \\mathrm{Id}||_{\\infty}$ continuous \\\\",
            "$K$", " compact set"
        ).scale(0.75).next_to(inf_f_m_id_tex, DOWN, buff=0.5)
        conclusion_1_bis = MathTex(
            "&\\exists z \\in K, \\\\",
            "&\\inf_K ||f - \\mathrm{Id}||_{\\infty} = ||f(z) - z||_{\\infty} = 0"
        ).scale(0.75).next_to(conclusion_1, DOWN, buff=0.5)
        conclusion_1[1].set_color(RED)  
        conclusion_2 = MathTex("f(z) = z").scale(0.8).next_to(conclusion_1_bis, DOWN, buff=0.6)
        conclusion_2_rectangle = SurroundingRectangle(conclusion_2, buff=0.2)      


        self.play(Write(conclusion_1), run_time=3)
        self.wait()
        self.play(Write(conclusion_1_bis), run_time=4)
        self.wait()
        self.play(Write(conclusion_2), run_time=2)
        self.play(Create(conclusion_2_rectangle), run_time=1.5)
        self.wait()
        self.play(FadeIn(Rectangle(color=BLACK, width=30, height=20, fill_opacity=1).set_z_index(100)))
        self.wait()
        
        
class ConclusionAndCredits(Scene):
    def construct(self):
        eq_tex = Tex("\\textsc{Hex} theorem  $\\iff$ \\textsc{Brouwer}'s theorem").scale(1.25)
        credits_tex = Tex(
            "Animations made with Manim CE \\\\ \\vspace{0.3cm} Musics : 'Odyssey' \\& 'Disquiet' by Kevin MacLeod \\\\ \\vspace{0.3cm} Proofs : Wikipedia page for B. thm, El Jj blog page \\& David \\textsc{Gale}'s article about B. thm",
            tex_environment="flushleft"
        ).scale(0.6)
        self.wait()
        self.play(FadeIn(eq_tex))
        self.wait(2)
        self.play(FadeOut(eq_tex))
        self.wait(3)
        self.play(Write(credits_tex), run_time=8)
        self.wait(4)
        self.play(FadeOut(credits_tex))
        self.wait()
                


        






