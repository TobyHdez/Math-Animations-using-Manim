from alg_common import *


class Q06(Scene):
    """-18(x - 5) = -42(x - 9)."""

    def construct(self):
        q_card(self, 6)
        self.play(Write(atitle(6, "Distribute on Both Sides")))

        eq0 = aeq("-18", "(x", "-5)", "=", "-42", "(x", "-9)")
        self.play(Write(eq0))
        cap = acap("Step 1: Distribute the -18")
        self.play(FadeIn(cap, shift=UP * 0.2))
        eq = distribute(self, eq0, 0, [1, 2], ["-18 \\cdot x = -18x", "-18 \\cdot (-5) = +90"],
                        aeq("-18x", "+90", "=", "-42", "(x", "-9)"))

        cap = next_cap(self, cap, "Step 2: Distribute the -42")
        eq = distribute(self, eq, 3, [4, 5], ["-42 \\cdot x = -42x", "-42 \\cdot (-9) = +378"],
                        aeq("-18x", "+90", "=", "-42x", "+378"))

        cap = next_cap(self, cap, "Step 3: Add 42x to both sides")
        eq = op_step(self, eq, ops=("+42x", "+42x"), under=([0, 1], [3, 4]),
                     mid=aeq("-18x", "+90", "+42x", "=", "{}-42x", "+378", "+42x"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4), (4, 5)], op_idx=(2, 6),
                     cancel=[4, 6], combine=([0, 2], "-18x + 42x = 24x"),
                     result=aeq("24x", "+90", "=", "378"))

        cap = next_cap(self, cap, "Step 4: Subtract 90 from both sides")
        eq = op_step(self, eq, ops=("-90", "-90"), under=([0, 1], [3]),
                     mid=aeq("24x", "+90", "-90", "=", "378", "-90"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[1, 2], combine=([4, 5], "378 - 90 = 288"),
                     result=aeq("24x", "=", "288"))

        cap = next_cap(self, cap, "Step 5: Divide both sides by 24")
        eq = op_step(self, eq, ops=("\\div 24", "\\div 24"), under=([0], [2]),
                     mid=aeq("{24x", "\\over", "24}", "=", "{288", "\\over", "24}"),
                     combine=([4, 5, 6], "288 \\div 24 = 12"),
                     result=aeq("x", "=", "12"))
        self.play(eq[2].animate.set_color(ANSWER))
        self.wait(1)

        self.play(FadeOut(eq))
        cap, grp = check_step(self, cap, [
            "-18(12 - 5) = -18(7) = -126",
            "-42(12 - 9) = -42(3) = -126 \\ \\checkmark",
        ])
        a_banner(self, "Answer: A   x = 12")
        self.wait(3)
