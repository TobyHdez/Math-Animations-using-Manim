from alg_common import *


class Q23(Scene):
    """|5x - 8| = 3."""

    def construct(self):
        q_card(self, 23)
        self.play(Write(atitle(23, "Absolute Value Equation")))

        eq0 = aeq("|5x-8|", "=", "3")
        self.play(Write(eq0))
        cap = acap("Step 1: The absolute value is already alone")
        self.play(FadeIn(cap, shift=UP * 0.2))
        self.wait(1.5)

        cap = next_cap(self, cap, "Step 2: Split into two cases")
        t = Text("The inside can equal 3 OR -3", font_size=28, color=GIVEN).move_to(UP * 2.2)
        self.play(FadeIn(t, shift=DOWN * 0.2))
        c1 = aeq("5x", "-8", "=", "3", scale=1.1).move_to(UP * 0.5 + LEFT * 3.5)
        c2 = aeq("5x", "-8", "=", "-3", scale=1.1).move_to(UP * 0.5 + RIGHT * 3.5)
        l1 = Text("Case 1", font_size=26, color=GREEN).next_to(c1, UP, buff=0.9)
        l2 = Text("Case 2", font_size=26, color=ORANGE).next_to(c2, UP, buff=0.9)
        self.play(ReplacementTransform(eq0.copy(), c1), ReplacementTransform(eq0, c2), FadeIn(l1), FadeIn(l2))
        self.wait(1.5)

        cap = next_cap(self, cap, "Step 3: Add 8 to both sides")
        c1 = op_step(self, c1, ops=("+8", "+8"), under=([0, 1], [3]),
                     mid=aeq("5x", "{}-8", "+8", "=", "3", "+8", scale=1.1),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[1, 2], combine=([4, 5], "3 + 8 = 11"),
                     result=aeq("5x", "=", "11", scale=1.1))
        c2 = op_step(self, c2, ops=("+8", "+8"), under=([0, 1], [3]),
                     mid=aeq("5x", "{}-8", "+8", "=", "-3", "+8", scale=1.1),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[1, 2], combine=([4, 5], "-3 + 8 = 5"),
                     result=aeq("5x", "=", "5", scale=1.1))

        cap = next_cap(self, cap, "Step 4: Divide both sides by 5")
        c1 = op_step(self, c1, ops=("\\div 5", "\\div 5"), under=([0], [2]),
                     mid=aeq("{5x", "\\over", "5}", "=", "{11", "\\over", "5}", scale=1.1),
                     result=aeq("x", "=", "{11", "\\over", "5}", scale=1.1))
        c2 = op_step(self, c2, ops=("\\div 5", "\\div 5"), under=([0], [2]),
                     mid=aeq("{5x", "\\over", "5}", "=", "{5", "\\over", "5}", scale=1.1),
                     combine=([4, 5, 6], "5 \\div 5 = 1"),
                     result=aeq("x", "=", "1", scale=1.1))
        self.play(c1.animate.set_color(ANSWER), c2.animate.set_color(ANSWER))
        self.wait(1.5)

        self.play(FadeOut(VGroup(c1, c2, l1, l2, t)))
        cap, grp = check_step(self, cap, [
            "x = \\tfrac{11}{5}:\\quad |5 \\cdot \\tfrac{11}{5} - 8| = |11 - 8| = 3 \\ \\checkmark",
            "x = 1:\\quad |5(1) - 8| = |-3| = 3 \\ \\checkmark",
        ])
        a_banner(self, "Answer: A   x = 1 or x = 11/5")
        self.wait(3)
