class RubanMoebius(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=np.pi/2.75, theta=np.pi/6, distance=2)

        def f_moebius(u, v):
            return np.array([
                (1 + u/2 * np.cos(v/2)) * np.cos(v),
                (1 + u/2 * np.cos(v/2)) * np.sin(v),
                u/2 * np.sin(v/2)
            ])

        RubanMoebius = ParametricSurface(
            f_moebius, u_min=-1, u_max=1, v_min=0, v_max=2*np.pi
        )
        self.add(RubanMoebius)
