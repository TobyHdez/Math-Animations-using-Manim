from common import *


def U(deg):
    return np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0.0])


def tag(tex, pos, color, scale=0.75):
    m = MathTex(tex, color=color).scale(scale)
    m.add_background_rectangle(BLACK, opacity=0.85, buff=0.05)
    return m.move_to(pos)


def ttag(text, pos, color, fs=22):
    m = Text(text, font_size=fs, color=color)
    m.add_background_rectangle(BLACK, opacity=0.85, buff=0.06)
    return m.move_to(pos)


def check_mark(pos, s=0.22):
    m = VMobject(color=GREEN, stroke_width=9)
    m.set_points_as_corners([pos + np.array([-s * 0.9, 0, 0]),
                             pos + np.array([-s * 0.3, -s * 0.7, 0]),
                             pos + np.array([s, s * 0.9, 0])])
    return m


def cross_mark(pos, s=0.2):
    return VGroup(Line(pos + np.array([-s, -s, 0]), pos + np.array([s, s, 0]), color=RED, stroke_width=9),
                  Line(pos + np.array([-s, s, 0]), pos + np.array([s, -s, 0]), color=RED, stroke_width=9))


def chevron(x, y):
    m = VMobject(color=YELLOW, stroke_width=5)
    m.set_points_as_corners([np.array([x - 0.13, y + 0.13, 0]), np.array([x, y, 0]), np.array([x - 0.13, y - 0.13, 0])])
    return m


class PL:
    """Parallel lines cut by a transversal that leans down-right (or the reverse for up > 90 deg).

    up = direction (degrees) of the transversal's upward ray.
    Sectors at an intersection: TR (0..up), TL (up..180), BL (180..180+up), BR (180+up..360).
    """

    def __init__(self, up, ys, xs, names, x0=-6.5, x1=-1.0, ext=0.8):
        self.up = up
        self.I = [np.array([x, y, 0.0]) for x, y in zip(xs, ys)]
        self.lines = VGroup(*[Line([x0, y, 0], [x1, y, 0], color=WHITE, stroke_width=5) for y in ys])
        du = U(up)
        L = ext / np.sin(np.radians(up))
        self.trans = Line(self.I[-1] - du * L, self.I[0] + du * L, color=WHITE, stroke_width=5)
        self.names = VGroup(*[MathTex(n).scale(0.9).move_to([x0 - 0.4, y, 0]) for n, y in zip(names, ys)])
        self.arcs, self.labs = {}, {}
        self.nums = VGroup()

    def sec(self, name):
        u = self.up
        return {"TR": (0, u), "TL": (u, 180 - u), "BL": (180, u), "BR": (180 + u, 180 - u)}[name]

    def add_angle(self, n, i, name, color, tex=None, r_arc=0.42, r_lab=0.78):
        s, size = self.sec(name)
        c = self.I[i]
        arc = Arc(radius=r_arc, start_angle=np.radians(s), angle=np.radians(size), arc_center=c,
                  color=color, stroke_width=6)
        lab = tag(tex or str(n), c + r_lab * U(s + size / 2), WHITE, 0.6)
        self.arcs[n] = arc
        self.labs[n] = lab
        self.nums.add(lab)
        return arc

    def draw(self, scene):
        scene.play(Create(self.lines), Create(self.trans), FadeIn(self.names))


def banner(scene, text, fs=32):
    t = Text(text, font_size=fs, color=ANSWER)
    box = SurroundingRectangle(t, color=YELLOW, buff=0.2)
    g = VGroup(t, box).move_to(RIGHT * CX + DOWN * 2.9)
    scene.play(FadeIn(t, shift=UP * 0.2), Create(box))
    return g


