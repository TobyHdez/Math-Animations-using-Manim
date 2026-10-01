from alg_common import *


class Q20(Scene):
    """|-16 - 4x| - 50 = -20."""

    def construct(self):
        q_card(self, 20)
        self.play(Write(atitle(20, "Absolute Value Equation")))

        eq0 = aeq("|-16-4x|", "-50", "=", "-20")
        self.play(Write(eq0))
        cap = acap("Step 1: Get the absolute value alone")
        self.play(FadeIn(cap, shift=UP * 0.2))
        eq = op_step(self, eq0, ops=("+50", "+50"), under=([0, 1], [3]),
                     mid=aeq("|-16-4x|", "-50", "+50", "=", "-20", "+50"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[1, 2], combine=([4, 5], "-20 + 50 = 30"),
                     result=aeq("|-16-4x|", "=", "30"))

        cap = next_cap(self, cap, "Step 2: Split into two cases")
        t = Text("The inside can equal 30 OR -30", font_size=28, color=GIVEN).move_to(UP * 2.2)
        self.play(FadeIn(t, shift=DOWN * 0.2))
        c1 = aeq("-16", "-4x", "=", "30", scale=1.1).move_to(UP * 0.5 + LEFT * 3.5)
        c2 = aeq("-16", "-4x", "=", "-30", scale=1.1).move_to(UP * 0.5 + RIGHT * 3.5)
        l1 = Text("Case 1", font_size=26, color=GREEN).next_to(c1, UP, buff=0.9)
        l2 = Text("Case 2", font_size=26, color=ORANGE).next_to(c2, UP, buff=0.9)
        self.play(ReplacementTransform(eq.copy(), c1), ReplacementTransform(eq, c2), FadeIn(l1), FadeIn(l2))
        self.wait(1.5)

        cap = next_cap(self, cap, "Step 3: Add 16 to both sides")
        c1 = op_step(self, c1, ops=("+16", "+16"), under=([0, 1], [3]),
                     mid=aeq("-16", "-4x", "+16", "=", "30", "+16", scale=1.1),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[0, 2], combine=([4, 5], "30 + 16 = 46"),
                     result=aeq("-4x", "=", "46", scale=1.1))
        c2 = op_step(self, c2, ops=("+16", "+16"), under=([0, 1], [3]),
                     mid=aeq("-16", "-4x", "+16", "=", "-30", "+16", scale=1.1),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[0, 2], combine=([4, 5], "-30 + 16 = -14"),
                     result=aeq("-4x", "=", "-14", scale=1.1))

        cap = next_cap(self, cap, "Step 4: Divide both sides by -4")
        c1 = op_step(self, c1, ops=("\\div(-4)", "\\div(-4)"), under=([0], [2]),
                     mid=aeq("{-4x", "\\over", "-4}", "=", "{46", "\\over", "-4}", scale=1.1),
                     combine=([4, 5, 6], "46 \\div (-4) = -11.5"),
                     result=aeq("x", "=", "-11.5", scale=1.1))
        c2 = op_step(self, c2, ops=("\\div(-4)", "\\div(-4)"), under=([0], [2]),
                     mid=aeq("{-4x", "\\over", "-4}", "=", "{-14", "\\over", "-4}", scale=1.1),
                     combine=([4, 5, 6], "-14 \\div (-4) = 3.5"),
                     result=aeq("x", "=", "3.5", scale=1.1))
        self.play(c1.animate.set_color(ANSWER), c2.animate.set_color(ANSWER))
        self.wait(1.5)

        self.play(FadeOut(VGroup(c1, c2, l1, l2, t)))
        cap, grp = check_step(self, cap, [
            "x = -11.5:\\quad |-16 - 4(-11.5)| - 50 = |30| - 50 = -20 \\ \\checkmark",
            "x = 3.5:\\quad |-16 - 4(3.5)| - 50 = |-30| - 50 = -20 \\ \\checkmark",
        ])
        a_banner(self, "Answer: A   x = -11.5 or x = 3.5")
        self.wait(3)
