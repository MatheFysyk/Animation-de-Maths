from manim import *
from numba import njit
from scipy.integrate import quad



SCREEN_RATIO = 1920 / 1080
UNIT_SIZE_X, UNIT_SIZE_Y = 192, 108
MULTIPLE_X, MULTIPLE_Y = 10, 10     


@njit
def newton_fractal(
        zeros_list: np.ndarray = np.zeros(1, dtype=np.float),
        max_iterations: int = 100,
        threshold: float = .1,
        a: complex = complex(1, 0),
        x_range: np.ndarray = np.array([-1.5 * SCREEN_RATIO, 1.5 * SCREEN_RATIO, MULTIPLE_X * UNIT_SIZE_X], dtype=np.float),
        y_range: np.ndarray = np.array([-1.5, 1.5, MULTIPLE_Y * UNIT_SIZE_Y], dtype=np.float)
    ) -> np.ndarray:
    x_min, x_max, nx = x_range
    y_min, y_max, ny = y_range
    nx, ny = int(nx), int(ny)
    dx, dy = np.abs(x_max - x_min) / nx, np.abs(y_max - y_min) / ny

    res_array = np.zeros((ny, nx, 3), dtype=np.uint8)

    color_list = np.linspace(0, 1, len(zeros_list))

    for line in range(len(res_array)):
        for column in range(len(res_array[0])):
            z_0 = complex(x_min + column * dx, y_max - line * dy)

            iteration = -1

            while iteration < max_iterations:
                P_z_0 = 1
                dP_z_0 = 0
                
                for i in range(len(zeros_list)):
                    P_z_0 *= (z_0 - zeros_list[i])
                    dP_z_0_term = 1
                    for j in range(len(zeros_list)):
                        if j != i:
                            dP_z_0_term *= (z_0 - zeros_list[j])
                    dP_z_0 += dP_z_0_term
                
                if dP_z_0 != 0:
                    z_0 = z_0 - a * P_z_0 / dP_z_0
                
                else:
                    z_0 = z_0

                iteration += 1
                stop = False

                for zero_index in range(len(zeros_list)):
                    if np.abs(z_0 - zeros_list[zero_index]) <= threshold:

                        l = .5 * (1 - (iteration / max_iterations))
                        H = int(240 * color_list[zero_index])

                        D = 1 - np.abs(2 * l - 1)
                        m = 255 * (l - D / 2)
                        x = D * (1 - np.abs((H / 60) % 2 - 1))

                        if 0 <= H < 60:
                            R = np.uint8(255 * D + m)
                            G = np.uint8(255 * x + m)
                            B = np.uint8(m)

                        if 60 <= H < 120:
                            R = np.uint8(255 * x + m)
                            G = np.uint8(255 * D + m)
                            B = np.uint8(m)

                        if 120 <= H < 180:
                            R = np.uint8(m)
                            G = np.uint8(255 * D + m)
                            B = np.uint8(255 * x + m)

                        if 180 <= H <= 240:
                            R = np.uint8(m)
                            G = np.uint8(255 * x + m)
                            B = np.uint8(255 * D + m)

                        res_array[line, column] = np.array([R, G, B], dtype=np.uint8)
                        stop = True
                        break
                
                if stop:
                    break

    return res_array


def fit_screen_height(mob: Mobject) -> Mobject:
    mob.match_height(Rectangle(height=config.frame_height))
    return mob


def unit_roots(n: int) -> np.ndarray:
    return np.array([np.exp(2 * complex(0, 1) * k * PI / n) for k in range(n)])


def get_array(z: complex) -> np.ndarray:
    return np.array([z.real, z.imag, 0])


def normalize(array: np.ndarray) -> np.ndarray:
    if np.linalg.norm(array) == 0:
        return np.zeros(3, dtype=np.float)
    return array / np.linalg.norm(array)



def smooth_increase(t: float) -> float:
    integral = quad(lambda x: np.exp(-1/(1 - 4 * (x - .5)**2)), 0, 1)[0]
    try:
        return t * quad(lambda x: np.exp(-1/(1 - 4 * (x - .5)**2)) / integral, 0, t)[0]
    except ZeroDivisionError:
        return 0
    

def smooth_decrease(t: float) -> float:
    return smooth_increase(1 - t)



