from common import *

TEAL_C = TEAL
PINK_C = PINK


def tag(tex, pos, color, scale=0.7):
    m = MathTex(tex, color=color).scale(scale)
    m.add_background_rectangle(BLACK, opacity=0.85, buff=0.06)
    return m.move_to(pos)


def note(txt, pos, color=WHITE, size=26, width=6.5):
    t = Text(txt, font_size=size, color=color, line_spacing=0.9)
    if t.width > width:
        t.scale_to_fit_width(width)
    return t.move_to(pos)


def swap_cap(scene, old, text):
    new = caption(text)
    scene.play(ReplacementTransform(old, new))
    return new


def sector(c, a0, a1, r, color, op=0.55):
    return Sector(radius=r, start_angle=a0, angle=a1 - a0, arc_center=c,
                  color=color, fill_opacity=op, stroke_width=3)


def bearing(frm, to):
    d = to - frm
    return float(np.arctan2(d[1], d[0]))


def clear_right(scene, keep):
    """Fade everything in the right-hand work column except the kept objects."""
    items = [m for m in scene.mobjects if m.get_center()[0] > 0.2 and m not in keep]
    if items:
        scene.play(*[FadeOut(m) for m in items])


def clear_all(scene):
    scene.play(*[FadeOut(m) for m in scene.mobjects])


