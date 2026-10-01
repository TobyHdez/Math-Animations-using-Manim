from common import *

UNIT_SIZE = 5.6
PLANE_CENTER = LEFT * 4.0 + DOWN * 0.4
RX = RIGHT * CX


def make_plane(lo, hi, ylo=None, yhi=None):
    ylo = lo if ylo is None else ylo
    yhi = hi if yhi is None else yhi
    plane = NumberPlane(
        x_range=[lo, hi, 1], y_range=[ylo, yhi, 1],
        x_length=UNIT_SIZE, y_length=UNIT_SIZE,
        background_line_style={"stroke_color": GREY_B, "stroke_width": 1.2, "stroke_opacity": 0.3},
        axis_config={"stroke_color": WHITE, "stroke_width": 2.5},
    ).move_to(PLANE_CENTER)
    nums = VGroup()
    for v in range(-10, 11):
        if v == 0 or v % 2:
            continue
        if lo <= v <= hi:
            nums.add(MathTex(str(v)).scale(0.4).next_to(plane.c2p(v, 0), DOWN, buff=0.08))
        if ylo <= v <= yhi:
            nums.add(MathTex(str(v)).scale(0.4).next_to(plane.c2p(0, v), LEFT, buff=0.08))
    return plane, nums


def poly(P, verts, color, fill=0.25, sw=4):
    return Polygon(*[P(*v) for v in verts], color=color, fill_color=color,
                   fill_opacity=fill, stroke_width=sw)


def pt_label(text, P, p, direction, color, scale=0.75):
    t = MathTex(text, color=color).scale(scale)
    t.add_background_rectangle(BLACK, opacity=0.85, buff=0.05)
    return t.next_to(P(*p), direction, buff=0.1)


def fmt(p):
    return f"({p[0]},{p[1]})"


def mark(ok):
    return MathTex("\\checkmark", color=GREEN) if ok else MathTex("\\times", color=RED)


def choice_line(text, y, color=WHITE):
    t = Text(text, font_size=26, color=color)
    t.move_to(RIGHT * 0.1 + UP * y, aligned_edge=LEFT)
    t.align_to(RIGHT * 0.0, LEFT)
    t.set_y(y)
    return t


def table(rows, y, colors=(YELLOW, GREEN), scale=0.9, gap=0.55):
    g = VGroup()
    for i, (a, b) in enumerate(rows):
        r = MathTex(a, "\\to", b).scale(scale)
        r[0].set_color(colors[0])
        r[2].set_color(colors[1])
        g.add(r)
    g.arrange(DOWN, buff=gap - 0.3)
    return g.move_to(RX + UP * y)


