from alg_common import *


class Q17(Scene):
    """-3x + 5 < 2(x - 10): solve and graph."""

    def construct(self):
        q_card(self, 17)
        self.play(Write(atitle(17, "Solve and Graph the Inequality")))

        eq0 = aeq("-3x", "+5", "<", "2", "(x", "-10)")
        self.play(Write(eq0))
        cap = acap("Step 1: Distribute the 2")
        self.play(FadeIn(cap, shift=UP * 0.2))
        eq = distribute(self, eq0, 3, [4, 5], ["2 \\cdot x = 2x", "2 \\cdot (-10) = -20"],
                        aeq("-3x", "+5", "<", "2x", "-20"))

        cap = next_cap(self, cap, "Step 2: Add 3x to both sides")
        tip = Text("Keep x on the side that stays positive.", font_size=26, color=GIVEN).move_to(DOWN * 0.9)
        self.play(FadeIn(tip, shift=UP * 0.2))
        eq = op_step(self, eq, ops=("+3x", "+3x"), under=([0, 1], [3, 4]),
                     mid=aeq("-3x", "+5", "+3x", "<", "2x", "-20", "+3x"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4), (4, 5)], op_idx=(2, 6),
                     cancel=[0, 2], combine=([4, 6], "2x + 3x = 5x"),
                     result=aeq("5", "<", "5x", "-20"))
        self.play(FadeOut(tip))

        cap = next_cap(self, cap, "Step 3: Add 20 to both sides")
        eq = op_step(self, eq, ops=("+20", "+20"), under=([0], [2, 3]),
                     mid=aeq("5", "+20", "<", "5x", "{}-20", "+20"),
                     mapping=[(0, 0), (1, 2), (2, 3), (3, 4)], op_idx=(1, 5),
                     cancel=[4, 5], combine=([0, 1], "5 + 20 = 25"),
                     result=aeq("25", "<", "5x"))

        cap = next_cap(self, cap, "Step 4: Divide both sides by 5")
        eq = op_step(self, eq, ops=("\\div 5", "\\div 5"), under=([0], [2]),
                     mid=aeq("{25", "\\over", "5}", "<", "{5x", "\\over", "5}"),
                     combine=([0, 1, 2], "25 \\div 5 = 5"),
                     result=aeq("5", "<", "x"))
        note = Text("5 < x  means  x is bigger than 5", font_size=28, color=GIVEN).move_to(DOWN * 0.7)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(1.5)
        flipped = aeq("x", ">", "5").set_color(ANSWER)
        self.play(ReplacementTransform(eq, flipped), FadeOut(note))
        self.wait(1)

        cap = next_cap(self, cap, "Step 5: Graph x > 5")
        self.play(flipped.animate.scale(0.7).move_to(UP * 2.3))
        nl = NumberLine(x_range=[-2, 12, 1], length=11, include_numbers=True, font_size=22).move_to(DOWN * 0.2)
        self.play(Create(nl))
        oc = open_circle(nl.n2p(5))
        arr = Arrow(nl.n2p(5), nl.n2p(12), color=GREEN, buff=0, stroke_width=10, max_tip_length_to_length_ratio=0.1)
        t1 = Text("open circle: 5 is not included", font_size=24, color=YELLOW).next_to(oc, UP, buff=0.6)
        t2 = Text("shade right: bigger numbers", font_size=24, color=GREEN).next_to(arr, DOWN, buff=0.6)
        self.play(FadeIn(oc, scale=2), FadeIn(t1))
        self.play(Create(arr), FadeIn(t2))
        self.wait(2)

        self.play(FadeOut(VGroup(nl, oc, arr, t1, t2, flipped)))
        cap, grp = check_step(self, cap, [
            "x = 6:\\quad -3(6) + 5 = -13",
            "2(6 - 10) = -8,\\quad -13 < -8 \\ \\checkmark",
        ])
        a_banner(self, "Answer: x > 5  (open circle at 5, shade right)")
        self.wait(3)
