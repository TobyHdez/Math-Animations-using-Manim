from alg_common import *


class Q30(Scene):
    """Table of an absolute value function: x -3 -1 0 1 3 / f(x) 7 3 1 3 7 -> vertex."""

    def construct(self):
        q_card(self, 30)
        self.play(Write(make_title("Question 30: Vertex From a Table")))

        xs = [-3, -1, 0, 1, 3]
        ys = [7, 3, 1, 3, 7]
        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-1, 9, 2], x_length=5.2, y_length=4.6,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.2, "stroke_opacity": 0.3},
            axis_config={"stroke_color": WHITE, "stroke_width": 2.5},
        ).move_to(LEFT * 3.9 + DOWN * 0.3)
        P = plane.c2p
        nums = VGroup()
        for v in (-3, -2, -1, 1, 2, 3):
            nums.add(MathTex(str(v)).scale(0.4).next_to(P(v, 0), DOWN, buff=0.06))
        for v in (2, 4, 6, 8):
            nums.add(MathTex(str(v)).scale(0.4).next_to(P(0, v), LEFT, buff=0.06))
        self.play(FadeIn(plane), FadeIn(nums))

        # Step 1: table + plot
        cap = caption("Step 1: Plot the table")
        self.play(FadeIn(cap, shift=UP * 0.2))
        tab = VGroup(
            VGroup(MathTex("x"), *[MathTex(str(x)) for x in xs]).arrange(RIGHT, buff=0.5),
            VGroup(MathTex("f(x)"), *[MathTex(str(y), color=YELLOW) for y in ys]).arrange(RIGHT, buff=0.5),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(EQ_POS + UP * 0.9)
        for r in tab:
            for i, m in enumerate(r[1:]):
                m.move_to([tab[0][i + 1].get_x(), m.get_y(), 0])
            r[0].next_to(r[1], LEFT, buff=0.55)
        self.play(Write(tab))
        dots = VGroup(*[Dot(P(x, y), color=YELLOW, radius=0.08) for x, y in zip(xs, ys)])
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.2))
        vee = VGroup(Line(P(-3, 7), P(0, 1)), Line(P(0, 1), P(3, 7))).set_color(RED_C).set_stroke(width=5)
        self.play(Create(vee))
        self.wait(1)

        # Step 2: lowest output
        new_cap = caption("Step 2: Find the lowest output")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        low_box = SurroundingRectangle(VGroup(tab[0][3], tab[1][3]), color=GREEN, buff=0.12)
        t = Text("Smallest f(x) is 1, at x = 0", font_size=28, color=GREEN).move_to(EQ_POS + DOWN * 0.5)
        self.play(Create(low_box), FadeIn(t, shift=UP * 0.2), Indicate(dots[2], color=GREEN, scale_factor=2.5))
        self.wait(1.5)

        # Step 3: symmetry
        new_cap = caption("Step 3: Check the mirror image")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        mirror = DashedLine(P(0, -0.5), P(0, 9), color=PURPLE_B, stroke_width=4)
        s1 = Text("f(-1) = f(1) = 3   and   f(-3) = f(3) = 7", font_size=26, color=GIVEN).move_to(EQ_POS + DOWN * 1.25)
        self.play(Create(mirror), FadeIn(s1, shift=UP * 0.2))
        self.wait(2)
        vtx = MathTex("\\text{vertex} = (0,\\ 1)", color=ANSWER).scale(1.1).move_to(EQ_POS + DOWN * 0.5)
        vdot = Dot(P(0, 1), color=ANSWER, radius=0.13)
        self.play(FadeOut(t), FadeOut(s1), FadeOut(low_box), FadeOut(tab), FadeOut(mirror), FadeIn(vdot, scale=3), Write(vtx))
        self.wait(1.5)

        # Step 4: choices
        new_cap = caption("Step 4: Match the answer choices")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        self.play(FadeOut(vtx))
        rows = VGroup(
            VGroup(MathTex("A.\\ (0,\\ 1)"), MathTex("\\checkmark", color=GREEN)),
            VGroup(MathTex("B.\\ (1,\\ 0)"), MathTex("\\times", color=RED), Text("x and y swapped", font_size=24, color=GREY_B)),
            VGroup(MathTex("C.\\ (0,\\ 3)"), MathTex("\\times", color=RED), Text("f(0) is 1, not 3", font_size=24, color=GREY_B)),
            VGroup(MathTex("D.\\ (-3,\\ 7)"), MathTex("\\times", color=RED), Text("an end point, not the tip", font_size=24, color=GREY_B)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.3)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(EQ_POS + UP * 0.2)
        rows[0][0].set_color(ANSWER)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(0.5)
        self.wait(1.5)
        ban = Text("Answer: A   (0, 1)", font_size=32, color=ANSWER)
        box = SurroundingRectangle(ban, color=YELLOW, buff=0.2)
        VGroup(ban, box).move_to(RIGHT * CX + DOWN * 3.1)
        self.play(FadeIn(ban, shift=UP * 0.2), Create(box))
        self.wait(3)
