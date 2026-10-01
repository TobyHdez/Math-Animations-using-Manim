from common import *

PLANE_C = LEFT * 4.0 + DOWN * 0.3
STAGE = [ORANGE, GREEN]


# ---------------------------------------------------------------- helpers
def fmt(p):
    return f"({p[0]},{p[1]})"


def fit(m, w=6.8):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def mk_plane(xr, yr, xlen, ylen, step=2):
    plane = NumberPlane(
        x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1],
        x_length=xlen, y_length=ylen,
        background_line_style={"stroke_color": GREY_B, "stroke_width": 1.2, "stroke_opacity": 0.3},
        axis_config={"stroke_color": WHITE, "stroke_width": 2.5},
    ).move_to(PLANE_C)
    nums = VGroup()
    for v in range(xr[0], xr[1] + 1):
        if v != 0 and v % step == 0:
            nums.add(MathTex(str(v)).scale(0.35).next_to(plane.c2p(v, 0), DOWN, buff=0.07))
    for v in range(yr[0], yr[1] + 1):
        if v != 0 and v % step == 0:
            nums.add(MathTex(str(v)).scale(0.35).next_to(plane.c2p(0, v), LEFT, buff=0.07))
    return plane, nums


def tri(plane, pts, color, op=0.25, sw=4):
    return Polygon(*[plane.c2p(*p) for p in pts], color=color, fill_color=color,
                   fill_opacity=op, stroke_width=sw)


def vlabels(plane, pts, names, color, scale=0.55, off=0.3):
    c = np.mean(np.array(pts, dtype=float), axis=0)
    g = VGroup()
    for p, n in zip(pts, names):
        d = np.array(p, dtype=float) - c
        nd = np.linalg.norm(d)
        d = d / nd if nd > 1e-6 else np.array([0, 1.0])
        t = MathTex(n, color=color).scale(scale)
        t.add_background_rectangle(BLACK, opacity=0.75, buff=0.04)
        t.move_to(plane.c2p(*p) + np.array([d[0], d[1], 0]) * off)
        g.add(t)
    return g


def tag(plane, text, at, color, scale=0.5):
    t = Text(text, font_size=26, color=color)
    t.add_background_rectangle(BLACK, opacity=0.8, buff=0.06)
    t.move_to(plane.c2p(*at))
    return t


def apply(op, pts):
    k = op[0]
    out = []
    for x, y in pts:
        if k == "rx":
            out.append((x, -y))
        elif k == "ry":
            out.append((-x, y))
        elif k == "r180":
            out.append((-x, -y))
        elif k == "ccw90":
            out.append((-y, x))
        elif k == "cw90":
            out.append((y, -x))
        elif k == "ccw270":          # 270 degrees counterclockwise = 90 clockwise
            out.append((y, -x))
        elif k == "cw270":           # 270 degrees clockwise = 90 counterclockwise
            out.append((-y, x))
        elif k == "shift":
            out.append((x + op[1], y + op[2]))
    return out


def anim(plane, m, op):
    O = plane.c2p(0, 0)
    k = op[0]
    if k == "rx":
        return Rotate(m, PI, axis=RIGHT, about_point=O)
    if k == "ry":
        return Rotate(m, PI, axis=UP, about_point=O)
    if k == "r180":
        return Rotate(m, PI, about_point=O)
    if k == "ccw90":
        return Rotate(m, PI / 2, about_point=O)
    if k == "cw90":
        return Rotate(m, -PI / 2, about_point=O)
    if k == "cw270":
        return Rotate(m, -3 * PI / 2, about_point=O)
    if k == "shift":
        return m.animate.shift(plane.c2p(op[1], op[2]) - O)


def mark(row, ok):
    m = MathTex("\\checkmark" if ok else "\\times", color=GREEN if ok else RED).scale(0.9)
    return m.next_to(row, RIGHT, buff=0.2)


def verdict_row(k, text, y0=2.85, dy=0.42):
    t = Text(text, font_size=24)
    t.move_to(np.array([-0.2, y0 - dy * k, 0]), aligned_edge=LEFT)
    return t