class ParallelLines(Scene):
    """Questions 2-5: parallel lines cut by a transversal."""

    def construct(self):
        self.q2()
        self.clear_all()
        self.q3()
        self.clear_all()
        self.q4()
        self.clear_all()
        self.q5()
        self.wait(2)

    def clear_all(self):
        self.play(*[FadeOut(m) for m in self.mobjects])

    def swap_cap(self, cap, text, pos=None):
        new = caption(text)
        if pos is not None:
            new.move_to(pos)
        self.play(ReplacementTransform(cap, new))
        return new

    # ------------------------------------------------------------------
    # Question 2: two-column proof
    # ------------------------------------------------------------------
    def q2(self):
        question_card(self, 2, hold=5)
        title = make_title("Question 2: Two-Column Proof")
        d = PL(112, ys=[1.7, -1.1], xs=[-4.9, -3.77], names=["p", "q"])
        d.add_angle(1, 0, "BL", ORANGE)
        d.add_angle(2, 0, "BR", GREEN)
        d.add_angle(7, 1, "TL", YELLOW)
        cap_pos = RIGHT * CX + DOWN * 2.5

        self.play(Write(title))
        d.draw(self)
        self.play(FadeIn(d.nums))
        self.wait(0.5)

        # goal
        cap = caption("Goal: show angle 2 = angle 7").move_to(cap_pos)
        self.play(FadeIn(cap, shift=UP * 0.2))
        goal = MathTex("\\text{Given: } p \\parallel q", "\\qquad", "\\text{Prove: } \\angle 2 \\cong \\angle 7").scale(0.8)
        goal.arrange(DOWN, buff=0.4)
        goal[1].set_opacity(0)
        goal.move_to(EQ_POS)
        goal = VGroup(goal[0], goal[2]).arrange(DOWN, buff=0.45).move_to(EQ_POS)
        self.play(Write(goal))
        self.play(Create(d.arcs[2]), Create(d.arcs[7]))
        self.play(Indicate(d.arcs[2], scale_factor=1.4), Indicate(d.arcs[7], scale_factor=1.4))
        self.wait(1.5)

        # table
        TX0, TX1, TXM = 0.2, 6.8, 3.5
        TOP, HB, RH = 3.1, 2.65, 0.7
        row_y = lambda k: HB - RH * (k - 0.5)
        bottom = HB - RH * 6
        frame = VGroup(
            Line([TX0, TOP, 0], [TX1, TOP, 0]), Line([TX0, HB, 0], [TX1, HB, 0]),
            Line([TX0, TOP, 0], [TX0, bottom, 0]), Line([TXM, TOP, 0], [TXM, bottom, 0]),
            Line([TX1, TOP, 0], [TX1, bottom, 0]),
            *[Line([TX0, HB - RH * k, 0], [TX1, HB - RH * k, 0]) for k in range(1, 7)],
        ).set_color(GREY_B).set_stroke(width=2)
        head = VGroup(Text("Statement", font_size=22).move_to([(TX0 + TXM) / 2, (TOP + HB) / 2, 0]),
                      Text("Reason", font_size=22).move_to([(TXM + TX1) / 2, (TOP + HB) / 2, 0]))
        self.play(FadeOut(goal), FadeIn(frame), FadeIn(head))

        # word bank
        reasons = ["Linear Pair\n(Supplementary Angles)", "Same-Side Interior\nAngles Postulate",
                   "Substitution\nProperty", "Subtraction Property\nof Equality"]
        chips = VGroup()
        pos = [(-5.4, -2.65), (-2.4, -2.65), (-5.4, -3.4), (-2.4, -3.4)]
        for r, (cx, cy) in zip(reasons, pos):
            t = Text(r, font_size=20, line_spacing=0.7)
            t.scale_to_fit_width(min(t.width, 2.6))
            box = RoundedRectangle(corner_radius=0.1, width=2.95, height=0.62, color=ORANGE, stroke_width=3)
            g = VGroup(box, t)
            g.move_to([cx, cy, 0])
            chips.add(g)
        wb = Text("Word Bank", font_size=20, color=ORANGE).move_to([-5.9, -2.12, 0])
        self.play(FadeIn(wb), FadeIn(chips))

        def stmt(parts, k):
            m = MathTex(*parts).scale(0.62)
            if m.width > TXM - TX0 - 0.25:
                m.scale_to_fit_width(TXM - TX0 - 0.25)
            m.move_to([TX0 + 0.12 + m.width / 2, row_y(k), 0])
            return m

        def blank(num, k):
            lab = Text(f"[{num}]", font_size=20, color=GREY_B).move_to([TXM + 0.4, row_y(k), 0])
            ul = Line([TXM + 0.75, row_y(k) - 0.2, 0], [TX1 - 0.1, row_y(k) - 0.2, 0], color=GREY_B, stroke_width=2)
            return VGroup(lab, ul)

        def drop(ci, k, bl):
            chip = chips[ci]
            tgt = Text(reasons[ci], font_size=20, color=GREEN, line_spacing=0.7)
            tgt.scale_to_fit_width(min(tgt.width, 2.7))
            tgt.move_to([(TXM + TX1) / 2, row_y(k), 0])
            cp = chip[1].copy()
            self.add(cp)
            self.play(chip[0].animate.set_stroke(opacity=0.25), chip[1].animate.set_opacity(0.3),
                      FadeOut(bl), ReplacementTransform(cp, tgt), run_time=1.3)
            return tgt

        m_ = "\\text{m}\\angle "
        # row 1
        cap = self.swap_cap(cap, "Step 1: The lines are parallel", cap_pos)
        r1 = stmt(["p", "\\parallel", "q"], 1)
        g1 = Text("Given", font_size=22).move_to([(TXM + TX1) / 2, row_y(1), 0])
        par = VGroup(chevron(-1.8, d.I[0][1]), chevron(-1.8, d.I[1][1]))
        self.play(Write(r1), FadeIn(g1), Create(par))
        self.wait(1.5)

        # row 2
        cap = self.swap_cap(cap, "Step 2: 1 and 2 form a linear pair", cap_pos)
        r2 = stmt([m_ + "1", "+", m_ + "2", "=", "180^\\circ"], 2)
        b2 = blank(1, 2)
        semi = Arc(radius=1.25, start_angle=np.pi, angle=np.pi, arc_center=d.I[0], color=WHITE, stroke_width=3)
        t180 = tag("180^\\circ", d.I[0] + DOWN * 1.58, WHITE, 0.6)
        self.play(Write(r2), FadeIn(b2))
        self.play(Create(d.arcs[1]), Create(semi), FadeIn(t180))
        self.play(Indicate(d.arcs[1], scale_factor=1.4), Indicate(d.arcs[2], scale_factor=1.4))
        t = Text("Together they make a straight line", font_size=24, color=GIVEN).move_to(RIGHT * CX + DOWN * 1.95)
        self.play(FadeIn(t, shift=UP * 0.15))
        self.wait(1)
        self.play(Indicate(chips[0], color=GREEN))
        rs2 = drop(0, 2, b2)
        self.wait(1)
        self.play(FadeOut(t), FadeOut(semi), FadeOut(t180))

        # row 3
        cap = self.swap_cap(cap, "Step 3: 1 and 7 are same-side interior", cap_pos)
        r3 = stmt([m_ + "1", "+", m_ + "7", "=", "180^\\circ"], 3)
        b3 = blank(2, 3)
        a1, a7 = d.arcs[1], d.arcs[7]
        dash = DashedLine(a1.point_from_proportion(0.5), a7.point_from_proportion(0.5), color=WHITE, stroke_width=3)
        t3 = tag("180^\\circ", dash.get_center() + LEFT * 0.7, WHITE, 0.6)
        self.play(Write(r3), FadeIn(b3))
        self.play(Indicate(a1, scale_factor=1.4), Indicate(a7, scale_factor=1.4))
        self.play(Create(dash), FadeIn(t3))
        t = Text("Inside the lines, same side: add to 180°", font_size=22, color=GIVEN).move_to(RIGHT * CX + DOWN * 1.95)
        self.play(FadeIn(t, shift=UP * 0.15))
        self.wait(1)
        self.play(Indicate(chips[1], color=GREEN))
        rs3 = drop(1, 3, b3)
        self.wait(1)
        self.play(FadeOut(t), FadeOut(dash), FadeOut(t3))

        # row 4
        cap = self.swap_cap(cap, "Step 4: Both sums equal 180°", cap_pos)
        r4 = stmt([m_ + "1", "+", m_ + "2", "=", m_ + "1", "+", m_ + "7"], 4)
        b4 = blank(3, 4)
        self.play(Indicate(r2[4], color=GREEN), Indicate(r3[4], color=GREEN))
        self.play(Write(r4), FadeIn(b4))
        self.wait(0.8)
        self.play(Indicate(chips[2], color=GREEN))
        rs4 = drop(2, 4, b4)
        self.wait(1)

        # row 5
        cap = self.swap_cap(cap, "Step 5: Subtract angle 1 each side", cap_pos)
        sl = VGroup(slash(r4[0]), slash(r4[4]))
        self.play(Create(sl), run_time=0.7)
        self.wait(1)
        r5 = stmt([m_ + "2", "=", m_ + "7"], 5)
        b5 = blank(4, 5)
        self.play(Write(r5), FadeIn(b5))
        self.play(Indicate(chips[3], color=GREEN))
        rs5 = drop(3, 5, b5)
        self.play(FadeOut(sl))
        self.wait(1)

        # row 6
        cap = self.swap_cap(cap, "Step 6: Equal measures = congruent", cap_pos)
        r6 = stmt(["\\angle 2", "\\cong", "\\angle 7"], 6)
        d6 = Text("Definition of\nCongruent Angles", font_size=20, line_spacing=0.7).move_to([(TXM + TX1) / 2, row_y(6), 0])
        d6.scale_to_fit_width(min(d6.width, 2.7))
        self.play(Write(r6), FadeIn(d6))
        self.play(Indicate(d.arcs[2], scale_factor=1.5), Indicate(d.arcs[7], scale_factor=1.5))
        self.wait(2)

        self.play(FadeOut(cap))
        t = Text("[1] Linear Pair    [2] Same-Side Interior\n[3] Substitution    [4] Subtraction",
                 font_size=24, color=ANSWER, line_spacing=0.9)
        t.scale_to_fit_width(min(t.width, 6.2))
        box = SurroundingRectangle(t, color=YELLOW, buff=0.2)
        g = VGroup(t, box).move_to(RIGHT * CX + DOWN * 2.9)
        self.play(FadeIn(t, shift=UP * 0.2), Create(box))
        self.wait(4)

    # ------------------------------------------------------------------
    # shared diagram for questions 3 and 4
    # ------------------------------------------------------------------
    def eight_angle_diagram(self):
        d = PL(112, ys=[1.6, -1.2], xs=[-4.9, -3.77], names=["a", "b"])
        small, big = GREEN, ORANGE
        spec = [(1, 0, "TL", small), (2, 0, "TR", big), (3, 0, "BL", big), (4, 0, "BR", small),
                (5, 1, "TL", small), (6, 1, "TR", big), (7, 1, "BL", big), (8, 1, "BR", small)]
        for n, i, s, c in spec:
            d.add_angle(n, i, s, c)
        return d

    def color_by_size(self, d):
        """Show that every angle is either small (68) or big (112)."""
        legend = VGroup(Text("green = small angle (68°)", font_size=22, color=GREEN),
                        Text("orange = big angle (112°)", font_size=22, color=ORANGE)
                        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([-4.0, -3.1, 0])
        self.play(*[Create(a) for a in d.arcs.values()], FadeIn(legend))
        return legend

    def run_options(self, d, opts, ys, label):
        rows, verdicts = [], []
        for (letter, tex, pair, verdict, ok), y in zip(opts, ys):
            row = MathTex(f"\\text{{{letter}}}\\quad {tex}").scale(0.85)
            row.move_to([0.3 + row.width / 2, y, 0])
            rows.append(row)
        self.play(*[FadeIn(r, shift=LEFT * 0.2) for r in rows])
        self.wait(1)
        cap = None
        for (letter, tex, pair, verdict, ok), y, row in zip(opts, ys, rows):
            new = caption(f"Test {letter}: angles {pair[0]} and {pair[1]}")
            if cap is None:
                self.play(FadeIn(new, shift=UP * 0.2))
            else:
                self.play(ReplacementTransform(cap, new))
            cap = new
            anims = []
            for n, a in d.arcs.items():
                if n in pair:
                    anims.append(a.animate.set_stroke(opacity=1, width=10))
                else:
                    anims.append(a.animate.set_stroke(opacity=0.15, width=6))
            self.play(*anims, row.animate.set_color(YELLOW))
            self.play(*[Indicate(d.arcs[n], scale_factor=1.4) for n in pair])
            v = Text(verdict, font_size=22, color=WHITE)
            v.scale_to_fit_width(min(v.width, 5.7))
            v.move_to([0.9 + v.width / 2, y - 0.4, 0])
            mk = check_mark(np.array([6.4, y - 0.1, 0])) if ok else cross_mark(np.array([6.4, y - 0.1, 0]))
            self.play(FadeIn(v, shift=UP * 0.1))
            self.play(Create(mk))
            self.play(row.animate.set_color(GREEN if ok else RED))
            self.wait(1.2)
        self.play(*[a.animate.set_stroke(opacity=1, width=6) for a in d.arcs.values()])
        return cap

    # ------------------------------------------------------------------
    def q3(self):
        question_card(self, 3, hold=5)
        title = make_title("Question 3: Which Must Be True?")
        d = self.eight_angle_diagram()
        self.play(Write(title))
        d.draw(self)
        self.play(FadeIn(d.nums))
        self.wait(0.5)

        cap = caption("Step 1: Color the angles by size")
        self.play(FadeIn(cap, shift=UP * 0.2))
        legend = self.color_by_size(d)
        t1 = Text("Parallel lines make only 2 sizes:", font_size=26, color=GIVEN)
        t2 = Text("small + big = 180°", font_size=26, color=GIVEN)
        t3 = Text("same size = congruent", font_size=26, color=GREEN)
        intro = VGroup(t1, t2, t3).arrange(DOWN, buff=0.35).move_to(EQ_POS + UP * 0.6)
        self.play(FadeIn(t1, shift=DOWN * 0.2))
        self.play(FadeIn(t2, shift=DOWN * 0.2))
        self.play(FadeIn(t3, shift=DOWN * 0.2))
        self.wait(2.5)
        self.play(FadeOut(intro))

        opts = [
            ("A", "\\text{m}\\angle 3 \\cong \\text{m}\\angle 5", (3, 5), "same-side interior: 112° + 68° = 180°", False),
            ("B", "\\text{m}\\angle 4 \\cong \\text{m}\\angle 6", (4, 6), "same-side interior: 68° + 112° = 180°", False),
            ("C", "\\text{m}\\angle 2 \\cong \\text{m}\\angle 7", (2, 7), "alternate exterior: 112° = 112°", True),
            ("D", "\\text{m}\\angle 1 \\cong \\text{m}\\angle 6", (1, 6), "small vs big: 68° and 112° differ", False),
        ]
        ys = [2.4, 1.5, 0.6, -0.3]
        self.play(FadeOut(cap))
        cap = self.run_options(d, opts, ys, "3")
        self.play(FadeOut(cap))
        banner(self, "Answer: C")
        self.wait(4)

    # ------------------------------------------------------------------
    def q4(self):
        question_card(self, 4, hold=5)
        title = make_title("Question 4: Select All Congruent Pairs")
        d = self.eight_angle_diagram()
        self.play(Write(title))
        d.draw(self)
        self.play(FadeIn(d.nums))
        legend = self.color_by_size(d)
        self.wait(0.5)

        opts = [
            ("A", "\\angle 1 \\text{ and } \\angle 4 \\text{ (vertical)}", (1, 4), "vertical angles: 68° = 68°", True),
            ("B", "\\angle 2 \\text{ and } \\angle 6 \\text{ (corresponding)}", (2, 6), "corresponding angles: 112° = 112°", True),
            ("C", "\\angle 3 \\text{ and } \\angle 5 \\text{ (same-side int.)}", (3, 5), "same-side interior: 112° + 68° = 180°", False),
            ("D", "\\angle 4 \\text{ and } \\angle 6 \\text{ (same-side int.)}", (4, 6), "same-side interior: 68° + 112° = 180°", False),
            ("E", "\\angle 1 \\text{ and } \\angle 6", (1, 6), "small vs big: not equal", False),
        ]
        ys = [2.85, 2.0, 1.15, 0.3, -0.55]
        cap = self.run_options(d, opts, ys, "4")
        cap2 = caption("Equal sizes are congruent").move_to(cap)
        self.play(ReplacementTransform(cap, cap2))
        self.wait(1.5)
        self.play(FadeOut(cap2))
        banner(self, "Answer: A and B")
        self.wait(4)

    # ------------------------------------------------------------------
    def q5(self):
        question_card(self, 5, hold=6)
        title = make_title("Question 5: Same-Side Interior Angles")
        d = PL(70, ys=[1.8, 0.2, -1.4], xs=[-3.5, -4.08, -4.66], names=["p", "q", "r"], ext=0.9)
        a110 = Arc(radius=0.55, start_angle=np.radians(250), angle=np.radians(110), arc_center=d.I[0],
                   color=YELLOW, stroke_width=6)
        l110 = tag("110^\\circ", d.I[0] + 1.05 * U(305), YELLOW, 0.65)
        a1 = d.add_angle(1, 1, "TR", GREEN, r_arc=0.5, r_lab=0.8)
        strip = Polygon(d.I[0], np.array([-1.0, 1.8, 0]), np.array([-1.0, 0.2, 0]), d.I[1],
                        color=ORANGE, fill_color=ORANGE, fill_opacity=0.18, stroke_width=0)

        self.play(Write(title))
        d.draw(self)
        self.play(Create(a110), FadeIn(l110))
        self.play(Create(a1), FadeIn(d.nums))
        cap = caption("Step 1: Find the angles")
        self.play(FadeIn(cap, shift=UP * 0.2))
        t1 = Text("We know 110°. We want angle 1.", font_size=26, color=GIVEN).move_to(EQ_POS + UP * 0.7)
        self.play(FadeIn(t1, shift=DOWN * 0.2))
        self.play(Indicate(a110, scale_factor=1.4), Indicate(a1, scale_factor=1.4))
        self.wait(1.5)

        cap = self.swap_cap(cap, "Step 2: Same-side interior angles")
        t2a = Text("Both are between the parallel lines", font_size=26, color=GIVEN)
        t2b = Text("and on the same side of Main St.", font_size=26, color=GIVEN)
        t2 = VGroup(t2a, t2b).arrange(DOWN, buff=0.3).move_to(EQ_POS + UP * 0.7)
        self.play(FadeOut(t1), FadeIn(strip))
        self.play(FadeIn(t2, shift=DOWN * 0.2))
        self.play(Indicate(a110, scale_factor=1.4), Indicate(a1, scale_factor=1.4))
        self.wait(2)

        cap = self.swap_cap(cap, "Step 3: They add up to 180°")
        t3a = Text("Same-side interior angles", font_size=26, color=GIVEN)
        t3b = Text("are supplementary (add to 180°)", font_size=26, color=GIVEN)
        t3 = VGroup(t3a, t3b).arrange(DOWN, buff=0.3).move_to(EQ_POS + UP * 1.0)
        self.play(FadeOut(t2), FadeIn(t3, shift=DOWN * 0.2))
        self.wait(1.5)
        e1 = eq_tex("\\text{m}\\angle 1", "+110", "=", "180").move_to(EQ_POS + DOWN * 0.3 + LEFT * 0.5)
        self.play(Write(e1))
        self.wait(1.5)
        t4 = Text("Not equal! They only add up to 180°.", font_size=24, color=RED).move_to(EQ_POS + UP * 1.0)
        self.play(FadeOut(t3), FadeIn(t4))
        self.wait(1.5)
        self.play(FadeOut(t4))

        cap = self.swap_cap(cap, "Step 4: Subtract 110 from both sides")
        eq = op_step(self, e1, ops=("-110", "-110"), under=([0, 1], [3]),
                     mid=eq_tex("\\text{m}\\angle 1", "+110", "-110", "=", "180", "-110").move_to(EQ_POS + DOWN * 0.3 + LEFT * 0.5),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[1, 2], combine=([4, 5], "180 - 110 = 70"),
                     result=eq_tex("\\text{m}\\angle 1", "=", "70").move_to(EQ_POS + DOWN * 0.3 + LEFT * 0.5))
        self.play(eq[2].animate.set_color(ANSWER))
        self.wait(1)

        cap = self.swap_cap(cap, "Step 5: Check on the diagram")
        new_l = tag("70^\\circ", d.nums[0].get_center(), ANSWER, 0.65)
        self.play(Transform(d.nums[0], new_l))
        chk = Text("Check: 70° + 110° = 180°", font_size=26, color=GIVEN).move_to(EQ_POS + DOWN * 1.2)
        self.play(FadeIn(chk, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(cap))
        answer_banner(self, "Answer: B) 70°")
        self.wait(4)
