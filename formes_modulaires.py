from manim import *
from numba import njit
from colorsys import hls_to_rgb
from cmath import phase
from typing import Sequence, Callable


@njit
def G(k: int, tau: complex, max_term_order: int = 10):
    lattice_values = np.array([(m, n) for m in range(1, max_term_order + 1) for n in range(1, max_term_order + 1)])
    return 1 + 1 / tau ** (2 * k) + np.sum(np.array([1 / (value[0] + value[1] * tau) ** (2 * k) for value in lattice_values]))

        
@njit
def plot_complex_function(
        f: Callable[[complex], complex],
        real_range: Sequence = [-1.5, 1.5, .005],
        imag_range: Sequence = [-1, 1, .005],
        h_factor: float = 1
    ) -> np.ndarray:

    x_min, x_max, dx = real_range
    y_min, y_max, dy = imag_range
    n_x, n_y = int(np.abs(x_max - x_min) / dx), int(np.abs(y_max - y_min) / dy)
    res_array = np.zeros((n_y, n_x, 3), dtype="uint8")
    for n in range(len(res_array)):
        for p in range(len(res_array[0])):
            z = complex(x_min + p * dx, y_max - n * dy)
            h = (phase(f(z)) + PI) / (2 * PI)
            l = (h_factor * np.log(np.abs(f(z))) / (1 + np.abs(h_factor * np.log(np.abs(f(z))))) + 1) / 2

            H = int(360 * h)

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

            if 180 <= H < 240:
                R = np.uint8(m)
                G = np.uint8(255 * x + m)
                B = np.uint8(255 * D + m)

            if 240 <= H < 300:
                R = np.uint8(255 * x + m)
                G = np.uint8(m)
                B = np.uint8(255 * D + m)

            if 300 <= H < 360:
                R = np.uint8(255 * D + m)
                G = np.uint8(m)
                B = np.uint8(255 * x + m)

            res_array[n, p] = R, G, B
            #res_array[n, p] = h, l, 1.
    return res_array


@njit
def plot_eisenstein_series(
        k: int,
        max_term_order: int = 10,
        matrix_for_action: np.ndarray = np.eye(2),
        real_range: Sequence = np.array([-1.5, 1.5, 3 / 1000]),
        imag_range: np.ndarray = np.array([0.01, 1.5, 1.5 / (1000 * 1080 / 1920)])
    ) -> np.ndarray:
    x_min, x_max, dx = real_range
    y_min, y_max, dy = imag_range
    n_x, n_y = int(np.abs(x_max - x_min) / dx), int(np.abs(y_max - y_min) / dy)
    res_array = np.zeros((n_y, n_x, 3), dtype="uint8")
    a, b, c, d = matrix_for_action[0, 0], matrix_for_action[0, 1], matrix_for_action[1, 0], matrix_for_action[1, 1]

    for n in range(len(res_array)):
        for p in range(len(res_array[0])):
            z = complex(x_min + p * dx, y_max - n * dy)
            matrix_acting_on_z = (a * z + b) / (c * z + d)
            
            lattice_values = np.array([(m, n) for m in range(-max_term_order, max_term_order + 1) for n in range(-max_term_order, max_term_order + 1)])
            f_z = 1 / (c * z + d) ** (2 * k) * np.sum(np.array([1 / (value[0] + value[1] * matrix_acting_on_z) ** (2 * k) for value in lattice_values if value[0] != 0 or value[1] != 0]))

            h = (phase(f_z) + PI) / (2 * PI)
            l = (0.05 * np.log(np.abs(f_z)) / (1 + 0.05 * np.abs(np.log(np.abs(f_z)))) + 1) / 2

            H = int(360 * h)

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

            if 180 <= H < 240:
                R = np.uint8(m)
                G = np.uint8(255 * x + m)
                B = np.uint8(255 * D + m)

            if 240 <= H < 300:
                R = np.uint8(255 * x + m)
                G = np.uint8(m)
                B = np.uint8(255 * D + m)

            if 300 <= H < 360:
                R = np.uint8(255 * D + m)
                G = np.uint8(m)
                B = np.uint8(255 * x + m)

            res_array[n, p] = R, G, B
            #res_array[n, p] = h, l, 1.
    return res_array


def convert_to_rgb_array(array: np.ndarray) -> np.ndarray:
    res = np.zeros((len(array), len(array[0]), 3), dtype="uint8")
    for n in range(len(array)):
        for p in range(len(array[0])):
            h, l, s = array[n, p]
            r, g, b = hls_to_rgb(h, l, 1)
            res[n, p] = np.uint8(255 * r), np.uint8(255 * g), np.uint8(255 * b)
    return res


class EisensteinSeriesG10(Scene):
    def construct(self):
        a, b, c, d = ValueTracker(1), ValueTracker(0), ValueTracker(0), ValueTracker(1)

        screen_rect = Rectangle(height=config.frame_height)

        im = always_redraw(
            lambda: ImageMobject(plot_eisenstein_series(
                k=10,
                max_term_order=10,
                matrix_for_action=np.array([[a.get_value(), b.get_value()], [c.get_value(), d.get_value()]])
            )).match_height(screen_rect)
        )

        self.add(im)
        self.wait()
        #self.play(a.animate.set_value(1), b.animate.set_value(1), c.animate.set_value(1), d.animate.set_value(0), run_time=8, rate_func=linear)
        self.wait()

      


class PlotComplexFunctions(Scene):
    def construct(self):
        def func(z: complex) -> complex:
            try:
                return np.exp(-1/z)
            except ZeroDivisionError:
                return 0
            
        RATIO = 1920 / 1080
        x_min, x_max = -2, 2
        num = 1000
        y_min, y_max = -2, 2
        rect = Rectangle(height=config.frame_height)

        im = ImageMobject(
            plot_complex_function(func, real_range=[x_min * RATIO, x_max * RATIO, np.abs(x_max - x_min) / num], imag_range=[y_min, y_max, np.abs(y_max - y_min) / num], h_factor=0.1)
        )
        im.match_height(rect).move_to(ORIGIN)
        self.add(im)