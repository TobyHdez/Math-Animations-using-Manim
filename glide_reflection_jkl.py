from manim import *
import numpy as np

# Vertices read from the textbook graph (1 gridline = 1 unit).
J, K, L = (-5, -2), (-2, 3), (-3, -2)
J1, K1, L1 = (-5, 4), (-2, -1), (-3, 4)    # J', K', L'  (after the flip)
J2, K2, L2 = (0, 4), (3, -1), (2, 4)       # J'', K'', L''  (final image)
MIRROR_Y = 1                                # line of reflection y = 1
SLIDE = 5                                   # then translate 5 units right

ORIG = WHITE
IMG = ORANGE          # J''K''L''
MIRROR = PURPLE_B     # the line of reflection and the in-between triangle J'K'L'
MOVE = GREEN


class GlideReflectionJKL(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # Intro: the problem as printed
        # ------------------------------------------------------------------
        problem = ImageMobject("images/glide2_problem.png").scale_to_fit_width(10.5)
        self.play(FadeIn(problem))
        self.wait(4)
        self.play(FadeOut(problem))

        # ------------------------------------------------------------------
        # Layout: coordinate plane on the left, work on the right
        # ------------------------------------------------------------------
        title = Text("What glide reflection maps JKL to J''K''L''?", font_size=30)
        title.to_edge(UP)

        plane = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-4, 5, 1],
            x_length=6.0, y_length=4.5,
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

        tri_pre, dots_pre = tri([J, K, L], ORIG), dots([J, K, L], ORIG)
        tri_img, dots_img = tri([J2, K2, L2], IMG), dots([J2, K2, L2], IMG)
        labs_pre = VGroup(label("J", J, DL, ORIG), label("K", K, UP, ORIG), label("L", L, DR, ORIG))
        labs_img = VGroup(label("J''", J2, UL, IMG), label("K''", K2, DR, IMG), label("L''", L2, UP, IMG))

        self.play(Write(title), FadeIn(plane), FadeIn(nums))
        self.play(FadeIn(tri_pre), FadeIn(dots_pre), FadeIn(labs_pre),
                  FadeIn(tri_img), FadeIn(dots_img), FadeIn(labs_img))
        self.wait(1)

        # ------------------------------------------------------------------
        # Step 1: flip up/down or left/right?
        # ------------------------------------------------------------------
        cap = caption("Step 1: Which way did it flip?")
        self.play(FadeIn(cap, shift=UP * 0.2))
        base1 = Line(P(*J), P(*L), color=YELLOW, stroke_width=9)
        base2 = Line(P(*J2), P(*L2), color=YELLOW, stroke_width=9)
        t1 = Text("K is above JL.", font_size=28, color=YELLOW)
        t2 = Text("K'' is below J''L''.", font_size=28, color=YELLOW)
        t3 = Text("Up and down flipped,", font_size=28, color=YELLOW)
        t4 = Text("but left and right did not.", font_size=28, color=YELLOW)
        t5 = Text("So the mirror line is horizontal.", font_size=28, color=MIRROR)
        txt = VGroup(t1, t2, t3, t4, t5).arrange(DOWN, buff=0.28).move_to(EQ_POS)
        self.play(FadeIn(t1, shift=DOWN * 0.2), Create(base1), Indicate(dots_pre[1], color=YELLOW, scale_factor=2))
        self.play(FadeIn(t2, shift=DOWN * 0.2), Create(base2), Indicate(dots_img[1], color=YELLOW, scale_factor=2))
        self.wait(1)
        self.play(FadeIn(t3, shift=DOWN * 0.2))
        self.play(FadeIn(t4, shift=DOWN * 0.2))
        self.wait(1)
        self.play(FadeIn(t5, shift=DOWN * 0.2))
        self.wait(1.5)
        self.play(FadeOut(txt), FadeOut(base1), FadeOut(base2), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 2: work backward -- undo the slide
        # ------------------------------------------------------------------
        cap = caption("Step 2: Undo the slide")
        self.play(FadeIn(cap, shift=UP * 0.2))
        u1 = Text("Flipping up/down keeps x the same,", font_size=28, color=YELLOW)
        u2 = Text("so the slide moved J from x = -5", font_size=28, color=YELLOW)
        u3 = Text("to x = 0:", font_size=28, color=YELLOW)
        calc = MathTex("0", "-", "(-5)", "=", "5").scale(1.3)
        calc[4].set_color(MOVE)
        u4 = Text("Undo it: slide left 5.", font_size=28, color=MOVE)
        work = VGroup(u1, u2, u3, calc, u4).arrange(DOWN, buff=0.3).move_to(EQ_POS)
        self.play(FadeIn(u1, shift=DOWN * 0.2))
        self.play(FadeIn(u2, shift=DOWN * 0.2), FadeIn(u3, shift=DOWN * 0.2))
        self.play(Write(calc))
        self.wait(1)
        self.play(FadeIn(u4, shift=DOWN * 0.2))

        ghost = VGroup(tri([J2, K2, L2], MIRROR, 0.3), dots([J2, K2, L2], MIRROR))
        arrow = Arrow(P(*K2), P(*K1), color=MOVE, buff=0, stroke_width=7)
        arrow_lab = label("\\text{left } 5", (1.5, -1.5), DOWN, MOVE).move_to(P(1.5, -1.6))
        self.add(ghost)
        self.play(GrowArrow(arrow), FadeIn(arrow_lab))
        self.play(ghost.animate.shift(P(-SLIDE, 0) - P(0, 0)), run_time=2.5)
        labs_ghost = VGroup(label("J'", J1, UP, MIRROR), label("K'", K1, DOWN, MIRROR), label("L'", L1, UP, MIRROR))
        self.play(FadeIn(labs_ghost))
        self.wait(1.5)
        self.play(FadeOut(work), FadeOut(arrow), FadeOut(arrow_lab), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 3: now each point lines up with its partner -- find the mirror
        # ------------------------------------------------------------------
        cap = caption("Step 3: Find the line of reflection")
        self.play(FadeIn(cap, shift=UP * 0.2))
        hint = Text("Halfway between y = -2 and y = 4", font_size=28, color=YELLOW)
        calc = MathTex("{-2", "+", "4", "\\over", "2}", "=", "1").scale(1.3)
        calc[0].set_color(YELLOW)
        calc[2].set_color(YELLOW)
        calc[6].set_color(MIRROR)
        check = Text("Same for K and K': (3 + (-1)) / 2 = 1", font_size=26, color=GREY_B)
        work = VGroup(hint, calc, check).arrange(DOWN, buff=0.45).move_to(EQ_POS)

        span = Line(P(*J), P(*J1), color=YELLOW, stroke_width=7)
        d_mid = Dot(P(-5, MIRROR_Y), color=MIRROR, radius=0.11)
        self.play(FadeIn(hint, shift=DOWN * 0.2), Create(span))
        self.wait(1)
        self.play(Write(calc))
        self.play(FadeIn(d_mid, scale=3), Indicate(calc[6], color=MIRROR))
        mirror_line = DashedLine(P(-6, MIRROR_Y), P(6, MIRROR_Y), color=MIRROR, stroke_width=5)
        line_lab = label("y = 1", (5, MIRROR_Y), UP, MIRROR)
        self.play(Create(mirror_line), FadeIn(line_lab))
        self.play(FadeIn(check, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(VGroup(work, span, d_mid)), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 4: check it going forward -- flip, then slide
        # ------------------------------------------------------------------
        cap = caption("Step 4: Check it going forward")
        self.play(FadeIn(cap, shift=UP * 0.2), FadeOut(ghost), FadeOut(labs_ghost))
        hint = Text("Flip over y = 1", font_size=28, color=YELLOW)
        table1 = MathTex(
            "\\begin{array}{ccc}"
            "J(-5,-2) & \\to & J'(-5,4)\\\\"
            "K(-2,3) & \\to & K'(-2,-1)\\\\"
            "L(-3,-2) & \\to & L'(-3,4)"
            "\\end{array}",
            color=YELLOW,
        ).scale(1.0)
        work = VGroup(hint, table1).arrange(DOWN, buff=0.5).move_to(EQ_POS)
        self.play(FadeIn(hint, shift=DOWN * 0.2))

        flip = VGroup(tri([J, K, L], MIRROR, 0.3), dots([J, K, L], MIRROR))
        self.add(flip)
        self.play(Rotate(flip, angle=PI, axis=RIGHT, about_point=P(0, MIRROR_Y)), run_time=2.5)
        labs_flip = VGroup(label("J'", J1, UP, MIRROR), label("K'", K1, DOWN, MIRROR), label("L'", L1, UP, MIRROR))
        self.play(FadeIn(labs_flip), Write(table1), run_time=2)
        self.wait(2)

        hint2 = Text("Slide right 5", font_size=28, color=MOVE)
        table2 = MathTex(
            "\\begin{array}{ccc}"
            "J'(-5,4) & \\to & J''(0,4)\\\\"
            "K'(-2,-1) & \\to & K''(3,-1)\\\\"
            "L'(-3,4) & \\to & L''(2,4)"
            "\\end{array}",
            color=YELLOW,
        ).scale(1.0)
        work2 = VGroup(hint2, table2).arrange(DOWN, buff=0.5).move_to(EQ_POS)
        self.play(FadeOut(work))
        self.play(FadeIn(hint2, shift=DOWN * 0.2))
        flipped = VGroup(flip, labs_flip)
        self.play(flipped.animate.shift(P(SLIDE, 0) - P(0, 0)), run_time=2.5)
        self.play(Write(table2), run_time=2)
        self.play(FadeOut(flipped), Indicate(VGroup(tri_img, dots_img), color=IMG, scale_factor=1.05))
        self.wait(1.5)
        self.play(FadeOut(work2), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 5: name the two motions
        # ------------------------------------------------------------------
        cap = caption("Step 5: Name the two motions")
        self.play(FadeIn(cap, shift=UP * 0.2))
        a1 = Text("1. Reflect across y = 1", font_size=32, color=MIRROR)
        a2 = Text("2. Translate 5 units right", font_size=32, color=MOVE)
        answer = VGroup(a1, a2).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 0.8 + RIGHT * CX)
        box = SurroundingRectangle(answer, color=YELLOW, buff=0.3)
        self.play(FadeIn(a1, shift=RIGHT * 0.3))
        self.play(FadeIn(a2, shift=RIGHT * 0.3))
        self.play(Create(box))
        note = Text("This is a glide reflection.", font_size=30, color=YELLOW)
        note.move_to(DOWN * 0.55 + RIGHT * CX)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(4)
