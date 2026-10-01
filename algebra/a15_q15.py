from alg_common import *


def bus(label="65"):
    body = RoundedRectangle(corner_radius=0.12, width=1.5, height=0.75, color=YELLOW, stroke_width=4,
                            fill_color=YELLOW, fill_opacity=0.25)
    wheels = VGroup(*[Circle(radius=0.12, color=WHITE, fill_color=GREY, fill_opacity=1, stroke_width=2) for _ in range(2)])
    wheels[0].move_to(body.get_bottom() + LEFT * 0.45)
    wheels[1].move_to(body.get_bottom() + RIGHT * 0.45)
    txt = Text(label, font_size=28, color=WHITE).move_to(body)
    return VGroup(body, wheels, txt)


class Q15(Scene):
    """372 students + 18 chaperones, 65 seats per bus: inequality for b."""

    def construct(self):
        q_card(self, 15)
        self.play(Write(atitle(15, "Buses for the Field Trip")))

        # Step 1: total people
        cap = acap("Step 1: Count everyone going")
        self.play(FadeIn(cap, shift=UP * 0.2))
        eq0 = aeq("372", "+", "18", "=", "?")
        t1 = Text("students + chaperones", font_size=28, color=GIVEN).next_to(eq0, UP, buff=0.5)
        self.play(FadeIn(t1, shift=DOWN * 0.2), Write(eq0))
        self.wait(1)
        eq1 = aeq("372", "+", "18", "=", "390")
        eq1[4].set_color(ANSWER)
        self.play(ReplacementTransform(eq0, eq1))
        self.wait(1.5)
        self.play(FadeOut(eq1), FadeOut(t1))

        # Step 2: build the inequality
        cap = next_cap(self, cap, "Step 2: Write the inequality")
        t2 = Text("Each bus seats at most 65, so b buses seat 65b.", font_size=28, color=GIVEN).move_to(UP * 2.0)
        t3 = Text("The seats must be AT LEAST the people:", font_size=28, color=GIVEN).next_to(t2, DOWN, buff=0.3)
        self.play(FadeIn(t2, shift=DOWN * 0.2))
        self.play(FadeIn(t3, shift=DOWN * 0.2))
        ineq = aeq("65b", "\\ge", "390").move_to(UP * 0.3)
        self.play(Write(ineq))
        self.wait(1.5)
        self.play(FadeOut(t2), FadeOut(t3))
        self.play(ineq.animate.move_to(AEQ))

        # Step 3: divide both sides by 65
        cap = next_cap(self, cap, "Step 3: Divide both sides by 65")
        eq = op_step(self, ineq, ops=("\\div 65", "\\div 65"), under=([0], [2]),
                     mid=aeq("{65b", "\\over", "65}", "\\ge", "{390", "\\over", "65}"),
                     combine=([4, 5, 6], "390 \\div 65 = 6"),
                     result=aeq("b", "\\ge", "6"))
        self.play(eq.animate.set_color(ANSWER))
        self.wait(1)

        # Step 4: check with buses
        cap = next_cap(self, cap, "Step 4: Check with real buses")
        self.play(eq.animate.scale(0.7).move_to(UP * 2.5))
        row5 = VGroup(*[bus() for _ in range(5)]).arrange(RIGHT, buff=0.35)
        row5.move_to(UP * 0.7)
        t5 = MathTex("5 \\cdot 65 = 325 < 390", color=RED).scale(1.0).next_to(row5, DOWN, buff=0.4)
        x5 = MathTex("\\times", color=RED).scale(1.6).next_to(t5, RIGHT, buff=0.3)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in row5], lag_ratio=0.25))
        self.play(Write(t5), FadeIn(x5))
        self.wait(1.5)
        sixth = bus().next_to(row5, RIGHT, buff=0.35)
        row6 = VGroup(row5, sixth)
        self.play(FadeOut(t5), FadeOut(x5), row5.animate.shift(LEFT * 0.9), FadeIn(sixth.shift(LEFT * 0.9), shift=DOWN * 0.2))
        t6 = MathTex("6 \\cdot 65 = 390 \\ge 390", color=GREEN).scale(1.0).next_to(row6, DOWN, buff=0.4)
        c6 = MathTex("\\checkmark", color=GREEN).scale(1.6).next_to(t6, RIGHT, buff=0.3)
        self.play(Write(t6), FadeIn(c6))
        self.wait(1.5)
        note = Text("6 is the least number of buses.", font_size=28, color=YELLOW).move_to(DOWN * 1.0)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(VGroup(row6, t6, c6, note, eq)))
        a_banner(self, "Answer: A   b ≥ 6")
        self.wait(3)
