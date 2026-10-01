from alg_common import *

# (number, color, equation tex, start, end, tag position)
LINES = [
    (1, RED_C, "y = 2x - 1", (-2.5, -6), (3.5, 6), (2.7, 4.4)),
    (2, BLUE_C, "y = -x + 4", (-2, 6), (6, -2), (-1.3, 5.4)),
    (3, GREEN_C, "y = \\tfrac{1}{2}x + 2", (-6, -1), (6, 5), (5.2, 4.5)),
    (4, PURPLE_C, "x = -2", (-2, -6), (-2, 6), (-2, -5.2)),
    (5, ORANGE, "y = -3", (-6, -3), (6, -3), (5.2, -3.7)),
    (6, TEAL_C, "y = x", (-6, -6), (6, 6), (-5.2, -4.5)),
]


class Q26(Scene):
    """Label six graphed lines with equations from a word bank."""

    def construct(self):
        q_card(self, 26)
        self.play(Write(make_title("Question 26: Match the Lines to Equations")))

        plane = NumberPlane(
            x_range=[-6, 6, 2], y_range=[-6, 6, 2], x_length=5.2, y_length=5.2,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.2, "stroke_opacity": 0.3},
            axis_config={"stroke_color": WHITE, "stroke_width": 2.5},
        ).move_to(LEFT * 3.9 + DOWN * 0.4)
        P = plane.c2p
        nums = VGroup()
        for v in (-4, -2, 2, 4):
            nums.add(MathTex(str(v)).scale(0.4).next_to(P(v, 0), DOWN, buff=0.06))
            nums.add(MathTex(str(v)).scale(0.4).next_to(P(0, v), LEFT, buff=0.06))
        self.play(FadeIn(plane), FadeIn(nums))

        lines, tags = {}, {}
        for n, col, eq, a, b, tp in LINES:
            lines[n] = Line(P(*a), P(*b), color=col, stroke_width=5)
            t = Text(str(n), font_size=22, color=WHITE, weight=BOLD)
            badge = VGroup(RoundedRectangle(corner_radius=0.05, width=0.32, height=0.32, fill_color=col,
                                            fill_opacity=1, stroke_width=0), t)
            t.move_to(badge[0])
            tags[n] = badge.move_to(P(*tp))
        self.play(*[Create(lines[n]) for n in lines], run_time=2)
        self.play(*[FadeIn(tags[n]) for n in tags])

        # right-hand answer list
        slots = {}
        for i, (n, col, eq, a, b, tp) in enumerate(LINES):
            row = VGroup(Text(f"Line {n}:", font_size=26, color=col), MathTex(eq, color=col)).arrange(RIGHT, buff=0.3)
            row.move_to([CX, 2.55 - 0.52 * i, 0]).align_to([CX - 2.4, 0, 0], LEFT)
            slots[n] = row

        def reveal(n):
            self.play(FadeIn(slots[n], shift=LEFT * 0.2), run_time=0.8)

        def focus(ns):
            self.play(*[lines[k].animate.set_stroke(width=10 if k in ns else 3, opacity=1 if k in ns else 0.35) for k in lines],
                      run_time=0.6)

        note = lambda s, col=YELLOW: Text(s, font_size=26, color=col).move_to([CX, -0.95, 0])

        cap = caption("Step 1: Straight lines first")
        self.play(FadeIn(cap, shift=UP * 0.2))
        focus([4])
        n1 = note("Line 4 is straight up and down: x = a number")
        self.play(FadeIn(n1, shift=UP * 0.2)); reveal(4); self.wait(1.2)
        self.play(FadeOut(n1))
        focus([5])
        n2 = note("Line 5 is flat: y = a number")
        self.play(FadeIn(n2, shift=UP * 0.2)); reveal(5); self.wait(1.2)
        self.play(FadeOut(n2))

        new_cap = caption("Step 2: The line through (0, 0)")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        focus([6])
        o = Dot(P(0, 0), color=YELLOW, radius=0.09)
        n3 = note("Rise 1, run 1, no y-intercept: y = x")
        self.play(FadeIn(o, scale=2), FadeIn(n3, shift=UP * 0.2)); reveal(6); self.wait(1.2)
        self.play(FadeOut(n3), FadeOut(o))

        new_cap = caption("Step 3: Read the y-intercept")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        for n, b, txt in [(1, -1, "Line 1 crosses at -1 and is steep: slope 2"),
                          (2, 4, "Line 2 crosses at 4 and falls: slope -1"),
                          (3, 2, "Line 3 crosses at 2 and rises gently: slope 1/2")]:
            focus([n])
            d = Dot(P(0, b), color=YELLOW, radius=0.09)
            nt = note(txt)
            self.play(FadeIn(d, scale=2), FadeIn(nt, shift=UP * 0.2)); reveal(n); self.wait(1.2)
            self.play(FadeOut(nt), FadeOut(d))
        self.play(*[lines[k].animate.set_stroke(width=5, opacity=1) for k in lines])
        self.wait(1)
        ban = Text("All six lines labeled", font_size=32, color=ANSWER)
        box = SurroundingRectangle(ban, color=YELLOW, buff=0.2)
        VGroup(ban, box).move_to(RIGHT * CX + DOWN * 3.1)
        self.play(FadeIn(ban, shift=UP * 0.2), Create(box))
        self.wait(3)