class NewtonFractalsP2(Scene):
    def construct(self):
        z_1, z_2, z_3, z_4, z_5 = ComplexValueTracker(0), ComplexValueTracker(0), ComplexValueTracker(0), ComplexValueTracker(0), ComplexValueTracker(0)
        
        ### For parts following part 1, to set the correct values of each ending of the previous Part
        z_1.set_value(complex(1, 1))
        z_2.set_value(unit_roots(5)[4])
        z_3.set_value(complex(-.75, .5))
        z_4.set_value(unit_roots(5)[3])
        z_5.set_value(unit_roots(5)[4])
        ###

        complex_plane = NumberPlane(
            x_range=np.array([-1.5 * SCREEN_RATIO, 1.5 * SCREEN_RATIO, MULTIPLE_X * UNIT_SIZE_X], dtype=np.float),
            y_range=np.array([-1.5, 1.5, MULTIPLE_Y * UNIT_SIZE_Y], dtype=np.float),
            x_length=config.frame_width,
            y_length=config.frame_height
        )
        
        Dot_z_1 = always_redraw(lambda: Dot(complex_plane.c2p(z_1.get_value().real, z_1.get_value().imag), color=BLACK, radius=DEFAULT_SMALL_DOT_RADIUS)),
        Dot_z_2 = always_redraw(lambda: Dot(complex_plane.c2p(z_2.get_value().real, z_2.get_value().imag), color=BLACK, radius=DEFAULT_SMALL_DOT_RADIUS)),
        Dot_z_3 = always_redraw(lambda: Dot(complex_plane.c2p(z_3.get_value().real, z_3.get_value().imag), color=BLACK, radius=DEFAULT_SMALL_DOT_RADIUS)),
        Dot_z_4 = always_redraw(lambda: Dot(complex_plane.c2p(z_4.get_value().real, z_4.get_value().imag), color=BLACK, radius=DEFAULT_SMALL_DOT_RADIUS)),
        Dot_z_5 = always_redraw(lambda: Dot(complex_plane.c2p(z_5.get_value().real, z_5.get_value().imag), color=BLACK, radius=DEFAULT_SMALL_DOT_RADIUS)),
        
        roots_dots = [Dot_z_1[0], Dot_z_2[0], Dot_z_3[0], Dot_z_4[0], Dot_z_5[0]]

        label_z_1 = MathTex(
            "z_1", color=BLACK
        ).move_to(complex_plane.c2p(*get_array(unit_roots(5)[0]))).shift(.4 * normalize(complex_plane.c2p(*get_array(unit_roots(5)[0])))),
        label_z_2 = MathTex(
            "z_2", color=BLACK
        ).move_to(complex_plane.c2p(*get_array(unit_roots(5)[1]))).shift(.4 * normalize(complex_plane.c2p(*get_array(unit_roots(5)[1])))),
        label_z_3 = MathTex(
            "z_3", color=BLACK
        ).move_to(complex_plane.c2p(*get_array(unit_roots(5)[2]))).shift(.4 * normalize(complex_plane.c2p(*get_array(unit_roots(5)[2])))),
        label_z_4 = MathTex(
            "z_4", color=BLACK
        ).move_to(complex_plane.c2p(*get_array(unit_roots(5)[3]))).shift(.4 * normalize(complex_plane.c2p(*get_array(unit_roots(5)[3])))),
        label_z_5 = MathTex(
            "z_5", color=BLACK
        ).move_to(complex_plane.c2p(*get_array(unit_roots(5)[4]))).shift(.4 * normalize(complex_plane.c2p(*get_array(unit_roots(5)[4])))),

        def update_labels(label, tracker):
            label.move_to(complex_plane.c2p(tracker.get_value().real, tracker.get_value().imag)).shift(.4 * normalize(complex_plane.c2p(tracker.get_value().real, tracker.get_value().imag)))

        roots_dots_labels = [label_z_1[0], label_z_2[0], label_z_3[0], label_z_4[0], label_z_5[0]]

        im = always_redraw(lambda: fit_screen_height(ImageMobject(newton_fractal(
            np.array([z_1.get_value(), z_2.get_value(), z_3.get_value(), z_4.get_value(), z_5.get_value()], dtype=complex)
        ))))


        self.add(im)
        self.add(*roots_dots)

        """
        self.wait()
        self.play(
            AnimationGroup(
                AnimationGroup(
                    z_1.animate.set_value(unit_roots(5)[0]),
                    FadeIn(label_z_1[0], shift=complex_plane.c2p(*get_array(unit_roots(5)[0])) + .4 * normalize(complex_plane.c2p(*get_array(unit_roots(5)[0]))))
                ),
                AnimationGroup(
                    z_2.animate.set_value(unit_roots(5)[1]),
                    FadeIn(label_z_2[0], shift=complex_plane.c2p(*get_array(unit_roots(5)[1])) + .4 * normalize(complex_plane.c2p(*get_array(unit_roots(5)[1]))))
                ),
                AnimationGroup(
                    z_3.animate.set_value(unit_roots(5)[2]),
                    FadeIn(label_z_3[0], shift=complex_plane.c2p(*get_array(unit_roots(5)[2])) + .4 * normalize(complex_plane.c2p(*get_array(unit_roots(5)[2]))))
                ),
                AnimationGroup(
                    z_4.animate.set_value(unit_roots(5)[3]),
                    FadeIn(label_z_4[0], shift=complex_plane.c2p(*get_array(unit_roots(5)[3])) + .4 * normalize(complex_plane.c2p(*get_array(unit_roots(5)[3]))))
                ),
                AnimationGroup(
                    z_5.animate.set_value(unit_roots(5)[4]),
                    FadeIn(label_z_5[0], shift=complex_plane.c2p(*get_array(unit_roots(5)[4])) + .4 * normalize(complex_plane.c2p(*get_array(unit_roots(5)[4]))))
                ), lag_ratio=.5
            ), run_time=10
        )
        #self.wait()
        """

        label_z_1[0].add_updater(lambda label: update_labels(label, z_1))
        label_z_2[0].add_updater(lambda label: update_labels(label, z_2))
        label_z_3[0].add_updater(lambda label: update_labels(label, z_3))
        label_z_4[0].add_updater(lambda label: update_labels(label, z_4))
        label_z_5[0].add_updater(lambda label: update_labels(label, z_5))

        self.add(label_z_1[0], label_z_2[0], label_z_3[0], label_z_4[0], label_z_5[0])

        """
        #self.play(z_1.animate.set_value(complex(1, 1)), run_time=2)
        #self.wait()
        #self.play(z_3.animate.set_value(complex(-.75, .5)), z_2.animate.set_value(unit_roots(5)[4]), run_time=4, rate_func=smooth_increase)
        #self.wait()
        """

        self.play(z_4.animate.set_value(complex(0, -1)), z_5.animate.set_value(complex(-1, -1)), run_time=3, rate_func=linear)
        self.play(
            z_1.animate.set_value(unit_roots(3)[0]),
            z_2.animate.set_value(unit_roots(3)[1]),
            z_3.animate.set_value(unit_roots(3)[1]),
            z_4.animate.set_value(unit_roots(3)[2]),
            z_5.animate.set_value(unit_roots(3)[2]),
            run_time=3, rate_func=smooth_decrease
        )
        self.wait()
        self.play(
            z_1.animate.set_value(unit_roots(3)[2]),
            z_2.animate.set_value(unit_roots(3)[0]),
            z_3.animate.set_value(unit_roots(3)[0]),
            z_4.animate.set_value(unit_roots(3)[1]),
            z_5.animate.set_value(unit_roots(3)[1]),
            run_time=3, rate_func=smooth_increase
        )
        self.play(
            z_1.animate.set_value(unit_roots(3)[1]),
            z_2.animate.set_value(unit_roots(3)[2]),
            z_3.animate.set_value(unit_roots(3)[2]),
            z_4.animate.set_value(unit_roots(3)[0]),
            z_5.animate.set_value(unit_roots(3)[0]),
            run_time=3, rate_func=smooth_decrease
        )
        self.wait()
        self.play(
            z_1.animate.set_value(unit_roots(5)[0]),
            z_2.animate.set_value(unit_roots(5)[1]),
            z_3.animate.set_value(unit_roots(5)[2]),
            z_4.animate.set_value(unit_roots(5)[3]),
            z_5.animate.set_value(unit_roots(5)[4]),
            run_time=4
        )
        self.wait()


