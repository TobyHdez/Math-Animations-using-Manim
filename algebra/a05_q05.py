from alg_common import *


class Q05(Scene):
    """0.4x = 0.9x + 15."""

    def construct(self):
        q_card(self, 5)
        title = atitle(5, "Solve for x")
        self.play(Write(title))

        eq0 = aeq("0.4x", "=", "0.9x", "+15")
        self.play(Write(eq0))
        cap = acap("Step 1: Subtract 0.9x from both sides")
        self.play(FadeIn(cap, shift=UP * 0.2))
        hint = Text("Get the x-terms on one side", font_size=28, color=GIVEN).move_to(DOWN * 0.8)
        self.play(FadeIn(hint, shift=UP * 0.2))
        self.wait(1)
        self.play(FadeOut(hint))
        eq = op_step(self, eq0, ops=("-0.9x", "-0.9x"), under=([0], [2, 3]),
                     mid=aeq("0.4x", "-0.9x", "=", "{}0.9x", "+15", "-0.9x"),
                     mapping=[(0, 0), (1, 2), (2, 3), (3, 4)], op_idx=(1, 5),
                     cancel=[3, 5], combine=([0, 1], "0.4x - 0.9x = -0.5x"),
                     result=aeq("-0.5x", "=", "15"))

        cap = next_cap(self, cap, "Step 2: Divide both sides by -0.5")
        eq = op_step(self, eq, ops=("\\div (-0.5)", "\\div (-0.5)"), under=([0], [2]),
                     mid=aeq("{-0.5x", "\\over", "-0.5}", "=", "{15", "\\over", "-0.5}"),
                     combine=([4, 5, 6], "15 \\div (-0.5) = -30"),
                     result=aeq("x", "=", "-30"))
        self.play(eq[2].animate.set_color(ANSWER))
        self.wait(1)

        self.play(FadeOut(eq))
        cap, grp = check_step(self, cap, [
            "0.4(-30) = -12",
            "0.9(-30) + 15 = -27 + 15 = -12 \\ \\checkmark",
        ])
        a_banner(self, "Answer: A   x = -30")
        self.wait(3)
