from common import *


def ang_pt(origin, deg, r):
    return origin + r * np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])


def tag(tex, pos, color, scale=0.75):
    m = MathTex(tex, color=color).scale(scale)
    m.add_background_rectangle(BLACK, opacity=0.85, buff=0.05)
    return m.move_to(pos)


class AngleSums(Scene):
    """Questions 7 and 22: angle addition, exterior angle theorem, triangle sum."""

    def construct(self):
        self.q7()
        self.q22()

    # ------------------------------------------------------------------
    def q7(self):
        question_card(self, 7)
        title = make_title("Question 7: Angle Addition")
        Y = np.array([-3.9, -1.6, 0])
        dx, dw, dz = 158, 86, 10          # drawn directions (true proportions)
        x_end, w_end, z_end = ang_pt(Y, dx, 2.7), ang_pt(Y, dw, 2.7), ang_pt(Y, dz, 2.7)
        rays = VGroup(*[Line(Y, e, color=WHITE, stroke_width=5) for e in (x_end, w_end, z_end)])
        pts = VGroup(
            MathTex("X").scale(0.9).next_to(x_end, LEFT, buff=0.15),
            MathTex("W").scale(0.9).next_to(w_end, UP, buff=0.15),
            MathTex("Z").scale(0.9).next_to(z_end, RIGHT, buff=0.15),
            MathTex("Y").scale(0.9).next_to(Y, DOWN, buff=0.15),
        )
        arc1 = Arc(radius=0.8, start_angle=np.radians(dw), angle=np.radians(dx - dw), arc_center=Y, color=YELLOW, stroke_width=5)
        arc2 = Arc(radius=0.8, start_angle=np.radians(dz), angle=np.radians(dw - dz), arc_center=Y, color=YELLOW, stroke_width=5)
        arc3 = Arc(radius=2.15, start_angle=np.radians(dz), angle=np.radians(dx - dz), arc_center=Y, color=GREEN, stroke_width=5)
        l1 = tag("(2x+40)^\\circ", ang_pt(Y, 122, 1.5), YELLOW, 0.65)
        l2 = tag("(3x+28)^\\circ", ang_pt(Y, 48, 1.5), YELLOW, 0.65)
        l3 = tag("148^\\circ", ang_pt(Y, 104, 2.15), GREEN, 0.7)

        self.play(Write(title))
        self.play(Create(rays), FadeIn(pts))
        self.play(Create(arc1), Create(arc2), FadeIn(l1), FadeIn(l2))
        self.play(Create(arc3), FadeIn(l3))

        cap = caption("Step 1: The two parts make the whole")
        self.play(FadeIn(cap, shift=UP * 0.2))
        t = Text("Angle Addition Postulate:", font_size=28, color=GIVEN)
        e0 = MathTex("m\\angle XYW", "+", "m\\angle WYZ", "=", "m\\angle XYZ").scale(0.85)
        VGroup(t, e0).arrange(DOWN, buff=0.4).move_to(EQ_POS)
        self.play(FadeIn(t, shift=DOWN * 0.2), Write(e0))
        self.wait(2)

        new_cap = caption("Step 2: Plug in the expressions")
        self.play(ReplacementTransform(cap, new_cap), FadeOut(t)); cap = new_cap
        e1 = eq_tex("(2x+40)", "+", "(3x+28)", "=", "148")
        self.play(ReplacementTransform(e0, e1))
        self.play(Indicate(l1, color=GREEN), Indicate(l2, color=GREEN), Indicate(l3, color=GREEN))
        self.wait(1)

        new_cap = caption("Step 3: Combine like terms")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        c1 = MathTex("2x + 3x = 5x", color=CONST).scale(0.9)
        c2 = MathTex("40 + 28 = 68", color=CONST).scale(0.9)
        VGroup(c1, c2).arrange(DOWN, buff=0.25).next_to(e1, DOWN, buff=0.4)
        self.play(FadeIn(c1, shift=UP * 0.2))
        self.play(FadeIn(c2, shift=UP * 0.2))
        self.wait(1)
        e2 = eq_tex("5x", "+68", "=", "148")
        self.play(ReplacementTransform(e1, e2), FadeOut(c1), FadeOut(c2))
        self.wait(1)

        new_cap = caption("Step 4: Subtract 68 from both sides")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        eq = op_step(self, e2, ops=("-68", "-68"), under=([0, 1], [3]),
                     mid=eq_tex("5x", "+68", "-68", "=", "148", "-68"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[1, 2], combine=([4, 5], "148 - 68 = 80"),
                     result=eq_tex("5x", "=", "80"))
        new_cap = caption("Step 5: Divide both sides by 5")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        eq = op_step(self, eq, ops=("\\div 5", "\\div 5"), under=([0], [2]),
                     mid=eq_tex("{5x", "\\over", "5}", "=", "{80", "\\over", "5}"),
                     combine=([4, 5, 6], "80 \\div 5 = 16"),
                     result=eq_tex("x", "=", "16"))
        self.play(eq[2].animate.set_color(ANSWER))
        self.wait(1)

        new_cap = caption("Step 6: Check on the diagram")
        self.play(ReplacementTransform(cap, new_cap), FadeOut(eq)); cap = new_cap
        chk = VGroup(MathTex("2(16) + 40 = 72"), MathTex("3(16) + 28 = 76"),
                     MathTex("72 + 76 = 148")).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(EQ_POS)
        self.play(Write(chk[0]))
        self.play(Transform(l1, tag("72^\\circ", ang_pt(Y, 122, 1.5), ANSWER, 0.7)))
        self.play(Write(chk[1]))
        self.play(Transform(l2, tag("76^\\circ", ang_pt(Y, 48, 1.5), ANSWER, 0.7)))
        self.play(Write(chk[2]))
        self.wait(1.5)
        answer_banner(self, "Answer: B) x = 16")
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])

    # ------------------------------------------------------------------
    def q22(self):
        question_card(self, 22)
        title = make_title("Question 22: Exterior Angle Theorem")
        Lp = np.array([-6.6, -1.5, 0])
        Rp = np.array([-3.4, -1.5, 0])
        Tp = Lp + 3.96 * np.array([np.cos(np.radians(65)), np.sin(np.radians(65)), 0])
        tri = Polygon(Lp, Rp, Tp, color=WHITE, stroke_width=5)
        ext = Line(Rp, Rp + RIGHT * 2.0, color=WHITE, stroke_width=5)
        dir_top = np.degrees(np.arctan2(Tp[1] - Rp[1], Tp[0] - Rp[0]))   # about 113 degrees
        arc_a = Arc(radius=0.75, start_angle=0, angle=np.radians(dir_top), arc_center=Rp, color=GREEN, stroke_width=5)
        arc_b = Arc(radius=0.45, start_angle=np.radians(dir_top), angle=np.radians(180 - dir_top), arc_center=Rp, color=ORANGE, stroke_width=5)
        arc_l = Arc(radius=0.7, start_angle=0, angle=np.radians(65), arc_center=Lp, color=YELLOW, stroke_width=5)
        to_left = np.degrees(np.arctan2(Lp[1] - Tp[1], Lp[0] - Tp[0])) % 360
        to_right = np.degrees(np.arctan2(Rp[1] - Tp[1], Rp[0] - Tp[0])) % 360
        arc_t = Arc(radius=0.6, start_angle=np.radians(to_left), angle=np.radians(to_right - to_left),
                    arc_center=Tp, color=YELLOW, stroke_width=5)
        lab_l = tag("65^\\circ", Lp + np.array([1.2, 0.3, 0]), YELLOW)
        lab_t = tag("48^\\circ", Tp + np.array([0.0, -1.0, 0]), YELLOW)
        lab_a = tag("a", Rp + np.array([0.85, 0.65, 0]), GREEN)
        lab_b = tag("b", Rp + np.array([-0.66, 0.45, 0]), ORANGE)

        self.play(Write(title))
        self.play(Create(tri), Create(ext))
        self.play(Create(arc_l), Create(arc_t), FadeIn(lab_l), FadeIn(lab_t))
        self.play(Create(arc_a), Create(arc_b), FadeIn(lab_a), FadeIn(lab_b))

        # Part A
        cap = caption("Part A: Exterior angle theorem")
        self.play(FadeIn(cap, shift=UP * 0.2))
        t1 = Text("Exterior angle = the sum of the", font_size=28, color=GIVEN)
        t2 = Text("two remote interior angles", font_size=28, color=GIVEN)
        VGroup(t1, t2).arrange(DOWN, buff=0.3).move_to(EQ_POS + UP * 0.9)
        self.play(FadeIn(t1, shift=DOWN * 0.2), FadeIn(t2, shift=DOWN * 0.2))
        self.play(Indicate(arc_l, color=GREEN, scale_factor=1.3), Indicate(arc_t, color=GREEN, scale_factor=1.3))
        ea = eq_tex("a", "=", "65", "+", "48").move_to(EQ_POS + DOWN * 0.3)
        self.play(Write(ea))
        self.wait(1)
        ea2 = eq_tex("a", "=", "113").move_to(ea)
        self.play(ReplacementTransform(ea, ea2))
        self.play(ea2[2].animate.set_color(ANSWER))
        self.play(Transform(lab_a, tag("113^\\circ", Rp + np.array([1.0, 0.7, 0]), ANSWER)))
        self.wait(1)
        ban = answer_banner(self, "Part A: A) 113°")
        self.wait(2)
        self.play(FadeOut(VGroup(t1, t2, ea2)), FadeOut(ban))

        # Part B
        new_cap = caption("Part B: Triangle angles add to 180°")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        e0 = eq_tex("65", "+48", "+b", "=", "180")
        self.play(Write(e0))
        self.wait(1)
        box = SurroundingRectangle(VGroup(e0[0], e0[1]), color=CONST, buff=0.08)
        cl = MathTex("65 + 48 = 113", color=CONST).scale(0.9).next_to(box, DOWN, buff=0.3)
        self.play(Create(box), FadeIn(cl))
        self.wait(1)
        e1 = eq_tex("113", "+b", "=", "180")
        self.play(FadeOut(box), FadeOut(cl), ReplacementTransform(e0, e1))
        new_cap = caption("Subtract 113 from both sides")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        eq = op_step(self, e1, ops=("-113", "-113"), under=([0, 1], [3]),
                     mid=eq_tex("113", "+b", "-113", "=", "180", "-113"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[0, 2], combine=([4, 5], "180 - 113 = 67"),
                     result=eq_tex("b", "=", "67"))
        self.play(eq[2].animate.set_color(ANSWER),
                  Transform(lab_b, tag("67^\\circ", Rp + np.array([-0.72, 0.5, 0]), ANSWER, 0.6)))
        chk = Text("Check: 113° + 67° = 180° (a straight line)", font_size=26, color=GIVEN).move_to(EQ_POS + DOWN * 1.0)
        self.play(FadeIn(chk, shift=UP * 0.2))
        self.wait(1.5)
        answer_banner(self, "Part B: B) 67°")
        self.wait(3)
