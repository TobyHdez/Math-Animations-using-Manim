from common import *


class SectionRatio(Scene):
    """Questions 19 and 20: the point that divides a segment in a given ratio."""

    def problem(self, q, start, end, sname, ename, parts, xr, yr, plane_len, answer_txt):
        """start/end are the points the segment is measured FROM and TO.
        parts = (m, n): ratio m:n, so the point is m/(m+n) of the way from start to end."""
        m, n = parts
        total = m + n
        title = make_title(f"Question {q}: Divide a Segment in a Ratio")
        plane = NumberPlane(
            x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1],
            x_length=plane_len[0], y_length=plane_len[1],
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.2, "stroke_opacity": 0.3},
            axis_config={"stroke_color": WHITE, "stroke_width": 2.5},
        ).move_to(LEFT * 3.9 + DOWN * 0.4)
        P = plane.c2p
        S = np.array(start, dtype=float)
        E = np.array(end, dtype=float)
        D = E - S
        pt = S + D * m / total

        nums = VGroup()
        step = 2 if (xr[1] - xr[0]) <= 14 else 4
        for v in range(int(np.ceil(xr[0] / step) * step), xr[1] + 1, step):
            if v != 0:
                nums.add(MathTex(str(v)).scale(0.4).next_to(P(v, 0), DOWN, buff=0.08))
        for v in range(int(np.ceil(yr[0] / step) * step), yr[1] + 1, step):
            if v != 0:
                nums.add(MathTex(str(v)).scale(0.4).next_to(P(0, v), LEFT, buff=0.08))

        seg = Line(P(*S), P(*E), color=WHITE, stroke_width=5)
        d_s, d_e = Dot(P(*S), color=YELLOW, radius=0.08), Dot(P(*E), color=YELLOW, radius=0.08)

        def pl(name, p, direction, color=YELLOW):
            t = MathTex(f"{name}({p[0]:g},{p[1]:g})".replace("-", "-"), color=color).scale(0.6)
            t.add_background_rectangle(BLACK, opacity=0.85, buff=0.05)
            return t.next_to(P(*p), direction, buff=0.12)
        dir_s = DOWN if S[1] <= E[1] else UP
        dir_e = UP if S[1] <= E[1] else DOWN
        lab_s = pl(sname, S, dir_s)
        lab_e = pl(ename, E, dir_e)

        self.play(Write(title), FadeIn(plane), FadeIn(nums))
        self.play(Create(seg), FadeIn(d_s), FadeIn(d_e), FadeIn(lab_s), FadeIn(lab_e))
        self.wait(1)

        # Step 1: count the equal parts
        cap = caption("Step 1: Count the equal parts")
        self.play(FadeIn(cap, shift=UP * 0.2))
        t1 = Text(f"Ratio {m}:{n}  means  {m} + {n} = {total} equal parts", font_size=28, color=GIVEN)
        t2 = Text(f"from {sname} to {ename}.", font_size=28, color=GIVEN)
        VGroup(t1, t2).arrange(DOWN, buff=0.3).move_to(EQ_POS + UP * 0.8)
        self.play(FadeIn(t1, shift=DOWN * 0.2), FadeIn(t2, shift=DOWN * 0.2))
        ticks = VGroup()
        for k in range(1, total):
            p = S + D * k / total
            ticks.add(Line(P(*p) + UP * 0.12, P(*p) + DOWN * 0.12, color=GREEN, stroke_width=5)
                      .rotate(Line(P(*S), P(*E)).get_angle(), about_point=P(*p)))
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.3))
        frac = MathTex(f"\\text{{point is }}", "{" + str(m), "\\over", f"{total}" + "}", "\\text{ of the way}").scale(0.9)
        frac[1].set_color(GREEN); frac[3].set_color(GREEN)
        frac.next_to(VGroup(t1, t2), DOWN, buff=0.4)
        self.play(Write(frac))
        first = Line(P(*S), P(*pt), color=GREEN, stroke_width=9)
        self.play(Create(first))
        self.wait(1.5)
        self.play(FadeOut(VGroup(t1, t2, frac)))

        # Step 2: the run and rise of the whole segment
        new_cap = caption(f"Step 2: Find {ename} − {sname}")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        diff = MathTex(f"{ename} - {sname}", "=", f"({E[0]:g}-({S[0]:g}),\\ {E[1]:g}-({S[1]:g}))").scale(0.85)
        res = MathTex("=", f"({D[0]:g},\\ {D[1]:g})", color=GIVEN).scale(1.0)
        VGroup(diff, res).arrange(DOWN, buff=0.35).move_to(EQ_POS)
        self.play(Write(diff))
        self.play(Write(res))
        # show the run / rise on the plane
        corner = np.array([E[0], S[1]])
        run_l = Line(P(*S), P(*corner), color=ORANGE, stroke_width=5)
        rise_l = Line(P(*corner), P(*E), color=ORANGE, stroke_width=5)
        self.play(Create(run_l), Create(rise_l))
        self.wait(1.5)

        # Step 3: take the fraction of that jump
        new_cap = caption(f"Step 3: Take {m}/{total} of the jump")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        jump = np.array([D[0] * m / total, D[1] * m / total])
        step3 = MathTex(f"\\tfrac{{{m}}}{{{total}}}", f"({D[0]:g},\\ {D[1]:g})", "=", f"({jump[0]:g},\\ {jump[1]:g})").scale(1.0)
        step3[0].set_color(GREEN)
        step3.move_to(EQ_POS)
        self.play(FadeOut(VGroup(diff, res)), FadeIn(step3[:2]))
        self.play(Write(step3[2:]))
        self.wait(1)
        self.play(FadeOut(VGroup(run_l, rise_l)))

        # Step 4: add to the starting point
        new_cap = caption(f"Step 4: Add it to {sname}")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        add = MathTex(f"{sname}", "+", f"({jump[0]:g},\\ {jump[1]:g})", "=", f"({S[0]:g}+({jump[0]:g}),\\ {S[1]:g}+({jump[1]:g}))").scale(0.8)
        fin = MathTex("=", f"({pt[0]:g},\\ {pt[1]:g})", color=ANSWER).scale(1.1)
        VGroup(add, fin).arrange(DOWN, buff=0.35).move_to(EQ_POS)
        self.play(FadeOut(step3), Write(add))
        self.play(Write(fin))
        d_p = Dot(P(*pt), color=ANSWER, radius=0.12)
        lab_p = pl("", pt, UP, ANSWER)
        lab_p = MathTex(f"({pt[0]:g},{pt[1]:g})", color=ANSWER).scale(0.7)
        lab_p.add_background_rectangle(BLACK, opacity=0.85, buff=0.05)
        lab_p.next_to(P(*pt), UR if D[1] * D[0] >= 0 else DR, buff=0.15)
        self.play(FadeIn(d_p, scale=3), FadeIn(lab_p))
        self.play(Indicate(d_p, color=ANSWER, scale_factor=2))
        self.wait(1.5)
        answer_banner(self, answer_txt)
        self.wait(3)
        self.play(*[FadeOut(m_) for m_ in self.mobjects])

    def construct(self):
        # Q19: P(-5,-2), Q(3,6); from Q to P in ratio 1:3
        question_card(self, 19)
        self.problem(19, start=(3, 6), end=(-5, -2), sname="Q", ename="P", parts=(1, 3),
                     xr=(-7, 5), yr=(-4, 8), plane_len=(5.4, 5.0),
                     answer_txt="Answer: A) (1, 4)")
        # Q20: A(-6,4), B(9,-6); ratio 2:3
        question_card(self, 20)
        self.problem(20, start=(-6, 4), end=(9, -6), sname="A", ename="B", parts=(2, 3),
                     xr=(-8, 11), yr=(-8, 6), plane_len=(5.8, 4.5),
                     answer_txt="Answer: A) (0, 0)")
