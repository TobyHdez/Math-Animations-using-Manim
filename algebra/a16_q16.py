from alg_common import *


class Q16(Scene):
    """-3 < x - 4 <= 5."""

    def construct(self):
        q_card(self, 16)
        self.play(Write(atitle(16, "Three-Part Inequality")))

        eq0 = aeq("-3", "<", "x", "-4", "\\le", "5")
        self.play(Write(eq0))
        cap = acap("Step 1: Do the same to ALL three parts")
        self.play(FadeIn(cap, shift=UP * 0.2))
        hint = Text("x is in the middle, so undo the -4 everywhere.", font_size=28, color=GIVEN).move_to(DOWN * 0.8)
        self.play(FadeIn(hint, shift=UP * 0.2), eq0[2].animate.set_color(YELLOW))
        self.wait(1.5)
        self.play(FadeOut(hint))

        cap = next_cap(self, cap, "Step 2: Add 4 to all three parts")
        eq = op_step_n(self, eq0, ops=["+4", "+4", "+4"], under=[[0], [2, 3], [5]],
                       mid=aeq("-3", "+4", "<", "x", "{}-4", "+4", "\\le", "5", "+4"),
                       mapping=[(0, 0), (1, 2), (2, 3), (3, 4), (4, 6), (5, 7)], op_idx=[1, 5, 8],
                       cancel=[4, 5], combine=[([0, 1], "-3 + 4 = 1"), ([7, 8], "5 + 4 = 9")],
                       result=aeq("1", "<", "x", "\\le", "9"))
        self.play(eq.animate.set_color(ANSWER))
        self.wait(1)

        cap = next_cap(self, cap, "Step 3: Graph it")
        self.play(eq.animate.scale(0.7).move_to(UP * 2.3))
        nl = NumberLine(x_range=[-2, 12, 1], length=11, include_numbers=True, font_size=22).move_to(DOWN * 0.2)
        self.play(Create(nl))
        oc = open_circle(nl.n2p(1))
        cc = closed_circle(nl.n2p(9))
        shade = Line(nl.n2p(1), nl.n2p(9), color=GREEN, stroke_width=10)
        t1 = Text("open: 1 not included (<)", font_size=24, color=YELLOW).next_to(oc, UP, buff=0.6)
        t2 = Text("closed: 9 included (≤)", font_size=24, color=YELLOW).next_to(cc, UP, buff=0.6)
        self.play(FadeIn(oc, scale=2), FadeIn(t1))
        self.play(FadeIn(cc, scale=2), FadeIn(t2), Create(shade))
        self.wait(2)

        self.play(FadeOut(VGroup(nl, oc, cc, shade, t1, t2, eq)))
        eq_final = aeq("1", "<", "x", "\\le", "9").set_color(ANSWER)
        self.play(Write(eq_final))
        self.wait(0.5)
        self.play(FadeOut(eq_final))
        cap, grp = check_step(self, cap, [
            "x = 5:\\quad -3 < 5 - 4 \\le 5 \\ \\Rightarrow\\ -3 < 1 \\le 5 \\ \\checkmark",
            "x = 1:\\quad 1 - 4 = -3,\\ \\text{and } -3 < -3 \\text{ is false}",
        ])
        a_banner(self, "Answer: A   1 < x ≤ 9")
        self.wait(3)
