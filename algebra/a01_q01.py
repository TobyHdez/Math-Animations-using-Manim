from alg_common import *


class Q01(Scene):
    """T = Pr + Pn  ->  solve for P."""

    def construct(self):
        q_card(self, 1)
        title = atitle(1, "Rearrange the Formula for P")
        self.play(Write(title))

        eq0 = aeq("T", "=", "P", "r", "+", "P", "n")
        self.play(Write(eq0))
        cap = acap("Step 1: Factor out P")
        self.play(FadeIn(cap, shift=UP * 0.2))
        hint = Text("P is in BOTH terms", font_size=28, color=GIVEN).move_to(DOWN * 0.7)
        self.play(FadeIn(hint, shift=UP * 0.2),
                  eq0[2].animate.set_color(YELLOW), eq0[5].animate.set_color(YELLOW))
        self.play(Indicate(eq0[2], color=YELLOW), Indicate(eq0[5], color=YELLOW))
        self.wait(1)
        eq1 = aeq("T", "=", "P", "(r+n)")
        eq1[2].set_color(YELLOW)
        self.play(FadeOut(hint), TransformMatchingTex(eq0, eq1))
        self.wait(1.5)

        cap = next_cap(self, cap, "Step 2: Divide both sides by (r + n)")
        eq = op_step(self, eq1, ops=("\\div (r+n)", "\\div (r+n)"), under=([0], [2, 3]),
                     mid=aeq("{T", "\\over", "r+n}", "=", "{P", "(r+n)", "\\over", "r+n}"),
                     cancel=[5, 7],
                     result=aeq("P", "=", "{T", "\\over", "r+n}"))
        self.play(eq[0].animate.set_color(ANSWER))
        self.wait(1)

        self.play(FadeOut(eq))
        cap, grp = check_step(self, cap, [
            "r = 2,\\ n = 3,\\ P = 4:\\quad T = 4(2) + 4(3) = 20",
            "P = \\dfrac{20}{2 + 3} = 4 \\ \\checkmark",
        ])
        a_banner(self, "Answer: A   P = T / (r + n)")
        self.wait(3)
