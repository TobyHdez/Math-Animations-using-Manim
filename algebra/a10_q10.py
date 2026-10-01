from alg_common import *


class Q10(Scene):
    """Parallel to 4x + 3y = 6 through (3, -2)."""

    def construct(self):
        q_card(self, 10)
        self.play(Write(atitle(10, "Parallel Line Through a Point")))

        # Step 1: slope of the given line
        eq0 = aeq("4x", "+3y", "=", "6")
        self.play(Write(eq0))
        cap = acap("Step 1: Get the slope of the given line")
        self.play(FadeIn(cap, shift=UP * 0.2))
        hint = Text("Solve for y to read the slope", font_size=28, color=GIVEN).move_to(DOWN * 0.7)
        self.play(FadeIn(hint, shift=UP * 0.2))
        self.wait(1)
        self.play(FadeOut(hint))
        eq = op_step(self, eq0, ops=("-4x", "-4x"), under=([0, 1], [3]),
                     mid=aeq("4x", "+3y", "-4x", "=", "6", "-4x"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[0, 2],
                     result=aeq("3y", "=", "6", "-4x"))
        eq = op_step(self, eq, ops=("\\div 3", "\\div 3"), under=([0], [2, 3]),
                     mid=aeq("{3y", "\\over", "3}", "=", "{6", "-4x", "\\over", "3}"),
                     result=aeq("y", "=", "-\\frac{4}{3}x", "+2"))
        eq[2].set_color(GREEN)
        slope = MathTex("\\text{slope } m = -\\tfrac{4}{3}", color=GREEN).scale(1.0).move_to(DOWN * 0.7)
        self.play(Indicate(eq[2], color=GREEN), FadeIn(slope, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(eq), FadeOut(slope))

        # Step 2: parallel = same slope
        cap = next_cap(self, cap, "Step 2: Parallel lines share a slope")
        t1 = Text("Same slope, so the new line has", font_size=28, color=GIVEN)
        t2 = MathTex("m = -\\tfrac{4}{3}", color=GREEN).scale(1.4)
        VGroup(t1, t2).arrange(DOWN, buff=0.4).move_to(AEQ)
        self.play(FadeIn(t1, shift=DOWN * 0.2), Write(t2))
        self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2))

        # Step 3: point-slope form
        cap = next_cap(self, cap, "Step 3: Use point-slope form")
        gen = aeq("y", "-", "y_1", "=", "m", "(x", "-", "x_1", ")")
        self.play(Write(gen))
        self.play(gen[2].animate.set_color(YELLOW), gen[7].animate.set_color(YELLOW), gen[4].animate.set_color(GREEN))
        self.wait(1)
        pt = Text("Point (3, -2):  x₁ = 3,  y₁ = -2", font_size=26, color=YELLOW).move_to(DOWN * 0.5)
        self.play(FadeIn(pt, shift=UP * 0.2))
        self.wait(1)
        eq1 = aeq("y", "+2", "=", "-\\frac{4}{3}", "(x", "-3)")
        eq1[1].set_color(YELLOW)
        eq1[5].set_color(YELLOW)
        eq1[3].set_color(GREEN)
        self.play(FadeOut(pt), TransformMatchingTex(gen, eq1))
        self.wait(1)

        # Step 4: distribute
        cap = next_cap(self, cap, "Step 4: Distribute -4/3")
        eq = distribute(self, eq1, 3, [4, 5], ["-\\tfrac{4}{3} \\cdot x = -\\tfrac{4}{3}x", "-\\tfrac{4}{3} \\cdot (-3) = +4"],
                        aeq("y", "+2", "=", "-\\frac{4}{3}x", "+4"))

        # Step 5: subtract 2
        cap = next_cap(self, cap, "Step 5: Subtract 2 from both sides")
        eq = op_step(self, eq, ops=("-2", "-2"), under=([0, 1], [3, 4]),
                     mid=aeq("y", "+2", "-2", "=", "-\\frac{4}{3}x", "+4", "-2"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4), (4, 5)], op_idx=(2, 6),
                     cancel=[1, 2], combine=([5, 6], "4 - 2 = 2"),
                     result=aeq("y", "=", "-\\frac{4}{3}x", "+2"))
        self.play(eq[2].animate.set_color(GREEN), eq[3].animate.set_color(CONST))
        self.wait(1)

        self.play(FadeOut(eq))
        cap, grp = check_step(self, cap, [
            "\\text{Does } (3, -2) \\text{ work?}",
            "-\\tfrac{4}{3}(3) + 2 = -4 + 2 = -2 \\ \\checkmark",
        ])
        a_banner(self, "Answer: A   y = -(4/3)x + 2")
        self.wait(3)
