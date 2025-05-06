from manim import *
import numpy as np


x_min = -3
x_max = 3
y_min = -2
y_max = 2
h = 10**(-2)
point = -1
point_2 = 1
ordre = 8


HAUT = np.array([-4.5, 3.35, 0])


class DL(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(self,
            x_min=x_min,
            x_max=x_max,
            num_graph_anchor_points=200,
            y_min=-y_min,
            y_max=y_max,
            #x_labeled_nums=range(x_min, x_max),
            #y_labeled_nums=range(y_min, y_max),
            graph_origin= np.array([0, 0, 0]),
            include_tip=True,
            axes_color=GREEN,
            **kwargs)

        self.function_exp_color = BLUE
        self.fonction_dl_color  = RED
        self.x_min, self.x_max, self.y_min, self.y_max = x_min, x_max, y_min, y_max
        
        
    def construct(self):
        self.setup_axes(animate=True)
        self.animation_dl()
        

    def animation_dl(self):
        func = lambda x : np.exp(-x**2)
        graph_func = self.get_graph(func, self.function_exp_color, x_min=self.x_min, x_max=self.x_max).set_z_index(2)
        self.axes.set_z_index(1)
        self.play(ShowCreation(graph_func))

        point_value = ValueTracker(point)

        line_1 = self.get_vertical_line_to_graph(point, graph_func, color=YELLOW).set_z_index(9)
        dot = Dot(np.array([self.coords_to_point(point, func(point))[0], self.coords_to_point(point, func(point))[1], 0]), color=YELLOW).set_z_index(10)

        label_text = TexMobject("a = ")
        label_tex = DecimalNumber(point).add_updater(lambda value : value.set_value(point_value.get_value()))
        label_text.next_to(label_tex, LEFT)

        label = VGroup(label_text, label_tex).set_z_index(9)
        label.next_to(line_1, DOWN)

        def derivative(self, f):
            def df(x):
                return (f(x+h) - f(x-h))/(2*h)
            return df

        def derivative_n(self, f, n):
            if n == 0:
                return f
            else:
                return derivative_n(self, derivative(self, f), n-1)

        def f_n(x, ordre, point):
            li = [derivative_n(self, func, k)(point)/np.math.factorial(k) * (x - point)**k for k in range(0, ordre, 1)]
            return np.sum(li)

        term_num, liste_des_graphes = [], []

        for k in range(1, ordre):
            def f_k(x):
                return f_n(x, k, point)
            text = TexMobject("n = " + str(k-1))
            text.move_to(HAUT)
            term_num.append(text)
            graph_k = self.get_graph(f_k, self.fonction_dl_color, x_min=self.x_min, x_max=self.x_max).set_z_index(6)
            liste_des_graphes.append(graph_k)

        self.play(ShowCreation(liste_des_graphes[0]))
        self.play(ShowCreation(term_num[0]))
        self.play(ShowCreation(line_1), ShowCreation(dot))

        for k in range(len(liste_des_graphes) - 1):
            self.play(Transform(
                liste_des_graphes[k], liste_des_graphes[k+1]), Transform(term_num[k], term_num[k+1]), run_time=1.3)
            self.wait(0.2)
            self.remove(liste_des_graphes[k], term_num[k])

        self.add(liste_des_graphes[-1], term_num[-1])
        self.wait(2)

        def func_moving(a):
            return lambda x : f_n(x, ordre-1, a)
        
        graph = self.get_graph(func_moving(point), self.fonction_dl_color, x_min=self.x_min, x_max=self.x_max).set_z_index(6)

        self.add(graph)
        self.remove(liste_des_graphes[-1])
        self.play(Uncreate(term_num[-1]))
        self.play(ShowCreation(label))

        graph.add_updater(lambda graph: graph.become(self.get_graph(func_moving(point_value.get_value()), self.fonction_dl_color, x_min=self.x_min, x_max=self.x_max).set_z_index(6)))
        line_1.add_updater(lambda line: line.become(self.get_vertical_line_to_graph(point_value.get_value(), graph_func, color=YELLOW).set_z_index(9)))
        dot.add_updater(lambda dot: dot.become(
                Dot(np.array([self.coords_to_point(point_value.get_value(), func(point_value.get_value()))[0],
                self.coords_to_point(point_value.get_value(), func(point_value.get_value()))[1], 0]), color=YELLOW).set_z_index(10)
                ))
        label.add_updater(lambda label : label.next_to(line_1, DOWN))

        self.play(point_value.animate.set_value(point_2), rate_func=linear, run_time=6)
        self.wait(2)
