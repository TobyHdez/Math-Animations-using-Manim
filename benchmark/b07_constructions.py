from common import *

R = 1.6            # compass width for the angle arcs
ANG = 38           # size of the original angle (degrees)
SIDE = 3.2         # length of drawn rays
V0 = np.array([-6.0, 0.5, 0])    # vertex of the original angle
Q0 = np.array([-6.0, -2.4, 0])   # start of the new ray
HINT_POS = RIGHT * CX + UP * 0.9
NEEDLE = ORANGE


def d(a):
    """Unit vector at angle a (degrees)."""
    return np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])


class Constructions(Scene):
    """Questions 8-11: copy a segment / copy an angle with compass and straightedge."""

    # ---------- small helpers ----------
    def set_cap(self, text):
        new = caption(text)
        old = getattr(self, "_cap", None)
        if old is None:
            self.play(FadeIn(new, shift=UP * 0.2))
        else:
            self.play(ReplacementTransform(old, new))
        self._cap = new
        self.wait(1.2)

    def clear_cap(self):
        self._cap = None

    def tag(self, text, pos, direction, color=WHITE):
        t = Text(text, font_size=26, color=color).add_background_rectangle(BLACK, opacity=0.6, buff=0.06)
        t.next_to(pos, direction, buff=0.15)
        return t

    def mark(self, pos, name, direction, color=YELLOW):
        dot = Dot(pos, radius=0.09, color=color)
        lab = self.tag(name, pos, direction, color)
        self.play(FadeIn(dot, scale=2), FadeIn(lab), run_time=0.7)
        return VGroup(dot, lab)

    def ray(self, a, b, color=WHITE):
        return Arrow(a, b, buff=0, color=color, stroke_width=5, tip_length=0.25,
                     max_tip_length_to_length_ratio=1)

    def hint(self, *lines, color=GIVEN):
        g = VGroup(*[Text(s, font_size=28, color=color) for s in lines]).arrange(DOWN, buff=0.3)
        return g.move_to(HINT_POS)

    def sweep(self, c, r, a0, a1, rt=3.5):
        """Compass: needle point at c, pencil swings from angle a0 to a1 drawing an arc."""
        needle = Line(c, c + r * d(a0), color=NEEDLE, stroke_width=6)
        pivot = Dot(c, radius=0.1, color=NEEDLE)
        arc = Arc(radius=r, start_angle=np.radians(a0), angle=np.radians(a1 - a0),
                  arc_center=c, color=BLUE, stroke_width=5)
        self.play(FadeIn(needle), FadeIn(pivot), run_time=0.6)
        self.wait(0.4)
        self.play(Rotate(needle, np.radians(a1 - a0), about_point=c, rate_func=linear),
                  Create(arc, rate_func=linear), run_time=rt)
        self.play(FadeOut(needle), FadeOut(pivot), run_time=0.5)
        return arc

    def wipe(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.clear_cap()

    # ---------- angle figures ----------
    def original_angle(self, vname, end_names=None):
        side1 = self.ray(V0, V0 + SIDE * d(0))        # toward R
        side2 = self.ray(V0, V0 + SIDE * d(ANG))      # toward P
        self.play(Create(side1), Create(side2))
        labs = [self.tag(vname, V0, DL)]
        if end_names:
            labs.append(self.tag(end_names[0], V0 + SIDE * d(ANG), UP))
            labs.append(self.tag(end_names[1], V0 + SIDE * d(0), RIGHT))
        self.play(*[FadeIn(l) for l in labs])
        return VGroup(side1, side2, *labs)

    def new_ray(self, name, end_name=None):
        r_ = self.ray(Q0, Q0 + SIDE * d(0))
        self.play(Create(r_))
        labs = [self.tag(name, Q0, DL)]
        if end_name:
            labs.append(self.tag(end_name, Q0 + SIDE * d(0), RIGHT))
        self.play(*[FadeIn(l) for l in labs])
        return VGroup(r_, *labs)

    # ---------- Question 8 ----------
    def q8(self):
        question_card(self, 8)
        self.play(Write(make_title("Question 8: What construction?")))
        A, B = np.array([-6.0, 2.5, 0]), np.array([-3.0, 2.5, 0])
        C = np.array([-6.0, 0.0, 0])
        L = 3.0
        seg = Line(A, B, color=WHITE, stroke_width=5)
        self.play(Create(seg))
        ab = VGroup(Dot(A, radius=0.09), Dot(B, radius=0.09),
                    self.tag("A", A, UP), self.tag("B", B, UP))
        self.play(FadeIn(ab))
        ray = self.ray(C, C + 5.0 * RIGHT)
        self.play(Create(ray))
        cl = VGroup(Dot(C, radius=0.09), self.tag("C", C, LEFT))
        self.play(FadeIn(cl))
        h = self.hint("Clue: a segment AB and", "a ray starting at C")
        self.play(FadeIn(h))
        self.wait(2)

        self.set_cap("Step 1: Set compass to AB")
        needle = Line(A, B, color=NEEDLE, stroke_width=7)
        pv = Dot(A, radius=0.11, color=NEEDLE)
        self.play(Create(needle), FadeIn(pv))
        h2 = self.hint("Needle on A, pencil on B:", "the width is the length AB")
        self.play(ReplacementTransform(h, h2))
        self.wait(2.5)

        self.set_cap("Step 2: Move the compass to C")
        comp = VGroup(needle, pv)
        self.play(comp.animate.shift(C - A), run_time=2)
        self.wait(0.5)
        self.play(Rotate(comp, np.radians(35), about_point=C), run_time=1)

        self.set_cap("Step 3: Swing an arc over the ray")
        arc = Arc(radius=L, start_angle=np.radians(35), angle=np.radians(-62),
                  arc_center=C, color=BLUE, stroke_width=5)
        self.play(Rotate(comp, np.radians(-62), about_point=C, rate_func=linear),
                  Create(arc, rate_func=linear), run_time=3)
        self.wait(0.5)
        self.play(FadeOut(comp))

        self.set_cap("Step 4: Mark D on the ray")
        Dp = C + L * RIGHT
        dm = self.mark(Dp, "D", DOWN)
        cd = Line(C, Dp, color=GREEN, stroke_width=8)
        ab_g = Line(A, B, color=GREEN, stroke_width=8)
        self.play(Create(cd), Create(ab_g))
        h3 = self.hint("CD = AB", color=ANSWER)
        h4 = self.hint("Compass width carried onto a ray", "copies the segment", color=GIVEN)
        self.play(ReplacementTransform(h2, h3))
        self.wait(1.5)
        self.play(ReplacementTransform(h3, h4))
        self.wait(2.5)
        ban = answer_banner(self, "Answer: C) Copy a segment")
        self.wait(3)
        self.wipe()

    # ---------- Question 9 ----------
    def q9(self):
        question_card(self, 9)
        self.play(Write(make_title("Question 9: What construction?")))
        self.original_angle("Q", ("P", "R"))
        self.new_ray("S", "T")
        self.set_cap("Clue: an arc on the angle")
        h = self.hint("Compass point on vertex Q,", "arc across both sides")
        self.play(FadeIn(h))
        arc1 = self.sweep(V0, R, 0, ANG)
        self.wait(1)

        self.set_cap("Same width, new ray")
        h2 = self.hint("Same compass width,", "point on S: a matching arc")
        self.play(ReplacementTransform(h, h2))
        arc2 = self.sweep(Q0, R, -8, 50)
        self.wait(1)

        h3 = self.hint("An angle's arc, repeated on", "a new ray: copy an angle")
        self.play(ReplacementTransform(h2, h3), Indicate(arc1, color=YELLOW), Indicate(arc2, color=YELLOW))
        self.wait(2.5)
        answer_banner(self, "Answer: B) Copy an angle")
        self.wait(3)
        self.wipe()

    # ---------- Question 10 ----------
    def q10(self):
        question_card(self, 10)
        self.play(Write(make_title("Question 10: What next?")))
        self.original_angle("Q", ("P", "R"))
        self.new_ray("S", "T")
        self.set_cap("Jamal's arc at Q is drawn")
        arc1 = self.sweep(V0, R, 0, ANG)
        self.wait(0.5)

        opts = VGroup(
            Text("A. At S, same width, arc on ST", font_size=26),
            Text("B. At Q, widen to PQ", font_size=26),
            Text("C. Connect P and R", font_size=26),
            Text("D. At T, arc through new angle", font_size=26),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * CX + UP * 1.0)
        self.play(FadeIn(opts))
        self.wait(1.5)

        self.set_cap("Next: copy the arc to S")
        note = Text("The same width goes to the new ray", font_size=26, color=GIVEN).move_to(RIGHT * CX + DOWN * 0.7)
        self.play(FadeIn(note))
        arc2 = self.sweep(Q0, R, -8, 50)
        self.play(opts[0].animate.set_color(ANSWER), Indicate(arc2, color=YELLOW))
        self.wait(1.5)

        self.set_cap("Why not B, C or D?")
        wrongs = [(1, "Widening changes the arc width"),
                  (2, "That draws a chord, not the copy"),
                  (3, "T is the wrong end of the ray")]
        cur = note
        for idx, msg in wrongs:
            x = Cross(opts[idx], stroke_color=RED, stroke_width=5)
            n2 = Text(msg, font_size=26, color=RED).move_to(note)
            self.play(Create(x), ReplacementTransform(cur, n2))
            cur = n2
            self.wait(1.6)
        self.play(FadeOut(cur))
        answer_banner(self, "Answer: A) Set compass at S")
        self.wait(3)
        self.wipe()

    # ---------- Question 11 ----------
    def q11(self):
        question_card(self, 11)
        self.play(Write(make_title("Question 11: Order the steps")))
        self.original_angle("V")
        rows = VGroup(
            Text("W. Same width at P, mark M", font_size=26),
            Text("X. Draw a new ray from P", font_size=26),
            Text("Y. Arc at V across both sides", font_size=26),
            Text("Z. Width EF to M, mark L, ray", font_size=26),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * CX + UP * 1.3)
        rows.shift(RIGHT * 0.3)
        self.play(FadeIn(rows, shift=LEFT * 0.3))
        self.set_cap("Scrambled: find the order")
        self.wait(2.5)

        def done(row, n):
            badge = Text(str(n), font_size=28, color=GREEN).next_to(row, LEFT, buff=0.3)
            box = SurroundingRectangle(row, color=YELLOW, buff=0.1)
            self.play(Create(box), FadeIn(badge))
            return VGroup(box, badge)

        def unbox(g):
            self.play(g[0].animate.set_color(ANSWER))

        # 1st: X
        self.set_cap("1st: X, draw the new ray")
        g1 = done(rows[1], 1)
        self.new_ray("P")
        self.wait(1)
        unbox(g1)

        # 2nd: Y
        self.set_cap("2nd: Y, arc across both sides")
        g2 = done(rows[2], 2)
        arc1 = self.sweep(V0, R, 0, ANG)
        E, F = V0 + R * d(0), V0 + R * d(ANG)
        self.mark(E, "E", DOWN)
        self.mark(F, "F", UL)
        self.wait(1)
        unbox(g2)

        # 3rd: W
        self.set_cap("3rd: W, same arc at P")
        g3 = done(rows[0], 3)
        arc2 = self.sweep(Q0, R, -8, 50)
        M = Q0 + R * d(0)
        self.mark(M, "M", DOWN)
        self.wait(1)
        unbox(g3)

        # 4th: Z
        self.set_cap("4th: Z, measure EF, move to M")
        g4 = done(rows[3], 4)
        ef = Line(E, F, color=NEEDLE, stroke_width=7)
        self.play(Create(ef))
        self.wait(1.5)
        ef2 = ef.copy()
        self.play(ef2.animate.shift(M - E), run_time=2)
        ang0 = 75.0
        self.play(Rotate(ef2, np.radians(ang0 - (90 + ANG / 2)), about_point=M), run_time=1)
        self.play(FadeOut(ef2), FadeOut(ef), run_time=0.3)
        wid = 2 * R * np.sin(np.radians(ANG / 2))
        arc3 = self.sweep(M, wid, ang0, 145)
        Lp = Q0 + R * d(ANG)
        self.mark(Lp, "L", UL)
        self.set_cap("Draw the ray from P through L")
        newside = self.ray(Q0, Q0 + SIDE * d(ANG))
        self.play(Create(newside))
        self.wait(1)
        unbox(g4)
        self.play(Indicate(arc1, color=YELLOW), Indicate(arc2, color=YELLOW), run_time=1.5)
        self.wait(1.5)
        answer_banner(self, "Order: X, Y, W, Z")
        self.wait(3)
        self.wipe()

    def construct(self):
        self.q8()
        self.q9()
        self.q10()
        self.q11()
