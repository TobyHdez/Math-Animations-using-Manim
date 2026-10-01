from alg_common import *


class Q08(Scene):
    """x + 0.50(20) = 0.75(x + 20)."""

    def construct(self):
        q_card(self, 8)
        self.play(Write(atitle(8, "Decimals and Distributing")))

        eq0 = aeq("x", "+0.50(20)", "=", "0.75", "(x", "+20)")
        self.play(Write(eq0))
        cap = acap("Step 1: Multiply 0.50 times 20")
        self.play(FadeIn(cap, shift=UP * 0.2))
        box = SurroundingRectangle(eq0[1], color=CONST, buff=0.08)
        lab = MathTex("0.50 \\cdot 20 = 10", color=CONST).scale(0.9).next_to(box, DOWN, buff=0.3)
        self.add(box, lab)
        self.play(Create(box), FadeIn(lab))
        self.wait(1.2)
        eq1 = aeq("x", "+10", "=", "0.75", "(x", "+20)")
        self.play(FadeOut(box), FadeOut(lab), TransformMatchingTex(eq0, eq1))
        self.wait(0.8)

        cap = next_cap(self, cap, "Step 2: Distribute the 0.75")
        eq = distribute(self, eq1, 3, [4, 5], ["0.75 \\cdot x = 0.75x", "0.75 \\cdot 20 = 15"],
                        aeq("x", "+10", "=", "0.75x", "+15"))

        cap = next_cap(self, cap, "Step 3: Subtract 0.75x from both sides")
        eq = op_step(self, eq, ops=("-0.75x", "-0.75x"), under=([0, 1], [3, 4]),
                     mid=aeq("x", "+10", "-0.75x", "=", "{}0.75x", "+15", "-0.75x"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4), (4, 5)], op_idx=(2, 6),
                     cancel=[4, 6], combine=([0, 2], "x - 0.75x = 0.25x"),
                     result=aeq("0.25x", "+10", "=", "15"))

        cap = next_cap(self, cap, "Step 4: Subtract 10 from both sides")
        eq = op_step(self, eq, ops=("-10", "-10"), under=([0, 1], [3]),
                     mid=aeq("0.25x", "+10", "-10", "=", "15", "-10"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[1, 2], combine=([4, 5], "15 - 10 = 5"),
                     result=aeq("0.25x", "=", "5"))

        cap = next_cap(self, cap, "Step 5: Divide both sides by 0.25")
        eq = op_step(self, eq, ops=("\\div 0.25", "\\div 0.25"), under=([0], [2]),
                     mid=aeq("{0.25x", "\\over", "0.25}", "=", "{5", "\\over", "0.25}"),
                     combine=([4, 5, 6], "5 \\div 0.25 = 20"),
                     result=aeq("x", "=", "20"))
        self.play(eq[2].animate.set_color(ANSWER))
        self.wait(1)

        self.play(FadeOut(eq))
        cap, grp = check_step(self, cap, [
            "20 + 0.50(20) = 20 + 10 = 30",
            "0.75(20 + 20) = 0.75(40) = 30 \\ \\checkmark",
        ])
        a_banner(self, "Answer: C   x = 20")
        self.wait(3)
