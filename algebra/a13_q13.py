from alg_common import *


class Q13(Scene):
    """x - 7 >= 3  or  x/4 < -1."""

    def construct(self):
        q_card(self, 13)
        self.play(Write(atitle(13, "Compound Inequality With OR")))

        # ---- first inequality ----
        eq0 = aeq("x", "-7", "\\ge", "3")
        self.play(Write(eq0))
        cap = acap("Step 1: Solve the first inequality")
        self.play(FadeIn(cap, shift=UP * 0.2))
        eq = op_step(self, eq0, ops=("+7", "+7"), under=([0, 1], [3]),
                     mid=aeq("x", "-7", "+7", "\\ge", "3", "+7"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[1, 2], combine=([4, 5], "3 + 7 = 10"),
                     result=aeq("x", "\\ge", "10"))
        self.play(eq.animate.scale(0.75).move_to(UP * 2.2 + LEFT * 3.4).set_color(YELLOW))
        sol1 = eq

        # ---- second inequality ----
        cap = next_cap(self, cap, "Step 2: Solve the second inequality")
        eq0 = aeq("{x", "\\over", "4}", "<", "-1")
        self.play(Write(eq0))
        eq = op_step(self, eq0, ops=("\\cdot 4", "\\cdot 4"), under=([0, 1, 2], [4]),
                     mid=aeq("{x", "\\over", "4}", "\\cdot 4", "<", "-1", "\\cdot 4"),
                     mapping=[(0, 0), (1, 1), (2, 2), (3, 4), (4, 5)], op_idx=(3, 6),
                     cancel=[2, 3], combine=([5, 6], "-1 \\cdot 4 = -4"),
                     result=aeq("x", "<", "-4"))
        self.play(eq.animate.scale(0.75).move_to(UP * 2.2 + RIGHT * 3.4).set_color(YELLOW))
        sol2 = eq
        or_t = Text("or", font_size=32, color=GREEN).move_to(UP * 2.2)
        self.play(FadeIn(or_t))
        self.wait(1)

        # ---- graph ----
        cap = next_cap(self, cap, "Step 3: Graph both pieces")
        nl = NumberLine(x_range=[-8, 14, 2], length=11.5, include_numbers=True, font_size=22).move_to(DOWN * 0.4)
        self.play(Create(nl))
        pt = nl.n2p
        d10 = Dot(pt(10), color=YELLOW, radius=0.13)
        o4 = Circle(radius=0.13, color=YELLOW, stroke_width=5, fill_color=BLACK, fill_opacity=1).move_to(pt(-4))
        right = Arrow(pt(10), pt(14), color=GREEN, buff=0, stroke_width=8, max_tip_length_to_length_ratio=0.15)
        left = Arrow(pt(-4), pt(-8), color=GREEN, buff=0, stroke_width=8, max_tip_length_to_length_ratio=0.15)
        t_closed = Text("closed: 10 is included", font_size=24, color=YELLOW).next_to(d10, UP, buff=0.5)
        t_open = Text("open: -4 is NOT included", font_size=24, color=YELLOW).next_to(o4, UP, buff=0.5)
        self.play(FadeIn(d10, scale=2), Create(right), FadeIn(t_closed))
        self.play(FadeIn(o4, scale=2), Create(left), FadeIn(t_open))
        self.wait(1.5)

        cap = next_cap(self, cap, "Step 4: OR means either piece counts")
        words = Text("The solution is BOTH shaded pieces together.", font_size=28, color=GIVEN).move_to(DOWN * 2.3)
        self.play(FadeIn(words, shift=UP * 0.2))
        self.wait(2)
        final = aeq("x", "\\ge", "10", "\\ \\text{or}\\ ", "x", "<", "-4").scale(0.8)
        self.play(FadeOut(VGroup(nl, d10, o4, right, left, t_closed, t_open, words, sol1, sol2, or_t)))
        self.play(Write(final.set_color(ANSWER)))
        self.wait(1.5)
        a_banner(self, "Answer: A   x ≥ 10 or x < -4")
        self.wait(3)
