from common import *


def number_line(lo, hi, length, tick_step, y=0.5):
    nl = NumberLine(x_range=[lo, hi, tick_step], length=length, include_numbers=False,
                    include_tip=False, stroke_width=4, tick_size=0.12)
    nl.move_to(LEFT * 3.7 + UP * y)
    return nl


class NumberLineFraction(Scene):
    """Questions 23 and 24: the point that is a fraction of the way between two numbers."""

    def num_labels(self, nl, vals, size=0.55):
        return VGroup(*[MathTex(str(v)).scale(size).next_to(nl.n2p(v), DOWN, buff=0.18) for v in vals])

    def construct(self):
        self.q23()
        self.q24()

    # ------------------------------------------------------------------
    def q23(self):
        question_card(self, 23)
        title = make_title("Question 23: A Fraction of the Way")
        nl = number_line(-8, 16, 6.0, 3)
        labs = self.num_labels(nl, [-8, -5, -2, 1, 4, 7, 10, 13, 16], 0.5)
        labs[0].set_color(YELLOW); labs[-1].set_color(YELLOW)
        a_dot = Dot(nl.n2p(-8), color=YELLOW, radius=0.1)
        b_dot = Dot(nl.n2p(16), color=YELLOW, radius=0.1)
        self.play(Write(title))
        self.play(Create(nl), FadeIn(a_dot), FadeIn(b_dot))

        # Step 1: total distance
        cap = caption("Step 1: Find the total distance")
        self.play(FadeIn(cap, shift=UP * 0.2))
        brace = Brace(Line(nl.n2p(-8), nl.n2p(16)), DOWN, buff=0.45)
        blab = MathTex("24", color=CONST).scale(0.9).next_to(brace, DOWN, buff=0.1)
        d = MathTex("16", "-", "(-8)", "=", "24").scale(1.2).move_to(EQ_POS)
        self.play(Write(d), GrowFromCenter(brace), FadeIn(blab))
        self.wait(1.5)

        # Step 2: split into 8 equal parts
        new_cap = caption("Step 2: Cut it into 8 equal parts")
        self.play(ReplacementTransform(cap, new_cap), FadeOut(d)); cap = new_cap
        t1 = Text("Denominator 8 = 8 equal parts", font_size=28, color=GIVEN)
        t2 = MathTex("24 \\div 8 = 3", color=CONST).scale(1.2)
        VGroup(t1, t2).arrange(DOWN, buff=0.4).move_to(EQ_POS)
        self.play(FadeIn(t1, shift=DOWN * 0.2))
        ticks = VGroup(*[Line(nl.n2p(-8 + 3 * k) + UP * 0.2, nl.n2p(-8 + 3 * k) + DOWN * 0.2, color=GREEN, stroke_width=5)
                         for k in range(1, 8)])
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.2), FadeIn(labs))
        self.play(Write(t2))
        self.wait(1.2)

        # Step 3: hop 3 parts
        new_cap = caption("Step 3: Hop 3 parts from -8")
        self.play(ReplacementTransform(cap, new_cap), FadeOut(VGroup(t1, t2))); cap = new_cap
        hops = VGroup()
        for k in range(3):
            arc = ArcBetweenPoints(nl.n2p(-8 + 3 * k) + UP * 0.05, nl.n2p(-5 + 3 * k) + UP * 0.05, angle=-PI / 2.4, color=GREEN, stroke_width=5)
            hops.add(arc)
        counts = VGroup(*[MathTex(str(k + 1), color=GREEN).scale(0.7).move_to((hops[k].get_center()) + UP * 0.35) for k in range(3)])
        for k in range(3):
            self.play(Create(hops[k]), FadeIn(counts[k]), run_time=0.8)
        land = Dot(nl.n2p(1), color=ANSWER, radius=0.13)
        self.play(FadeIn(land, scale=3))
        self.wait(1)

        # Step 4: the calculation
        new_cap = caption("Step 4: Check with arithmetic")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        c1 = MathTex("\\tfrac{3}{8}", "\\cdot 24", "=", "9").scale(1.2)
        c2 = MathTex("-8", "+", "9", "=", "1").scale(1.2)
        c1[0].set_color(GREEN)
        c2[4].set_color(ANSWER)
        VGroup(c1, c2).arrange(DOWN, buff=0.5).move_to(EQ_POS)
        self.play(Write(c1))
        self.play(Write(c2))
        self.play(Indicate(land, color=ANSWER, scale_factor=2))
        self.wait(1.5)
        answer_banner(self, "Answer: 1")
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])

    # ------------------------------------------------------------------
    def q24(self):
        question_card(self, 24)
        title = make_title("Question 24: Weighted Average")
        nl = number_line(-12, 16, 6.0, 4, y=1.0)
        labs = self.num_labels(nl, [-12, -8, -4, 0, 4, 8, 12, 16], 0.5)
        a_dot = Dot(nl.n2p(-12), color=YELLOW, radius=0.1)
        b_dot = Dot(nl.n2p(16), color=YELLOW, radius=0.1)
        self.play(Write(title))
        self.play(Create(nl), FadeIn(labs), FadeIn(a_dot), FadeIn(b_dot))

        cap = caption("Step 1: Find the target point")
        self.play(FadeIn(cap, shift=UP * 0.2))
        t1 = MathTex("16", "-", "(-12)", "=", "28").scale(1.0)
        t2 = MathTex("28 \\div 7 = 4 \\text{ per part}", color=CONST).scale(1.0)
        t3 = MathTex("3 \\text{ parts: } -12 + 3(4) = 0", color=ANSWER).scale(1.0)
        VGroup(t1, t2, t3).arrange(DOWN, buff=0.4).move_to(EQ_POS)
        self.play(Write(t1))
        ticks = VGroup(*[Line(nl.n2p(-12 + 4 * k) + UP * 0.2, nl.n2p(-12 + 4 * k) + DOWN * 0.2, color=GREEN, stroke_width=5)
                         for k in range(1, 7)])
        self.play(Write(t2), LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.2))
        target = Dot(nl.n2p(0), color=ANSWER, radius=0.13)
        self.play(Write(t3), FadeIn(target, scale=3))
        self.wait(1.5)

        new_cap = caption("Step 2: Test each expression")
        self.play(ReplacementTransform(cap, new_cap), FadeOut(VGroup(t1, t2, t3))); cap = new_cap
        t = Text("The target is 0.  Which one gives 0?", font_size=28, color=GIVEN)
        t.move_to(EQ_POS + UP * 1.75)
        opts = VGroup(
            MathTex("A.\\ -12 + 16\\left(\\tfrac{3}{7}\\right)", "\\approx -5.1"),
            MathTex("B.\\ -12\\left(\\tfrac{4}{7}\\right) + 16\\left(\\tfrac{3}{7}\\right)", "= 0"),
            MathTex("C.\\ -12\\left(\\tfrac{3}{7}\\right) + 16\\left(\\tfrac{4}{7}\\right)", "= 4"),
            MathTex("D.\\ -12 + \\tfrac{3}{7}(16 - 12)", "\\approx -10.3"),
        ).scale(0.72)
        for o in opts:
            o.arrange(RIGHT, buff=0.3)
        opts.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(EQ_POS + DOWN * 0.3)
        self.play(FadeIn(t, shift=DOWN * 0.2))
        for i, o in enumerate(opts):
            self.play(Write(o[0]), run_time=0.8)
            self.play(Write(o[1]), run_time=0.6)
            self.wait(0.4)
            if i != 1:
                self.play(o.animate.set_color(GREY_B), run_time=0.4)
            else:
                self.play(o.animate.set_color(ANSWER), Indicate(target, color=ANSWER, scale_factor=2))
        self.wait(1)

        new_cap = caption("Why B works")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        why = VGroup(
            Text("Fraction t of the way from A to B:", font_size=26, color=GIVEN),
            MathTex("A(1 - t) + B(t)", color=GIVEN).scale(1.1),
            MathTex("t = \\tfrac{3}{7}:\\ \\ -12\\!\\left(\\tfrac{4}{7}\\right) + 16\\!\\left(\\tfrac{3}{7}\\right) = 0", color=ANSWER).scale(0.85),
        ).arrange(DOWN, buff=0.4)
        why.move_to(EQ_POS)
        self.play(FadeOut(VGroup(t, opts)))
        self.play(FadeIn(why[0], shift=DOWN * 0.2))
        self.play(Write(why[1]))
        self.play(Write(why[2]))
        self.wait(1.5)
        answer_banner(self, "Answer: B")
        self.wait(3)