class Proofs(Scene):
    """Questions 21 and 28: triangle angle-sum proof, segment addition."""

    def construct(self):
        self.q21()
        clear_all(self)
        self.wait(0.5)
        self.q28()
        self.wait(2)

    # ------------------------------------------------------------------
    def q21(self):
        question_card(self, 21)
        title = make_title("Question 21: Triangle Angle-Sum Proof")
        X = np.array([-5.5, -1.5, 0])
        Z = np.array([-1.5, -1.5, 0])
        Y = np.array([-3.4, 0.8, 0])
        W = np.array([-5.9, 0.8, 0])
        V = np.array([-0.9, 0.8, 0])
        R = 0.7

        tri = Polygon(X, Y, Z, color=WHITE, stroke_width=5)
        labs = VGroup(
            MathTex("X").next_to(X, DL, buff=0.1),
            MathTex("Z").next_to(Z, DR, buff=0.1),
            MathTex("Y").next_to(Y, UP, buff=0.15),
        )
        self.play(Write(title))
        self.play(Create(tri), FadeIn(labs))
        cap = caption("Step 1: Draw WV parallel to XZ")
        self.play(FadeIn(cap, shift=UP * 0.2))
        wv = Line(W, V, color=WHITE, stroke_width=5)
        wvlab = VGroup(MathTex("W").next_to(W, LEFT, buff=0.1),
                       MathTex("V").next_to(V, RIGHT, buff=0.1))

        def chevron(c):
            return VGroup(Line(c + np.array([-0.1, 0.16, 0]), c + np.array([0.1, 0, 0])),
                          Line(c + np.array([0.1, 0, 0]), c + np.array([-0.1, -0.16, 0]))
                          ).set_color(GIVEN).set_stroke(width=5)
        par = VGroup(chevron(np.array([-5.1, 0.8, 0])), chevron(np.array([-3.4, -1.5, 0])))
        self.play(Create(wv), FadeIn(wvlab))
        self.play(FadeIn(par))
        g = note("Given: WV is parallel to XZ", EQ_POS + UP * 0.3, GIVEN, 28)
        self.play(FadeIn(g, shift=DOWN * 0.2))
        self.wait(2)

        # alternate interior angles
        aX = bearing(X, Y)                     # angle at X: 0 .. aX
        aZ = bearing(Z, Y)                     # angle at Z: aZ .. pi
        yX = bearing(Y, X) % TAU               # direction Y->X
        yZ = bearing(Y, Z) % TAU               # direction Y->Z
        cap = swap_cap(self, cap, "Step 2: Mark the alternate angles")
        sx = sector(X, 0, aX, R, TEAL_C)
        sz = sector(Z, aZ, PI, R, PINK_C)
        wyx = Arc(radius=R, start_angle=PI, angle=yX - PI, arc_center=Y, color=TEAL_C, stroke_width=6)
        vyz = Arc(radius=R, start_angle=yZ, angle=TAU - yZ, arc_center=Y, color=PINK_C, stroke_width=6)
        self.play(FadeOut(g), FadeIn(sx), Create(wyx))
        e1 = MathTex("\\angle X", "=", "\\angle WYX").scale(0.95).move_to(EQ_POS + UP * 0.3)
        e1[0].set_color(TEAL_C); e1[2].set_color(TEAL_C)
        self.play(Write(e1))
        self.wait(1)
        self.play(FadeIn(sz), Create(vyz))
        e2 = MathTex("\\angle Z", "=", "\\angle VYZ").scale(0.95).next_to(e1, DOWN, buff=0.4)
        e2[0].set_color(PINK_C); e2[2].set_color(PINK_C)
        self.play(Write(e2))
        why = note("Alternate interior angles are equal", EQ_POS + UP * 1.7, GIVEN, 26)
        self.play(FadeIn(why, shift=DOWN * 0.2))
        self.wait(2.5)

        # slide the angles up to Y
        cap = swap_cap(self, cap, "Step 3: Slide both angles up to Y")
        sy = sector(Y, yX, yZ, R, GIVEN)
        self.play(FadeIn(sy))
        self.play(Indicate(sy, color=GIVEN, scale_factor=1.15))
        cx = sx.copy()
        cz = sz.copy()
        self.add(cx, cz)
        self.play(Rotate(cx, PI, about_point=X), run_time=1.2)
        self.play(cx.animate.shift(Y - X), run_time=1.6)
        self.wait(0.5)
        self.play(Rotate(cz, PI, about_point=Z), run_time=1.2)
        self.play(cz.animate.shift(Y - Z), run_time=1.6)
        self.wait(1)

        cap = swap_cap(self, cap, "Step 4: They form a straight line")
        semi = Arc(radius=1.05, start_angle=PI, angle=PI, arc_center=Y, color=WHITE, stroke_width=6)
        self.play(Create(semi), run_time=1.5)
        st = note("WYV is a straight angle: 180°", np.array([-3.4, 2.15, 0]), WHITE, 26, 6.0)
        st.add_background_rectangle(BLACK, opacity=0.85, buff=0.08)
        self.play(FadeIn(st, shift=DOWN * 0.15))
        e3 = MathTex("\\angle WYX", "+", "\\angle Y", "+", "\\angle VYZ", "=", "180^\\circ").scale(0.85)
        e3[0].set_color(TEAL_C); e3[2].set_color(GIVEN); e3[4].set_color(PINK_C)
        e3.move_to(EQ_POS)
        self.play(FadeOut(why), FadeOut(e1), FadeOut(e2))
        self.play(Write(e3))
        self.wait(2.5)

        # proof table
        cap = swap_cap(self, cap, "Step 5: Build the proof, row by row")
        self.play(FadeOut(e3))
        xs = [0.2, 4.2, 6.8]
        ys = [2.9, 2.2, 1.3, 0.4]
        hdr_bg = Rectangle(width=xs[2] - xs[0], height=0.7, fill_color=GREY_D, fill_opacity=0.8,
                           stroke_width=0).move_to([(xs[0] + xs[2]) / 2, 2.55, 0])
        lines = VGroup(*[Line([xs[0], y, 0], [xs[2], y, 0], stroke_width=3) for y in ys],
                       *[Line([x, ys[0], 0], [x, ys[-1], 0], stroke_width=3) for x in xs])
        h1 = Text("Statement", font_size=26).move_to([2.2, 2.55, 0])
        h2 = Text("Reason", font_size=26).move_to([5.5, 2.55, 0])
        self.play(FadeIn(hdr_bg), Create(lines), FadeIn(h1), FadeIn(h2))

        def stmt(a, b, y):
            m = MathTex(a, "+", "\\angle Y", "+", b, "=", "180^\\circ")
            m.scale_to_fit_width(3.7)
            m.move_to([2.2, y, 0])
            return m

        r1 = stmt("\\angle WYX", "\\angle VYZ", 1.75)
        r1[0].set_color(TEAL_C); r1[2].set_color(GIVEN); r1[4].set_color(PINK_C)
        q1 = Text("?", font_size=36, color=GIVEN).move_to([5.5, 1.75, 0])
        ex = note("Row 1: the three angles fill the straight line WV.", [3.5, -0.3, 0], WHITE, 26, 6.6)
        self.play(Write(r1), FadeIn(q1))
        self.play(FadeIn(ex))
        self.wait(3)

        cap = swap_cap(self, cap, "Step 6: Fill in the missing reason")
        reason1 = Text("Definition of a\nstraight angle", font_size=24, color=ANSWER,
                       line_spacing=0.9).move_to([5.5, 1.75, 0])
        ex2 = note("A straight angle measures 180°, so that is our reason.", [3.5, -0.3, 0], WHITE, 26, 6.6)
        self.play(ReplacementTransform(q1, reason1), ReplacementTransform(ex, ex2))
        self.play(Indicate(reason1, color=ANSWER))
        self.wait(2.5)

        r2 = stmt("\\angle Z", "\\angle Z", 0.85)
        r2 = MathTex("\\angle X", "+", "\\angle Y", "+", "\\angle Z", "=", "180^\\circ")
        r2.scale_to_fit_width(3.7).move_to([2.2, 0.85, 0])
        r2[0].set_color(TEAL_C); r2[2].set_color(GIVEN); r2[4].set_color(PINK_C)
        reason2 = Text("Substitution", font_size=24).move_to([5.5, 0.85, 0])
        ex3 = note("Row 2: swap in the equal angles, WYX to X and VYZ to Z.", [3.5, -0.3, 0], WHITE, 26, 6.6)
        cp = r1.copy()
        self.add(cp)
        self.play(ReplacementTransform(cp, r2), ReplacementTransform(ex2, ex3), run_time=1.6)
        self.play(FadeIn(reason2))
        self.wait(3)

        # check choices
        cap = swap_cap(self, cap, "Step 7: Check the other choices")
        self.play(FadeOut(ex3), FadeOut(r1), FadeOut(r2), FadeOut(reason1), FadeOut(reason2),
                  FadeOut(hdr_bg), FadeOut(lines), FadeOut(h1), FadeOut(h2))
        texts = ["A.  Definition of a straight angle",
                 "B.  Alternate Interior Angles are congruent",
                 "C.  Supplementary angles sum to 180°",
                 "D.  Same-Side Interior Angles Postulate"]
        items = []
        for i, t in enumerate(texts):
            it = Text(t, font_size=24)
            if it.width > 5.9:
                it.scale_to_fit_width(5.9)
            it.move_to([0.75, 2.7 - 0.6 * i, 0], aligned_edge=LEFT)
            items.append(it)
        self.play(*[FadeIn(it) for it in items])
        why_not = {
            1: "B gave us the equal pairs earlier, not 180°.",
            2: "Supplementary covers only two angles.",
            3: "Same-side interior is a different angle pair.",
        }
        for i in (1, 2, 3):
            x = MathTex("\\times", color=CANCEL).scale(1.0).move_to([0.4, items[i].get_center()[1], 0])
            w = note(why_not[i], [3.5, -0.3, 0], CANCEL, 26, 6.6)
            self.play(FadeIn(x), items[i].animate.set_color(GREY_B), FadeIn(w))
            self.wait(2)
            self.play(FadeOut(w))
        ck = MathTex("\\checkmark", color=ANSWER).scale(1.0).move_to([0.4, items[0].get_center()[1], 0])
        w = note("Three angles on a line: straight angle, 180°.", [3.5, -0.3, 0], ANSWER, 26, 6.6)
        self.play(FadeIn(ck), items[0].animate.set_color(ANSWER), FadeIn(w))
        self.wait(2)
        answer_banner(self, "Answer: A (straight angle)")
        self.wait(3)

    # ------------------------------------------------------------------
    def q28(self):
        question_card(self, 28)
        title = make_title("Question 28: Segment Addition")
        Y0 = 1.3
        Px, Qx, Rx = -6.2, -4.1, -1.3

        def pt(x, y=Y0):
            return np.array([x, y, 0])

        def seg(a, b, color, y=Y0):
            return Line(pt(a, y), pt(b, y), color=color, stroke_width=14)

        base = Line(pt(-6.8), pt(-0.5), color=GREY, stroke_width=4)
        dots = {k: Dot(pt(x), color=WHITE, radius=0.1) for k, x in (("P", Px), ("Q", Qx), ("R", Rx))}
        labs = {k: MathTex(k).scale(0.9).next_to(dots[k], UP, buff=0.2) for k in dots}

        self.play(Write(title))
        cap = caption("Step 1: P, Q, R lie on one line")
        self.play(FadeIn(cap, shift=UP * 0.2))
        self.play(Create(base), *[FadeIn(d) for d in dots.values()], *[FadeIn(l) for l in labs.values()])
        t1 = note("Given: P, Q, R are collinear", EQ_POS + UP * 1.2, GIVEN, 28)
        t2 = note("Conjecture:", EQ_POS + UP * 0.1, WHITE, 28)
        conj = MathTex("PQ", "+", "QR", "=", "PR").scale(1.0).next_to(t2, DOWN, buff=0.3)
        conj[0].set_color(TEAL_C); conj[2].set_color(PINK_C); conj[4].set_color(YELLOW)
        self.play(FadeIn(t1, shift=DOWN * 0.2))
        self.play(FadeIn(t2), Write(conj))
        self.wait(2.5)

        # phase 1: Q between P and R
        cap = swap_cap(self, cap, "Step 2: Measure the two pieces")
        pq = seg(Px, Qx, TEAL_C)
        qr = seg(Qx, Rx, PINK_C)
        tpq = tag("PQ=3", pt((Px + Qx) / 2, Y0 - 0.4), TEAL_C, 0.7)
        tqr = tag("QR=4", pt((Qx + Rx) / 2, Y0 - 0.4), PINK_C, 0.7)
        self.play(Create(pq), FadeIn(tpq))
        self.play(Create(qr), FadeIn(tqr))
        self.add(*dots.values())
        self.wait(1.5)

        cap = swap_cap(self, cap, "Step 3: Snap the pieces end to end")
        c1, c2 = pq.copy(), qr.copy()
        self.add(c1, c2)
        gap = 1.0
        self.play(c1.animate.shift(DOWN), c2.animate.shift(DOWN + RIGHT * gap), run_time=1.2)
        self.wait(0.6)
        self.play(c2.animate.shift(LEFT * gap), run_time=1.4)
        n1 = tag("3", pt((Px + Qx) / 2, Y0 - 1.35), TEAL_C, 0.8)
        n2 = tag("4", pt((Qx + Rx) / 2, Y0 - 1.35), PINK_C, 0.8)
        self.play(FadeIn(n1), FadeIn(n2))
        self.wait(1)

        cap = swap_cap(self, cap, "Step 4: They equal the whole PR")
        whole = seg(Px, Rx, YELLOW, Y0 - 2.1)
        nw = tag("PR=7", pt((Px + Rx) / 2, Y0 - 2.5), YELLOW, 0.8)
        self.play(Create(whole), FadeIn(nw))
        self.play(Indicate(c1), Indicate(c2), Indicate(whole))
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(conj))
        head = note("Segment Addition Postulate", EQ_POS + UP * 1.3, GIVEN, 28)
        eq = MathTex("PQ", "+", "QR", "=", "PR").move_to(EQ_POS)
        eq[0].set_color(TEAL_C); eq[2].set_color(PINK_C); eq[4].set_color(YELLOW)
        num = MathTex("3", "+", "4", "=", "7").next_to(eq, DOWN, buff=0.45)
        num[0].set_color(TEAL_C); num[2].set_color(PINK_C); num[4].set_color(YELLOW)
        self.play(FadeIn(head, shift=DOWN * 0.2), Write(eq))
        self.play(Write(num))
        ok = note("True when Q is between P and R", EQ_POS + DOWN * 1.65, ANSWER, 26)
        self.play(FadeIn(ok))
        self.wait(3)

        # phase 2: rearrange
        cap = swap_cap(self, cap, "Step 5: Now put R between P and Q")
        self.play(*[FadeOut(m) for m in (pq, qr, tpq, tqr, c1, c2, n1, n2, whole, nw, head, num, ok)])
        newR, newQ = -3.4, -1.3
        self.play(dots["R"].animate.move_to(pt(newR)), labs["R"].animate.move_to(pt(newR) + UP * 0.55),
                  dots["Q"].animate.move_to(pt(newQ)), labs["Q"].animate.move_to(pt(newQ) + UP * 0.55),
                  run_time=2)
        self.wait(1)
        pr = seg(Px, newR, YELLOW)
        rq = seg(newR, newQ, PINK_C)
        tpr = tag("PR=4", pt((Px + newR) / 2, Y0 - 0.4), YELLOW, 0.7)
        trq = tag("RQ=3", pt((newR + newQ) / 2, Y0 - 0.4), PINK_C, 0.7)
        self.play(Create(pr), FadeIn(tpr))
        self.play(Create(rq), FadeIn(trq))
        self.add(*dots.values())
        self.wait(1)

        cap = swap_cap(self, cap, "Step 6: Test the conjecture here")
        pq2 = seg(Px, newQ, TEAL_C, Y0 - 2.1)
        tpq2 = tag("PQ=7", pt((Px + newQ) / 2, Y0 - 2.5), TEAL_C, 0.8)
        self.play(Create(pq2), FadeIn(tpq2))
        test = MathTex("7", "+", "3", "=", "10", "\\neq", "4").next_to(eq, DOWN, buff=0.45)
        test[0].set_color(TEAL_C); test[2].set_color(PINK_C); test[6].set_color(YELLOW)
        test[4].set_color(CANCEL); test[5].set_color(CANCEL)
        self.play(Indicate(eq, color=GIVEN))
        self.play(Write(test))
        bad = note("False here: a counterexample!", EQ_POS + DOWN * 1.65, CANCEL, 26)
        self.play(FadeIn(bad))
        self.wait(3)

        cap = swap_cap(self, cap, "Step 7: Segments still add up")
        self.play(FadeOut(test), FadeOut(bad))
        c1, c2 = pr.copy(), rq.copy()
        self.add(c1, c2)
        self.play(c1.animate.shift(DOWN), c2.animate.shift(DOWN + RIGHT * gap), run_time=1.2)
        self.wait(0.5)
        self.play(c2.animate.shift(LEFT * gap), run_time=1.4)
        m1 = tag("4", pt((Px + newR) / 2, Y0 - 1.35), YELLOW, 0.8)
        m2 = tag("3", pt((newR + newQ) / 2, Y0 - 1.35), PINK_C, 0.8)
        self.play(FadeIn(m1), FadeIn(m2))
        self.play(Indicate(c1), Indicate(c2), Indicate(pq2))
        eq3 = MathTex("PR", "+", "RQ", "=", "PQ").move_to(EQ_POS)
        eq3[0].set_color(YELLOW); eq3[2].set_color(PINK_C); eq3[4].set_color(TEAL_C)
        num3 = MathTex("4", "+", "3", "=", "7").next_to(eq3, DOWN, buff=0.45)
        num3[0].set_color(YELLOW); num3[2].set_color(PINK_C); num3[4].set_color(TEAL_C)
        self.play(ReplacementTransform(eq, eq3))
        self.play(Write(num3))
        good = note("True: Segment Addition Postulate", EQ_POS + DOWN * 1.65, ANSWER, 26)
        self.play(FadeIn(good))
        self.wait(3)

        # check choices
        cap = swap_cap(self, cap, "Step 8: Check each choice")
        clear_right(self, [cap])
        texts = ["A.  QP + RQ = RP", "B.  PR + RQ = PQ", "C.  QR + PQ = PR",
                 "D.  The statement is true for\n      every arrangement."]
        ys = [2.8, 2.1, 1.4, 0.55]
        items = []
        for t, y in zip(texts, ys):
            it = Text(t, font_size=26, line_spacing=0.9)
            it.move_to([0.75, y, 0], aligned_edge=LEFT)
            items.append(it)
        self.play(*[FadeIn(it) for it in items])
        checks = {
            0: "7 + 3 = 10, but RP = 4. False.",
            2: "Same as the conjecture: 3 + 7 is not 4.",
            3: "We just found a counterexample.",
        }
        for i in (0, 2, 3):
            x = MathTex("\\times", color=CANCEL).move_to([0.4, items[i].get_center()[1], 0])
            w = note(checks[i], [3.5, -0.4, 0], CANCEL, 26, 6.6)
            self.play(FadeIn(x), items[i].animate.set_color(GREY_B), FadeIn(w))
            self.wait(2)
            self.play(FadeOut(w))
        ck = MathTex("\\checkmark", color=ANSWER).move_to([0.4, items[1].get_center()[1], 0])
        w = note("4 + 3 = 7 works, the postulate holds.", [3.5, -0.4, 0], ANSWER, 26, 6.6)
        self.play(FadeIn(ck), items[1].animate.set_color(ANSWER), FadeIn(w))
        self.wait(2)
        answer_banner(self, "Answer: B  PR + RQ = PQ")
        self.wait(3)
