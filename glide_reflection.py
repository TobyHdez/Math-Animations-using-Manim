from manim import *
import numpy as np

# Vertices read from the textbook graph (1 gridline = 1 unit).
A, B, C = (-5, 1), (-3, 4), (-3, 1)
A2, B2, C2 = (3, -4), (1, -1), (1, -4)   # A', B', C'
MIRROR_X = -1                             # line of reflection x = -1
SLIDE = 5                                 # then translate 5 units down

ORIG = WHITE
IMG = ORANGE          # A'B'C' (matches the textbook picture)
MIRROR = PURPLE_B     # the line of reflection and the in-between triangle
MOVE = GREEN


class GlideReflection(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # Intro: the problem as printed
        # ------------------------------------------------------------------
        problem = ImageMobject("images/glide_problem.png").scale_to_fit_width(11)
        self.play(FadeIn(problem))
        self.wait(4)
        self.play(FadeOut(problem))

        # ------------------------------------------------------------------
        # Layout: coordinate plane on the left, work on the right
        # ------------------------------------------------------------------
        title = Text("Which two rigid motions map ABC to A'B'C'?", font_size=30)
        title.to_edge(UP)

        plane = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-5, 5, 1],
            x_length=6.0, y_length=5.0,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.5, "stroke_opacity": 0.35},
            axis_config={"stroke_color": WHITE, "stroke_width": 3},
        )
        plane.move_to(LEFT * 4.0 + DOWN * 0.4)
        P = plane.c2p

        nums = VGroup()
        for v in (-4, -2, 2, 4):
            nums.add(MathTex(str(v)).scale(0.5).next_to(P(v, 0), DOWN, buff=0.12))
            nums.add(MathTex(str(v)).scale(0.5).next_to(P(0, v), LEFT, buff=0.12))
        nums.add(MathTex("x").scale(0.6).next_to(P(6, 0), UP, buff=0.1))
        nums.add(MathTex("y").scale(0.6).next_to(P(0, 5), RIGHT, buff=0.1))

        def tri(pts, color, fill=0.2):
            return Polygon(*[P(*p) for p in pts], color=color, stroke_width=5,
                           fill_color=color, fill_opacity=fill)

        def dots(pts, color):
            return VGroup(*[Dot(P(*p), color=color, radius=0.07) for p in pts])

        def label(text, pt, direction, color):
            m = MathTex(text, color=color).scale(0.7)
            m.add_background_rectangle(BLACK, opacity=0.85, buff=0.06)
            return m.next_to(P(*pt), direction, buff=0.12)

        CX = 3.4
        EQ_POS = UP * 0.9 + RIGHT * CX
        STEP_POS = DOWN * 1.8 + RIGHT * CX

        def caption(text):
            return Text(text, font_size=28, color=BLUE).move_to(STEP_POS)

        def lines(*texts, color=YELLOW, size=28, buff=0.3):
            return VGroup(*[Text(t, font_size=size, color=color) for t in texts]).arrange(DOWN, buff=buff)

        tri_abc, dots_abc = tri([A, B, C], ORIG), dots([A, B, C], ORIG)
        tri_img, dots_img = tri([A2, B2, C2], IMG), dots([A2, B2, C2], IMG)
        labs_abc = VGroup(label("A", A, DL, ORIG), label("B", B, UP, ORIG), label("C", C, DR, ORIG))
        labs_img = VGroup(label("A'", A2, DR, IMG), label("B'", B2, RIGHT, IMG), label("C'", C2, DL, IMG))

        self.play(Write(title), FadeIn(plane), FadeIn(nums))
        self.play(FadeIn(tri_abc), FadeIn(dots_abc), FadeIn(labs_abc),
                  FadeIn(tri_img), FadeIn(dots_img), FadeIn(labs_img))
        self.wait(1)

        # ------------------------------------------------------------------
        # Step 1: read the coordinates
        # ------------------------------------------------------------------
        cap = caption("Step 1: Read the coordinates")
        self.play(FadeIn(cap, shift=UP * 0.2))
        table = MathTex(
            "\\begin{array}{ccc}"
            "A(-5,1) & \\to & A'(3,-4)\\\\"
            "B(-3,4) & \\to & B'(1,-1)\\\\"
            "C(-3,1) & \\to & C'(1,-4)"
            "\\end{array}",
            color=YELLOW,
        ).scale(1.1).move_to(EQ_POS)
        self.play(Write(table), run_time=2)
        self.wait(2)
        self.play(FadeOut(table), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 2: which way did it flip?
        # ------------------------------------------------------------------
        cap = caption("Step 2: Which way did it flip?")
        self.play(FadeIn(cap, shift=UP * 0.2))
        seg1 = Line(P(*A), P(*C), color=YELLOW, stroke_width=9)
        seg2 = Line(P(*A2), P(*C2), color=YELLOW, stroke_width=9)
        l1, l2, l3, l4 = (
            Text("A is left of C. A' is right of C'.", font_size=28, color=YELLOW),
            Text("Left and right flipped,", font_size=28, color=YELLOW),
            Text("but up and down did not.", font_size=28, color=YELLOW),
            Text("So the mirror line is vertical.", font_size=28, color=MIRROR),
        )
        txt = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.35).move_to(EQ_POS)
        self.play(FadeIn(l1, shift=DOWN * 0.2), Create(seg1), Create(seg2))
        self.wait(1.5)
        self.play(FadeIn(l2, shift=DOWN * 0.2))
        self.play(FadeIn(l3, shift=DOWN * 0.2))
        self.wait(1)
        self.play(FadeIn(l4, shift=DOWN * 0.2))
        self.wait(1.5)
        self.play(FadeOut(txt), FadeOut(seg1), FadeOut(seg2), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 3: the mirror line is halfway between the x-values
        # ------------------------------------------------------------------
        cap = caption("Step 3: Find the line of reflection")
        self.play(FadeIn(cap, shift=UP * 0.2))
        hint = Text("Halfway between x = -5 and x = 3", font_size=28, color=YELLOW)
        calc = MathTex("{-5", "+", "3", "\\over", "2}", "=", "-1").scale(1.3)
        calc[0].set_color(YELLOW)
        calc[2].set_color(YELLOW)
        calc[6].set_color(MIRROR)
        check = Text("Same for C and C': (-3 + 1) / 2 = -1", font_size=26, color=GREY_B)
        work = VGroup(hint, calc, check).arrange(DOWN, buff=0.45).move_to(EQ_POS)

        d_a, d_a2 = Dot(P(-5, 0), color=YELLOW, radius=0.09), Dot(P(3, 0), color=YELLOW, radius=0.09)
        d_mid = Dot(P(MIRROR_X, 0), color=MIRROR, radius=0.11)
        span = Line(P(-5, 0), P(3, 0), color=YELLOW, stroke_width=7)
        lab_a = MathTex("-5", color=YELLOW).scale(0.6).next_to(d_a, DOWN, buff=0.15)
        lab_a2 = MathTex("3", color=YELLOW).scale(0.6).next_to(d_a2, DOWN, buff=0.15)

        self.play(FadeIn(hint, shift=DOWN * 0.2),
                  Create(span), FadeIn(d_a, scale=2), FadeIn(d_a2, scale=2),
                  FadeIn(lab_a), FadeIn(lab_a2))
        self.wait(1)
        self.play(Write(calc))
        self.play(FadeIn(d_mid, scale=3), Indicate(calc[6], color=MIRROR))
        mirror_line = DashedLine(P(MIRROR_X, -5), P(MIRROR_X, 5), color=MIRROR, stroke_width=5)
        line_lab = label("x = -1", (MIRROR_X, -3), LEFT, MIRROR)
        self.play(Create(mirror_line), FadeIn(line_lab))
        self.play(FadeIn(check, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(VGroup(work, span, d_a, d_a2, d_mid, lab_a, lab_a2)), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 4: reflect ABC across x = -1
        # ------------------------------------------------------------------
        cap = caption("Step 4: Reflect across x = -1")
        self.play(FadeIn(cap, shift=UP * 0.2))
        hint = Text("Same height, other side of x = -1", font_size=28, color=YELLOW)
        table = MathTex(
            "\\begin{array}{ccc}"
            "A(-5,1) & \\to & A_1(3,1)\\\\"
            "B(-3,4) & \\to & B_1(1,4)\\\\"
            "C(-3,1) & \\to & C_1(1,1)"
            "\\end{array}",
            color=YELLOW,
        ).scale(1.1)
        work = VGroup(hint, table).arrange(DOWN, buff=0.5).move_to(EQ_POS)
        self.play(FadeIn(hint, shift=DOWN * 0.2))

        mirror_tri = VGroup(tri([A, B, C], MIRROR, 0.3), dots([A, B, C], MIRROR))
        self.add(mirror_tri)
        self.play(Rotate(mirror_tri, angle=PI, axis=UP, about_point=P(MIRROR_X, 0)), run_time=2.5)
        labs_mirror = VGroup(
            label("A_1", (3, 1), UR, MIRROR),
            label("B_1", (1, 4), UP, MIRROR),
            label("C_1", (1, 1), UL, MIRROR),
        )
        self.play(FadeIn(labs_mirror), Write(table), run_time=2)
        self.wait(2)
        self.play(FadeOut(work), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 5: slide parallel to the line (straight down)
        # ------------------------------------------------------------------
        cap = caption("Step 5: Slide parallel to the line")
        self.play(FadeIn(cap, shift=UP * 0.2))
        h1 = Text("Parallel to a vertical line", font_size=28, color=YELLOW)
        h2 = Text("means straight up or down.", font_size=28, color=YELLOW)
        h3 = Text("y goes from 1 down to -4:", font_size=28, color=YELLOW)
        eq = MathTex("-4", "-", "1", "=", "-5").scale(1.3)
        eq[4].set_color(MOVE)
        work = VGroup(h1, h2, h3, eq).arrange(DOWN, buff=0.35).move_to(EQ_POS)
        self.play(FadeIn(h1, shift=DOWN * 0.2))
        self.play(FadeIn(h2, shift=DOWN * 0.2))
        self.wait(1)

        arrow = Arrow(P(3, 1), P(3, -4), color=MOVE, buff=0, stroke_width=7)
        arrow_lab = label("\\text{down } 5", (3, -1.5), RIGHT, MOVE)
        self.play(FadeIn(h3, shift=DOWN * 0.2), GrowArrow(arrow))
        self.play(Write(eq), FadeIn(arrow_lab))
        self.wait(1)

        everything = VGroup(mirror_tri, labs_mirror)
        self.play(everything.animate.shift(P(0, -SLIDE) - P(0, 0)), run_time=2.5)
        self.wait(0.5)
        self.play(FadeOut(everything), FadeOut(arrow), FadeOut(arrow_lab),
                  Indicate(VGroup(tri_img, dots_img), color=IMG, scale_factor=1.05))
        self.wait(1.5)
        self.play(FadeOut(work), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 6: name the two motions
        # ------------------------------------------------------------------
        cap = caption("Step 6: Name the two motions")
        self.play(FadeIn(cap, shift=UP * 0.2))
        a1 = Text("1. Reflect across x = -1", font_size=32, color=MIRROR)
        a2 = Text("2. Translate 5 units down", font_size=32, color=MOVE)
        answer = VGroup(a1, a2).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 0.8 + RIGHT * CX)
        box = SurroundingRectangle(answer, color=YELLOW, buff=0.3)
        self.play(FadeIn(a1, shift=RIGHT * 0.3))
        self.play(FadeIn(a2, shift=RIGHT * 0.3))
        self.play(Create(box))
        note = Text("This is a glide reflection.", font_size=30, color=YELLOW)
        note.move_to(DOWN * 0.55 + RIGHT * CX)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(4)
