from alg_common import *


class Q25(Scene):
    """Slope and y-intercept of 2x + 5y = 20."""

    def construct(self):
        q_card(self, 25)
        self.play(Write(atitle(25, "Slope and y-Intercept")))

        eq0 = aeq("2x", "+5y", "=", "20")
        self.play(Write(eq0))
        cap = acap("Step 1: Solve for y")
        self.play(FadeIn(cap, shift=UP * 0.2))
        hint = Text("Slope-intercept form is  y = mx + b", font_size=28, color=GIVEN).move_to(DOWN * 0.8)
        self.play(FadeIn(hint, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(hint))

        cap = next_cap(self, cap, "Step 2: Subtract 2x from both sides")
        eq = op_step(self, eq0, ops=("-2x", "-2x"), under=([0, 1], [3]),
                     mid=aeq("2x", "+5y", "-2x", "=", "20", "-2x"),
                     mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                     cancel=[0, 2],
                     result=aeq("5y", "=", "20", "-2x"))
        reorder = aeq("5y", "=", "-2x", "+20")
        self.play(ReplacementTransform(eq, reorder))
        eq = reorder

        cap = next_cap(self, cap, "Step 3: Divide everything by 5")
        eq = op_step(self, eq, ops=("\\div 5", "\\div 5"), under=([0], [2, 3]),
                     mid=aeq("{5y", "\\over", "5}", "=", "{-2x", "+20", "\\over", "5}"),
                     result=aeq("y", "=", "-\\frac{2}{5}x", "+4"))
        self.play(eq[2].animate.set_color(GREEN), eq[3].animate.set_color(CONST))
        self.wait(1)

        cap = next_cap(self, cap, "Step 4: Read slope and y-intercept")
        labels = VGroup(
            MathTex("\\text{slope } m = -\\tfrac{2}{5}", color=GREEN),
            MathTex("\\text{y-intercept } b = 4", color=CONST),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 0.7)
        self.play(FadeIn(labels[0], shift=UP * 0.2), Indicate(eq[2], color=GREEN))
        self.play(FadeIn(labels[1], shift=UP * 0.2), Indicate(eq[3], color=CONST))
        self.wait(2)

        self.play(FadeOut(VGroup(eq, labels)))
        rows = VGroup(
            VGroup(MathTex("A.\\ m = -\\tfrac{2}{5},\\ b = 4"), MathTex("\\checkmark", color=GREEN)),
            VGroup(MathTex("B.\\ m = \\tfrac{2}{5},\\ b = 4"), MathTex("\\times", color=RED), Text("sign of the slope is wrong", font_size=24, color=GREY_B)),
            VGroup(MathTex("C.\\ m = -\\tfrac{2}{5},\\ b = 20"), MathTex("\\times", color=RED), Text("20 is before dividing by 5", font_size=24, color=GREY_B)),
            VGroup(MathTex("D.\\ m = \\tfrac{2}{5},\\ b = 20"), MathTex("\\times", color=RED), Text("both are wrong", font_size=24, color=GREY_B)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.35)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(UP * 0.3)
        rows[0][0].set_color(ANSWER)
        cap = next_cap(self, cap, "Step 5: Match the answer choices")
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(0.5)
        self.wait(1.5)
        self.play(FadeOut(rows))
        a_banner(self, "Answer: A   slope -2/5, y-intercept 4")
        self.wait(3)
