from alg_common import *


class Q24(Scene):
    """Which point lies on y = -3x + 8?  Choices (2,2) (2,14) (-2,2) (3,8)."""

    def construct(self):
        q_card(self, 24)
        self.play(Write(make_title("Question 24: Is the Point on the Line?")))

        plane = NumberPlane(
            x_range=[-4, 6, 1], y_range=[-2, 16, 2], x_length=4.6, y_length=5.2,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.2, "stroke_opacity": 0.3},
            axis_config={"stroke_color": WHITE, "stroke_width": 2.5},
        ).move_to(LEFT * 4.2 + DOWN * 0.4)
        P = plane.c2p
        nums = VGroup()
        for v in (-2, 2, 4):
            nums.add(MathTex(str(v)).scale(0.4).next_to(P(v, 0), DOWN, buff=0.06))
        for v in (4, 8, 12, 16):
            nums.add(MathTex(str(v)).scale(0.4).next_to(P(0, v), LEFT, buff=0.06))
        line = Line(P(-2, 14), P(10 / 3, -2), color=RED_C, stroke_width=6)
        self.play(FadeIn(plane), FadeIn(nums))
        self.play(Create(line))
        eq_lab = MathTex("y = -3x + 8", color=RED_C).scale(0.75).add_background_rectangle(BLACK, opacity=0.85, buff=0.05)
        eq_lab.next_to(P(0.5, 9.8), RIGHT, buff=0.1)
        self.play(FadeIn(eq_lab))

        pts = {"A": (2, 2), "B": (2, 14), "C": (-2, 2), "D": (3, 8)}
        dots = {k: Dot(P(*v), color=YELLOW, radius=0.09) for k, v in pts.items()}
        labs = {}
        dirs = {"A": DR, "B": UR, "C": DL, "D": UR}
        for k, v in pts.items():
            m = MathTex(f"{k}({v[0]},{v[1]})", color=YELLOW).scale(0.6).add_background_rectangle(BLACK, opacity=0.85, buff=0.04)
            labs[k] = m.next_to(dots[k], dirs[k], buff=0.08)
        self.play(*[FadeIn(dots[k], scale=2) for k in dots], *[FadeIn(labs[k]) for k in labs])

        cap = caption("Step 1: Plug each x into the equation")
        self.play(FadeIn(cap, shift=UP * 0.2))
        idea = Text("A point is on the line if its y matches.", font_size=26, color=GIVEN).move_to(EQ_POS + UP * 1.4)
        self.play(FadeIn(idea, shift=DOWN * 0.2))

        rows = [
            ("A", "y = -3(2) + 8 = 2", "2 = 2", True),
            ("B", "y = -3(2) + 8 = 2", "14 \\ne 2", False),
            ("C", "y = -3(-2) + 8 = 14", "2 \\ne 14", False),
            ("D", "y = -3(3) + 8 = -1", "8 \\ne -1", False),
        ]
        shown = VGroup()
        y0 = EQ_POS[1] + 0.6
        for i, (k, calc, cmpr, ok) in enumerate(rows):
            col = GREEN if ok else RED
            r = VGroup(MathTex(f"{k}:", color=YELLOW), MathTex(calc), MathTex(cmpr, color=col),
                       MathTex("\\checkmark" if ok else "\\times", color=col)).arrange(RIGHT, buff=0.25)
            r.scale(0.8).move_to([EQ_POS[0], y0 - i * 0.75, 0])
            r.align_to([EQ_POS[0] - 3.0, 0, 0], LEFT)
            self.play(Indicate(dots[k], color=col, scale_factor=2.2), FadeIn(r, shift=RIGHT * 0.2), run_time=1.1)
            self.wait(0.6)
            shown.add(r)
            if not ok:
                self.play(dots[k].animate.set_color(GREY_B), run_time=0.4)
        self.play(dots["A"].animate.set_color(GREEN), Indicate(dots["A"], color=GREEN, scale_factor=2.5))
        self.wait(2)
        self.play(FadeOut(idea))
        ban = Text("Answer: A   (2, 2)", font_size=32, color=ANSWER)
        box = SurroundingRectangle(ban, color=YELLOW, buff=0.2)
        VGroup(ban, box).move_to(RIGHT * CX + DOWN * 3.1)
        self.play(FadeIn(ban, shift=UP * 0.2), Create(box))
        self.wait(3)
