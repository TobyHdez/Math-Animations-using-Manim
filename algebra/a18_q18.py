from alg_common import *


class Q18(Scene):
    """Marcus lowers sodium by at least 15 mg but no more than 40 mg."""

    def construct(self):
        q_card(self, 18)
        self.play(Write(atitle(18, "Translate Words to an Inequality")))

        sent1 = Text("reduce it by  at least 15 mg", font_size=30)
        sent2 = Text("but  no more than 40 mg", font_size=30)
        VGroup(sent1, sent2).arrange(DOWN, buff=0.3).move_to(UP * 1.6)
        cap = acap("Step 1: Translate each phrase")
        self.play(FadeIn(cap, shift=UP * 0.2))
        self.play(FadeIn(sent1, shift=DOWN * 0.2), FadeIn(sent2, shift=DOWN * 0.2))
        self.wait(1)

        p1 = sent1[0:0]
        # highlight phrases by recoloring the whole lines (Text slices are per-glyph; keep it simple)
        self.play(sent1.animate.set_color(YELLOW))
        r1 = MathTex("\\text{at least } 15", "\\Rightarrow", "x \\ge 15", color=YELLOW).scale(1.0)
        r1[2].set_color(GREEN)
        r1.move_to(UP * 0.3)
        self.play(Write(r1))
        self.play(sent2.animate.set_color(YELLOW))
        r2 = MathTex("\\text{no more than } 40", "\\Rightarrow", "x \\le 40", color=YELLOW).scale(1.0)
        r2[2].set_color(GREEN)
        r2.move_to(DOWN * 0.5)
        self.play(Write(r2))
        self.wait(2)

        cap = next_cap(self, cap, "Step 2: Put them together")
        self.play(FadeOut(VGroup(sent1, sent2)))
        both = aeq("x", "\\ge", "15", "\\ \\text{and}\\ ", "x", "\\le", "40").scale(0.8)
        both.move_to(UP * 0.9)
        self.play(FadeOut(VGroup(r1, r2)), Write(both))
        self.wait(1)
        comb = aeq("15", "\\le", "x", "\\le", "40")
        comb.set_color(ANSWER)
        self.play(ReplacementTransform(both, comb))
        self.wait(1)

        cap = next_cap(self, cap, "Step 3: Check on a number line")
        self.play(comb.animate.scale(0.7).move_to(UP * 2.3))
        nl = NumberLine(x_range=[0, 50, 5], length=11, include_numbers=True, font_size=22).move_to(DOWN * 0.1)
        self.play(Create(nl))
        c1, c2 = closed_circle(nl.n2p(15)), closed_circle(nl.n2p(40))
        shade = Line(nl.n2p(15), nl.n2p(40), color=GREEN, stroke_width=10)
        t = Text("closed circles: 15 and 40 are allowed", font_size=24, color=YELLOW).move_to(UP * 1.0)
        self.play(FadeIn(c1, scale=2), FadeIn(c2, scale=2), Create(shade), FadeIn(t, shift=DOWN * 0.2))
        self.wait(2)
        self.play(FadeOut(VGroup(nl, c1, c2, shade, t)))

        cap = next_cap(self, cap, "Step 4: Rule out the others")
        self.play(comb.animate.move_to(UP * 2.4).scale(0.9))
        rows = VGroup(
            VGroup(MathTex("A.\\ 15 \\le x \\le 40"), MathTex("\\checkmark", color=GREEN)),
            VGroup(MathTex("B.\\ 15 < x < 40"), MathTex("\\times", color=RED), Text("excludes 15 and 40", font_size=24, color=GREY_B)),
            VGroup(MathTex("C.\\ 15 \\ge x \\ge 40"), MathTex("\\times", color=RED), Text("no number works", font_size=24, color=GREY_B)),
            VGroup(MathTex("D.\\ x \\le 15 \\text{ or } x \\ge 40"), MathTex("\\times", color=RED), Text("the OUTSIDE pieces", font_size=24, color=GREY_B)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.35)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 0.1)
        rows[0][0].set_color(ANSWER)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(0.6)
        self.wait(1.5)
        self.play(FadeOut(rows), FadeOut(comb))
        a_banner(self, "Answer: A   15 ≤ x ≤ 40")
        self.wait(3)
