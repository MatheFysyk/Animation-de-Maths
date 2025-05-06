class TorePince(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65*DEGREES, theta=180*DEGREES, distance=8)

        def f_tore_pince(u, v):
            a, b, k = 3, 1, 1/2
            return np.array([
                (a + b*np.cos(v)*np.cos(k*u))*np.cos(u),
                (a + b*np.cos(v)*np.cos(k*u))*np.sin(u),
                b*np.sin(v)*np.cos(k*u)
            ])

        TorePince = ParametricSurface(
            f_tore_pince, u_min=-4, u_max=4, v_min=0, v_max=2*np.pi
        )
        self.add(TorePince)
