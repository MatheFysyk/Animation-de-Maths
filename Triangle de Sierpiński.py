from manim import *
import random as rd


#Y'a plus optimisé que ça bien sûr, mais ça marche déjà très bien.
#Attention, avec 25000 points, ça prend un peu de temps ...

max_num_of_points = 25000


class SierpinskiTriangle(Scene):
    def construct(self):
        self.polygon = RegularPolygon(n=3, stroke_width=0.25, color=WHITE).scale(4).move_to(ORIGIN)
        group_of_points = [np.array([0., 0., 0.])]
        group_of_dots = VGroup(Dot(group_of_points[0], radius=0.0025))

        for k in range(max_num_of_points - 1):
            new_point = self.get_random_point(group_of_points)
            group_of_points.append(new_point)
            group_of_dots.add(Dot(new_point, radius=0.005))

        self.add(self.polygon)
        self.play(ShowIncreasingSubsets(group_of_dots), run_time=10)

        

    def get_random_point(self, group_of_points):
        rand_int = rd.randint(0, len(self.polygon.get_vertices()) - 1)
        return Line(group_of_points[-1], self.polygon.get_vertices()[rand_int]).get_midpoint()
