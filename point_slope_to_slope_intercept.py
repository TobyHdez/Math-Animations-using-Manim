from manim import *


class PointSlopeToSlopeIntercept(Scene):
    def construct(self):
        title = Text("Point-Slope to Slope-Intercept", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Step 0: starting equation, with the point (1, 3) and slope 2 highlighted
        eq1 = MathTex("y", "-", "3", "=", "2", "(", "x", "-", "1", ")")
        eq1.scale(1.3).shift(UP * 0.7)
        self.play(Write(eq1))

        # Blue step text lives well below the equation so work written
        # under the equation (like the +3) has room
        STEP_POS = DOWN * 1.3

        note1 = Text("Point: (1, 3)    Slope: 2", font_size=28, color=YELLOW)
        note1.move_to(STEP_POS)
        self.play(
            eq1[2].animate.set_color(YELLOW),
            eq1[8].animate.set_color(YELLOW),
            eq1[4].animate.set_color(GREEN),
            FadeIn(note1, shift=UP * 0.2),
        )
        self.wait(1.5)

        # Step 1: distribute -- the 2 bounces over each term in the parentheses
        step1 = Text("Step 1: Distribute the 2", font_size=28, color=BLUE)
        step1.move_to(STEP_POS)
        self.play(ReplacementTransform(note1, step1))

        two = eq1[4].copy().set_color(GREEN)
        hop_y = UP * 0.5
        self.add(two)
        for target, product in [(6, "2 \\cdot x = 2x"), (8, "2 \\cdot 1 = 2")]:
            self.play(
                two.animate(path_arc=-PI * 0.8).move_to(eq1[target].get_top() + hop_y),
                run_time=0.9,
            )
            result = MathTex(product, color=GREEN).scale(0.9)
            result.next_to(eq1, UP, buff=1.0)
            self.play(Indicate(eq1[target], color=GREEN), FadeIn(result, shift=DOWN * 0.2))
            self.wait(0.6)
            self.play(FadeOut(result))
        self.play(FadeOut(two))

        eq2 = MathTex("y", "-", "3", "=", "2x", "-", "2").scale(1.3)
        eq2.move_to(eq1)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(1.5)

        # Step 2: add 3 to both sides
        step2 = Text("Step 2: Add 3 to both sides", font_size=28, color=BLUE)
        step2.move_to(step1)
        # "+3" is written under BOTH sides of the equals sign
        left_side = VGroup(*eq2[0:3])
        right_side = VGroup(*eq2[4:7])
        plus3_l = MathTex("+3", color=RED).scale(1.3).next_to(left_side, DOWN, buff=0.4)
        plus3_r = MathTex("+3", color=RED).scale(1.3).next_to(right_side, DOWN, buff=0.4)
        self.play(ReplacementTransform(step1, step2))
        self.play(Write(plus3_l), Write(plus3_r))
        self.wait(1)

        # Show the +3 moved onto both sides of the equation
        eq_mid = MathTex("y", "-", "3", "+", "3", "=", "2x", "-", "2", "+", "3").scale(1.3)
        eq_mid.move_to(eq2)
        self.play(FadeOut(plus3_l), FadeOut(plus3_r), TransformMatchingTex(eq2, eq_mid))
        self.wait(1)

        # -3 + 3 cancels on the left: slash through both terms in red
        slashes = VGroup()
        for term in (VGroup(*eq_mid[1:3]), VGroup(*eq_mid[3:5])):
            slash = Line(
                term.get_corner(DL) + (DL + LEFT * 0.0) * 0.1,
                term.get_corner(UR) + (UR) * 0.1,
                color=RED, stroke_width=6,
            )
            slashes.add(slash)
        self.play(Create(slashes[0]), run_time=0.6)
        self.play(Create(slashes[1]), run_time=0.6)
        self.wait(1)

        eq3 = MathTex("y", "=", "2x", "-", "2", "+", "3").scale(1.3)
        eq3.move_to(eq_mid)
        self.play(FadeOut(slashes), TransformMatchingTex(eq_mid, eq3))
        self.wait(1)

        # Step 3: combine constants
        step3 = Text("Step 3: Combine -2 + 3", font_size=28, color=BLUE)
        step3.move_to(step2)
        eq4 = MathTex("y", "=", "2x", "+", "1").scale(1.3)
        eq4.move_to(eq3)
        self.play(ReplacementTransform(step2, step3))

        # Box the -2 + 3 on the right side and show what it combines to
        combine_box = SurroundingRectangle(VGroup(*eq3[3:7]), color=ORANGE, buff=0.12)
        combine_label = MathTex("-2 + 3 = 1", color=ORANGE).scale(1.1)
        combine_label.next_to(combine_box, DOWN, buff=0.35)
        self.play(Create(combine_box))
        self.play(Write(combine_label))
        self.wait(1.2)
        self.play(
            FadeOut(combine_box), FadeOut(combine_label),
            TransformMatchingTex(eq3, eq4),
        )
        self.play(
            eq4[2].animate.set_color(GREEN),
            eq4[4].animate.set_color(ORANGE),
        )
        self.wait(1)

        labels = VGroup(
            Text("slope m = 2", font_size=26, color=GREEN),
            Text("y-intercept b = 1", font_size=26, color=ORANGE),
        ).arrange(RIGHT, buff=0.8).next_to(step3, DOWN, buff=0.4)
        self.play(FadeIn(labels, shift=UP * 0.2))
        self.wait(2)

        # Shrink the algebra to the left, then graph the result as a check
        algebra = VGroup(eq4, step3, labels)
        self.play(FadeOut(title), algebra.animate.scale(0.55).to_corner(UL))

        axes = Axes(
            x_range=[-2, 4, 1], y_range=[-2, 8, 2],
            x_length=6, y_length=5,
            axis_config={"include_numbers": True},
        ).to_edge(DOWN).shift(RIGHT * 2)
        line = axes.plot(lambda x: 2 * x + 1, color=BLUE, x_range=[-1.5, 3.5])
        point = Dot(axes.c2p(1, 3), color=YELLOW, radius=0.1)
        point_label = MathTex("(1,3)", color=YELLOW).scale(0.8).next_to(point, RIGHT)
        intercept = Dot(axes.c2p(0, 1), color=ORANGE, radius=0.1)
        intercept_label = MathTex("(0,1)", color=ORANGE).scale(0.8).next_to(intercept, LEFT)

        self.play(Create(axes))
        self.play(Create(line))
        self.play(FadeIn(point, scale=2), Write(point_label))
        self.play(FadeIn(intercept, scale=2), Write(intercept_label))

        # Rise over run, always in the same order:
        # start at the y-intercept, move VERTICALLY first (rise), then RIGHT (run)
        rule = Text("Rise first (up/down), then run right", font_size=26, color=GREEN)
        slope_frac = MathTex(
            "m", "=", "{\\text{rise}", "\\over", "\\text{run}}", "=",
            "{2", "\\over", "1}",
        ).scale(0.9)
        slope_frac.set_color(GREEN)
        VGroup(rule, slope_frac).arrange(DOWN, buff=0.4).to_corner(UR, buff=0.5)
        self.play(FadeIn(rule, shift=DOWN * 0.2), Write(slope_frac))
        self.wait(1)

        rise = Line(axes.c2p(0, 1), axes.c2p(0, 3), color=GREEN, stroke_width=8)
        run = Line(axes.c2p(0, 3), axes.c2p(1, 3), color=GREEN, stroke_width=8)
        rise_label = Text("rise = 2", font_size=22, color=GREEN)
        rise_label.next_to(rise, LEFT, buff=0.95)
        run_label = Text("run = 1", font_size=22, color=GREEN)
        run_label.next_to(run, UP, buff=0.15)

        # 1) rise: highlight the top number, go up
        self.play(Indicate(slope_frac[6], color=YELLOW, scale_factor=1.4))
        self.play(Create(rise), Write(rise_label))
        self.wait(0.5)
        # 2) run: highlight the bottom number, go right
        self.play(Indicate(slope_frac[8], color=YELLOW, scale_factor=1.4))
        self.play(Create(run), Write(run_label))
        self.play(Indicate(point, scale_factor=2))
        self.wait(3)
