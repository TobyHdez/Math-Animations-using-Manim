from alg_common import *


class Q28(Scene):
    """V-shaped graph with vertex at the origin: which equation?"""

    def construct(self):
        q_card(self, 28)
        self.play(Write(make_title("Question 28: Match the Graph to an Equation")))

        plane = NumberPlane(
            x_range=[-6, 6, 2], y_range=[-1, 8, 2], x_length=5.4, y_length=4.05,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.2, "stroke_opacity": 0.3},
            axis_config={"stroke_color": WHITE, "stroke_width": 2.5},
        ).move_to(LEFT * 3.9 + DOWN * 0.3)
        P = plane.c2p
        nums = VGroup()
        for v in (-4, -2, 2, 4):
            nums.add(MathTex(str(v)).scale(0.4).next_to(P(v, 0), DOWN, buff=0.06))
        for v in (2, 4, 6):
            nums.add(MathTex(str(v)).scale(0.4).next_to(P(0, v), LEFT, buff=0.06))
        graph = VGroup(Line(P(-6, 6), P(0, 0)), Line(P(0, 0), P(6, 6))).set_color(GREEN).set_stroke(width=6)
        self.play(FadeIn(plane), FadeIn(nums))
        self.play(Create(graph))

        cap = caption("Step 1: Read points off the graph")
        self.play(FadeIn(cap, shift=UP * 0.2))
        xs = [-4, -2, 0, 2, 4]
        dots = VGroup(*[Dot(P(x, abs(x)), color=YELLOW, radius=0.08) for x in xs])
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.2))
        tab = VGroup(
            VGroup(Text("x", font_size=28), *[MathTex(str(x)) for x in xs]).arrange(RIGHT, buff=0.55),
            VGroup(Text("y", font_size=28), *[MathTex(str(abs(x)), color=YELLOW) for x in xs]).arrange(RIGHT, buff=0.55),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(EQ_POS + UP * 0.6)
        for r in tab:
            for i, m in enumerate(r[1:]):
                m.move_to([tab[0][i + 1].get_x(), m.get_y(), 0])
        self.play(Write(tab))
        self.wait(1.5)

        new_cap = caption("Step 2: Spot the pattern")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        p1 = Text("x and -x give the SAME y:", font_size=28, color=GIVEN).move_to(EQ_POS + DOWN * 0.7)
        p2 = Text("a mirror image across the y-axis", font_size=28, color=GIVEN).next_to(p1, DOWN, buff=0.25)
        mirror = DashedLine(P(0, 0), P(0, 7), color=MIRROR_C if False else PURPLE_B, stroke_width=4)
        self.play(FadeIn(p1, shift=UP * 0.2), Create(mirror))
        self.play(FadeIn(p2, shift=UP * 0.2))
        self.play(TransformFromCopy(dots[0], dots[4].copy()), run_time=0.01)
        self.wait(1.5)
        self.play(FadeOut(p1), FadeOut(p2), FadeOut(tab), FadeOut(mirror))

        new_cap = caption("Step 3: Test each answer choice")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        rows = VGroup(
            VGroup(MathTex("A.\\ y = x"), Text("x = -4 gives -4", font_size=24, color=GREY_B), MathTex("\\times", color=RED)),
            VGroup(MathTex("B.\\ y = |x|"), Text("x = -4 gives 4", font_size=24, color=GREEN), MathTex("\\checkmark", color=GREEN)),
            VGroup(MathTex("C.\\ y = x^2"), Text("x = 4 gives 16, not 4", font_size=24, color=GREY_B), MathTex("\\times", color=RED)),
            VGroup(MathTex("D.\\ y = \\sqrt{x}"), Text("no negative x at all", font_size=24, color=GREY_B), MathTex("\\times", color=RED)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.3)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(EQ_POS + UP * 0.1)
        rows[1][0].set_color(ANSWER)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(0.5)
        self.wait(1.5)
        ban = Text("Answer: B   y = |x|", font_size=32, color=ANSWER)
        box = SurroundingRectangle(ban, color=YELLOW, buff=0.2)
        VGroup(ban, box).move_to(RIGHT * CX + DOWN * 3.1)
        self.play(FadeIn(ban, shift=UP * 0.2), Create(box))
        self.wait(3)
