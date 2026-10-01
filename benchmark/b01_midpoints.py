from common import *


class Midpoints(Scene):
    """Questions 1 and 6: midpoint -> set the two halves equal -> solve -> add."""

    def figure(self, names, exprs):
        xs = [-6.4, -4.0, -1.6]
        y = 0.4
        pts = [np.array([x, y, 0]) for x in xs]
        line = Line(pts[0], pts[2], color=WHITE, stroke_width=5)
        dots = VGroup(*[Dot(p, radius=0.09) for p in pts])
        letters = VGroup(*[MathTex(n).scale(0.9).next_to(p, DOWN, buff=0.25) for n, p in zip(names, pts)])
        labs = VGroup(*[
            MathTex(e, color=GIVEN).scale(0.9).next_to((pts[i] + pts[i + 1]) / 2, UP, buff=0.3)
            for i, e in enumerate(exprs)
        ])
        ticks = VGroup(*[
            Line(UP * 0.15, DOWN * 0.15, color=GREEN, stroke_width=6).move_to((pts[i] + pts[i + 1]) / 2)
            for i in range(2)
        ])
        return pts, line, dots, letters, labs, ticks

    def problem_run(self, q, names, exprs, start, steps, xval, subst_lines, finals, answer):
        a, m, c = names
        title = make_title(f"Question {q}: Midpoint")
        pts, line, dots, letters, labs, ticks = self.figure(names, exprs)
        self.play(Write(title))
        self.play(Create(line), FadeIn(dots), FadeIn(letters))
        self.play(FadeIn(labs))

        # Step 1: midpoint = equal halves
        cap = caption("Step 1: Midpoint = equal halves")
        self.play(FadeIn(cap, shift=UP * 0.2))
        self.play(Create(ticks))
        t1 = Text(f"{m} is the midpoint of {a}{c},", font_size=28, color=GIVEN)
        t2 = Text("so the two halves are equal:", font_size=28, color=GIVEN)
        eq0 = MathTex(f"{a}{m}", "=", f"{m}{c}").scale(EQ_SCALE)
        VGroup(t1, t2, eq0).arrange(DOWN, buff=0.4).move_to(EQ_POS)
        self.play(FadeIn(t1, shift=DOWN * 0.2), FadeIn(t2, shift=DOWN * 0.2))
        self.play(Write(eq0))
        self.wait(1.5)

        # Step 2: write the expressions in
        new_cap = caption("Step 2: Set the halves equal")
        self.play(FadeOut(VGroup(t1, t2)), ReplacementTransform(cap, new_cap))
        cap = new_cap
        self.play(ReplacementTransform(eq0, start))
        self.play(Indicate(labs[0], color=GREEN), Indicate(labs[1], color=GREEN))
        self.wait(1)

        # Steps 3-5: solve, same operation on both sides
        eq = start
        for text, kwargs in steps:
            new_cap = caption(text)
            self.play(ReplacementTransform(cap, new_cap))
            cap = new_cap
            eq = op_step(self, eq, **kwargs)
        self.play(eq[2].animate.set_color(ANSWER))
        self.wait(1)

        # Step 6: substitute back
        new_cap = caption(f"Step 6: Substitute x = {xval}")
        self.play(ReplacementTransform(cap, new_cap), FadeOut(eq))
        cap = new_cap
        lines = VGroup(*[MathTex(s_).scale(1.0) for s_ in subst_lines]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        lines.move_to(EQ_POS)
        self.play(Write(lines[0]))
        self.play(Transform(labs[0], MathTex(finals[0], color=ANSWER).scale(0.9).move_to(labs[0])))
        self.play(Write(lines[1]))
        self.play(Transform(labs[1], MathTex(finals[1], color=ANSWER).scale(0.9).move_to(labs[1])))
        self.wait(0.5)
        brace = Brace(VGroup(dots[0], dots[2]), DOWN, buff=0.75)
        blab = MathTex(f"{a}{c} = {finals[2]}", color=ANSWER).scale(0.9).next_to(brace, DOWN, buff=0.15)
        self.play(Write(lines[2]), GrowFromCenter(brace), FadeIn(blab))
        self.wait(1.5)
        answer_banner(self, answer)
        self.wait(3)
        self.play(*[FadeOut(m_) for m_ in self.mobjects])

    def construct(self):
        # ---------------- Question 1 ----------------
        question_card(self, 1)
        start = eq_tex("2x", "+5", "=", "4x", "-3")
        steps = [
            ("Step 3: Subtract 2x from both sides", dict(
                ops=("-2x", "-2x"), under=([0, 1], [3, 4]),
                mid=eq_tex("{}2x", "+5", "-2x", "=", "4x", "-3", "-2x"),
                mapping=[(0, 0), (1, 1), (2, 3), (3, 4), (4, 5)], op_idx=(2, 6),
                cancel=[0, 2], combine=([4, 6], "4x - 2x = 2x"),
                result=eq_tex("5", "=", "2x", "-3"))),
            ("Step 4: Add 3 to both sides", dict(
                ops=("+3", "+3"), under=([0], [2, 3]),
                mid=eq_tex("5", "+3", "=", "2x", "{}-3", "+3"),
                mapping=[(0, 0), (1, 2), (2, 3), (3, 4)], op_idx=(1, 5),
                cancel=[4, 5], combine=([0, 1], "5 + 3 = 8"),
                result=eq_tex("8", "=", "2x"))),
            ("Step 5: Divide both sides by 2", dict(
                ops=("\\div 2", "\\div 2"), under=([0], [2]),
                mid=eq_tex("{8", "\\over", "2}", "=", "{2x", "\\over", "2}"),
                combine=([0, 1, 2], "8 \\div 2 = 4"),
                result=eq_tex("4", "=", "x"))),
        ]
        self.problem_run(1, ("A", "B", "C"), ("2x+5", "4x-3"), start, steps, 4,
                         ["AB = 2(4) + 5 = 13", "BC = 4(4) - 3 = 13", "AC = 13 + 13 = 26"],
                         ("13", "13", "26"), "Answer: C) 26")

        # ---------------- Question 6 ----------------
        question_card(self, 6)
        start = eq_tex("7x", "-3", "=", "4x", "+12")
        steps = [
            ("Step 3: Subtract 4x from both sides", dict(
                ops=("-4x", "-4x"), under=([0, 1], [3, 4]),
                mid=eq_tex("7x", "-3", "-4x", "=", "{}4x", "+12", "-4x"),
                mapping=[(0, 0), (1, 1), (2, 3), (3, 4), (4, 5)], op_idx=(2, 6),
                cancel=[4, 6], combine=([0, 2], "7x - 4x = 3x"),
                result=eq_tex("3x", "-3", "=", "12"))),
            ("Step 4: Add 3 to both sides", dict(
                ops=("+3", "+3"), under=([0, 1], [3]),
                mid=eq_tex("3x", "{}-3", "+3", "=", "12", "+3"),
                mapping=[(0, 0), (1, 1), (2, 3), (3, 4)], op_idx=(2, 5),
                cancel=[1, 2], combine=([4, 5], "12 + 3 = 15"),
                result=eq_tex("3x", "=", "15"))),
            ("Step 5: Divide both sides by 3", dict(
                ops=("\\div 3", "\\div 3"), under=([0], [2]),
                mid=eq_tex("{3x", "\\over", "3}", "=", "{15", "\\over", "3}"),
                combine=([4, 5, 6], "15 \\div 3 = 5"),
                result=eq_tex("x", "=", "5"))),
        ]
        self.problem_run(6, ("D", "E", "F"), ("7x-3", "4x+12"), start, steps, 5,
                         ["DE = 7(5) - 3 = 32", "EF = 4(5) + 12 = 32", "DF = 32 + 32 = 64"],
                         ("32", "32", "64"), "Answer: C) 64")
