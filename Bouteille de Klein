class BouteilleKlein(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=80*DEGREES, theta=-100*DEGREES, distance=10)

        def f_klein(u, v):
            a, b, c = 3, 4, 2
            r = c*(1 - np.cos(u)/2)
            if u <= np.pi:
                x = (a * (1 + np.sin(u)) + r*np.cos(v))*np.cos(u)
                y = (b + r*np.cos(v))*np.sin(u)
            else:
                x = a*(1 + np.sin(u))*np.cos(u) - r*np.cos(v)
                y = b*np.sin(u)
            z = r*np.sin(v)
            return np.array([0.5*x, 0.75*y, 0.5*z])

        axes = ThreeDAxes()
        self.begin_ambient_camera_rotation(rate=0.2, about="theta")
        BouteilleKlein = ParametricSurface(f_klein, u_min=0, u_max=2*np.pi, v_min=0, v_max=2*np.pi)
        BouteilleKlein.center().rotate(PI/8, np.array([1, 0, 0])).shift(np.array([0, 0, 0.8]))
        self.play(Create(axes), Create(BouteilleKlein))
        self.wait(10)
