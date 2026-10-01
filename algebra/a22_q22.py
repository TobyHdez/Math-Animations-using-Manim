from alg_common import *


class Q22(Scene):
    """9 - |2x - 5| = 4."""

    def construct(self):
        q_card(self, 22)
        self.play(Write(atitle(22, "Absolute Value Equation")))

        eq0 = aeq("9", "-|2x-5|", "=", "4")
        self.play(Write(eq0))
        cap = acap("Step 1: Subtract 9 from both sides")
        self.play(FadeIn(cap, shift=UP * 0.2))
        eq = op_step(self, eq0, ops=("-9", "-9"), under=([0, 1], [3]),
                     mid=aeq("{}9", "-|2x-5|", "-9", "=", "4", "-9"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[0, 2], combine=([4, 5], "4 - 9 = -5"),
                     result=aeq("-|2x-5|", "=", "-5"))

        cap = next_cap(self, cap, "Step 2: Multiply both sides by -1")
        hint = Text("The absolute value must be positive.", font_size=28, color=GIVEN).move_to(DOWN * 0.8)
        self.play(FadeIn(hint, shift=UP * 0.2))
        self.wait(1)
        self.play(FadeOut(hint))
        eq = op_step_n(self, eq, ops=["\\cdot(-1)", "\\cdot(-1)"], under=[[0], [2]],
                       mid=aeq("-|2x-5|", "\\cdot(-1)", "=", "-5", "\\cdot(-1)"),
                       mapping=[(0, 0), (1, 2), (2, 3)], op_idx=[1, 4],
                       combine=[([0, 1], "\\text{(-)(-) = +}"), ([3, 4], "-5 \\cdot (-1) = 5")],
                       result=aeq("|2x-5|", "=", "5"))

        cap = next_cap(self, cap, "Step 3: Split into two cases")
        t = Text("The inside can equal 5 OR -5", font_size=28, color=GIVEN).move_to(UP * 2.2)
        self.play(FadeIn(t, shift=DOWN * 0.2))
        c1 = aeq("2x", "-5", "=", "5", scale=1.1).move_to(UP * 0.5 + LEFT * 3.5)
        c2 = aeq("2x", "-5", "=", "-5", scale=1.1).move_to(UP * 0.5 + RIGHT * 3.5)
        l1 = Text("Case 1", font_size=26, color=GREEN).next_to(c1, UP, buff=0.9)
        l2 = Text("Case 2", font_size=26, color=ORANGE).next_to(c2, UP, buff=0.9)
        self.play(ReplacementTransform(eq.copy(), c1), ReplacementTransform(eq, c2), FadeIn(l1), FadeIn(l2))
        self.wait(1.5)

        cap = next_cap(self, cap, "Step 4: Add 5 to both sides")
        c1 = op_step(self, c1, ops=("+5", "+5"), under=([0, 1], [3]),
                     mid=aeq("2x", "{}-5", "+5", "=", "5", "+5", scale=1.1),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[1, 2], combine=([4, 5], "5 + 5 = 10"),
                     result=aeq("2x", "=", "10", scale=1.1))
        c2 = op_step(self, c2, ops=("+5", "+5"), under=([0, 1], [3]),
                     mid=aeq("2x", "{}-5", "+5", "=", "-5", "+5", scale=1.1),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[1, 2], combine=([4, 5], "-5 + 5 = 0"),
                     result=aeq("2x", "=", "0", scale=1.1))

        cap = next_cap(self, cap, "Step 5: Divide both sides by 2")
        c1 = op_step(self, c1, ops=("\\div 2", "\\div 2"), under=([0], [2]),
                     mid=aeq("{2x", "\\over", "2}", "=", "{10", "\\over", "2}", scale=1.1),
                     combine=([4, 5, 6], "10 \\div 2 = 5"),
                     result=aeq("x", "=", "5", scale=1.1))
        c2 = op_step(self, c2, ops=("\\div 2", "\\div 2"), under=([0], [2]),
                     mid=aeq("{2x", "\\over", "2}", "=", "{0", "\\over", "2}", scale=1.1),
                     combine=([4, 5, 6], "0 \\div 2 = 0"),
                     result=aeq("x", "=", "0", scale=1.1))
        self.play(c1.animate.set_color(ANSWER), c2.animate.set_color(ANSWER))
        self.wait(1.5)

        self.play(FadeOut(VGroup(c1, c2, l1, l2, t)))
        cap, grp = check_step(self, cap, [
            "x = 5:\\quad 9 - |2(5) - 5| = 9 - 5 = 4 \\ \\checkmark",
            "x = 0:\\quad 9 - |2(0) - 5| = 9 - 5 = 4 \\ \\checkmark",
        ])
        a_banner(self, "Answer: x = 0 or x = 5")
        self.wait(3)
