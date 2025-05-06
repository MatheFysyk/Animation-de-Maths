from manim import *
import numpy as np

ordre = 11
HAUT = np.array([-0.52, 3.35, 0])

class Blanc_manger(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(self,
            x_min=0,
            x_max=0.55,
            num_graph_anchor_points=200,
            y_min=0,
            y_max=0.4,
            graph_origin= 4.6*LEFT + 3*DOWN,
            include_tip=True,
            axes_color=GREEN,
            **kwargs
        )
        self.function_color = RED
     
    def construct(self):
        self.setup_axes(animate=True)

        def g_n(x, n):
            li = [min(2**i*x - np.floor(2**i*x), np.ceil(2**i*x) -
                      2**i*x)/(2**i) for i in range(1, n)]
            return np.sum(li)

        term_num = [
            TexMobject("n = " + str(n))
            for n in range(0, ordre - 2)]
        
        for term in term_num:
            term.move_to(HAUT)

        liste_des_graphes = []

        for k in range(2, ordre):
            g_k = lambda x : g_n(x, k)
            liste_des_graphes.append(self.get_graph(g_k, self.function_color, x_min=0, x_max=0.5))
        
        self.play(ShowCreation(liste_des_graphes[0]))
        self.play(ShowCreation(term_num[0]))

        for k in range(len(liste_des_graphes) - 1):
            self.play(Transform(liste_des_graphes[k], liste_des_graphes[k+1]), Transform(term_num[k], term_num[k+1]))
            self.remove(liste_des_graphes[k], term_num[k])

        self.add(liste_des_graphes[-1], term_num[-1])
        self.wait(2)
