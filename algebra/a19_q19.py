from alg_common import *


class Q19(Scene):
    """|x| = 11."""

    def construct(self):
        q_card(self, 19)
        self.play(Write(atitle(19, "Absolute Value Equation")))

        eq0 = aeq("|x|", "=", "11")
        self.play(Write(eq0))
        cap = acap("Step 1: Absolute value = distance from 0")
        self.play(FadeIn(cap, shift=UP * 0.2))
        t = Text("|x| = 11 means: x is 11 units away from 0.", font_size=28, color=GIVEN).move_to(DOWN * 0.7)
        self.play(FadeIn(t, shift=UP * 0.2))
        self.wait(1.5)
        self.play(eq0.animate.scale(0.7).move_to(UP * 2.3), FadeOut(t))

        nl = NumberLine(x_range=[-14, 14, 2], length=11.5, include_numbers=True, font_size=22).move_to(DOWN * 0.3)
        self.play(Create(nl))
        zero = closed_circle(nl.n2p(0), color=WHITE, r=0.12)
        z_lab = Text("0", font_size=26).next_to(zero, UP, buff=0.3)
        self.play(FadeIn(zero, scale=2), FadeIn(z_lab))

        cap = next_cap(self, cap, "Step 2: Go 11 units right")
        right = Arrow(nl.n2p(0), nl.n2p(11), color=GREEN, buff=0, stroke_width=8)
        r_lab = Text("11 units", font_size=26, color=GREEN).next_to(right, UP, buff=0.3)
        d11 = closed_circle(nl.n2p(11), color=YELLOW)
        self.play(Create(right), FadeIn(r_lab))
        self.play(FadeIn(d11, scale=2))
        x1 = MathTex("x = 11", color=YELLOW).next_to(d11, UP, buff=1.0)
        self.play(FadeIn(x1, shift=DOWN * 0.2))
        self.wait(1)

        cap = next_cap(self, cap, "Step 3: Go 11 units left")
        left = Arrow(nl.n2p(0), nl.n2p(-11), color=ORANGE, buff=0, stroke_width=8)
        l_lab = Text("11 units", font_size=26, color=ORANGE).next_to(left, DOWN, buff=0.5)
        dm11 = closed_circle(nl.n2p(-11), color=YELLOW)
        self.play(Create(left), FadeIn(l_lab))
        self.play(FadeIn(dm11, scale=2))
        x2 = MathTex("x = -11", color=YELLOW).next_to(dm11, UP, buff=1.0)
        self.play(FadeIn(x2, shift=DOWN * 0.2))
        self.wait(1.5)

        cap = next_cap(self, cap, "Step 4: Both distances equal 11")
        chk = VGroup(MathTex("|11| = 11 \\ \\checkmark"), MathTex("|-11| = 11 \\ \\checkmark")).arrange(RIGHT, buff=1.2)
        chk.move_to(DOWN * 2.6 + LEFT * 0.0)
        chk.set_color(ANSWER)
        self.play(FadeIn(chk, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(VGroup(nl, zero, z_lab, right, r_lab, d11, x1, left, l_lab, dm11, x2, chk, eq0)))

        rows = VGroup(
            VGroup(MathTex("A.\\ x = 11 \\text{ or } x = -11"), MathTex("\\checkmark", color=GREEN)),
            VGroup(MathTex("B.\\ x = 11 \\text{ only}"), MathTex("\\times", color=RED), Text("misses -11", font_size=24, color=GREY_B)),
            VGroup(MathTex("C.\\ x = -11 \\text{ only}"), MathTex("\\times", color=RED), Text("misses 11", font_size=24, color=GREY_B)),
            VGroup(MathTex("D.\\ \\text{no solution}"), MathTex("\\times", color=RED), Text("distance 11 exists", font_size=24, color=GREY_B)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.35)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(UP * 0.4)
        rows[0][0].set_color(ANSWER)
        cap = next_cap(self, cap, "Match the answer choices")
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(0.5)
        self.wait(1.5)
        self.play(FadeOut(rows))
        a_banner(self, "Answer: A   x = 11 or x = -11")
        self.wait(3)
