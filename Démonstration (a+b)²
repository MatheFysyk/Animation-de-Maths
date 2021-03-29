#Bon, ce code ne marche probablement plus dans la nouvelle version de manim ...
#Si vous savez comment le modifier, je suis preneur :)
#Ah, me jugez pas, c'est mon premier "gros" projet manim, le code est dégueulasse, pas du tout optimisé xD

import numpy as np
from manimlib import *

class Demoapluabcarre(Scene):

    CONFIG={
        "couleur_carre_a":YELLOW,
        "couleur_carre_b":RED,
        "couleur_rectangle_c":ORANGE,
        "couleur_rectangle_d":ORANGE,
        "grosseur_ligne":1,
        "opacite":1,
        }

    def construct(self):
        title = TextMobject("Démonstration de ", "$(a+b)^2$ ", "$= a^2 + 2ab + b^2$")

        aplusb = TexMobject("(a+b)")
        deuxab = TexMobject("2ab")
        ab_1 = TexMobject("ab")
        acarre = TexMobject("a^2")
        bcarre = TexMobject("b^2")
        ab_copie = ab_1.copy()
        acarre.move_to([0,3.1,0])
        bcarre.move_to([1.25,3.08,0])
        ab_1.move_to([2.45,3.05,0])
        ab_copie.move_to([3.85,3.05,0])
        a_1 = TexMobject("a")
        plus = TexMobject("+")
        egal = TexMobject("=")
        aplusbcarre = TexMobject("(a+b)^2")

        self.play(Write(title))

        self.wait(2)

        vec_1 = np.array([-2.3,3,0])
        egal.move_to([-1,3,0])
        a_1.move_to(vec_1)
        aplusb.move_to(vec_1)
        a_1.move_to(vec_1)
        aplusbcarre.move_to([-2.3,3.05,0])
        m=np.array([-2,1.5,0])
        n=np.array([2,1.5,0])
        p=np.array([2,-2.5,0])
        q=np.array([-2,-2.5,0])
        a=np.array([-2,0.5,0])
        b=np.array([1,0.5,0])
        c=np.array([1,-2.5,0])
        d=np.array([1,1.5,0])
        e=np.array([2,0.5,0])

        ligne_a = Line(start=q,end=c,color=self.couleur_carre_a)
        ligne_b = Line(start=c,end=p,color=self.couleur_rectangle_c)

        cote_a = TexMobject("a")
        cote_b = TexMobject("b")
        cote_abis = TexMobject("a")
        cote_bbis = TexMobject("b")
        coord_cote_a = np.array([-2.5,-1,0])
        coord_cote_b = np.array([-2.5,1,0])
        coord_cote_abis = np.array([-0.5,-3,0])
        coord_cote_bbis = np.array([1.5,-3,0])
        cote_a.move_to(coord_cote_a)
        cote_b.move_to(coord_cote_b)
        cote_abis.move_to(coord_cote_abis)
        cote_bbis.move_to(coord_cote_bbis)

        self.play(FadeOut(title[0]), FadeOut(title[2]), title[1].move_to, vec_1, Transform(title[1], a_1), Write(cote_abis), ShowCreation(ligne_a))
        self.wait()
        self.play(Write(cote_bbis), ShowCreation(ligne_b), Transform(title[1], aplusb))
        self.wait()

        carre_a=Polygon(a,b,c,q,color=self.couleur_carre_a).set_fill(self.couleur_carre_a,self.opacite).set_stroke(None,self.grosseur_ligne)
        carre_b=Polygon(d,n,e,b,color=self.couleur_carre_b).set_fill(self.couleur_carre_b,self.opacite).set_stroke(None,self.grosseur_ligne)
        rectangle_c=Polygon(m,d,b,a,color=self.couleur_rectangle_c).set_fill(self.couleur_rectangle_c,self.opacite).set_stroke(None,self.grosseur_ligne)
        rectangle_d=Polygon(b,e,p,c,color=self.couleur_rectangle_d).set_fill(self.couleur_rectangle_d,self.opacite).set_stroke(None,self.grosseur_ligne)

        self.play(ShowCreation(carre_a), ShowCreation(carre_b), ShowCreation(rectangle_c), ShowCreation(rectangle_d), Write(cote_a), Write(cote_b), ReplacementTransform(title[1], aplusbcarre))
        self.wait()

        groupe_a_copie = carre_a.copy()
        groupe_b_copie = carre_b.copy()
        groupe_c_copie = rectangle_c.copy()
        groupe_d_copie = rectangle_d.copy()

        plus_1 = plus.copy()
        plus_1.move_to([0.76,3,0])
        plus_2 = plus.copy()
        plus_2.move_to([1.72,3,0])
        plus_3 = plus.copy()
        plus_3.move_to([3.2,3,0])

        self.play(Write(egal), groupe_a_copie.move_to, [0,3,0], groupe_a_copie.scale, 0.25, Write(plus_1))
        self.play(groupe_b_copie.move_to, [1.25,3,0], groupe_b_copie.scale, 0.25, Write(plus_2))
        self.play(groupe_c_copie.move_to, [2.45,3,0], groupe_c_copie.scale, 0.25, Write(plus_3))
        self.play(groupe_d_copie.move_to, [3.7,3,0], groupe_d_copie.scale, 0.25)
        self.wait()

        cote_a_copie = cote_a.copy()
        cote_b_copie = cote_b.copy()
        cote_abis_copie = cote_abis.copy()      
        cote_bbis_copie = cote_bbis.copy()
        cote_a_copiie = cote_a_copie.copy()
        cote_b_copiie = cote_b_copie.copy()
        cote_abis_copiie = cote_abis_copie.copy()
        cote_bbis_copiie = cote_bbis_copie.copy()

        self.play(cote_a_copie.move_to, [-0.12,3,0], cote_abis_copie.move_to, [0.12,3,0])
        self.play(Transform(groupe_a_copie, acarre), FadeOut(cote_a_copie), FadeOut(cote_abis_copie))
        self.play(cote_b_copie.move_to, [1.13,3,0], cote_bbis_copie.move_to, [1.37,3,0])
        self.play(Transform(groupe_b_copie, bcarre), FadeOut(cote_b_copie), FadeOut(cote_bbis_copie))
        self.play(cote_abis_copiie.move_to, [2.33,3,0], cote_b_copiie.move_to, [2.57,3.07,0])
        self.play(Transform(groupe_c_copie, ab_1), FadeOut(cote_abis_copiie), FadeOut(cote_b_copiie))
        self.play(cote_bbis_copiie.move_to, [3.58,3.07,0], cote_a_copiie.move_to, [3.82,3,0])
        self.play(Transform(groupe_d_copie, ab_copie), FadeOut(cote_bbis_copiie), FadeOut(cote_a_copiie))
        self.wait()
        formule_f = TexMobject("(a+b)^2 = a^2 + 2ab + b^2")
        formule_f.move_to([0,3,0])
        groupe_bis = VGroup(groupe_a_copie, groupe_b_copie, groupe_c_copie, groupe_d_copie, plus_1, plus_2, plus_3, egal, aplusbcarre)
        self.play(Transform(groupe_bis, formule_f))
        self.remove()
        fin = TextMobject("Voilà :)")
        self.wait()
        self.play(Write(fin))
        self.wait()
