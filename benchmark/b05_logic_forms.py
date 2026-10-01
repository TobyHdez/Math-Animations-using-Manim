from common import *

XL = -3.9            # left edge of the statement boxes
Y_P, Y_Q = 0.9, -0.75
P_COL, Q_COL = YELLOW, ORANGE


def sbox(text, color):
    t = Text(text, font_size=30)
    r = RoundedRectangle(corner_radius=0.15, width=max(t.width + 0.6, 3.6), height=t.height + 0.45, color=color, stroke_width=4)
    t.move_to(r)
    g = VGroup(r, t)
    return g


def cap_top(text):
    return Text(text, font_size=28, color=CAP).move_to(UP * 2.45)


class LogicForms(Scene):
    """Questions 12-15: converse, contrapositive, and truth values."""

    # ---- building blocks -------------------------------------------------
    def statement(self, p_text, q_text):
        pb, qb = sbox(p_text, P_COL), sbox(q_text, Q_COL)
        pb.move_to([XL + pb[0].width / 2, Y_P, 0])
        qb.move_to([XL + qb[0].width / 2, Y_Q, 0])
        t_if = Text("If", font_size=30, color=P_COL).move_to([XL - 0.6, Y_P, 0])
        t_then = Text("then", font_size=30, color=Q_COL).move_to([XL - 0.85, Y_Q, 0])
        arrow = Arrow(UP * (Y_P - 0.6) + LEFT * 5.0, UP * (Y_Q + 0.6) + LEFT * 5.0, buff=0, color=GREY_B, stroke_width=4) if False else None
        return pb, qb, t_if, t_then

    def not_tag(self, box):
        tag = Text("NOT", font_size=26, color=RED)
        tag.next_to(box, UP, aligned_edge=LEFT, buff=0.06)
        return tag

    def swap(self, pg, qg):
        vp = np.array([XL + pg[0].width / 2, Y_Q, 0]) - pg[0].get_center()
        vq = np.array([XL + qg[0].width / 2, Y_P, 0]) - qg[0].get_center()
        self.play(pg.animate(path_arc=-PI / 2).shift(vp), qg.animate(path_arc=-PI / 2).shift(vq), run_time=1.8)

    def readout(self, text, color=GREEN):
        t = Text(text, font_size=30, color=color).move_to(DOWN * 2.2)
        self.play(FadeIn(t, shift=UP * 0.2))
        return t

    def show_others(self, items):
        grp = VGroup(*[Text(s, font_size=26, color=GREY_B) for s in items]).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(DOWN * 2.3)
        self.play(FadeIn(grp, shift=UP * 0.2))
        return grp

    # ---- mini lesson -----------------------------------------------------
    def lesson(self):
        title = make_title("Converse and Contrapositive")
        self.play(Write(title))
        specs = [
            ("Conditional", "\\text{If } P\\text{, then } Q", None, 1.3),
            ("Converse", "\\text{If } Q\\text{, then } P", "swap P and Q", 0.0),
            ("Contrapositive", "\\text{If not } Q\\text{, then not } P", "swap AND say 'not'", -1.3),
        ]
        groups = []
        for name, tex, note, y in specs:
            lab = Text(name, font_size=30, color=WHITE)
            lab.move_to([-6.2 + lab.width / 2, y, 0])
            f = MathTex(tex).scale(1.15)
            f.set_color_by_tex("P", P_COL)
            f.set_color_by_tex("Q", Q_COL)
            f.move_to([1.2 + f.width / 2 - 0.6, y, 0])
            g = VGroup(lab, f)
            if note:
                n = Text(note, font_size=26, color=GREEN).next_to(f, DOWN, buff=0.12, aligned_edge=LEFT)
                g.add(n)
            groups.append(g)
        for g in groups:
            self.play(FadeIn(g, shift=UP * 0.2))
            self.wait(0.8)
        tip = Text("A conditional and its contrapositive are always both true or both false.", font_size=26, color=YELLOW)
        tip.move_to(DOWN * 3.0)
        self.play(FadeIn(tip, shift=UP * 0.2))
        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects])

    # ---- one question ----------------------------------------------------
    def converse_q(self, q, p_text, q_text, result, others, answer, part=""):
        question_card(self, q)
        title = make_title(f"Question {q}: Converse")
        self.play(Write(title))
        pb, qb, t_if, t_then = self.statement(p_text, q_text)
        cap = cap_top("Step 1: Find the hypothesis (P) and conclusion (Q)")
        self.play(FadeIn(cap, shift=UP * 0.2))
        self.play(FadeIn(t_if), FadeIn(pb), FadeIn(t_then), FadeIn(qb))
        self.wait(2)
        new_cap = cap_top("Step 2: Converse = swap P and Q")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        self.swap(pb, qb)
        self.wait(1)
        r = self.readout(result)
        self.wait(2.5)
        return title, cap, [pb, qb, t_if, t_then, r]

    def finish(self, title, cap, extra, others, answer):
        self.play(FadeOut(extra[-1]))
        grp = self.show_others(others)
        self.wait(2.5)
        self.play(FadeOut(grp))
        answer_banner_c(self, answer)
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def construct(self):
        self.lesson()

        # ---------------- Question 12 ----------------
        title, cap, ex = self.converse_q(
            12, "a figure is a rhombus", "it is a quadrilateral with\nfour congruent sides",
            "If a figure is a quadrilateral with four congruent sides,\nthen it is a rhombus.", None, None)
        self.finish(title, cap, ex,
                    ["A: swaps AND says 'not'  (that's the inverse)",
                     "C: says 'not' AND swaps  (that's the contrapositive)",
                     "D: changes the conclusion"], "Answer: B")

        # ---------------- Question 13 ----------------
        title, cap, ex = self.converse_q(
            13, "a polygon is a regular hexagon", "it has 6 sides",
            "If a polygon has 6 sides, then it is a regular hexagon.", None, None)
        self.play(FadeOut(ex[-1]))
        ban = Text("Part A: A", font_size=32, color=ANSWER)
        box = SurroundingRectangle(ban, color=YELLOW, buff=0.2)
        g = VGroup(ban, box).move_to(DOWN * 3.3)
        self.play(FadeIn(ban), Create(box))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])
        # Part B: is the converse true?
        new_title = make_title("Question 13 Part B: Is the converse true?")
        self.play(ReplacementTransform(title, new_title))
        conv = Text("If a polygon has 6 sides, then it is a regular hexagon.", font_size=30, color=GREEN).move_to(UP * 2.2)
        self.play(FadeIn(conv, shift=DOWN * 0.2))
        cap = cap_top("Look for a counterexample")
        cap.move_to(UP * 1.4)
        self.play(FadeIn(cap, shift=UP * 0.2))
        reg = RegularPolygon(6, color=WHITE, stroke_width=5).scale(1.2).move_to(LEFT * 3.3 + DOWN * 0.7)
        pts = [np.array([p[0], p[1], 0.0]) for p in [(0.5, 1.3), (1.9, 0.7), (1.7, -0.9), (0.0, -1.2), (-1.4, -0.6), (-1.1, 0.8)]]
        irr = Polygon(*[p + np.array([3.3, -0.7, 0.0]) for p in pts], color=ORANGE, stroke_width=5)
        l1 = Text("6 sides, all equal", font_size=26, color=WHITE).next_to(reg, DOWN, buff=0.3)
        l2 = Text("6 sides, NOT equal", font_size=26, color=ORANGE).next_to(irr, DOWN, buff=0.3)
        self.play(Create(reg), FadeIn(l1))
        self.play(Create(irr), FadeIn(l2))
        verdict = Text("It has 6 sides but is not regular, so the converse is FALSE.", font_size=28, color=YELLOW)
        verdict.move_to(DOWN * 2.9)
        self.play(FadeIn(verdict, shift=UP * 0.2))
        self.wait(2.5)
        ban = Text("Part B: B  (False)", font_size=32, color=ANSWER)
        box = SurroundingRectangle(ban, color=YELLOW, buff=0.2)
        self.play(FadeOut(verdict), FadeIn(ban.move_to(DOWN * 3.3)), Create(box.move_to(DOWN * 3.3)))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ---------------- Question 14 ----------------
        self.contra_q(14, "two angles are vertical angles", "they are congruent",
                      "If two angles are not congruent,\nthen they are not vertical angles.",
                      ["A: only swaps  (that's the converse)",
                       "B: only says 'not'  (that's the inverse)",
                       "D: says 'not' on just one part"], "Answer: C", truth=None)

        # ---------------- Question 15 ----------------
        self.contra_q(15, "two lines are perpendicular", "they intersect to form\na right angle",
                      "If two lines do not intersect to form a right angle,\nthen they are not perpendicular.",
                      None, "Answer: A  (TRUE)", truth=True)

    # ---- contrapositive questions ---------------------------------------
    def contra_q(self, q, p_text, q_text, result, others, answer, truth):
        question_card(self, q)
        title = make_title(f"Question {q}: Contrapositive")
        self.play(Write(title))
        pb, qb, t_if, t_then = self.statement(p_text, q_text)
        cap = cap_top("Step 1: Find the hypothesis (P) and conclusion (Q)")
        self.play(FadeIn(cap, shift=UP * 0.2))
        self.play(FadeIn(t_if), FadeIn(pb), FadeIn(t_then), FadeIn(qb))
        self.wait(2)
        new_cap = cap_top("Step 2: Put 'not' on both parts")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        n1, n2 = self.not_tag(pb), self.not_tag(qb)
        self.play(FadeIn(n1, shift=DOWN * 0.1), FadeIn(n2, shift=DOWN * 0.1))
        self.wait(1)
        new_cap = cap_top("Step 3: Swap them")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        pg, qg = VGroup(pb, n1), VGroup(qb, n2)
        self.swap(pg, qg)
        self.wait(1)
        r = self.readout(result)
        self.wait(2.5)
        self.play(FadeOut(r))
        if truth is None:
            grp = self.show_others(others)
            self.wait(2.5)
            self.play(FadeOut(grp))
        else:
            new_cap = cap_top("Step 4: Is it true or false?")
            self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
            t = VGroup(
                Text("The original is TRUE: perpendicular lines", font_size=28, color=YELLOW),
                Text("do form right angles.", font_size=28, color=YELLOW),
                Text("A contrapositive has the same truth value,", font_size=28, color=GREEN),
                Text("so the contrapositive is TRUE.", font_size=28, color=GREEN),
            ).arrange(DOWN, buff=0.22).move_to(DOWN * 2.65)
            self.play(FadeIn(t[0], shift=UP * 0.2), FadeIn(t[1], shift=UP * 0.2))
            self.wait(1.5)
            self.play(FadeIn(t[2], shift=UP * 0.2), FadeIn(t[3], shift=UP * 0.2))
            self.wait(2.5)
            self.play(FadeOut(t))
        answer_banner_c(self, answer)
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


def answer_banner_c(scene, text):
    t = Text(text, font_size=32, color=ANSWER)
    box = SurroundingRectangle(t, color=YELLOW, buff=0.2)
    g = VGroup(t, box).move_to(DOWN * 3.3)
    scene.play(FadeIn(t, shift=UP * 0.2), Create(box))
    return g
