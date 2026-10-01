from manim import *
import numpy as np

# Segment from (-1, -1) to (3, 1); both endpoints are open circles.
P1, P2 = (-1, -1), (3, 1)

SEG = RED_C        # the graph (matches the textbook picture)
DOM = GREEN        # domain / x-values
RAN = ORANGE       # range / y-values


class DomainRangeSegment(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # Intro: the problem as printed
        # ------------------------------------------------------------------
        problem = ImageMobject("images/domain_range_problem.png").scale_to_fit_width(9)
        self.play(FadeIn(problem))
        self.wait(4)
        self.play(FadeOut(problem))

        # ------------------------------------------------------------------
        # Layout: graph on the left, work on the right
        # ------------------------------------------------------------------
        title = Text("Describe the domain and range of the graph", font_size=30)
        title.to_edge(UP)

        plane = NumberPlane(
            x_range=[-3, 5, 1], y_range=[-3, 3, 1],
            x_length=5.6, y_length=4.2,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.5, "stroke_opacity": 0.35},
            axis_config={"stroke_color": WHITE, "stroke_width": 3},
        )
        plane.move_to(LEFT * 3.9 + DOWN * 0.4)
        P = plane.c2p

        nums = VGroup()
        for v in (-2, 2, 4):
            nums.add(MathTex(str(v)).scale(0.5).next_to(P(v, 0), DOWN, buff=0.12))
        for v in (-2, 2):
            nums.add(MathTex(str(v)).scale(0.5).next_to(P(0, v), LEFT, buff=0.12))
        nums.add(MathTex("x").scale(0.6).next_to(P(5, 0), UP, buff=0.1))
        nums.add(MathTex("y").scale(0.6).next_to(P(0, 3), RIGHT, buff=0.1))

        def open_circle(pt, color):
            return Circle(radius=0.1, color=color, stroke_width=4,
                          fill_color=BLACK, fill_opacity=1).move_to(P(*pt))

        def label(text, pt, direction, color, scale=0.7):
            m = MathTex(text, color=color).scale(scale)
            m.add_background_rectangle(BLACK, opacity=0.85, buff=0.06)
            return m.next_to(P(*pt), direction, buff=0.12)

        CX = 3.4
        EQ_POS = UP * 0.9 + RIGHT * CX
        STEP_POS = DOWN * 1.8 + RIGHT * CX

        def caption(text):
            return Text(text, font_size=28, color=BLUE).move_to(STEP_POS)

        seg = Line(P(*P1), P(*P2), color=SEG, stroke_width=7)
        oc1, oc2 = open_circle(P1, YELLOW), open_circle(P2, YELLOW)
        graph = VGroup(seg, oc1, oc2)
        lab1 = label("(-1,\\,-1)", P1, DL, YELLOW)
        lab2 = label("(3,\\,1)", P2, UR, YELLOW)

        self.play(Write(title), FadeIn(plane), FadeIn(nums))
        self.play(Create(seg), FadeIn(oc1, scale=2), FadeIn(oc2, scale=2))
        self.wait(1)

        # ------------------------------------------------------------------
        # Step 1: endpoints (open circles)
        # ------------------------------------------------------------------
        cap = caption("Step 1: Find the endpoints")
        self.play(FadeIn(cap, shift=UP * 0.2))
        e1 = Text("Endpoints: (-1, -1) and (3, 1)", font_size=28, color=YELLOW)
        e2 = Text("Open circles mean those", font_size=28, color=YELLOW)
        e3 = Text("two points are NOT included.", font_size=28, color=YELLOW)
        txt = VGroup(e1, e2, e3).arrange(DOWN, buff=0.35).move_to(EQ_POS)
        self.play(FadeIn(e1, shift=DOWN * 0.2), FadeIn(lab1), FadeIn(lab2))
        self.play(Indicate(oc1, color=YELLOW, scale_factor=1.8), Indicate(oc2, color=YELLOW, scale_factor=1.8))
        self.play(FadeIn(e2, shift=DOWN * 0.2))
        self.play(FadeIn(e3, shift=DOWN * 0.2))
        self.wait(2)
        self.play(FadeOut(txt), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 2: domain = shadow on the x-axis
        # ------------------------------------------------------------------
        cap = caption("Step 2: Domain = x-values")
        self.play(FadeIn(cap, shift=UP * 0.2))
        d1 = Text("Domain = all the x-values", font_size=28, color=DOM)
        d2 = Text("Squash the graph onto the x-axis.", font_size=28, color=YELLOW)
        d3 = Text("It covers x from -1 to 3,", font_size=28, color=YELLOW)
        d4 = Text("but not -1 or 3 itself.", font_size=28, color=YELLOW)
        d_ineq = MathTex("-1", "<", "x", "<", "3").scale(1.5)
        d_ineq[0].set_color(DOM)
        d_ineq[4].set_color(DOM)
        txt = VGroup(d1, d2, d3, d4, d_ineq).arrange(DOWN, buff=0.3).move_to(EQ_POS)

        self.play(FadeIn(d1, shift=DOWN * 0.2))
        drops = VGroup(
            DashedLine(P(*P1), P(-1, 0), color=DOM, stroke_width=3),
            DashedLine(P(*P2), P(3, 0), color=DOM, stroke_width=3),
        )
        self.play(FadeIn(d2, shift=DOWN * 0.2), Create(drops))
        src = VGroup(Line(P(*P1), P(*P2), color=DOM, stroke_width=7),
                     open_circle(P1, DOM), open_circle(P2, DOM))
        flat = VGroup(Line(P(-1, 0), P(3, 0), color=DOM, stroke_width=9),
                      open_circle((-1, 0), DOM), open_circle((3, 0), DOM))
        self.add(src)
        self.play(Transform(src, flat), run_time=2.5)
        x_labs = VGroup(
            MathTex("-1", color=DOM).scale(0.65).next_to(P(-1, 0), DOWN, buff=0.18),
            MathTex("3", color=DOM).scale(0.65).next_to(P(3, 0), DOWN, buff=0.18),
        )
        self.play(FadeIn(x_labs), FadeIn(d3, shift=DOWN * 0.2))
        self.play(FadeIn(d4, shift=DOWN * 0.2))
        self.play(Write(d_ineq))
        self.wait(2)
        self.play(FadeOut(txt), FadeOut(drops), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 3: range = shadow on the y-axis
        # ------------------------------------------------------------------
        cap = caption("Step 3: Range = y-values")
        self.play(FadeIn(cap, shift=UP * 0.2))
        r1 = Text("Range = all the y-values", font_size=28, color=RAN)
        r2 = Text("Squash the graph onto the y-axis.", font_size=28, color=YELLOW)
        r3 = Text("It covers y from -1 to 1,", font_size=28, color=YELLOW)
        r4 = Text("but not -1 or 1 itself.", font_size=28, color=YELLOW)
        r_ineq = MathTex("-1", "<", "y", "<", "1").scale(1.5)
        r_ineq[0].set_color(RAN)
        r_ineq[4].set_color(RAN)
        txt = VGroup(r1, r2, r3, r4, r_ineq).arrange(DOWN, buff=0.3).move_to(EQ_POS)

        self.play(FadeIn(r1, shift=DOWN * 0.2))
        drops = VGroup(
            DashedLine(P(*P1), P(0, -1), color=RAN, stroke_width=3),
            DashedLine(P(*P2), P(0, 1), color=RAN, stroke_width=3),
        )
        self.play(FadeIn(r2, shift=DOWN * 0.2), Create(drops))
        src = VGroup(Line(P(*P1), P(*P2), color=RAN, stroke_width=7),
                     open_circle(P1, RAN), open_circle(P2, RAN))
        flat = VGroup(Line(P(0, -1), P(0, 1), color=RAN, stroke_width=9),
                      open_circle((0, -1), RAN), open_circle((0, 1), RAN))
        self.add(src)
        self.play(Transform(src, flat), run_time=2.5)
        y_labs = VGroup(
            MathTex("-1", color=RAN).scale(0.65).next_to(P(0, -1), LEFT, buff=0.18),
            MathTex("1", color=RAN).scale(0.65).next_to(P(0, 1), LEFT, buff=0.18),
        )
        self.play(FadeIn(y_labs), FadeIn(r3, shift=DOWN * 0.2))
        self.play(FadeIn(r4, shift=DOWN * 0.2))
        self.play(Write(r_ineq))
        self.wait(2)
        self.play(FadeOut(txt), FadeOut(drops), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 4: (a) inequalities -- and the boxes they describe
        # ------------------------------------------------------------------
        cap = caption("Step 4: Write as inequalities")
        self.play(FadeIn(cap, shift=UP * 0.2))
        row_d = MathTex("\\text{Domain: }", "-1", "<", "x", "<", "3").scale(0.95)
        row_r = MathTex("\\text{Range: }", "-1", "<", "y", "<", "1").scale(0.95)
        for row, c in ((row_d, DOM), (row_r, RAN)):
            row[0].set_color(c)
            row[1].set_color(YELLOW)
            row[5].set_color(YELLOW)
        rows = VGroup(row_d, row_r).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(EQ_POS)
        hint = Text("Open circles: use <, not ≤", font_size=28, color=YELLOW)
        hint.next_to(rows, DOWN, buff=0.6)

        band_d = Rectangle(width=P(3, 0)[0] - P(-1, 0)[0], height=P(0, 3)[1] - P(0, -3)[1],
                           stroke_width=0, fill_color=DOM, fill_opacity=0.15).move_to(P(1, 0))
        band_r = Rectangle(width=P(5, 0)[0] - P(-3, 0)[0], height=P(0, 1)[1] - P(0, -1)[1],
                           stroke_width=0, fill_color=RAN, fill_opacity=0.15).move_to(P(1, 0))
        self.play(Write(row_d), FadeIn(band_d))
        self.play(Write(row_r), FadeIn(band_r))
        self.wait(1)
        self.play(FadeIn(hint, shift=UP * 0.2))
        self.wait(2.5)
        self.play(FadeOut(hint), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 5: (b) set-builder notation
        # ------------------------------------------------------------------
        cap = caption("Step 5: Write in set-builder form")
        self.play(FadeIn(cap, shift=UP * 0.2))
        new_d = MathTex("\\text{Domain: }", "\\{x \\mid", "-1", "<", "x", "<", "3", "\\}").scale(0.95)
        new_r = MathTex("\\text{Range: }", "\\{y \\mid", "-1", "<", "y", "<", "1", "\\}").scale(0.95)
        for row, c in ((new_d, DOM), (new_r, RAN)):
            row[0].set_color(c)
            row[2].set_color(YELLOW)
            row[6].set_color(YELLOW)
        new_rows = VGroup(new_d, new_r).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 1.6 + RIGHT * CX)
        self.play(TransformMatchingTex(row_d, new_d), TransformMatchingTex(row_r, new_r), run_time=2)
        read = Text("The bar | means \"such that\"", font_size=28, color=YELLOW)
        read2 = Text("{x | ...} = all x such that ...", font_size=28, color=YELLOW)
        VGroup(read, read2).arrange(DOWN, buff=0.3).next_to(new_rows, DOWN, buff=0.5)
        self.play(FadeIn(read, shift=UP * 0.2))
        self.play(FadeIn(read2, shift=UP * 0.2))
        self.wait(2)

        box = SurroundingRectangle(new_rows, color=YELLOW, buff=0.3)
        self.play(Create(box))
        self.wait(4)
