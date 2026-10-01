from alg_common import *


class Q14(Scene):
    """Closed circle at -3, open circle at 6, shaded between: which compound inequality?"""

    def construct(self):
        q_card(self, 14)
        self.play(Write(atitle(14, "Graph to Inequality")))

        nl = NumberLine(x_range=[-8, 10, 1], length=11.5, include_numbers=True, font_size=22).move_to(DOWN * 0.2)
        pt = nl.n2p
        self.play(Create(nl))
        closed = Dot(pt(-3), color=YELLOW, radius=0.14)
        opn = Circle(radius=0.14, color=YELLOW, stroke_width=5, fill_color=BLACK, fill_opacity=1).move_to(pt(6))
        shade = Line(pt(-3), pt(6), color=GREEN, stroke_width=10)
        self.play(FadeIn(closed, scale=2), FadeIn(opn, scale=2))
        self.play(Create(shade))
        self.wait(1)

        # Step 1: circles
        cap = acap("Step 1: Closed or open circles?")
        self.play(FadeIn(cap, shift=UP * 0.2))
        t_c = Text("Closed circle: -3 IS included", font_size=28, color=YELLOW).move_to(UP * 2.3 + LEFT * 3.0)
        t_o = Text("Open circle: 6 is NOT included", font_size=28, color=YELLOW).move_to(UP * 1.6 + LEFT * 3.0)
        self.play(FadeIn(t_c, shift=DOWN * 0.2), Indicate(closed, color=YELLOW, scale_factor=2))
        self.play(FadeIn(t_o, shift=DOWN * 0.2), Indicate(opn, color=YELLOW, scale_factor=2))
        sym = VGroup(MathTex("\\le", color=GREEN).scale(1.5), MathTex("<", color=GREEN).scale(1.5))
        sym[0].next_to(closed, UP, buff=0.6)
        sym[1].next_to(opn, UP, buff=0.6)
        self.play(FadeIn(sym[0], shift=DOWN * 0.2), FadeIn(sym[1], shift=DOWN * 0.2))
        self.wait(2)
        self.play(FadeOut(VGroup(t_c, t_o)))

        # Step 2: shading between
        cap = next_cap(self, cap, "Step 2: Where is it shaded?")
        t_s = Text("Shaded BETWEEN the circles: one sandwich inequality", font_size=28, color=YELLOW).move_to(UP * 2.0)
        self.play(FadeIn(t_s, shift=DOWN * 0.2))
        self.play(Indicate(shade, color=GREEN))
        self.wait(1.5)
        self.play(FadeOut(t_s))

        # Step 3: write it
        cap = next_cap(self, cap, "Step 3: Write the inequality")
        ineq = MathTex("-3", "\\le", "x", "<", "6").scale(1.6).move_to(UP * 1.6)
        ineq[0].set_color(YELLOW); ineq[4].set_color(YELLOW)
        self.play(Write(ineq[0]))
        self.play(TransformFromCopy(sym[0], ineq[1]))
        self.play(Write(ineq[2]))
        self.play(TransformFromCopy(sym[1], ineq[3]))
        self.play(Write(ineq[4]))
        self.play(ineq.animate.set_color(ANSWER))
        self.wait(1.5)

        # Step 4: rule out the others
        cap = next_cap(self, cap, "Step 4: Rule out the others")
        self.play(FadeOut(VGroup(nl, closed, opn, shade, sym)), ineq.animate.scale(0.6).move_to(UP * 2.4))
        rows = VGroup(
            VGroup(MathTex("A.\\ -3 \\le x < 6"), MathTex("\\checkmark", color=GREEN)),
            VGroup(MathTex("B.\\ -3 < x \\le 6"), MathTex("\\times", color=RED), Text("circles swapped", font_size=24, color=GREY_B)),
            VGroup(MathTex("C.\\ x \\le -3 \\text{ or } x > 6"), MathTex("\\times", color=RED), Text("shades the OUTSIDE", font_size=24, color=GREY_B)),
            VGroup(MathTex("D.\\ x < -3 \\text{ or } x \\ge 6"), MathTex("\\times", color=RED), Text("shades the OUTSIDE", font_size=24, color=GREY_B)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.35)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 0.1)
        rows[0][0].set_color(ANSWER)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(0.6)
        self.wait(1.5)
        self.play(FadeOut(rows), FadeOut(ineq))
        a_banner(self, "Answer: A   -3 ≤ x < 6")
        self.wait(3)
