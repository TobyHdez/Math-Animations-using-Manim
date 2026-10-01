from alg_common import *


class Q11(Scene):
    """Perpendicular to y = 3x - 5 through (6, 1)."""

    def construct(self):
        q_card(self, 11)
        self.play(Write(atitle(11, "Perpendicular Line Through a Point")))

        # Step 1: slope of the given line
        given = aeq("y", "=", "3x", "-5")
        self.play(Write(given))
        cap = acap("Step 1: Read the slope")
        self.play(FadeIn(cap, shift=UP * 0.2))
        self.play(given[2].animate.set_color(GREEN))
        note = MathTex("\\text{slope } m = 3", color=GREEN).move_to(DOWN * 0.6)
        self.play(FadeIn(note, shift=UP * 0.2), Indicate(given[2], color=GREEN))
        self.wait(1.5)
        self.play(FadeOut(given), FadeOut(note))

        # Step 2: perpendicular slope
        cap = next_cap(self, cap, "Step 2: Find the perpendicular slope")
        grp = flip_slope(self, 3, 1)
        self.play(FadeOut(grp))

        # Step 3: point-slope form
        cap = next_cap(self, cap, "Step 3: Use point-slope form")
        gen = aeq("y", "-", "y_1", "=", "m", "(x", "-", "x_1", ")")
        self.play(Write(gen))
        self.play(gen[2].animate.set_color(YELLOW), gen[7].animate.set_color(YELLOW), gen[4].animate.set_color(GREEN))
        pt = Text("Point (6, 1):  x₁ = 6,  y₁ = 1", font_size=26, color=YELLOW).move_to(DOWN * 0.5)
        self.play(FadeIn(pt, shift=UP * 0.2))
        self.wait(1)
        eq1 = aeq("y", "-1", "=", "-\\frac{1}{3}", "(x", "-6)")
        eq1[1].set_color(YELLOW)
        eq1[5].set_color(YELLOW)
        eq1[3].set_color(GREEN)
        self.play(FadeOut(pt), TransformMatchingTex(gen, eq1))
        self.wait(1)

        # Step 4: distribute
        cap = next_cap(self, cap, "Step 4: Distribute -1/3")
        eq = distribute(self, eq1, 3, [4, 5], ["-\\tfrac{1}{3} \\cdot x = -\\tfrac{1}{3}x", "-\\tfrac{1}{3} \\cdot (-6) = +2"],
                        aeq("y", "-1", "=", "-\\frac{1}{3}x", "+2"))

        # Step 5: add 1
        cap = next_cap(self, cap, "Step 5: Add 1 to both sides")
        eq = op_step(self, eq, ops=("+1", "+1"), under=([0, 1], [3, 4]),
                     mid=aeq("y", "-1", "+1", "=", "-\\frac{1}{3}x", "+2", "+1"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4), (4, 5)], op_idx=(2, 6),
                     cancel=[1, 2], combine=([5, 6], "2 + 1 = 3"),
                     result=aeq("y", "=", "-\\frac{1}{3}x", "+3"))
        self.play(eq[2].animate.set_color(GREEN), eq[3].animate.set_color(CONST))
        self.wait(1)

        self.play(FadeOut(eq))
        cap, grp = check_step(self, cap, [
            "\\text{Does } (6, 1) \\text{ work?}",
            "-\\tfrac{1}{3}(6) + 3 = -2 + 3 = 1 \\ \\checkmark",
            "3 \\cdot \\left(-\\tfrac{1}{3}\\right) = -1 \\ \\checkmark",
        ])
        a_banner(self, "Answer: D   y = -(1/3)x + 3")
        self.wait(3)