class TransformationsA(Scene):
    """Questions 16, 17, 18: rotations, translations, and a two-step transformation."""

    # ------------------------------------------------------------------ Q16
    def q16(self):
        title = make_title("Question 16: Rotations")
        plane, nums = make_plane(-6, 6)
        P = plane.c2p
        O = P(0, 0)
        self.play(Write(title), FadeIn(plane), FadeIn(nums))

        V = [(-5, -1), (-2, -1), (-2, -4)]
        tri = poly(P, V, YELLOW)
        quad = Text("III", font_size=44, color=GREY_B).move_to(P(-5, -5))
        self.play(FadeIn(tri), FadeIn(quad))
        d0 = Dot(P(*V[0]), color=YELLOW, radius=0.08)
        self.play(FadeIn(d0))
        self.wait(1)

        # Step 1: rotate 270 ccw
        cap = caption("Step 1: Rotate 270° counterclockwise")
        self.play(FadeIn(cap, shift=UP * 0.2))
        rule = MathTex("270^\\circ\\ \\text{ccw}:\\ (x,y)\\to(y,-x)", color=GREEN).scale(0.9).move_to(RX + UP * 2.4)
        self.play(Write(rule))
        self.wait(1)
        img = tri.copy().set_color(GREEN).set_fill(GREEN, 0.25)
        arc = Arc(radius=np.hypot(5, 1) * UNIT_SIZE / 12, start_angle=np.arctan2(-1, -5),
                  angle=1.5 * PI, arc_center=O, color=GREEN, stroke_width=4)
        arc.add_tip(tip_length=0.2)
        self.play(Rotate(img, angle=1.5 * PI, about_point=O, run_time=4),
                  Create(arc, run_time=4))
        d1 = Dot(P(-1, 5), color=GREEN, radius=0.08)
        self.play(FadeIn(d1))
        self.wait(0.5)

        rows = [(fmt(v), fmt((v[1], -v[0]))) for v in V]
        tb = table(rows, 1.0)
        self.play(FadeIn(tb, shift=LEFT * 0.2))
        self.wait(2.5)
        self.play(FadeOut(tb), FadeOut(arc))

        # Step 2: test the choices on the first vertex
        new_cap = caption("Step 2: Test each answer choice")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        target = MathTex("\\text{Target: }", "(-5,-1)", "\\to", "(-1,5)").scale(0.8).move_to(RX + UP * 2.4)
        target[1].set_color(YELLOW); target[3].set_color(GREEN)
        self.play(ReplacementTransform(rule, target))
        self.wait(1)

        tests = [
            ("A) 90° counterclockwise", PI / 2, "(x,y)\\to(-y,x)", (1, -5), False),
            ("B) 180° clockwise", -PI, "(x,y)\\to(-x,-y)", (5, 1), False),
            ("C) 90° clockwise", -PI / 2, "(x,y)\\to(y,-x)", (-1, 5), True),
            ("D) 270° clockwise", -1.5 * PI, "(x,y)\\to(-y,x)", (1, -5), False),
        ]
        lines = VGroup()
        for i, (name, ang, r, dest, ok) in enumerate(tests):
            ln = choice_line(name, 0.6 - 0.55 * i)
            self.play(FadeIn(ln, shift=LEFT * 0.2))
            rtex = MathTex(r, color=ORANGE).scale(0.85).move_to(RX + UP * 1.9)
            self.play(FadeIn(rtex))
            test = VGroup(tri.copy().set_color(ORANGE).set_fill(ORANGE, 0.15),
                          Dot(P(*V[0]), color=ORANGE, radius=0.1))
            self.add(test)
            self.play(Rotate(test, angle=ang, about_point=O, run_time=2.5))
            res = MathTex("(-5,-1)", "\\to", fmt(dest), color=GREEN if ok else RED).scale(0.85)
            res.move_to(RX + UP * 1.35)
            self.play(FadeIn(res))
            m = mark(ok).next_to(ln, RIGHT, buff=0.3)
            if ok:
                self.play(FadeIn(m, scale=1.5), Indicate(img, color=GREEN))
            else:
                self.play(FadeIn(m, scale=1.5))
            self.wait(2.2)
            lines.add(ln, m)
            self.play(FadeOut(test), FadeOut(rtex), FadeOut(res))
        self.wait(0.5)

        # Step 3: why
        new_cap = caption("Step 3: Together: a full turn")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        why = MathTex("270^\\circ\\ \\text{ccw}", "+", "90^\\circ\\ \\text{cw}", "=", "360^\\circ").scale(0.85)
        why[0].set_color(GREEN); why[2].set_color(GREEN)
        why.move_to(RX + UP * 1.7)
        self.play(Write(why))
        self.wait(2.5)
        banner = answer_banner(self, "Answer: C) 90° clockwise")
        self.wait(3)
        self.play(*[FadeOut(m_) for m_ in self.mobjects])

    # ------------------------------------------------------------------ Q17
    def q17(self):
        title = make_title("Question 17: Translations")
        plane, nums = make_plane(-7, 7)
        P = plane.c2p
        self.play(Write(title), FadeIn(plane), FadeIn(nums))

        V = [(-5, -6), (-2, -6), (-5, -3)]
        names = ["P", "Q", "R"]
        dirs = [DL, DR, UL]
        tri = poly(P, V, YELLOW)
        labs = VGroup(*[pt_label(n, P, v, d, YELLOW) for n, v, d in zip(names, V, dirs)])
        self.play(FadeIn(tri), FadeIn(labs))
        self.wait(1)

        cap = caption("Step 1: Read the vertices")
        self.play(FadeIn(cap, shift=UP * 0.2))
        pts = VGroup(*[MathTex(f"{n}{fmt(v)}", color=YELLOW).scale(0.9) for n, v in zip(names, V)])
        pts.arrange(DOWN, buff=0.25).move_to(RX + UP * 1.2)
        self.play(FadeIn(pts))
        self.wait(2)

        new_cap = caption("Step 2: Slide to the new spot")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        W = [(v[0] + 8, v[1] + 9) for v in V]
        arrows = VGroup(*[Arrow(P(*a), P(*b), buff=0, color=GREEN, stroke_width=4,
                                max_tip_length_to_length_ratio=0.08) for a, b in zip(V, W)])
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.3), run_time=2)
        img = tri.copy().set_color(GREEN).set_fill(GREEN, 0.25)
        self.add(img)
        self.play(img.animate.shift(P(8, 9) - P(0, 0)), run_time=3)
        labs2 = VGroup(*[pt_label(n + "'", P, w, d, GREEN) for n, w, d in zip(names, W, dirs)])
        self.play(FadeIn(labs2))
        self.wait(1)

        rows = [(f"{n}{fmt(v)}", f"{n}'{fmt(w)}") for n, v, w in zip(names, V, W)]
        tb = table(rows, 1.7)
        rule = MathTex("(x,y)\\to(x+8,\\ y+9)", color=GREEN).scale(0.95).move_to(RX + UP * 0.2)
        self.play(ReplacementTransform(pts, tb))
        self.wait(1)
        self.play(Write(rule))
        self.wait(2.5)
        self.play(FadeOut(tb), FadeOut(rule), FadeOut(arrows))

        # Step 3: compare
        new_cap = caption("Step 3: Compare the triangles")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        legs = VGroup(
            pt_label("3", P, (-3.5, -6), DOWN, WHITE, 0.7), pt_label("3", P, (-5, -4.5), LEFT, WHITE, 0.7),
            pt_label("3", P, (4.5, 3), DOWN, WHITE, 0.7), pt_label("3", P, (3, 4.5), LEFT, WHITE, 0.7),
        )
        self.play(FadeIn(legs))
        t1 = Text("Same side lengths", font_size=28, color=GIVEN).move_to(RX + UP * 1.7)
        t2 = Text("Same angles (90°, 45°, 45°)", font_size=28, color=GIVEN).move_to(RX + UP * 1.0)
        t3 = Text("Slide only moves it: congruent", font_size=28, color=GREEN).move_to(RX + UP * 0.3)
        for t in (t1, t2, t3):
            self.play(FadeIn(t, shift=LEFT * 0.2))
            self.wait(2.5)
        self.wait(1)

        new_cap = caption("Step 4: Check each choice")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        self.play(FadeOut(VGroup(t1, t2, t3)))
        opts = [("A) Congruent, shape unchanged", True),
                ("B) Side lengths change", False),
                ("C) Angle measures change", False),
                ("D) Only for right triangles", False)]
        for i, (txt, ok) in enumerate(opts):
            ln = choice_line(txt, 1.8 - 0.65 * i)
            m = mark(ok).next_to(ln, RIGHT, buff=0.3)
            self.play(FadeIn(ln, shift=LEFT * 0.2))
            self.wait(0.6)
            self.play(FadeIn(m, scale=1.5))
            self.wait(2.2)
        self.wait(0.5)
        answer_banner(self, "Answer: A) congruent")
        self.wait(3)
        self.play(*[FadeOut(m_) for m_ in self.mobjects])

    # ------------------------------------------------------------------ Q18
    def q18(self):
        title = make_title("Question 18: Two Transformations")
        plane, nums = make_plane(-5, 5, -1, 9)
        P = plane.c2p
        O = P(0, 0)
        self.play(Write(title), FadeIn(plane), FadeIn(nums))

        V = [(-1, 1), (1, 1), (-1, 4)]
        tri = poly(P, V, YELLOW)
        labs = VGroup(*[pt_label(n, P, v, d, YELLOW) for n, v, d in
                        zip("ABC", V, [DL, DR, UL])])
        # label for the original, kept clear of the axes
        self.play(FadeIn(tri), FadeIn(labs))
        orig_txt = MathTex("A(-1,1)\\ \\ B(1,1)\\ \\ C(-1,4)", color=YELLOW).scale(0.85).move_to(RX + UP * 2.5)
        self.play(Write(orig_txt))
        self.wait(2)

        # ---- Image 1
        cap = caption("Step 1: Image 1, look at x and y")
        self.play(FadeIn(cap, shift=UP * 0.2))
        W1 = [(-3, 1), (-1, 1), (-3, 4)]
        img1 = tri.copy().set_color(GREEN).set_fill(GREEN, 0.25)
        arrows = VGroup(*[Arrow(P(*a), P(*b), buff=0.03, color=GREEN, stroke_width=4,
                                max_tip_length_to_length_ratio=0.2) for a, b in zip(V, W1)])
        # draw only two non-overlapping arrows (A and C tops); B's arrow overlaps the shape edge
        arrows = VGroup(arrows[0], arrows[2])
        self.play(Create(arrows))
        self.add(img1)
        self.play(img1.animate.shift(LEFT * 2 * UNIT_SIZE / 10), run_time=2.5)
        l1 = VGroup(*[pt_label(n + "'", P, w, d, GREEN, 0.7) for n, w, d in
                      zip("ABC", W1, [DL, DOWN, UL])])
        # B' sits on the original's A; keep labels readable
        l1[1].next_to(P(-1, 1), DR, buff=0.1)
        l1[0].next_to(P(-3, 1), DL, buff=0.1)
        self.play(FadeIn(l1))
        self.wait(1)

        rule1 = MathTex("(x,y)\\to(x-2,\\ y)", color=GREEN).scale(0.95).move_to(RX + UP * 1.85)
        rows = [(f"{n}{fmt(v)}", f"{n}'{fmt(w)}") for n, v, w in zip("ABC", V, W1)]
        tb = table(rows, 0.6, scale=0.8)
        self.play(Write(rule1))
        self.play(FadeIn(tb))
        self.wait(2)
        n1 = Text("Same sizes (2, 3, √13): congruent", font_size=26, color=GIVEN).move_to(RX + DOWN * 0.55)
        self.play(FadeIn(n1, shift=UP * 0.2))
        self.wait(4)
        self.play(FadeOut(tb), FadeOut(rule1), FadeOut(n1))

        new_cap = caption("Step 2: Image 1 is a translation")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        la = choice_line("A) Image 1: translation", 1.6)
        lb = choice_line("B) Image 1: dilation", 1.0)
        ma, mb = mark(True).next_to(la, RIGHT, buff=0.3), mark(False).next_to(lb, RIGHT, buff=0.3)
        self.play(FadeIn(la, shift=LEFT * 0.2)); self.wait(0.6); self.play(FadeIn(ma, scale=1.5))
        self.wait(1)
        self.play(FadeIn(lb, shift=LEFT * 0.2)); self.wait(0.6); self.play(FadeIn(mb, scale=1.5))
        self.wait(3)
        self.play(FadeOut(VGroup(la, lb, ma, mb)), FadeOut(img1), FadeOut(l1), FadeOut(arrows))

        # ---- Image 2
        new_cap = caption("Step 3: Image 2, compare to original")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        W2 = [(2 * a, 2 * b) for a, b in V]
        img2 = tri.copy().set_color(GREEN).set_fill(GREEN, 0.18)
        self.add(img2)
        guides = VGroup(*[DashedLine(O, P(*w), color=GREY_B, stroke_width=2) for w in W2])
        self.play(Create(guides), run_time=1)
        self.play(img2.animate.scale(2, about_point=O), run_time=3)
        l2 = VGroup(
            pt_label("A'", P, W2[0], DL, GREEN, 0.7),
            pt_label("B'", P, W2[1], DR, GREEN, 0.7),
            pt_label("C'", P, W2[2], UL, GREEN, 0.7),
        )
        self.play(FadeIn(l2))
        self.wait(1)

        rule2 = MathTex("(x,y)\\to(2x,\\ 2y)", color=GREEN).scale(0.95).move_to(RX + UP * 1.85)
        rows = [(f"{n}{fmt(v)}", f"{n}'{fmt(w)}") for n, v, w in zip("ABC", V, W2)]
        tb = table(rows, 0.6, scale=0.8)
        self.play(Write(rule2))
        self.play(FadeIn(tb))
        self.wait(2)
        n2a = Text("Sides 2, 3, √13 become 4, 6, 2√13", font_size=26, color=GIVEN).move_to(RX + DOWN * 0.55)
        n2b = Text("Scale factor 2: similar, not congruent", font_size=26, color=GIVEN).move_to(RX + DOWN * 1.05)
        self.play(FadeIn(n2a, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeIn(n2b, shift=UP * 0.2))
        self.wait(4)
        self.play(FadeOut(tb), FadeOut(rule2), FadeOut(n2a), FadeOut(n2b))

        new_cap = caption("Step 4: Image 2 is a dilation")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        lc = choice_line("C) Image 2: dilation", 1.6)
        ld = choice_line("D) Image 2: translation", 1.0)
        mc, md = mark(True).next_to(lc, RIGHT, buff=0.3), mark(False).next_to(ld, RIGHT, buff=0.3)
        self.play(FadeIn(lc, shift=LEFT * 0.2)); self.wait(0.6); self.play(FadeIn(mc, scale=1.5))
        self.wait(1)
        self.play(FadeIn(ld, shift=LEFT * 0.2)); self.wait(0.6); self.play(FadeIn(md, scale=1.5))
        self.wait(2)
        answer_banner(self, "Answer: A and C")
        self.wait(3)
        self.play(*[FadeOut(m_) for m_ in self.mobjects])

    def construct(self):
        question_card(self, 16, hold=7)
        self.q16()
        question_card(self, 17, hold=7)
        self.q17()
        question_card(self, 18, hold=7)
        self.q18()
