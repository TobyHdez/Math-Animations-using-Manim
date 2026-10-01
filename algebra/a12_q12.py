from alg_common import *


class Q12(Scene):
    """Which equation is perpendicular to the graphed line?  (line from (-5,-2) to (4,7))"""

    def construct(self):
        q_card(self, 12)
        self.play(Write(make_title("Question 12: Perpendicular to a Graph")))

        plane = NumberPlane(
            x_range=[-8, 8, 2], y_range=[-8, 8, 2], x_length=5.0, y_length=5.0,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.2, "stroke_opacity": 0.3},
            axis_config={"stroke_color": WHITE, "stroke_width": 2.5},
        ).move_to(LEFT * 3.9 + DOWN * 0.4)
        P = plane.c2p
        nums = VGroup()
        for v in (-6, -4, -2, 2, 4, 6):
            nums.add(MathTex(str(v)).scale(0.4).next_to(P(v, 0), DOWN, buff=0.06))
            nums.add(MathTex(str(v)).scale(0.4).next_to(P(0, v), LEFT, buff=0.06))
        line = Line(P(-5, -2), P(4, 7), color=RED_C, stroke_width=6)
        self.play(FadeIn(plane), FadeIn(nums))
        self.play(Create(line))

        # Step 1: slope of the graphed line (rise first, then run right)
        cap = caption("Step 1: Find the slope of the line")
        self.play(FadeIn(cap, shift=UP * 0.2))
        a, b = (-3, 0), (0, 3)
        da, db = Dot(P(*a), color=YELLOW, radius=0.07), Dot(P(*b), color=YELLOW, radius=0.07)
        la = MathTex("(-3,0)", color=YELLOW).scale(0.55).add_background_rectangle(BLACK, opacity=0.85, buff=0.04)
        lb = MathTex("(0,3)", color=YELLOW).scale(0.55).add_background_rectangle(BLACK, opacity=0.85, buff=0.04)
        la.next_to(da, DR, buff=0.08)
        lb.next_to(db, UL, buff=0.08)
        rule = Text("Rise first, then run right", font_size=26, color=GREEN).move_to(EQ_POS + UP * 1.2)
        fr = MathTex("m", "=", "{\\text{rise}", "\\over", "\\text{run}}", "=", "{3", "\\over", "3}", "=", "1").scale(1.0)
        fr.move_to(EQ_POS)
        fr.set_color(GREEN)
        fr[0].set_color(WHITE); fr[1].set_color(WHITE)
        self.play(FadeIn(da), FadeIn(db), FadeIn(la), FadeIn(lb), FadeIn(rule, shift=DOWN * 0.2), Write(VGroup(*fr[:5])))
        rise = Line(P(*a), P(-3, 3), color=GREEN, stroke_width=7)
        run = Line(P(-3, 3), P(*b), color=GREEN, stroke_width=7)
        self.play(Create(rise))
        self.play(Write(VGroup(*fr[5:7])), Indicate(fr[6], color=YELLOW, scale_factor=1.4))
        self.play(Create(run))
        self.play(Write(VGroup(*fr[7:9])), Indicate(fr[8], color=YELLOW, scale_factor=1.4))
        self.play(Write(VGroup(*fr[9:])))
        self.wait(1.5)
        self.play(FadeOut(VGroup(rise, run, da, db, la, lb, rule, fr)))

        # Step 2: perpendicular slope
        new_cap = caption("Step 2: Find the perpendicular slope")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        grp = flip_slope(self, 1, 1, pos=EQ_POS, hint_pos=EQ_POS + DOWN * 1.4)
        why = Text("Opposite reciprocal of 1 is -1", font_size=26, color=GREEN).move_to(EQ_POS + DOWN * 2.1)
        self.play(FadeIn(why, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(grp), FadeOut(why))

        # Step 3: test the choices
        new_cap = caption("Step 3: Which choice has slope -1?")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        rows = VGroup(
            VGroup(MathTex("A.\\ y = -x + 5"), Text("slope -1", font_size=26, color=GREEN), MathTex("\\checkmark", color=GREEN)),
            VGroup(MathTex("B.\\ y = x - 4"), Text("slope 1  (parallel)", font_size=26, color=GREY_B), MathTex("\\times", color=RED)),
            VGroup(MathTex("C.\\ y = \\tfrac{1}{2}x + 3"), Text("slope 1/2", font_size=26, color=GREY_B), MathTex("\\times", color=RED)),
            VGroup(MathTex("D.\\ y = 2x + 1"), Text("slope 2", font_size=26, color=GREY_B), MathTex("\\times", color=RED)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.3)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(EQ_POS + DOWN * 0.1)
        rows[0][0].set_color(ANSWER)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(0.5)
        perp = Line(P(-2, 7), P(6, -1), color=GREEN, stroke_width=6)
        self.play(Create(perp))
        sq = Square(side_length=0.3, color=GREEN, stroke_width=4).move_to(P(1, 4))
        corner = RightAngle(Line(P(1, 4), P(2, 5)), Line(P(1, 4), P(2, 3)), length=0.3, color=YELLOW, quadrant=(1, 1))
        self.play(Create(corner))
        self.wait(1.5)
        a_banner_r = Text("Answer: A   y = -x + 5", font_size=32, color=ANSWER)
        box = SurroundingRectangle(a_banner_r, color=YELLOW, buff=0.2)
        VGroup(a_banner_r, box).move_to(RIGHT * CX + DOWN * 3.1)
        self.play(FadeIn(a_banner_r, shift=UP * 0.2), Create(box))
        self.wait(3)
