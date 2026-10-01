from alg_common import *


class Q03(Scene):
    """5y = (a - c) / (6b)  ->  solve for a."""

    def construct(self):
        q_card(self, 3)
        title = atitle(3, "Solve for a")
        self.play(Write(title))

        eq0 = aeq("5y", "=", "{a-c", "\\over", "6b}")
        self.play(Write(eq0))
        cap = acap("Step 1: Multiply both sides by 6b")
        self.play(FadeIn(cap, shift=UP * 0.2))
        hint = Text("This clears the fraction", font_size=28, color=GIVEN).move_to(DOWN * 0.8)
        self.play(FadeIn(hint, shift=UP * 0.2))
        self.wait(1)
        self.play(FadeOut(hint))
        eq = op_step(self, eq0, ops=("\\cdot 6b", "\\cdot 6b"), under=([0], [2, 3, 4]),
                     mid=aeq("5y", "\\cdot 6b", "=", "{a-c", "\\over", "6b}", "\\cdot 6b"),
                     mapping=[(0, 0), (1, 2), (2, 3), (3, 4), (4, 5)], op_idx=(1, 6),
                     cancel=[5, 6], combine=([0, 1], "5y \\cdot 6b = 30by"),
                     result=aeq("30by", "=", "a", "-c"))

        cap = next_cap(self, cap, "Step 2: Add c to both sides")
        eq = op_step(self, eq, ops=("+c", "+c"), under=([0], [2, 3]),
                     mid=aeq("30by", "+c", "=", "a", "{}-c", "+c"),
                     mapping=[(0, 0), (1, 2), (2, 3), (3, 4)], op_idx=(1, 5),
                     cancel=[4, 5],
                     result=aeq("a", "=", "30by", "+c"))
        self.play(eq[0].animate.set_color(ANSWER))
        self.wait(1)

        self.play(FadeOut(eq))
        cap, grp = check_step(self, cap, [
            "b = 2,\\ c = 1,\\ y = 1:\\quad a = 30(2)(1) + 1 = 61",
            "\\dfrac{61 - 1}{6(2)} = 5 = 5y \\ \\checkmark",
        ])
        a_banner(self, "Answer: A   a = 30by + c")
        self.wait(3)
