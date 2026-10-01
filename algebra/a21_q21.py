from alg_common import *


class Q21(Scene):
    """|4 - 2x| + 6 = 14."""

    def construct(self):
        q_card(self, 21)
        self.play(Write(atitle(21, "Absolute Value Equation")))

        eq0 = aeq("|4-2x|", "+6", "=", "14")
        self.play(Write(eq0))
        cap = acap("Step 1: Get the absolute value alone")
        self.play(FadeIn(cap, shift=UP * 0.2))
        eq = op_step(self, eq0, ops=("-6", "-6"), under=([0, 1], [3]),
                     mid=aeq("|4-2x|", "+6", "-6", "=", "14", "-6"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[1, 2], combine=([4, 5], "14 - 6 = 8"),
                     result=aeq("|4-2x|", "=", "8"))

        cap = next_cap(self, cap, "Step 2: Split into two cases")
        t = Text("The inside can equal 8 OR -8", font_size=28, color=GIVEN).move_to(UP * 2.2)
        self.play(FadeIn(t, shift=DOWN * 0.2))
        c1 = aeq("4", "-2x", "=", "8", scale=1.1).move_to(UP * 0.5 + LEFT * 3.5)
        c2 = aeq("4", "-2x", "=", "-8", scale=1.1).move_to(UP * 0.5 + RIGHT * 3.5)
        l1 = Text("Case 1", font_size=26, color=GREEN).next_to(c1, UP, buff=0.9)
        l2 = Text("Case 2", font_size=26, color=ORANGE).next_to(c2, UP, buff=0.9)
        self.play(ReplacementTransform(eq.copy(), c1), ReplacementTransform(eq, c2), FadeIn(l1), FadeIn(l2))
        self.wait(1.5)

        cap = next_cap(self, cap, "Step 3: Subtract 4 from both sides")
        c1 = op_step(self, c1, ops=("-4", "-4"), under=([0, 1], [3]),
                     mid=aeq("{}4", "-2x", "-4", "=", "8", "-4", scale=1.1),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[0, 2], combine=([4, 5], "8 - 4 = 4"),
                     result=aeq("-2x", "=", "4", scale=1.1))
        c2 = op_step(self, c2, ops=("-4", "-4"), under=([0, 1], [3]),
                     mid=aeq("{}4", "-2x", "-4", "=", "-8", "-4", scale=1.1),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[0, 2], combine=([4, 5], "-8 - 4 = -12"),
                     result=aeq("-2x", "=", "-12", scale=1.1))

        cap = next_cap(self, cap, "Step 4: Divide both sides by -2")
        c1 = op_step(self, c1, ops=("\\div(-2)", "\\div(-2)"), under=([0], [2]),
                     mid=aeq("{-2x", "\\over", "-2}", "=", "{4", "\\over", "-2}", scale=1.1),
                     combine=([4, 5, 6], "4 \\div (-2) = -2"),
                     result=aeq("x", "=", "-2", scale=1.1))
        c2 = op_step(self, c2, ops=("\\div(-2)", "\\div(-2)"), under=([0], [2]),
                     mid=aeq("{-2x", "\\over", "-2}", "=", "{-12", "\\over", "-2}", scale=1.1),
                     combine=([4, 5, 6], "-12 \\div (-2) = 6"),
                     result=aeq("x", "=", "6", scale=1.1))
        self.play(c1.animate.set_color(ANSWER), c2.animate.set_color(ANSWER))
        self.wait(1.5)

        self.play(FadeOut(VGroup(c1, c2, l1, l2, t)))
        cap, grp = check_step(self, cap, [
            "x = -2:\\quad |4 - 2(-2)| + 6 = |8| + 6 = 14 \\ \\checkmark",
            "x = 6:\\quad |4 - 2(6)| + 6 = |-8| + 6 = 14 \\ \\checkmark",
        ])
        a_banner(self, "Answer: A   x = -2 or x = 6")
        self.wait(3)
