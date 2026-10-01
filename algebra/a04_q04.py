from alg_common import *


class Q04(Scene):
    """7m = (p - q) / (3n)  ->  solve for q."""

    def construct(self):
        q_card(self, 4)
        title = atitle(4, "Solve for q")
        self.play(Write(title))

        eq0 = aeq("7m", "=", "{p-q", "\\over", "3n}")
        self.play(Write(eq0))
        cap = acap("Step 1: Multiply both sides by 3n")
        self.play(FadeIn(cap, shift=UP * 0.2))
        eq = op_step(self, eq0, ops=("\\cdot 3n", "\\cdot 3n"), under=([0], [2, 3, 4]),
                     mid=aeq("7m", "\\cdot 3n", "=", "{p-q", "\\over", "3n}", "\\cdot 3n"),
                     mapping=[(0, 0), (1, 2), (2, 3), (3, 4), (4, 5)], op_idx=(1, 6),
                     cancel=[5, 6], combine=([0, 1], "7m \\cdot 3n = 21mn"),
                     result=aeq("21mn", "=", "p", "-q"))

        cap = next_cap(self, cap, "Step 2: Subtract p from both sides")
        eq = op_step(self, eq, ops=("-p", "-p"), under=([0], [2, 3]),
                     mid=aeq("21mn", "-p", "=", "{}p", "-q", "-p"),
                     mapping=[(0, 0), (1, 2), (2, 3), (3, 4)], op_idx=(1, 5),
                     cancel=[3, 5],
                     result=aeq("21mn", "-p", "=", "-q"))

        cap = next_cap(self, cap, "Step 3: Multiply both sides by -1")
        hint = Text("q is still negative: -q", font_size=28, color=GIVEN).move_to(DOWN * 0.8)
        self.play(FadeIn(hint, shift=UP * 0.2), Indicate(eq[3], color=YELLOW))
        self.wait(1)
        self.play(FadeOut(hint))
        eq = op_step(self, eq, ops=("\\cdot (-1)", "\\cdot (-1)"), under=([0, 1], [3]),
                     mid=aeq("(21mn-p)(-1)", "=", "(-q)(-1)"),
                     combine=([0], "\\text{every sign flips}"),
                     result=aeq("-21mn", "+p", "=", "q"))
        self.wait(0.5)
        final = aeq("q", "=", "p", "-21mn")
        self.play(ReplacementTransform(eq, final))
        self.play(final[0].animate.set_color(ANSWER))
        self.wait(1)

        self.play(FadeOut(final))
        cap, grp = check_step(self, cap, [
            "m = 1,\\ n = 1,\\ p = 30:\\quad q = 30 - 21 = 9",
            "\\dfrac{30 - 9}{3(1)} = 7 = 7m \\ \\checkmark",
        ])
        a_banner(self, "Answer: A   q = p - 21mn")
        self.wait(3)
