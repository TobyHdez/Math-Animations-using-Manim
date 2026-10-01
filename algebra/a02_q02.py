from alg_common import *


class Q02(Scene):
    """V = (1/3)Bh  ->  solve for h."""

    def construct(self):
        q_card(self, 2)
        title = atitle(2, "Rearrange the Formula for h")
        self.play(Write(title))

        eq0 = aeq("V", "=", "\\frac{1}{3}", "B", "h")
        self.play(Write(eq0))
        cap = acap("Step 1: Multiply both sides by 3")
        self.play(FadeIn(cap, shift=UP * 0.2))
        eq = op_step(self, eq0, ops=("\\cdot 3", "\\cdot 3"), under=([0], [2, 3, 4]),
                     mid=aeq("V", "\\cdot 3", "=", "\\frac{1}{3}", "B", "h", "\\cdot 3"),
                     mapping=[(0, 0), (1, 2), (2, 3), (3, 4), (4, 5)], op_idx=(1, 6),
                     cancel=[3, 6],
                     result=aeq("3V", "=", "B", "h"))

        cap = next_cap(self, cap, "Step 2: Divide both sides by B")
        eq = op_step(self, eq, ops=("\\div B", "\\div B"), under=([0], [2, 3]),
                     mid=aeq("{3V", "\\over", "B}", "=", "{B", "h", "\\over", "B}"),
                     cancel=[4, 7],
                     result=aeq("h", "=", "{3V", "\\over", "B}"))
        self.play(eq[0].animate.set_color(ANSWER))
        self.wait(1)

        self.play(FadeOut(eq))
        cap, grp = check_step(self, cap, [
            "B = 6,\\ h = 5:\\quad V = \\tfrac{1}{3}(6)(5) = 10",
            "h = \\dfrac{3(10)}{6} = 5 \\ \\checkmark",
        ])
        a_banner(self, "Answer: A   h = 3V / B")
        self.wait(3)
