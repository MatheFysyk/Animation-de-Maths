from manim import *
from typing import Callable


a, b = 0.5, 2.5
f = lambda x: (x ** 2 + 1) * (x - 0.5) * (x - 2.5) * (x - 1.1) * (x - 1.9) + 1
g = lambda x: f(x) - f(x + delta_x)
n = 6
delta_x = (b - a)/n

def dichotomie(f: Callable[[float], float], a: float = a, b: float = b, epsilon: float = 10**-4):
    a_n, b_n = a, b
    while np.abs(f(a_n)) >= epsilon:
        c_n = (a_n + b_n)/2
        if f(a_n) * f(c_n) <= 0:
            b_n = c_n
        else:
            a_n = c_n
    return a_n

c_n = dichotomie(
    lambda x: f(x) - f(x + (b - a)/n)
)


class ThmCordesLevy(Scene):
    def construct(self):
        self.animate_thm_words()
        self.explanation_thm()



    def get_thm_words(self):
        thm_words = Tex(
            "Thm : ",
            "Soit  ",
            "  $f : [a, b] \\rightarrow \\mathbb{R}$  ",
            "  continue",
            " telle que ",
            "$f(a) = f(b)$",
            ". Alors :",
            "$$\\forall n \\in \\mathbb{N}, \\; \\exists c_n \\in \\left[a, b - \\frac{b-a}{n}\\right], \\quad f(c_n) = f\\left(c_n + \\frac{b-a}{n}\\right).$$",
        ).move_to(ORIGIN).scale(0.9)
        underline = always_redraw(lambda: Underline(thm_words[0], stroke_width=2).set_opacity([0, 1, 0]).set_length(1.1))
        thm_words[-1].next_to(thm_words[0], RIGHT, buff=0.2).shift(DOWN)
        thm_words[3].set_color(RED)
        thm_words[5].set_color(YELLOW)
        thm_words[-1][1].set_color(PURPLE)
        VGroup(thm_words[-1][6:8], thm_words[-1][23:25], thm_words[-1][29:31]).set_color(GREEN)
        VGroup(thm_words[-1][14:19], thm_words[-1][32:37]).set_color(BLUE)
        return thm_words, underline


    def animate_thm_words(self):
        thm_words, underline = self.get_thm_words()
        self.add(thm_words, underline)
        self.wait(5)
        self.play(thm_words.animate.scale(0.6 * 1/0.9).to_edge(UP))


    def explanation_thm(self):
        self.setup_axes_and_labels()
        self.setup_curve()
        self.display_b_a_over_n_label()
        self.compute_and_display_chord()
        self.transition()
        self.proof()

    def setup_axes_and_labels(self):
        self.axes = Axes(
            x_range=[-0.2, 3, 0.5],
            y_range=[-0.2, 2, 0.5],
            x_length=7,
            y_length=2.2 * 7/3.2,
            tips=False
        ).shift(0.75 * DOWN)
        self.a, self.b, self.f_a_f_b = MathTex("a").next_to(self.axes.c2p(a, 0), DOWN), MathTex("b").next_to(self.axes.c2p(b, 0), DOWN), MathTex("f(a) = f(b)").next_to(self.axes.c2p(0, f(a)), LEFT)
        self.labels_axis = self.axes.get_axis_labels("x", "f(x)")

        self.play(Create(self.axes), Write(self.labels_axis), Write(VGroup(self.a, self.b)), run_time=2.5)
        self.wait(0.5)

    def setup_curve(self):
        self.f_curve = self.axes.plot(f, x_range=[0.5, 2.5])
        self.dot_f_a, self.dot_f_b = Dot(self.axes.c2p(a, f(a)), color=YELLOW), Dot(self.axes.c2p(b, f(b)), color=YELLOW)
        self.play(Create(self.f_curve), Create(VGroup(self.dot_f_a, self.dot_f_b)), run_time=2)
        self.wait(0.5)

    def display_b_a_over_n_label(self):
        self.underbrace_delta_x = BraceLabel(Line(self.axes.c2p(a, 0), self.axes.c2p(a + delta_x, 0)), "\\frac{b-a}{n}", UP, buff=0, font_size=24, color=BLUE)
        self.underbrace_delta_x.label.shift(0.15 * DOWN).set_color(BLUE)
        self.play(FadeIn(self.underbrace_delta_x), run_time=1.5)
        self.wait(0.5)

    def compute_and_display_chord(self):
        n_tracker = ValueTracker(6)
        self.c_n_label = MathTex("c_n", color=GREEN).add_updater(lambda mob: mob.next_to(self.axes.c2p(
            dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())),
            0), DOWN))
        
        self.c_n_dot = always_redraw(lambda: Dot(self.axes.c2p(
            dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())),
            f(dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())))
        ), color=GREEN))

        self.c_n_delta_x_dot = always_redraw(lambda: Dot(self.axes.c2p(
            dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())) + (b - a)/n_tracker.get_value(),
            f(dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())) + (b - a)/n_tracker.get_value())
        ), color=GREEN))

        self.c_n_dashed_line = always_redraw(lambda: DashedLine(
            self.axes.c2p(
                dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())),
                f(dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())))),

            self.axes.c2p(
                dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())),
                0)
        ).set_z_index(self.c_n_dot.z_index - 1))

        self.line_c_n_c_n_delta_x = always_redraw(lambda: Line(
            self.axes.c2p(
                dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())),
                f(dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())))),

            self.axes.c2p(
                dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())) + (b - a)/n_tracker.get_value(),
                f(dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())) + (b - a)/n_tracker.get_value())),
            color=BLUE
        ).set_z_index(self.c_n_dot.z_index - 1))

        self.other_brace = self.underbrace_delta_x.copy()
        self.other_brace.label.set_color(BLUE)

        def update_brace_1(brace):
            brace.become(BraceLabel(Line(
                self.axes.c2p(a, 0),
                self.axes.c2p(a + (b - a)/n_tracker.get_value(), 0)),
                "\\frac{b-a}{n}", UP, buff=0, font_size=24, color=BLUE)
            )
            brace.label.shift(0.15 * DOWN).set_color(BLUE)

        self.underbrace_delta_x.add_updater(update_brace_1)

        self.play(
            Create(VGroup(self.c_n_dot, self.c_n_delta_x_dot, self.line_c_n_c_n_delta_x)),
            self.other_brace.animate.next_to(self.line_c_n_c_n_delta_x, UP, buff=0),
            run_time=2
        )

        def update_brace_2(brace):
            brace.become(BraceLabel(Line(
                self.axes.c2p(
                    dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())),
                    f(dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())))),
                self.axes.c2p(
                    dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())) + (b - a)/n_tracker.get_value(),
                    f(dichotomie(lambda x: f(x) - f(x + (b - a)/n_tracker.get_value())) + (b - a)/n_tracker.get_value()))),
                "\\frac{b-a}{n}", UP, buff=0, font_size=24, color=BLUE)
            )
            brace.label.shift(0.15 * DOWN).set_color(BLUE)

        self.other_brace.add_updater(update_brace_2)

        self.play(Create(self.c_n_dashed_line), Write(self.c_n_label))
        self.wait()
        
        self.play(n_tracker.animate.set_value(10), run_time=2)
        self.wait()
        self.play(n_tracker.animate.set_value(2), run_time=2.5)
        self.wait()
        self.play(n_tracker.animate.set_value(6), run_time=2)
        self.wait()

    def transition(self):
        self.new_axes = Axes(
            x_range=self.axes.x_range,
            y_range=[-1, 2, 0.5],
            x_length=(self.axes.y_length + 1) * 3.2/3 + 1,
            y_length=(self.axes.y_length + 1),
            tips=False
        ).scale(0.8).move_to(self.axes).to_edge(RIGHT, buff=0.5).shift(0.15 * DOWN)

        self.new_f_curve = self.new_axes.plot(f, x_range=[0.5, 2.5]).set_z_index(self.dot_f_a.z_index - 1)

        self.play(
            Uncreate(VGroup(self.underbrace_delta_x, self.other_brace, self.c_n_dot, self.c_n_delta_x_dot, self.line_c_n_c_n_delta_x, self.c_n_dashed_line)),
            Unwrite(self.c_n_label, self.f_a_f_b)
        )
            #VGroup(self.axes, self.labels_axis, self.a, self.b, self.f_curve, self.dot_f_a, self.dot_f_b).animate.scale(0.8).to_edge(RIGHT).shift(0.15 * UP),
        self.play(
            Transform(self.axes, self.new_axes),
            Transform(self.f_curve, self.new_f_curve),
            self.a.animate.scale(0.8).next_to(self.new_axes.c2p(a, 0), DOWN),
            self.b.animate.scale(0.8).next_to(self.new_axes.c2p(b, 0), DOWN),
            self.dot_f_a.animate.scale(0.8).move_to(self.new_f_curve.get_start()),
            self.dot_f_b.animate.scale(0.8).move_to(self.new_f_curve.get_end()),
            self.labels_axis[0].animate.scale(0.8).next_to(self.new_axes.x_axis, UR, buff=SMALL_BUFF),
            self.labels_axis[1].animate.scale(0.8).next_to(self.new_axes.y_axis, UP + 0.5 * RIGHT, buff=SMALL_BUFF),
            run_time=1.5
        )
        self.add(self.new_axes, self.new_f_curve)
        self.remove(self.axes, self.f_curve)



    def proof(self):
        self.animate_text_1()
        self.setup_g_curve()
        self.animate_g_sum()
        self.tvi()
        self.conclusion()

    def animate_text_1(self):
        self.proof_text = Tex("Démonstration : ").scale(0.7).to_edge().shift(1.75 * UP)
        self.text_1 = Tex("On introduit la fonction auxiliaire $g$ ", "continue", " :").next_to(self.proof_text, DOWN).scale(0.7).to_edge().shift(0.25 * DOWN)
        self.text_1[0][-1].set_color(ORANGE)
        self.text_1[1].set_color(RED)
        self.g_text = MathTex("g : &\\left[a, b - \\frac{b-a}{n}\\right] \\rightarrow \\mathbb{R} \\\\ &x \\mapsto f(x) - f\\left( x + \\frac{b - a}{n} \\right) ").scale(0.7).next_to(self.text_1, DOWN).shift(0.25 * DL)
        self.g_text[0][0].set_color(ORANGE)
        VGroup(self.g_text[0][7:12], self.g_text[0][27:32]).set_color(BLUE)
        self.g_text[0][15:].shift(0.5 * RIGHT)
        self.play(Write(self.proof_text))
        self.play(Write(self.text_1))
        self.play(DrawBorderThenFill(self.g_text))
        self.wait()

    def setup_g_curve(self):
        self.g_curve = self.new_axes.plot(g, x_range=[0.5, 2.5 - delta_x], color=ORANGE)
        self.g_curve_label = MathTex("g", color=ORANGE).scale(0.8).next_to(self.g_curve.get_end(), RIGHT)
        self.dot_g_a, self.dot_g_b = Dot(self.new_axes.c2p(a, g(a)), color=YELLOW).scale(0.8), Dot(self.new_axes.c2p(b - delta_x, g(b - delta_x)), color=YELLOW).scale(0.8)
        self.play(
            Create(self.g_curve),
            Create(VGroup(self.dot_g_a, self.dot_g_b)),
            Write(self.g_curve_label),
            self.new_f_curve.animate.set_stroke(opacity=0.35),
            VGroup(self.dot_f_a, self.dot_f_b).animate.set_opacity(0.5),
            run_time=2
        )
        self.wait()

    def animate_g_sum(self):
        self.g_sum_text = MathTex(
            "\\sum_{k = 0}^{n - 1} g\\left( a + k\\frac{b - a}{n} \\right) &= ",
            "\\sum_{k = 0}^{n - 1} f\\left( a + (k + 1)\\frac{b - a}{n} \\right) - f\\left( a + k\\frac{b - a}{n} \\right)\\\\",
            "&= f\\left( a + 1\\frac{b - a}{n} \\right)",
            "- f\\left( a + 0\\frac{b - a}{n} \\right) \\\\",
            "&+f\\left( a + 2\\frac{b - a}{n} \\right)",
            "- f\\left( a + 1\\frac{b - a}{n} \\right) \\\\",
            "&+ f\\left( a + 3\\frac{b - a}{n} \\right)",
            "- f\\left( a + 2\\frac{b - a}{n} \\right) \\\\",
            "&+ ... +",
            "f\\left( a + n\\frac{b - a}{n} \\right)", "- f\\left( a + (n-1)\\frac{b - a}{n} \\right)",
        ).scale(0.7).set_z_index(self.text_1.z_index + 2)
        self.g_sum_text[4:11].shift(0.3 * RIGHT)
        eq_sign = MathTex("=").scale(0.7).move_to(self.g_sum_text[2][0]).set_z_index(self.g_sum_text.z_index)
        f_a_m_f_b = MathTex("f(b)", " - f(a)").scale(0.7).next_to(eq_sign, RIGHT).set_z_index(self.g_sum_text.z_index)
        eq_zero = MathTex("= 0").scale(0.7).next_to(f_a_m_f_b, RIGHT).set_z_index(self.g_sum_text.z_index)
        crosses = VGroup(Cross(self.g_sum_text[2][1:12]).set_z_index(self.g_sum_text.z_index), *[Cross(self.g_sum_text[k]).set_z_index(self.g_sum_text.z_index) for k in [4, 5, 6, 7, 8, 10]])
        somme_telescopique = Tex("C'est une somme\\\\", "télescopique", " !").scale(0.7).set_z_index(self.g_sum_text.z_index).next_to(self.g_sum_text[0], DOWN, buff=1).shift(0.2*LEFT)
        somme_telescopique[1].set_color(RED)

        background_rectangle = BackgroundRectangle(
            self.g_sum_text,
            stroke_opacity=0.75,
            stroke_width=1.5,
            stroke_color=WHITE,
            fill_opacity=0.9,
            buff=0.5
        ).set_z_index(self.g_sum_text.z_index - 1)
        self.play(GrowFromCenter(background_rectangle))
        self.play(Write(self.g_sum_text), run_time=15)
        self.wait()
        self.play(
            Indicate(VGroup(self.g_sum_text[2][1:12], self.g_sum_text[5]), color=BLUE),
            Indicate(VGroup(self.g_sum_text[4], self.g_sum_text[7]), color=GREEN)
        )
        self.wait()
        self.play(*[GrowFromCenter(cross) for cross in crosses])
        self.wait()
        self.play(Write(somme_telescopique))
        self.wait()
        self.play(
            FadeOut(VGroup(*[self.g_sum_text[k] for k in [2, 4, 5, 6, 7, 8, 10]], crosses, somme_telescopique)),
            Write(eq_sign),
            Transform(self.g_sum_text[3], f_a_m_f_b[0]),
            Transform(self.g_sum_text[9], f_a_m_f_b[1]),
            Transform(background_rectangle, BackgroundRectangle(
                VGroup(*[self.g_sum_text[k] for k in [0, 1]], eq_zero, eq_sign, f_a_m_f_b),
                stroke_opacity=0.75,
                stroke_width=1.5,
                stroke_color=WHITE,
                fill_opacity=0.9,
                buff=0.5
            ).set_z_index(self.g_sum_text.z_index - 1)),
            run_time=2
        )
        self.remove(self.g_sum_text[3], self.g_sum_text[9])
        self.add(f_a_m_f_b)
        self.play(Write(eq_zero))
        g_sum_copy = MathTex("\\sum_{k = 0}^{n - 1} g\\left( a + k\\frac{b - a}{n} \\right) =").scale(0.7).next_to(self.proof_text, DOWN, buff=0.5).to_edge(LEFT)
        self.play(
            self.g_sum_text[0].animate.next_to(self.proof_text, DOWN, buff=0.5).to_edge(LEFT),
            eq_zero[0][1].animate.next_to(g_sum_copy, RIGHT),
            FadeOut(VGroup(background_rectangle, eq_sign, f_a_m_f_b, self.g_sum_text[1], eq_zero[0][0])),
            FadeOut(VGroup(self.text_1, self.g_text))
        )
        self.g_sum_eq_0 = VGroup(self.g_sum_text[0], eq_zero[0][1])
        self.wait()
        

    def tvi(self):
        text_g_nulle = Tex(
            "$g$",
            " est donc soit nulle partout, soit de signe \\\\", " non constant, car il faut que la somme soit\\\\",
            " nulle (ça se compense).",
            tex_environment="flushleft"
        ).scale(0.7).next_to(self.g_sum_eq_0, DOWN, buff=0.5).to_edge(LEFT)
        text_g_nulle[0].set_color(ORANGE)
        self.play(Write(text_g_nulle), run_time=3)
        self.wait()
        text_tvi = Tex("On utilise le TVI, ", " $g$ ", " s'annule donc quelque part.").scale(0.7).next_to(text_g_nulle, DOWN, buff=0.5).to_edge()
        text_tvi[1].set_color(ORANGE)
        self.play(Write(text_tvi), run_time=2)
        self.wait()
        
    def conclusion(self):
        root = dichotomie(g, 2, 2.5)
        dot_g_0 = Dot(self.new_axes.c2p(root, 0), color=GREEN).scale(0.8)

        group_dots_and_labels = VGroup(self.c_n_dot, self.c_n_delta_x_dot, self.c_n_dashed_line, self.line_c_n_c_n_delta_x)
        for item in group_dots_and_labels:
            item.clear_updaters()

        self.new_c_n_label = MathTex("c_n", color=GREEN).scale(0.8).next_to(self.new_axes.c2p(root, 0), DL, buff=0.2)
        self.c_n_dot.scale(0.8).move_to(self.new_axes.c2p(root, f(root))).set_z_index(self.g_curve.z_index + 2)
        self.c_n_delta_x_dot.scale(0.8).move_to(self.new_axes.c2p(root + delta_x, f(root + delta_x))).set_z_index(self.g_curve.z_index + 2)
        self.c_n_dashed_line = DashedLine(self.new_axes.c2p(root, 0), self.c_n_dot).set_z_index(self.g_curve.z_index + 1)
        self.line_c_n_c_n_delta_x = Line(self.c_n_dot, self.c_n_delta_x_dot, color=BLUE).set_z_index(self.g_curve.z_index + 1)
        dot_g_0.set_z_index(self.c_n_dashed_line.z_index + 1)
        self.new_c_n_label.set_z_index(self.c_n_dashed_line.z_index + 1)
        self.new_brace = BraceLabel(self.line_c_n_c_n_delta_x, "\\frac{b-a}{n}", UP, buff=0, font_size=24, color=BLUE)
        self.new_brace.brace.stretch(1.25, 0)
        self.new_brace.label.shift(0.15 * DOWN).set_color(BLUE)
        text_g_c_n_eq_0 = MathTex("g", "(", "c_n", ") = 0").scale(0.8).shift(3*RIGHT + 3*DOWN)
        text_g_c_n_eq_0[0].set_color(ORANGE)
        text_g_c_n_eq_0[2].set_color(GREEN)

        self.wait(0.5)
        self.play(
            FadeIn(VGroup(dot_g_0,self.c_n_dot, self.new_c_n_label, self.c_n_delta_x_dot, self.c_n_dashed_line, self.line_c_n_c_n_delta_x, self.new_brace)),
            self.new_f_curve.animate.set_stroke(opacity=1),
            VGroup(self.dot_f_a, self.dot_f_b).animate.set_opacity(1),
            Write(text_g_c_n_eq_0)
        )
        box = SurroundingRectangle(text_g_c_n_eq_0, buff=0.15)
        self.play(ShowCreationThenFadeOut(box))
        self.wait()







