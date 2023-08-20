from manim import *
from typing import Sequence


class TheoremObject(VMobject):
    def __init__(self, number: int, fill_color: str, stroke_color: str, **kwargs):
        self.rectangle = Rectangle()
        self.text = MathTex(r"\mathrm{Theorem \; %s \; : \quad} ..." %number, color=WHITE).move_to(self.rectangle).shift(1.5 * LEFT)

        self.rectangle.set_fill(fill_color, 1).set_stroke(stroke_color, 1.5, 1)
        self.rectangle.stretch_to_fit_height(self.text.copy().stretch(2.75, 1).height)
        self.rectangle.stretch_to_fit_width(self.text.copy().stretch(2, 0).width)
        self.rectangle.round_corners(0.25)
        self.text.set_z_index(self.rectangle.z_index + 1)

        super().__init__(self, **kwargs)
        self.add(self.rectangle, self.text)

    
class CoveringRectangle(Rectangle):
    def __init__(self) -> None:
        super().__init__(height=config.frame_height + 10, width=config.frame_width + 10, fill_color=BLACK, fill_opacity=1, stroke_width=0)
        self.set_z_index(1000)


class MorleyTriangle(VMobject):
    def __init__(
            self,
            vertices: Sequence[complex],
            direct: bool = True,
            outer_triangle_config: dict = {"line_color": YELLOW, "vertices_color": WHITE, "label_color": YELLOW, "angle_color": GREEN, "label_angle_color": GREEN},
            trisector_config: dict = {"color": WHITE, "stroke_opacity": 0.3},
            inner_triangle_config: dict = {"line_color": BLUE, "vertices_color": WHITE, "label_color": BLUE},
            outer_labels: Sequence[str] | None = None,
            inner_labels: Sequence[str] | None = None,
            **kwargs
        ) -> None:
        super().__init__(self, **kwargs)
        self.direct = direct
        self.vertices = vertices
        self.outer_labels = outer_labels
        self.inner_labels = inner_labels
        self.trisector_config = {"color": WHITE, "stroke_opacity": 0.3}
        self.outer_triangle_config = {"line_color": YELLOW, "vertices_color": WHITE, "label_color": WHITE, "angle_color": WHITE, "label_angle_color": WHITE}
        self.inner_triangle_config = {"line_color": YELLOW, "vertices_color": WHITE, "label_color": WHITE}
        self.trisector_config.update(trisector_config)
        self.outer_triangle_config.update(outer_triangle_config)
        self.inner_triangle_config.update(inner_triangle_config)

        self.U, self.V, self.W = self.vertices
        self.u, self.v, self.w = self.C2P(self.U), self.C2P(self.V), self.C2P(self.W)
        
        self.computations()
        self.create_trisectors()

        self.create_outer_triangle_angles()
        self.create_outer_triangle_edges()
        self.create_outer_triangle_vertices()

        self.create_inner_triangle_edges()
        self.create_inner_triangle_vertices()

        self.create_inner_triangle_vertices_labels()
        self.create_outer_triangle_vertices_labels()
        self.create_outer_triangle_angles_labels()

        self.outer_lines = VGroup(self.AB_line, self.BC_line, self.CA_line)
        self.outer_dots = VGroup(self.A, self.B, self.C)
        self.outer_labels = VGroup(self.A_label, self.B_label, self.C_label)
        self.outer_angle = VGroup(self.BAC_angle, self.CBA_angle, self.ACB_angle)
        self.outer_angle_labels = VGroup(self.BAC_angle_label, self.CBA_angle_label, self.ACB_angle_label)
        self.inner_lines = VGroup(self.PQ_line, self.QR_line, self.RP_line)
        self.inner_dots = VGroup(self.P, self.Q, self.R)
        self.inner_labels = VGroup(self.P_label, self.Q_label, self.R_label)
        self.trisectors = VGroup(self.trisectors_from_A, self.trisectors_from_B, self.trisectors_from_C)
        self.subvmobjects = VGroup(
            self.AB_line, self.BC_line, self.CA_line, self.A, self.B, self.C,
            self.A_label, self.B_label, self.C_label, self.BAC_angle, self.CBA_angle, self.ACB_angle,
            self.BAC_angle_label, self.CBA_angle_label, self.ACB_angle_label, self.PQ_line, self.QR_line, self.RP_line,
            self.P, self.Q, self.R, self.P_label, self.Q_label, self.R_label,
            self.trisectors_from_A, self.trisectors_from_B, self.trisectors_from_C
        )


    def computations(self):
        if self.direct:
            self.BAC_angle_value = Angle(Line(self.u, self.v), Line(self.u, self.w)).get_value()
            self.CBA_angle_value = Angle(Line(self.v, self.w), Line(self.v, self.u)).get_value()
            self.ACB_angle_value = Angle(Line(self.w, self.u), Line(self.w, self.v)).get_value()

            self.a1 = np.exp(2 * self.BAC_angle_value / 3 * complex(0, 1))
            self.a2 = np.exp(2 * self.CBA_angle_value / 3 * complex(0, 1))
            self.a3 = np.exp(2 * self.ACB_angle_value / 3 * complex(0, 1))

            self.b1 = self.U * (1 - self.a1)
            self.b2 = self.V * (1 - self.a2)
            self.b3 = self.W * (1 - self.a3)

            self.p = (self.a2 * self.b3 + self.b2) / (1 - self.a2 * self.a3)
            self.q = (self.a3 * self.b1 + self.b3) / (1 - self.a3 * self.a1)
            self.r = (self.a1 * self.b2 + self.b1) / (1 - self.a1 * self.a2)

        else:
            self.BAC_angle_value = Angle(Line(self.u, self.w), Line(self.u, self.v)).get_value()
            self.CBA_angle_value = Angle(Line(self.v, self.u), Line(self.v, self.w)).get_value()
            self.ACB_angle_value = Angle(Line(self.w, self.v), Line(self.w, self.u)).get_value()

            self.a1 = np.exp(-2 * self.BAC_angle_value / 3 * complex(0, 1))
            self.a2 = np.exp(-2 * self.CBA_angle_value / 3 * complex(0, 1))
            self.a3 = np.exp(-2 * self.ACB_angle_value / 3 * complex(0, 1))

            self.b1 = self.U * (1 - self.a1)
            self.b2 = self.V * (1 - self.a2)
            self.b3 = self.W * (1 - self.a3)

            self.p = (self.a2 * self.b3 + self.b2) / (1 - self.a2 * self.a3)
            self.q = (self.a3 * self.b1 + self.b3) / (1 - self.a3 * self.a1)
            self.r = (self.a1 * self.b2 + self.b1) / (1 - self.a1 * self.a2)


    def create_outer_triangle_angles(self):
        if self.direct:
            self.BAC_angle = Angle(Line(self.u, self.v), Line(self.u, self.w), radius=0.6, color=self.outer_triangle_config["angle_color"])
            self.CBA_angle = Angle(Line(self.v, self.w), Line(self.v, self.u), radius=0.6, color=self.outer_triangle_config["angle_color"])
            self.ACB_angle = Angle(Line(self.w, self.u), Line(self.w, self.v), radius=0.6, color=self.outer_triangle_config["angle_color"])
        else:
            self.BAC_angle = Angle(Line(self.u, self.w), Line(self.u, self.v), radius=0.6, color=self.outer_triangle_config["angle_color"])
            self.CBA_angle = Angle(Line(self.v, self.u), Line(self.v, self.w), radius=0.6, color=self.outer_triangle_config["angle_color"])
            self.ACB_angle = Angle(Line(self.w, self.v), Line(self.w, self.u), radius=0.6, color=self.outer_triangle_config["angle_color"])
        
        self.add(self.BAC_angle, self.CBA_angle, self.ACB_angle)


    def create_trisectors(self):
        self.trisectors_from_A = VGroup().add(DashedLine(self.u, self.C2P(self.r), **self.trisector_config), DashedLine(self.u, self.C2P(self.q), **self.trisector_config))
        self.trisectors_from_B = VGroup().add(DashedLine(self.v, self.C2P(self.p), **self.trisector_config), DashedLine(self.v, self.C2P(self.r), **self.trisector_config))
        self.trisectors_from_C = VGroup().add(DashedLine(self.w, self.C2P(self.q), **self.trisector_config), DashedLine(self.w, self.C2P(self.p), **self.trisector_config))     
        self.add(self.trisectors_from_A, self.trisectors_from_B, self.trisectors_from_C)


    def create_outer_triangle_edges(self):
        self.AB_line = Line(self.u, self.v, color=self.outer_triangle_config["line_color"])
        self.BC_line = Line(self.v, self.w, color=self.outer_triangle_config["line_color"])
        self.CA_line = Line(self.w, self.u, color=self.outer_triangle_config["line_color"])
        self.add(self.AB_line, self.BC_line, self.CA_line)


    def create_outer_triangle_vertices(self):
        self.A = Dot(self.u, color=self.outer_triangle_config["vertices_color"])
        self.B = Dot(self.v, color=self.outer_triangle_config["vertices_color"])
        self.C = Dot(self.w, color=self.outer_triangle_config["vertices_color"])
        self.add(self.A, self.B, self.C)


    def create_outer_triangle_vertices_labels(self):
        if self.outer_labels != None:
            a_label, b_label, c_label = self.outer_labels
        else:
            a_label, b_label, c_label = "A", "B", "C"

        if self.direct:
            unit_vector_for_A_label = -self.AB_line.copy().rotate(self.BAC_angle_value / 2).get_unit_vector()
            unit_vector_for_B_label = -self.BC_line.copy().rotate(self.CBA_angle_value / 2).get_unit_vector()
            unit_vector_for_C_label = -self.CA_line.copy().rotate(self.ACB_angle_value / 2).get_unit_vector()

            self.A_label = MathTex(a_label, color=self.outer_triangle_config["label_color"]).move_to(self.A).shift(0.5 * unit_vector_for_A_label)
            self.B_label = MathTex(b_label, color=self.outer_triangle_config["label_color"]).move_to(self.B).shift(0.5 * unit_vector_for_B_label)
            self.C_label = MathTex(c_label, color=self.outer_triangle_config["label_color"]).move_to(self.C).shift(0.5 * unit_vector_for_C_label)

        else:
            unit_vector_for_A_label = -self.AB_line.copy().rotate(-self.BAC_angle_value / 2).get_unit_vector()
            unit_vector_for_B_label = -self.BC_line.copy().rotate(-self.CBA_angle_value / 2).get_unit_vector()
            unit_vector_for_C_label = -self.CA_line.copy().rotate(-self.ACB_angle_value / 2).get_unit_vector()

            self.A_label = MathTex(a_label, color=self.outer_triangle_config["label_color"]).move_to(self.A).shift(0.5 * unit_vector_for_A_label)
            self.B_label = MathTex(b_label, color=self.outer_triangle_config["label_color"]).move_to(self.B).shift(0.5 * unit_vector_for_B_label)
            self.C_label = MathTex(c_label, color=self.outer_triangle_config["label_color"]).move_to(self.C).shift(0.5 * unit_vector_for_C_label)        
        
        self.add(self.A_label, self.B_label, self.C_label)


    def create_outer_triangle_angles_labels(self):
        if self.direct:
            self.BAC_angle_label = MathTex(r"3\alpha", color=self.outer_triangle_config["label_angle_color"]).move_to(Angle(Line(self.u, self.v), Line(self.u, self.w), radius=self.BAC_angle.radius + 0.4).point_from_proportion(0.5))
            self.CBA_angle_label = MathTex(r"3\beta", color=self.outer_triangle_config["label_angle_color"]).move_to(Angle(Line(self.v, self.w), Line(self.v, self.u), radius=self.CBA_angle.radius + 0.4).point_from_proportion(0.5))
            self.ACB_angle_label = MathTex(r"3\gamma", color=self.outer_triangle_config["label_angle_color"]).move_to(Angle(Line(self.w, self.u), Line(self.w, self.v), radius=self.ACB_angle.radius + 0.4).point_from_proportion(0.5))
        else:
            self.BAC_angle_label = MathTex(r"3\alpha", color=self.outer_triangle_config["label_angle_color"]).move_to(Angle(Line(self.u, self.w), Line(self.u, self.v), radius=self.BAC_angle.radius + 0.4).point_from_proportion(0.5))
            self.CBA_angle_label = MathTex(r"3\beta", color=self.outer_triangle_config["label_angle_color"]).move_to(Angle(Line(self.v, self.u), Line(self.v, self.w), radius=self.CBA_angle.radius + 0.4).point_from_proportion(0.5))
            self.ACB_angle_label = MathTex(r"3\gamma", color=self.outer_triangle_config["label_angle_color"]).move_to(Angle(Line(self.w, self.v), Line(self.w, self.u), radius=self.ACB_angle.radius + 0.4).point_from_proportion(0.5))
        self.add(self.BAC_angle_label, self.CBA_angle_label, self.ACB_angle_label)


    def create_inner_triangle_edges(self):
        self.PQ_line = Line(self.C2P(self.p), self.C2P(self.q), color=self.inner_triangle_config["line_color"])
        self.QR_line = Line(self.C2P(self.q), self.C2P(self.r), color=self.inner_triangle_config["line_color"])
        self.RP_line = Line(self.C2P(self.r), self.C2P(self.p), color=self.inner_triangle_config["line_color"])
        self.add(self.PQ_line, self.QR_line, self.RP_line)


    def create_inner_triangle_vertices(self):
        self.P = Dot(self.C2P(self.p), color=self.inner_triangle_config["vertices_color"])
        self.Q = Dot(self.C2P(self.q), color=self.inner_triangle_config["vertices_color"])
        self.R = Dot(self.C2P(self.r), color=self.inner_triangle_config["vertices_color"])
        self.add(self.P, self.Q, self.R)


    def create_inner_triangle_vertices_labels(self):
        if self.inner_labels != None:
            p_label, q_label, r_label = self.inner_labels
        else:
            p_label, q_label, r_label = "P", "Q", "R"

        if self.direct:
            unit_vector_for_P_label = -self.PQ_line.copy().rotate(PI / 6).get_unit_vector()
            unit_vector_for_Q_label = -self.QR_line.copy().rotate(PI / 6).get_unit_vector()
            unit_vector_for_R_label = -self.RP_line.copy().rotate(PI / 6).get_unit_vector()

            self.P_label = MathTex(p_label, color=self.inner_triangle_config["label_color"]).move_to(self.P).shift(0.5 * unit_vector_for_P_label)
            self.Q_label = MathTex(q_label, color=self.inner_triangle_config["label_color"]).move_to(self.Q).shift(0.5 * unit_vector_for_Q_label)
            self.R_label = MathTex(r_label, color=self.inner_triangle_config["label_color"]).move_to(self.R).shift(0.5 * unit_vector_for_R_label)
        else:
            unit_vector_for_P_label = -self.PQ_line.copy().rotate(-PI / 6).get_unit_vector()
            unit_vector_for_Q_label = -self.QR_line.copy().rotate(-PI / 6).get_unit_vector()
            unit_vector_for_R_label = -self.RP_line.copy().rotate(-PI / 6).get_unit_vector()

            self.P_label = MathTex(p_label, color=self.inner_triangle_config["label_color"]).move_to(self.P).shift(0.5 * unit_vector_for_P_label)
            self.Q_label = MathTex(q_label, color=self.inner_triangle_config["label_color"]).move_to(self.Q).shift(0.5 * unit_vector_for_Q_label)
            self.R_label = MathTex(r_label, color=self.inner_triangle_config["label_color"]).move_to(self.R).shift(0.5 * unit_vector_for_R_label)
        
        self.add(self.P_label, self.Q_label, self.R_label)

       
    def C2P(self, complex: complex) -> np.ndarray:
        return np.array([complex.real, complex.imag, 0])
    
    def P2C(self, point: np.ndarray) -> complex:
        return complex(point[0], point[1])

    def module(complex: complex) -> float:
        return np.sqrt(complex.real ** 2 + complex.imag ** 2)





