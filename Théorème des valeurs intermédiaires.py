from manim import *


a, b = 0.5, 3.5
k = 0.3 * 2.55 ** 3 - 0.7 * 2.55 ** 2 + 0.1 * 2.55 + 0.9
polynomial = [0.3, -0.7, 0.1, 0.9]
nb_etapes = 4


class TVIDichotomieFull(Scene):
    def construct(self):
        thm_words, underline = self.get_thm_words()
        self.add(thm_words, underline)
        self.wait(6)
        self.play(thm_words.animate.scale(0.6).to_edge(UP))
        
        
        self.add_graph()
        self.explication_thm()

        self.demo_dichotomie()


    def get_thm_words(self):
        template = TexTemplate()
        template.add_to_preamble("\\usepackage{mathabx}")

        thm_words = Tex(
            "Thm : ",
            "Soit  ",
            "  $f : [a, b] \\rightarrow \\mathbb{R}$  ",
            "  continue",
            ". Alors :",
            "$$\\forall k \\in \\underset{\\curvearrowbotleftright}{[f(a), f(b)]}, \\; \\exists x_k \\in [a, b], \\; f(x_k) = k.$$",
            tex_template=template
        )
        underline = always_redraw(lambda: Underline(thm_words[0], stroke_width=2).set_opacity([0, 1, 0]).set_length(1.1))
        thm_words[-1].scale(0.9).next_to(thm_words[0], RIGHT, buff=0.2).shift(0.85 * DOWN)
        thm_words[3].set_color(RED)
        thm_words[-1][1].set_color(GREEN)
        VGroup(thm_words[-1][17], thm_words[-1][18]).set_color(BLUE)
        return thm_words, underline


    def add_graph(self):
        self.axes = Axes(
            x_range=[0, 4, 0.5],
            y_range=[0, 3, 0.5],
            x_length=5,
            y_length=4,
            tips=False
        )        
        self.f = lambda x: 0.3 * (x - 1/2)**3 - 0.7 * (x - 1/2)**2 + 0.1 * (x - 1/2) + 0.9
        self.a, self.b = MathTex("a").scale(0.7).next_to(Dot(self.axes.c2p(a, 0)), DOWN), MathTex("b").scale(0.7).next_to(Dot(self.axes.c2p(b, 0)), DOWN)
        self.f_a, self.f_b = MathTex("f(a)").scale(0.7).next_to(Dot(self.axes.c2p(0, self.f(a))), LEFT), MathTex("f(b)").scale(0.7).next_to(Dot(self.axes.c2p(0, self.f(b))), LEFT)
        VGroup(self.axes, self.a, self.b, self.f_a, self.f_b).scale(1.2).move_to(ORIGIN).shift(0.5 * DOWN)
        self.dot_a_f_a, self.dot_b_f_b = Dot(self.axes.c2p(a, self.f(a))), Dot(self.axes.c2p(b, self.f(b)))
        
        self.graph = self.axes.plot(self.f, x_range=[a, b], color=YELLOW)
        
        self.play(
            FadeIn(VGroup(self.axes, self.graph, self.a, self.b, self.f_a, self.f_b, self.dot_a_f_a, self.dot_b_f_b)),
        )
        self.wait()

    
    def explication_thm(self):
        x_k = ValueTracker(3.05)
        self.k = always_redraw(lambda: MathTex("k", color=GREEN).scale(0.7 * 1.2).next_to(Dot(self.axes.c2p(0, self.f(x_k.get_value()))), LEFT))
        self.x_k = always_redraw(lambda: MathTex("x_k", color=BLUE).scale(0.7 * 1.2).next_to(Dot(self.axes.c2p(x_k.get_value(), 0)), DOWN))
        self.dashed_line_k = always_redraw(lambda: DashedLine(self.axes.c2p(0, self.f(x_k.get_value())), self.axes.c2p(x_k.get_value(), self.f(x_k.get_value()))))
        self.dashed_line_x_k = always_redraw(lambda: DashedLine(self.axes.c2p(x_k.get_value(), self.f(x_k.get_value())), self.axes.c2p(x_k.get_value(), 0)))
        self.curve_point = always_redraw(lambda: Dot(self.axes.c2p(x_k.get_value(), self.f(x_k.get_value())), color=DARK_BROWN).set_z_index(self.dashed_line_x_k.z_index + 1))

        self.play(Write(self.k), Create(self.dashed_line_k), run_time=1.5)
        self.play(Create(self.curve_point), Create(self.dashed_line_x_k), run_time=1.5)
        self.play(Write(self.x_k))
        self.wait()
        self.play(x_k.animate.set_value(3.45))
        self.wait(0.5)
        self.play(x_k.animate.set_value(1), run_time=2)
        self.wait(0.5)
        self.play(x_k.animate.set_value(3.05), run_time=1.5)
        self.wait()
        self.play(
            Unwrite(self.k),
            Uncreate(self.dashed_line_k),
            Uncreate(self.curve_point),
            Uncreate(self.dashed_line_x_k),
            Unwrite(self.x_k),
            VGroup(self.axes, self.a, self.b, self.f_a, self.f_b, self.graph, self.dot_a_f_a, self.dot_b_f_b).animate.shift(0.5 * UP).scale(1/1.2).to_edge(RIGHT, buff=0.7).shift(0.75 * DOWN),
            run_time=2
        )
        #VGroup(self.axes, self.a, self.b, self.f_a, self.f_b, self.graph, self.dot_a_f_a, self.dot_b_f_b).shift(0.5 * UP).scale(1/1.2).to_edge(RIGHT, buff=0.7).shift(0.75 * DOWN)
        self.wait(0.5)

    
    def demo_dichotomie(self):
        text_type_demo = Tex("Démontration par \\textit{dichotomie}.").scale(0.7).to_edge().shift(1.75 * UP)
        text_construction_suite = Tex("On construit les suites ", "$(a_n)$", " et ", "$(b_n)$", " suivantes :").scale(0.6).next_to(text_type_demo, DOWN, buff=0.5).to_edge()
        text_construction_suite[1].set_color(YELLOW)
        text_construction_suite[3].set_color(PURPLE)

        text_a_n_b_n = MathTex("\\begin{cases} a_0 = a, \\,\\, b_0 = b \\\\ a_{n+1} = \\begin{cases} c_n \\quad \\text{si} \\quad f(c_n) \\leqslant k \\\\ a_n \\quad \\text{sinon} \\end{cases} \\\\ b_{n+1} = \\begin{cases} b_n \\quad \\text{si} \\quad f(c_n) \\leqslant k \\\\ c_n \\quad \\text{sinon} \\end{cases} \\end{cases}").scale(0.6).next_to(text_construction_suite, DOWN, buff=0.5)
        text_c_n = Tex("où ", "$\\displaystyle{\\,\\, c_n = \\frac{a_n + b_n}{2} \\,\\,}$", " pour $n \\in \\mathbb{N}$.").scale(0.6).next_to(text_a_n_b_n, DOWN, buff=0.5).to_edge()

        text_a_0 = MathTex("a_0", color=YELLOW).scale(0.7 * 1.2 * 0.5).next_to(Dot(self.axes.c2p(a, 0)), DOWN, buff=0.15)#, RIGHT, buff=0.15).shift(0.035*DOWN)
        text_b_0 = MathTex("b_0", color=PURPLE).scale(0.7 * 1.2 * 0.5).next_to(Dot(self.axes.c2p(b, 0)), DOWN, buff=0.12)#, RIGHT, buff=0.15).shift(0.035*DOWN)
        k_dot = Dot(self.axes.c2p(0, k), radius=DEFAULT_SMALL_DOT_RADIUS, color=GREEN)
        x_k_dot = Dot(self.axes.c2p(3.05, 0), radius=DEFAULT_SMALL_DOT_RADIUS, color=BLUE)
        text_k = MathTex("k", color=GREEN).scale(0.7).next_to(k_dot, LEFT)
        text_x_k = MathTex("x_k", color=BLUE).scale(0.7).next_to(x_k_dot, DOWN)


        list_texts_a = [text_a_0]
        list_texts_b = [text_b_0]

        self.play(Write(text_type_demo), run_time=2)
        self.play(Write(text_construction_suite), run_time=2)
        self.play(DrawBorderThenFill(text_a_n_b_n))
        self.play(DrawBorderThenFill(text_c_n))
        self.wait(4)

        dot_a_0, dot_b_0 = Dot(self.axes.c2p(a, 0), radius=DEFAULT_SMALL_DOT_RADIUS, color=YELLOW), Dot(self.axes.c2p(b, 0), radius=DEFAULT_SMALL_DOT_RADIUS, color=PURPLE)
        dot_f_a_n, dot_f_b_n = Dot(self.axes.c2p(0, self.f(a)), radius=DEFAULT_SMALL_DOT_RADIUS, color=YELLOW), Dot(self.axes.c2p(0, self.f(b)), radius=DEFAULT_SMALL_DOT_RADIUS, color=PURPLE)
        text_f_a_0, text_f_b_0 = self.f_a.copy(), self.f_b.copy()

        list_text_f_a_n, list_text_f_b_n = [text_f_a_0], [text_f_b_0]

        self.play(
            Transform(self.a, text_a_0),
            Transform(self.b, text_b_0),
            Create(VGroup(dot_a_0, dot_b_0, k_dot, dot_f_a_n, dot_f_b_n)),
            Write(text_k)
        )
        
        self.add(text_a_0, text_b_0)
        self.remove(self.a, self.b)
        
        self.wait()

        a_n, b_n = [a], [b]
        list_dots = []
        text_b_4 = MathTex("b_4", color=PURPLE).scale(0.7 * 1.2 * 0.5).next_to(Dot(self.axes.c2p(3.25, 0)), UP, buff=0.13)

        for etape in range(nb_etapes):
            c_n = (a_n[etape] + b_n[etape])/2
            text_c_n_2 = MathTex("c_{}".format(etape)).next_to(Dot(self.axes.c2p(c_n, 0)), DOWN, buff=0.15).scale(0.7 * 1.2 * 0.5)

            dashed_line_c_n = DashedLine(self.axes.c2p(c_n, 0), self.axes.c2p(c_n, self.f(c_n)))
            dashed_line_f_c_n = DashedLine(self.axes.c2p(c_n, self.f(c_n)), self.axes.c2p(0, self.f(c_n)))
            c_n_f_c_n_dot = Dot(self.axes.c2p(c_n, self.f(c_n)), color=DARK_BROWN)
            f_c_n_dot = Dot(self.axes.c2p(0, self.f(c_n)), radius=DEFAULT_SMALL_DOT_RADIUS)
            c_n_f_c_n_dot.set_z_index(c_n_f_c_n_dot.z_index + 1)

            c_n_dot = Dot(self.axes.c2p(c_n, 0), radius=DEFAULT_SMALL_DOT_RADIUS, color=YELLOW * (self.f(c_n) <= k) + PURPLE * (self.f(c_n) > k))
            list_dots.append(c_n_dot)

            self.play(
                Write(text_c_n_2),
                Create(VGroup(c_n_dot, dashed_line_c_n)),
                run_time=1.5
            )

            self.play(Create(VGroup(c_n_f_c_n_dot, dashed_line_f_c_n)))
            self.play(Create(f_c_n_dot))
            self.wait(0.5)
            self.play(Indicate(VGroup(k_dot, f_c_n_dot), scale_factor=1.25))
            self.wait(0.5)
            self.play(FadeOut(VGroup(dashed_line_c_n, dashed_line_f_c_n, c_n_f_c_n_dot, f_c_n_dot)))
            self.wait(0.5)

            if self.f(c_n) <= k:
                new_a_n = c_n
                new_b_n = b_n[etape]
                text_new_a_n = MathTex("a_{}".format(etape + 1), color=YELLOW).scale(0.7 * 1.2 * 0.5).next_to(Dot(self.axes.c2p(c_n, 0)), DOWN * (etape < 3) + UP * (etape >= 3), buff=0.15)
                text_new_b_n = MathTex("= b_{}".format(etape + 1), color=PURPLE).scale(0.7 * 1.2 * 0.5).next_to(list_texts_b[etape], RIGHT, buff=0.08)
                a_n.append(new_a_n)
                b_n.append(new_b_n)
                list_texts_a.append(text_new_a_n)
                list_texts_b.append(text_new_b_n)

                text_f_a_n = MathTex("f(a_{})".format(etape + 1)).scale(0.7 * 1.2 * 0.5).next_to(self.axes.c2p(0, self.f(new_a_n)), LEFT)
                text_f_b_n = MathTex("f(b_{})".format(etape + 1)).scale(0.7 * 1.2 * 0.5).next_to(self.axes.c2p(0, self.f(new_b_n)), LEFT)
                VGroup(*text_f_a_n[0][2:4]).set_color(YELLOW)
                VGroup(*text_f_b_n[0][2:4]).set_color(PURPLE)

                self.play(
                    Transform(text_c_n_2, text_new_a_n),
                    Write(text_new_b_n),
                    dot_f_a_n.animate.move_to(self.axes.c2p(0, self.f(new_a_n))),
                    Transform(list_text_f_a_n[-1], text_f_a_n),
                    Transform(list_text_f_b_n[-1], text_f_b_n),
                    run_time=1.5
                )
                self.add(text_new_a_n, text_f_a_n, text_f_b_n)
                self.remove(text_c_n_2, list_text_f_a_n[-1], list_text_f_b_n[-1])
                list_text_f_a_n.append(text_f_a_n)
                list_text_f_b_n.append(text_f_b_n)
                self.wait(0.5)

            else:
                new_a_n = a_n[etape]
                new_b_n = c_n
                text_new_a_n = MathTex("= a_{}".format(etape + 1), color=YELLOW).scale(0.7 * 1.2 * 0.5).next_to(list_texts_a[etape], RIGHT, buff=0.08)
                text_new_b_n = MathTex("b_{}".format(etape + 1), color=PURPLE).scale(0.7 * 1.2 * 0.5).next_to(Dot(self.axes.c2p(c_n, 0)), DOWN * (etape < 2) + UP * (etape >= 2), buff=0.13)
                a_n.append(new_a_n)
                b_n.append(new_b_n)
                list_texts_a.append(text_new_a_n)
                list_texts_b.append(text_new_b_n)

                text_f_a_n = MathTex("f(a_{})".format(etape + 1)).scale(0.7 * 1.2 * 0.5).next_to(self.axes.c2p(0, self.f(new_a_n)), LEFT)
                text_f_b_n = MathTex("f(b_{})".format(etape + 1)).scale(0.7 * 1.2 * 0.5).next_to(self.axes.c2p(0, self.f(new_b_n)), LEFT)
                VGroup(*text_f_a_n[0][2:4]).set_color(YELLOW)
                VGroup(*text_f_b_n[0][2:4]).set_color(PURPLE)

                self.play(
                    Transform(text_c_n_2, text_new_b_n),
                    Write(text_new_a_n),
                    dot_f_b_n.animate.move_to(self.axes.c2p(0, self.f(new_b_n))),
                    Transform(list_text_f_a_n[-1], text_f_a_n),
                    Transform(list_text_f_b_n[-1], text_f_b_n),
                    run_time=1.5
                )
                self.add(text_new_b_n, text_f_a_n, text_f_b_n)
                self.remove(text_c_n_2, list_text_f_a_n[-1], list_text_f_b_n[-1])
                list_text_f_a_n.append(text_f_a_n)
                list_text_f_b_n.append(text_f_b_n)
                self.wait(0.5)

        self.play(
            FadeOut(VGroup(*list_texts_a[1:4], *list_texts_b[1:3], list_texts_b[4], *list_dots[0:2])),
            Transform(list_texts_b[3], text_b_4),
            Create(x_k_dot),
            Write(text_x_k),
            text_a_0.animate.scale(2/1.2).next_to(dot_a_0, DOWN),
            text_b_0.animate.scale(2/1.2).next_to(dot_b_0, DOWN, buff=0.22),
            text_k.animate.scale(1.2 * 0.5)
        )
        self.add(text_b_4)
        self.remove(list_texts_b[3])
        self.wait(0.4)

        self.play(FadeOut(VGroup(text_construction_suite, text_a_n_b_n, text_c_n)))
        self.wait(0.5)

        text_suites_adjacentes_1 = Tex("Les suites ", " $(a_n)$ ", " et ",  " $(b_n)$ ", " sont adjacentes,").scale(0.7).next_to(text_type_demo, DOWN, buff=0.4).to_edge()
        text_suites_adjacentes_2 = Tex("elles convergent donc vers la même limite", " $x_k$.").scale(0.7).next_to(text_suites_adjacentes_1, DOWN, buff=0.4).to_edge()
        text_continuite = Tex("Par ", " continuité ", " de $f$, ", " $f(a_n), f(b_n) \\to f(x_k)$.").scale(0.7).next_to(text_suites_adjacentes_2, DOWN, buff=0.4).to_edge()
        text_encadrement = Tex("Or", "$$\\forall n \\in \\mathbb{N}, f(a_n) \\leqslant k \\leqslant f(b_n)$$", "Donc par passage à la limite, ", "$k = f(x_k)$.", tex_environment="flushleft").scale(0.7).next_to(text_continuite, DOWN, buff=0.4).to_edge()
        text_continuite[3].shift(0.2 * RIGHT)
        text_encadrement[1].shift(2.75 * LEFT)
        VGroup(text_encadrement[2], text_encadrement[3]).shift(0.25 * DOWN)
        VGroup(*text_encadrement[1][5::]).shift(0.25 * RIGHT)

        VGroup(text_suites_adjacentes_1[1], *text_continuite[3][2:4], *text_encadrement[1][7: 9]).set_color(YELLOW)
        VGroup(text_suites_adjacentes_1[3], *text_continuite[3][8:10], *text_encadrement[1][15: 17]).set_color(PURPLE)
        VGroup(text_suites_adjacentes_2[1], *text_continuite[3][14:16], *text_encadrement[3][4:6]).set_color(BLUE)
        VGroup(text_encadrement[1][11], text_encadrement[3][0]).set_color(GREEN)
        text_continuite[1].set_color(RED)

        self.play(DrawBorderThenFill(text_suites_adjacentes_1))
        self.wait()
        self.play(DrawBorderThenFill(text_suites_adjacentes_2))
        self.wait()
        self.play(DrawBorderThenFill(text_continuite))
        self.wait()
        self.play(DrawBorderThenFill(text_encadrement))
        self.wait(5)

