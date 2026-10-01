from manim import *
import numpy as np

# ---------------------------------------------------------------------------
# Map image geometry (pixels in images/road_map.png, 750 x 700).
# The map's graph has the origin at (OX, OY) and each unit is UNIT pixels.
# (Each grid square on the map is 2 units.)
# ---------------------------------------------------------------------------
MAP_PX_W, MAP_PX_H = 750, 700
OX, OY, UNIT = 378, 508, 34.1

PERP = PURPLE_D  # color of the new (perpendicular) road


def make_frac(n, d, color=WHITE, scale=1.3):
    """Hand-built fraction so the numerator/denominator can be animated."""
    num = MathTex(n, color=color).scale(scale)
    den = MathTex(d, color=color).scale(scale)
    bar = Line(LEFT * 0.35, RIGHT * 0.35, color=color, stroke_width=3)
    num.next_to(bar, UP, buff=0.12)
    den.next_to(bar, DOWN, buff=0.12)
    return VGroup(num, bar, den)


class PerpendicularRoad(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # Intro: the problem as printed
        # ------------------------------------------------------------------
        problem = ImageMobject("images/road_problem.png").scale_to_fit_width(9)
        self.play(FadeIn(problem))
        self.wait(4)
        self.play(FadeOut(problem))

        # ------------------------------------------------------------------
        # Layout: map on the left, algebra on the right
        # ------------------------------------------------------------------
        title = Text(
            "Find the road through (1, 0) perpendicular to the red road",
            font_size=30,
        ).to_edge(UP)

        map_img = ImageMobject("images/road_map.png").scale_to_fit_height(4.8)
        map_img.move_to(LEFT * 4.2 + DOWN * 0.4)
        s = map_img.height / MAP_PX_H

        def g(gx, gy):
            """Graph coordinates -> scene coordinates on the map image."""
            px = OX + UNIT * gx
            py = OY - UNIT * gy
            return map_img.get_center() + np.array(
                [(px - MAP_PX_W / 2) * s, -(py - MAP_PX_H / 2) * s, 0]
            )

        def label_bg(mob):
            return mob.add_background_rectangle(BLACK, opacity=0.65, buff=0.06)

        CX = 2.9
        EQ_POS = UP * 0.7 + RIGHT * CX
        STEP_POS = DOWN * 1.3 + RIGHT * CX

        def caption(text):
            return Text(text, font_size=26, color=BLUE).move_to(STEP_POS)

        self.play(Write(title), FadeIn(map_img))
        self.wait(1)

        # ------------------------------------------------------------------
        # Step 1: slope of the red road (rise first, then run right)
        # ------------------------------------------------------------------
        cap = caption("Step 1: Find the slope of the red road")
        self.play(FadeIn(cap, shift=UP * 0.2))

        rule = Text("Rise first (up/down), then run right", font_size=24, color=GREEN)
        rule.move_to(UP * 1.9 + RIGHT * CX)
        frac = MathTex(
            "m_{\\text{red}}", "=", "{\\text{rise}", "\\over", "\\text{run}}",
            "=", "{6", "\\over", "2}", "=", "3",
        ).scale(1.2)
        frac.set_color(GREEN)
        frac[0].set_color(WHITE)
        frac[1].set_color(WHITE)
        frac.move_to(EQ_POS)
        self.play(FadeIn(rule, shift=DOWN * 0.2), Write(VGroup(*frac[:5])))

        p_a, p_b = g(0, 2), g(2, 8)
        dot_a = Dot(p_a, color=YELLOW, radius=0.08)
        dot_b = Dot(p_b, color=YELLOW, radius=0.08)
        lab_a = label_bg(MathTex("(0, 2)", color=YELLOW).scale(0.6)).next_to(dot_a, RIGHT, buff=0.12)
        lab_b = label_bg(MathTex("(2, 8)", color=YELLOW).scale(0.6)).next_to(dot_b, RIGHT, buff=0.12)
        self.play(FadeIn(dot_a, scale=2), FadeIn(lab_a), FadeIn(dot_b, scale=2), FadeIn(lab_b))
        self.wait(0.5)

        rise = Line(p_a, g(0, 8), color=GREEN, stroke_width=8)
        run = Line(g(0, 8), p_b, color=GREEN, stroke_width=8)
        rise_lab = label_bg(Text("rise = 6", font_size=20, color=GREEN)).next_to(rise, LEFT, buff=0.7)
        run_lab = label_bg(Text("run = 2", font_size=20, color=GREEN)).next_to(run, UP, buff=0.12)

        self.play(Create(rise), Write(rise_lab))
        self.play(Write(VGroup(*frac[5:7])))
        self.play(Indicate(frac[6], color=YELLOW, scale_factor=1.4))
        self.play(Create(run), Write(run_lab))
        self.play(Write(VGroup(*frac[7:9])))
        self.play(Indicate(frac[8], color=YELLOW, scale_factor=1.4))
        self.play(Write(VGroup(*frac[9:])))
        self.wait(1.5)

        self.play(
            FadeOut(VGroup(rise, run, rise_lab, run_lab, dot_a, dot_b, lab_a, lab_b)),
            FadeOut(rule), FadeOut(frac), FadeOut(cap),
        )

        # ------------------------------------------------------------------
        # Step 2: perpendicular slope = negative reciprocal (flip, change sign)
        # ------------------------------------------------------------------
        cap = caption("Step 2: Perpendicular slope = negative reciprocal")
        self.play(FadeIn(cap, shift=UP * 0.2))

        lhs = MathTex("m_{\\text{red}}", "=").scale(1.3)
        fr = make_frac("3", "1", color=GREEN)
        row = VGroup(lhs, fr).arrange(RIGHT, buff=0.3).move_to(EQ_POS)
        self.play(Write(lhs), FadeIn(fr))
        self.wait(1)

        hint = Text("Flip it, then change the sign", font_size=24, color=YELLOW)
        hint.move_to(DOWN * 0.3 + RIGHT * CX)
        self.play(FadeIn(hint, shift=UP * 0.2))
        num, bar, den = fr
        num_pos, den_pos = num.get_center(), den.get_center()
        self.play(
            num.animate(path_arc=PI).move_to(den_pos),
            den.animate(path_arc=PI).move_to(num_pos),
            run_time=1.4,
        )
        self.wait(0.8)

        new_lhs0 = MathTex("m_{\\perp}").scale(1.3).move_to(lhs[0])
        target = fr.copy().shift(RIGHT * 0.3)
        minus = MathTex("-", color=GREEN).scale(1.5).next_to(target, LEFT, buff=0.12)
        self.play(
            ReplacementTransform(lhs[0], new_lhs0),
            fr.animate.shift(RIGHT * 0.3),
            Write(minus),
        )
        self.wait(1.5)
        self.play(FadeOut(VGroup(new_lhs0, lhs[1], fr, minus, hint)), FadeOut(cap))

        # ------------------------------------------------------------------
        # Step 3: point-slope form with the point (1, 0) and m = -1/3
        # ------------------------------------------------------------------
        cap = caption("Step 3: Point-slope form with (1, 0) and m = -1/3")
        self.play(FadeIn(cap, shift=UP * 0.2))

        gen = MathTex("y", "-", "y_1", "=", "m", "(", "x", "-", "x_1", ")").scale(1.3)
        gen.move_to(EQ_POS)
        self.play(Write(gen))
        self.play(
            gen[2].animate.set_color(YELLOW),
            gen[8].animate.set_color(YELLOW),
            gen[4].animate.set_color(GREEN),
        )
        self.wait(1)

        eq1 = MathTex("y", "-", "0", "=", "-\\frac{1}{3}", "(", "x", "-", "1", ")").scale(1.3)
        eq1.move_to(EQ_POS)
        eq1[2].set_color(YELLOW)
        eq1[8].set_color(YELLOW)
        eq1[4].set_color(GREEN)
        self.play(TransformMatchingTex(gen, eq1))
        self.wait(1.5)

        # ------------------------------------------------------------------
        # Step 4: distribute -- the slope bounces over each term
        # ------------------------------------------------------------------
        cap4 = caption("Step 4: Distribute the -1/3")
        self.play(ReplacementTransform(cap, cap4))

        two = eq1[4].copy().set_color(GREEN)
        hop_y = UP * 0.5
        self.add(two)
        for target_i, product in [
            (6, "-\\frac{1}{3} \\cdot x = -\\frac{1}{3}x"),
            (8, "-\\frac{1}{3} \\cdot (-1) = +\\frac{1}{3}"),
        ]:
            self.play(
                two.animate(path_arc=-PI * 0.8).move_to(eq1[target_i].get_top() + hop_y),
                run_time=0.9,
            )
            result = MathTex(product, color=GREEN).scale(0.9)
            result.next_to(eq1, UP, buff=1.0)
            self.play(Indicate(eq1[target_i], color=GREEN), FadeIn(result, shift=DOWN * 0.2))
            self.wait(0.8)
            self.play(FadeOut(result))
        self.play(FadeOut(two))

        eq2 = MathTex("y", "-", "0", "=", "-\\frac{1}{3}x", "+", "\\frac{1}{3}").scale(1.3)
        eq2.move_to(eq1)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(1.5)

        # ------------------------------------------------------------------
        # Step 5: subtracting 0 changes nothing -- slash it
        # ------------------------------------------------------------------
        cap5 = caption("Step 5: Subtracting 0 changes nothing")
        self.play(ReplacementTransform(cap4, cap5))

        term = VGroup(*eq2[1:3])
        slash = Line(
            term.get_corner(DL) + (DL) * 0.1,
            term.get_corner(UR) + (UR) * 0.1,
            color=RED, stroke_width=6,
        )
        self.play(Create(slash), run_time=0.6)
        self.wait(1)

        eq3 = MathTex("y", "=", "-\\frac{1}{3}x", "+", "\\frac{1}{3}").scale(1.3)
        eq3.move_to(eq2)
        self.play(FadeOut(slash), TransformMatchingTex(eq2, eq3))
        self.play(
            eq3[2].animate.set_color(GREEN),
            eq3[4].animate.set_color(ORANGE),
        )
        self.wait(1)

        labels = VGroup(
            MathTex("\\text{slope } m = -\\tfrac{1}{3}", color=GREEN).scale(0.8),
            MathTex("\\text{y-intercept } b = \\tfrac{1}{3}", color=ORANGE).scale(0.8),
        ).arrange(RIGHT, buff=0.6).move_to(STEP_POS + DOWN * 0.7)
        self.play(FadeIn(labels, shift=UP * 0.2))
        self.wait(1.5)

        # ------------------------------------------------------------------
        # Step 6: check on the map -- graph the new road
        # ------------------------------------------------------------------
        cap6 = caption("Step 6: Check it on the map")
        self.play(ReplacementTransform(cap5, cap6), FadeOut(labels))

        start = Dot(g(1, 0), color=YELLOW, radius=0.09)
        start_lab = label_bg(MathTex("(1, 0)", color=YELLOW).scale(0.6)).next_to(start, UP, buff=0.12)
        self.play(FadeIn(start, scale=2), FadeIn(start_lab))

        # rise first (down 1 for the negative slope), then run right 3
        rise2 = Line(g(1, 0), g(1, -1), color=GREEN, stroke_width=8)
        run2 = Line(g(1, -1), g(4, -1), color=GREEN, stroke_width=8)
        rise2_lab = label_bg(Text("rise = -1", font_size=20, color=GREEN)).next_to(rise2, LEFT, buff=0.15)
        run2_lab = label_bg(Text("run = 3", font_size=20, color=GREEN)).next_to(run2, DOWN, buff=0.12)
        self.play(Create(rise2), Write(rise2_lab))
        self.play(Create(run2), Write(run2_lab))

        new_road = Line(g(-5, 2), g(7, -2), color=PERP, stroke_width=7)
        self.play(Create(new_road), run_time=1.5)
        self.play(Indicate(start, scale_factor=2))
        self.wait(1)

        check = MathTex(
            "3", "\\cdot", "\\left(-\\tfrac{1}{3}\\right)", "=", "-1",
        ).scale(1.1)
        check_cap = Text("Slopes multiply to -1, so the roads are perpendicular", font_size=22, color=YELLOW)
        VGroup(check_cap, check).arrange(DOWN, buff=0.3).move_to(DOWN * 2.9 + RIGHT * CX)
        self.play(FadeIn(check_cap, shift=UP * 0.2), Write(check))

        box = SurroundingRectangle(eq3, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(4)
