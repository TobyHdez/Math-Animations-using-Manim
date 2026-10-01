from alg_common import *


class Q07(Scene):
    """5(2x + 6) = 8x + 18."""

    def construct(self):
        q_card(self, 7)
        self.play(Write(atitle(7, "Distribute and Solve")))

        eq0 = aeq("5", "(2x", "+6)", "=", "8x", "+18")
        self.play(Write(eq0))
        cap = acap("Step 1: Distribute the 5")
        self.play(FadeIn(cap, shift=UP * 0.2))
        eq = distribute(self, eq0, 0, [1, 2], ["5 \\cdot 2x = 10x", "5 \\cdot 6 = 30"],
                        aeq("10x", "+30", "=", "8x", "+18"))

        cap = next_cap(self, cap, "Step 2: Subtract 8x from both sides")
        eq = op_step(self, eq, ops=("-8x", "-8x"), under=([0, 1], [3, 4]),
                     mid=aeq("10x", "+30", "-8x", "=", "{}8x", "+18", "-8x"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4), (4, 5)], op_idx=(2, 6),
                     cancel=[4, 6], combine=([0, 2], "10x - 8x = 2x"),
                     result=aeq("2x", "+30", "=", "18"))

        cap = next_cap(self, cap, "Step 3: Subtract 30 from both sides")
        eq = op_step(self, eq, ops=("-30", "-30"), under=([0, 1], [3]),
                     mid=aeq("2x", "+30", "-30", "=", "18", "-30"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[1, 2], combine=([4, 5], "18 - 30 = -12"),
                     result=aeq("2x", "=", "-12"))

        cap = next_cap(self, cap, "Step 4: Divide both sides by 2")
        eq = op_step(self, eq, ops=("\\div 2", "\\div 2"), under=([0], [2]),
                     mid=aeq("{2x", "\\over", "2}", "=", "{-12", "\\over", "2}"),
                     combine=([4, 5, 6], "-12 \\div 2 = -6"),
                     result=aeq("x", "=", "-6"))
        self.play(eq[2].animate.set_color(ANSWER))
        self.wait(1)

        self.play(FadeOut(eq))
        cap, grp = check_step(self, cap, [
            "5(2(-6) + 6) = 5(-6) = -30",
            "8(-6) + 18 = -48 + 18 = -30 \\ \\checkmark",
        ])
        a_banner(self, "Answer: x = -6")
        self.wait(3)