class TransformationSequences(Scene):
    """Questions 25, 26, 27, 29: sequences of rigid motions."""

    cap = None

    # ---- shared pieces
    def setcap(self, text):
        c = caption(text)
        if self.cap is None:
            self.play(FadeIn(c, shift=UP * 0.2))
        else:
            self.play(ReplacementTransform(self.cap, c))
        self.cap = c

    def banner(self, text):
        t = Text(text, font_size=30, color=ANSWER)
        fit(t, 6.4)
        box = SurroundingRectangle(t, color=YELLOW, buff=0.2)
        g = VGroup(t, box).move_to(RIGHT * CX + DOWN * 2.9)
        self.play(FadeIn(t, shift=UP * 0.2), Create(box))
        self.wait(3)

    def clear(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.cap = None

    def rule(self, tex, color=ORANGE, y=1.05):
        r = MathTex(tex, color=color).scale(0.8).move_to(RIGHT * CX + UP * y)
        return fit(r)

    def test_choice(self, plane, pts0, ops, rules, names, tnames, targets, k, vtext, ok,
                    final_hold=1.4):
        """Animate one candidate sequence and trace it in a small table."""
        row = verdict_row(k, vtext)
        self.play(FadeIn(row))
        mover = tri(plane, pts0, YELLOW, op=0.4, sw=5)
        self.play(FadeIn(mover))
        show = list(range(len(pts0))) if ok else [0]
        snaps = [pts0]
        parts = [[f"{names[i]}{fmt(pts0[i])}"] for i in show]
        trace_rows = []
        for r in range(len(show)):
            # build the row mobject once all snapshots are known: need them first
            pass
        # precompute snapshots
        cur = pts0
        for op in ops:
            cur = apply(op, cur)
            snaps.append(cur)
        rows = VGroup()
        for n, i in enumerate(show):
            ps = [f"{names[i]}{fmt(snaps[0][i])}"]
            for j in range(1, len(snaps)):
                ps += ["\\to", fmt(snaps[j][i])]
            if ok:
                ps += ["=", tnames[i]]
            else:
                ps += ["\\ne", f"{tnames[i]}{fmt(targets[i])}"]
            rows.add(MathTex(*ps).scale(0.72))
        rows.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        fit(rows)
        rows.move_to(RIGHT * CX + UP * 0.65, aligned_edge=UP)
        rows.set_x(CX)
        # colour the stage results
        for rw in rows:
            for j in range(1, len(snaps)):
                rw[2 * j].set_color(STAGE[(j - 1) % 2])
        cur_rule = None
        shown = VGroup()
        for j, op in enumerate(ops):
            new_rule = self.rule(rules[j], color=STAGE[j % 2])
            if cur_rule is None:
                self.play(FadeIn(new_rule, shift=UP * 0.1))
            else:
                self.play(ReplacementTransform(cur_rule, new_rule))
            cur_rule = new_rule
            if j == 0:
                first = VGroup(*[rw[0] for rw in rows])
                self.play(FadeIn(first))
            self.play(anim(plane, mover, op), run_time=1.5)
            cur_pts = snaps[j + 1]
            mover.become(tri(plane, cur_pts, YELLOW, op=0.4, sw=5))
            seg = VGroup(*[rw[2 * j + 1:2 * j + 3] for rw in rows])
            self.play(FadeIn(seg))
            shown.add(seg)
            self.wait(0.4)
        tail = VGroup(*[rw[2 * len(ops) + 1:] for rw in rows])
        if ok:
            tail.set_color(GREEN)
        else:
            tail[0][0].set_color(RED)
            tail[0][1].set_color(RED)
        self.play(FadeIn(tail))
        m = mark(row, ok)
        if ok:
            tgt_flash = tri(plane, targets, GREEN, op=0.0, sw=8)
            self.play(Indicate(mover, color=GREEN, scale_factor=1.05), Create(tgt_flash),
                      FadeIn(m, scale=2))
            self.wait(final_hold)
            self.play(FadeOut(tgt_flash))
            extra = []
        else:
            x = MathTex("\\times", color=RED).scale(3).move_to(mover.get_center())
            self.play(mover.animate.set_color(GREY), FadeIn(x, scale=2), FadeIn(m))
            self.wait(final_hold)
            extra = [x]
        self.play(FadeOut(mover), FadeOut(cur_rule), FadeOut(first), FadeOut(shown), FadeOut(tail),
                  *[FadeOut(e) for e in extra])
        return row, m

    # ------------------------------------------------------------ Q25
    def q25(self):
        question_card(self, 25, hold=7)
        title = make_title("Question 25: Sequence of Transformations")
        plane, nums = mk_plane((-10, 10), (-8, 8), 6.2, 4.96)
        ABC = [(-6, -5), (-3, -5), (-3, -2)]
        DEF = [(-6, 7), (-3, 7), (-3, 4)]
        t_abc, t_def = tri(plane, ABC, BLUE), tri(plane, DEF, RED)
        l_abc = vlabels(plane, ABC, ["A", "B", "C"], BLUE)
        l_def = vlabels(plane, DEF, ["D", "E", "F"], RED)
        self.play(Write(title), FadeIn(plane), FadeIn(nums))
        self.play(Create(t_abc), Create(t_def), FadeIn(l_abc), FadeIn(l_def))
        self.wait(1)

        self.setcap("Step 1: Match the vertices")
        rows = VGroup(*[MathTex(f"{a}{fmt(p)}", "\\to", f"{b}{fmt(q)}").scale(0.85)
                        for a, p, b, q in zip("ABC", ABC, "DEF", DEF)])
        rows.arrange(DOWN, buff=0.3).move_to(RIGHT * CX + UP * 1.2)
        for r in rows:
            r[0].set_color(BLUE)
            r[2].set_color(RED)
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4))
        hint = Text("x stays, y flips sign, then moves up", font_size=26, color=GIVEN)
        hint = fit(hint).move_to(RIGHT * CX + DOWN * 0.6)
        self.play(FadeIn(hint))
        self.wait(2.5)
        self.play(FadeOut(rows), FadeOut(hint))

        self.setcap("Step 2: Test each choice")
        rules = {
            "rx": "\\text{Reflect over x-axis: }(x,y)\\to(x,-y)",
            "ry": "\\text{Reflect over y-axis: }(x,y)\\to(-x,y)",
            "r180": "\\text{Rotate }180^\\circ\\text{: }(x,y)\\to(-x,-y)",
            "up2": "\\text{Up 2: }(x,y)\\to(x,y+2)",
            "right3": "\\text{Right 3: }(x,y)\\to(x+3,y)",
        }
        choices = [
            ("A  Reflect x-axis, then up 2", [("rx",), ("shift", 0, 2)], ["rx", "up2"], True),
            ("B  Reflect y-axis, then up 2", [("ry",), ("shift", 0, 2)], ["ry", "up2"], False),
            ("C  Rotate 180°, then right 3", [("r180",), ("shift", 3, 0)], ["r180", "right3"], False),
            ("D  Translate up 2 only", [("shift", 0, 2)], ["up2"], False),
        ]
        marks = []
        for k, (txt, ops, rk, ok) in enumerate(choices):
            if k == 1:
                self.setcap("Check the other choices")
            row, m = self.test_choice(plane, ABC, ops, [rules[r] for r in rk],
                                      "ABC", "DEF", DEF, k, txt, ok,
                                      final_hold=2.5 if ok else 1.6)
        self.wait(1)
        self.banner("Answer: A) Reflect x-axis, then up 2")
        self.clear()

    # ------------------------------------------------------------ Q26
    def q26(self):
        question_card(self, 26, hold=7)
        title = make_title("Question 26: Inverse of a Sequence")
        plane, nums = mk_plane((-6, 6), (-6, 6), 5.8, 5.8)
        T0 = [(1, 1), (4, 1), (1, 3)]
        T1 = apply(("cw90",), T0)
        T2 = apply(("ry",), T1)
        g0 = tri(plane, T0, BLUE)
        lab0 = vlabels(plane, T0, ["A", "B", "C"], BLUE)
        self.play(Write(title), FadeIn(plane), FadeIn(nums))
        self.play(Create(g0), FadeIn(lab0))

        # Step 1: forward
        self.setcap("Step 1: Follow the original")
        orig = VGroup(
            MathTex("1.\\ \\text{Rotate }90^\\circ\\text{ clockwise}", color=GIVEN).scale(0.8),
            MathTex("2.\\ \\text{Reflect over the y-axis}", color=GIVEN).scale(0.8),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * CX + UP * 2.3)
        self.play(FadeIn(orig[0]))
        mover = tri(plane, T0, YELLOW, op=0.4, sw=5)
        self.play(FadeIn(mover))
        self.play(anim(plane, mover, ("cw90",)), run_time=1.6)
        mover.become(tri(plane, T1, YELLOW, op=0.4, sw=5))
        ghost1 = tri(plane, T1, ORANGE, op=0.12, sw=3)
        lab1 = tag(plane, "after 1", (4.6, -2.6), ORANGE)
        self.play(FadeIn(ghost1), FadeIn(lab1))
        self.play(FadeIn(orig[1]))
        self.play(anim(plane, mover, ("ry",)), run_time=1.6)
        mover.become(tri(plane, T2, YELLOW, op=0.4, sw=5))
        ghost2 = tri(plane, T2, GREEN, op=0.12, sw=3)
        lab2 = tag(plane, "after 2", (-4.6, -2.6), GREEN)
        self.play(FadeIn(ghost2), FadeIn(lab2))
        self.wait(1.5)

        # Step 2: undo in reverse order
        self.setcap("Step 2: Undo in reverse order")
        undo = VGroup(
            MathTex("\\text{Undo step 2 first:}", color=GIVEN).scale(0.8),
            MathTex("\\text{Reflect over y-axis (same)}", color=ORANGE).scale(0.8),
            MathTex("\\text{Then undo step 1:}", color=GIVEN).scale(0.8),
            MathTex("\\text{Rotate }90^\\circ\\text{ counterclockwise}", color=GREEN).scale(0.8),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * CX + DOWN * 0.1)
        undo.set_x(CX)
        fit(undo)
        self.play(FadeIn(undo[0]))
        self.play(anim(plane, mover, ("ry",)), FadeIn(undo[1]), run_time=1.6)
        mover.become(tri(plane, T1, YELLOW, op=0.4, sw=5))
        self.wait(0.5)
        self.play(FadeIn(undo[2]))
        self.play(anim(plane, mover, ("ccw90",)), FadeIn(undo[3]), run_time=1.6)
        mover.become(tri(plane, T0, YELLOW, op=0.4, sw=5))
        self.play(Indicate(mover, color=GREEN, scale_factor=1.08), Indicate(g0, color=GREEN))
        self.wait(1.5)

        # Step 3: choices
        self.setcap("Step 3: Check the choices")
        self.play(FadeOut(orig), FadeOut(undo))
        rowA = verdict_row(0, "A  Reflect y-axis, rotate 90° ccw")
        mA = mark(rowA, True)
        self.play(FadeIn(rowA))
        self.play(FadeIn(mA, scale=2))
        self.wait(1)
        rowD = verdict_row(1, "D  Rotate 270° cw, reflect y-axis")
        self.play(FadeIn(rowD))
        # D: starts from after-2 position
        mover.become(tri(plane, T2, YELLOW, op=0.4, sw=5))
        self.wait(0.5)
        self.play(anim(plane, mover, ("cw270",)), run_time=1.8)
        S1 = apply(("cw270",), T2)
        mover.become(tri(plane, S1, YELLOW, op=0.4, sw=5))
        self.play(anim(plane, mover, ("ry",)), run_time=1.5)
        S2 = apply(("ry",), S1)
        mover.become(tri(plane, S2, YELLOW, op=0.4, sw=5))
        x = MathTex("\\times", color=RED).scale(3).move_to(mover.get_center())
        mD = mark(rowD, False)
        note = Text("It does not land back on ABC", font_size=26, color=RED)
        note = fit(note).move_to(RIGHT * CX + UP * 0.6)
        self.play(mover.animate.set_color(GREY), FadeIn(x, scale=2), FadeIn(mD), FadeIn(note))
        self.wait(2)
        self.play(FadeOut(mover), FadeOut(x), FadeOut(note))
        self.wait(0.5)
        self.banner("Answer: A) Reflect y-axis, then rotate 90° ccw")
        self.clear()

    # ------------------------------------------------------------ Q27
    def q27(self):
        question_card(self, 27, hold=7)
        title = make_title("Question 27: Name the Transformation")
        plane, nums = mk_plane((-8, 8), (-8, 8), 5.8, 5.8)
        ABC = [(1, 2), (4, 2), (1, 6)]
        PQR = [(1, -2), (4, -2), (1, -6)]
        g1, g2 = tri(plane, ABC, BLUE), tri(plane, PQR, RED)
        l1 = vlabels(plane, ABC, ["A", "B", "C"], BLUE)
        l2 = vlabels(plane, PQR, ["A'", "B'", "C'"], RED)
        self.play(Write(title), FadeIn(plane), FadeIn(nums))
        self.play(Create(g1), Create(g2), FadeIn(l1), FadeIn(l2))

        # Step 1: compare
        self.setcap("Step 1: Compare the points")
        rows = VGroup()
        for n, p, q in zip("ABC", ABC, PQR):
            r = MathTex(f"{n}(", str(p[0]), ",", str(p[1]), ")", "\\to", f"{n}'(", str(q[0]), ",", str(q[1]), ")")
            r.scale(0.9)
            r[1].set_color(GREEN)
            r[7].set_color(GREEN)
            r[3].set_color(ORANGE)
            r[9].set_color(ORANGE)
            rows.add(r)
        rows.arrange(DOWN, buff=0.3).move_to(RIGHT * CX + UP * 1.9)
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4))
        h1 = Text("x stays the same", font_size=28, color=GREEN)
        h2 = Text("y changes sign", font_size=28, color=ORANGE)
        hh = VGroup(h1, h2).arrange(DOWN, buff=0.25).move_to(RIGHT * CX + DOWN * 0.1)
        self.play(FadeIn(h1))
        self.play(FadeIn(h2))
        self.wait(2)

        # Step 2: name it
        self.setcap("Step 2: Name the motion")
        self.play(FadeOut(rows), FadeOut(hh))
        rule = MathTex("(x,\\ y)\\to(x,\\ -y)", color=ORANGE).scale(1.0).move_to(RIGHT * CX + UP * 1.5)
        name = Text("Reflection over the x-axis", font_size=30, color=GREEN)
        name = fit(name).move_to(RIGHT * CX + UP * 0.5)
        mover = tri(plane, ABC, YELLOW, op=0.4, sw=5)
        self.play(FadeIn(mover), Write(rule))
        self.play(anim(plane, mover, ("rx",)), run_time=2)
        mover.become(tri(plane, PQR, YELLOW, op=0.4, sw=5))
        self.play(FadeIn(name), Indicate(mover, color=GREEN, scale_factor=1.08))
        self.wait(2)
        self.play(FadeOut(mover), FadeOut(rule), FadeOut(name))

        # Step 3: distances / angles
        self.setcap("Step 3: Rigid or not?")
        lens = VGroup()
        for a, b, v in [("AB", "A'B'", 3), ("AC", "A'C'", 4), ("BC", "B'C'", 5)]:
            lens.add(MathTex(f"{a}={v}", "\\quad", f"{b}={v}").scale(0.9))
        lens.arrange(DOWN, buff=0.3).move_to(RIGHT * CX + UP * 1.8)
        for r in lens:
            r[0].set_color(BLUE)
            r[2].set_color(RED)
        self.play(LaggedStart(*[FadeIn(r) for r in lens], lag_ratio=0.5))
        same = Text("Same side lengths and angles", font_size=28, color=GREEN)
        same = fit(same).move_to(RIGHT * CX + DOWN * 0.2)
        self.play(FadeIn(same))
        self.wait(2)
        self.play(FadeOut(lens), FadeOut(same))

        # Step 4: choices
        self.setcap("Step 4: Pick the statement")
        texts = ["A  Rigid: keeps distance & angle",
                 "B  Non-rigid: keeps angle only",
                 "C  Rigid: keeps distance only",
                 "D  Non-rigid: keeps neither"]
        oks = [True, False, False, False]
        self.wait(0.3)
        for k, (t, ok) in enumerate(zip(texts, oks)):
            row = verdict_row(k, t, y0=2.3, dy=0.6)
            fit(row, 6.9)
            self.play(FadeIn(row))
            self.play(FadeIn(mark(row, ok), scale=2))
            self.wait(2 if ok else 1.4)
        note = Text("A reflection is a rigid motion.", font_size=28, color=GIVEN)
        note = fit(note).move_to(RIGHT * CX + DOWN * 0.3)
        self.play(FadeIn(note))
        self.wait(2)
        self.banner("Answer: A) Rigid reflection")
        self.clear()

    # ------------------------------------------------------------ Q29
    def q29(self):
        question_card(self, 29, hold=7)
        title = make_title("Question 29: Verify Congruence")
        plane, nums = mk_plane((-8, 8), (-8, 8), 5.8, 5.8)
        EFGH = [(2, 3), (6, 3), (6, 6), (3, 7)]
        TGT = [(-2, 3), (-6, 3), (-6, 6), (-3, 7)]
        g1, g2 = tri(plane, EFGH, BLUE), tri(plane, TGT, RED)
        l1 = vlabels(plane, EFGH, ["E", "F", "G", "H"], BLUE)
        l2 = vlabels(plane, TGT, ["E'", "F'", "G'", "H'"], RED)
        self.play(Write(title), FadeIn(plane), FadeIn(nums))
        self.play(Create(g1), Create(g2), FadeIn(l1), FadeIn(l2))

        self.setcap("Step 1: Pick a test point")
        t1 = Text("Follow E(2, 3). It must land", font_size=28, color=GIVEN)
        t2 = Text("exactly on E'(−2, 3).", font_size=28, color=GIVEN)
        t3 = Text("Congruent: every point matches.", font_size=28, color=GIVEN)
        tt = VGroup(t1, t2, t3).arrange(DOWN, buff=0.3).move_to(RIGHT * CX + UP * 1.2)
        self.play(FadeIn(tt))
        self.play(Indicate(l1[0], color=YELLOW), Indicate(l2[0], color=YELLOW))
        self.wait(2)
        self.play(FadeOut(tt))

        self.setcap("Step 2: Test each choice")
        rules = {
            "ccw90": "\\text{Rotate }90^\\circ\\text{ ccw: }(x,y)\\to(-y,x)",
            "r180": "\\text{Rotate }180^\\circ\\text{: }(x,y)\\to(-x,-y)",
            "rx": "\\text{Reflect x-axis: }(x,y)\\to(x,-y)",
            "ry": "\\text{Reflect y-axis: }(x,y)\\to(-x,y)",
        }
        choices = [
            ("A  Rotate 90°, reflect x-axis", [("ccw90",), ("rx",)], ["ccw90", "rx"], False),
            ("B  Rotate 90°, reflect y-axis", [("ccw90",), ("ry",)], ["ccw90", "ry"], False),
            ("C  Rotate 180°, reflect x-axis", [("r180",), ("rx",)], ["r180", "rx"], True),
            ("D  Rotate 180°, reflect y-axis", [("r180",), ("ry",)], ["r180", "ry"], False),
        ]
        for k, (txt, ops, rk, ok) in enumerate(choices):
            if k == 1:
                self.setcap("Check each choice in turn")
            self.test_choice(plane, EFGH, ops, [rules[r] for r in rk],
                             ["E", "F", "G", "H"], ["E'", "F'", "G'", "H'"], TGT, k, txt, ok,
                             final_hold=2.5 if ok else 1.6)
        self.wait(1)
        self.banner("Answer: C) Rotate 180°, reflect x-axis")
        self.clear()

    def construct(self):
        self.q25()
        self.q26()
        self.q27()
        self.q29()
