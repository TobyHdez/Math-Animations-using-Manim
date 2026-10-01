from alg_common import *


class Q09(Scene):
    """3(x + 5) + 4x = 20 -- what is the first step?"""

    def construct(self):
        q_card(self, 9)
        self.play(Write(atitle(9, "What Is the First Step?")))

        eq0 = aeq("3", "(x", "+5)", "+4x", "=", "20")
        self.play(Write(eq0))
        cap = acap("Step 1: Spot the parentheses")
        self.play(FadeIn(cap, shift=UP * 0.2))
        hint = Text("Clear the parentheses first:", font_size=28, color=GIVEN).move_to(DOWN * 0.5)
        hint2 = Text("multiply 3 times EVERY term inside.", font_size=28, color=GIVEN).next_to(hint, DOWN, buff=0.25)
        self.play(FadeIn(hint, shift=UP * 0.2), FadeIn(hint2, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(hint), FadeOut(hint2))

        cap = next_cap(self, cap, "Step 2: Distribute the 3")
        eq = distribute(self, eq0, 0, [1, 2], ["3 \\cdot x = 3x", "3 \\cdot 5 = 15"],
                        aeq("3x", "+15", "+4x", "=", "20"))
        self.play(eq.animate.set_color(ANSWER))
        self.wait(1)
        self.play(eq.animate.set_color(WHITE).shift(UP * 1.2).scale(0.8))

        cap = next_cap(self, cap, "Step 3: Match the answer choices")
        rows = VGroup(
            VGroup(MathTex("A.\\ 3x + 15 + 4x = 20"), MathTex("\\checkmark", color=GREEN)),
            VGroup(MathTex("B.\\ 3x + 5 + 4x = 20"), MathTex("\\times", color=RED), Text("forgot to multiply the 5", font_size=24, color=GREY_B)),
            VGroup(MathTex("C.\\ 3x + 15 = 5"), MathTex("\\times", color=RED), Text("lost the 4x and the 20", font_size=24, color=GREY_B)),
            VGroup(MathTex("D.\\ 7x = 5"), MathTex("\\times", color=RED), Text("skipped distributing", font_size=24, color=GREY_B)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.35)
        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(DOWN * 0.05)
        rows[0][0].set_color(ANSWER)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(0.6)
        self.wait(1.5)
        self.play(FadeOut(rows), FadeOut(eq))
        a_banner(self, "Answer: A   3x + 15 + 4x = 20")
        self.wait(3)
