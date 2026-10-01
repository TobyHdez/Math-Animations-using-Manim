from alg_common import *


class Q29(Scene):
    """Vertex of f(x) = 3|x - 2| + 7."""

    def construct(self):
        q_card(self, 29)
        self.play(Write(make_title("Question 29: Vertex of an Absolute Value Function")))

        plane = NumberPlane(
            x_range=[-4, 8, 2], y_range=[-1, 16, 4], x_length=5.4, y_length=5.0,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.2, "stroke_opacity": 0.3},
            axis_config={"stroke_color": WHITE, "stroke_width": 2.5},
        ).move_to(LEFT * 3.9 + DOWN * 0.4)
        P = plane.c2p
        nums = VGroup()
        for v in (-2, 2, 4, 6):
            nums.add(MathTex(str(v)).scale(0.4).next_to(P(v, 0), DOWN, buff=0.06))
        for v in (4, 8, 12, 16):
            nums.add(MathTex(str(v)).scale(0.4).next_to(P(0, v), LEFT, buff=0.06))
        self.play(FadeIn(plane), FadeIn(nums))

        # Step 1: the vertex form
        cap = caption("Step 1: Know the vertex form")
        self.play(FadeIn(cap, shift=UP * 0.2))
        gen = MathTex("f(x)", "=", "a", "|x", "-h|", "+k").scale(1.2).move_to(EQ_POS + UP * 1.3)
        gen[2].set_color(GREEN); gen[4].set_color(YELLOW); gen[5].set_color(CONST)
        self.play(Write(gen))
        vtx = MathTex("\\text{vertex} = (h,\\ k)", color=ANSWER).scale(1.0).next_to(gen, DOWN, buff=0.5)
        self.play(FadeIn(vtx, shift=UP * 0.2))
        self.wait(1.5)

        # Step 2: match the pieces
        new_cap = caption("Step 2: Match the pieces")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        f = MathTex("f(x)", "=", "3", "|x", "-2|", "+7").scale(1.2).move_to(EQ_POS + DOWN * 0.45)
        self.play(Write(f))
        f[2].set_color(GREEN); f[4].set_color(YELLOW); f[5].set_color(CONST)
        notes = VGroup(
            MathTex("a = 3", color=GREEN), MathTex("x - 2 \\Rightarrow h = 2", color=YELLOW), MathTex("k = 7", color=CONST),
        ).arrange(RIGHT, buff=0.6).scale(0.85).next_to(f, DOWN, buff=0.45)
        self.play(FadeIn(notes[0], shift=UP * 0.2), Indicate(f[2], color=GREEN))
        self.play(FadeIn(notes[1], shift=UP * 0.2), Indicate(f[4], color=YELLOW))
        self.play(FadeIn(notes[2], shift=UP * 0.2), Indicate(f[5], color=CONST))
        warn = Text("x - 2 means h = +2  (the sign flips)", font_size=26, color=YELLOW).next_to(notes, DOWN, buff=0.35)
        self.play(FadeIn(warn, shift=UP * 0.2))
        self.wait(2)

        # Step 3: graph it
        new_cap = caption("Step 3: Check on the graph")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        self.play(FadeOut(VGroup(gen, vtx, f, notes, warn)))
        graph = VGroup(Line(P(-1.0, 16), P(2, 7)), Line(P(2, 7), P(5, 16))).set_color(RED_C).set_stroke(width=6)
        # clip to the plane: slope 3, so reach y=16 at x = 2 +/- 3
        graph = VGroup(Line(P(-1, 16), P(2, 7)), Line(P(2, 7), P(5, 16))).set_color(RED_C).set_stroke(width=6)
        self.play(Create(graph))
        v = Dot(P(2, 7), color=YELLOW, radius=0.12)
        vl = MathTex("(2,\\ 7)", color=YELLOW).scale(0.7).add_background_rectangle(BLACK, opacity=0.85, buff=0.05)
        vl.next_to(v, UR, buff=0.12)
        self.play(FadeIn(v, scale=3), FadeIn(vl))
        low = Text("The lowest point of the V: vertex (2, 7)", font_size=26, color=YELLOW).move_to(EQ_POS + UP * 0.6)
        chk = MathTex("f(2) = 3|2 - 2| + 7 = 7", color=ANSWER).scale(0.95).move_to(EQ_POS + DOWN * 0.3)
        self.play(FadeIn(low, shift=DOWN * 0.2), Indicate(v, color=YELLOW, scale_factor=2))
        self.play(Write(chk))
        self.wait(2)
        self.play(FadeOut(low), FadeOut(chk))

        # Step 4: choices
        new_cap = caption("Step 4: Match the answer choices")
        self.play(ReplacementTransform(cap, new_cap)); cap = new_cap
        rows = VGroup(
            VGroup(MathTex("A.\\ (2,\\ 7)"), MathTex("\\checkmark", color=GREEN)),
            VGroup(MathTex("B.\\ (-2,\\ 7)"), MathTex("\\times", color=RED), Text("sign of h flipped", font_size=24, color=GREY_B)),
            VGroup(MathTex("C.\\ (7,\\ 2)"), MathTex("\\times", color=RED), Text("h and k swapped", font_size=24, color=GREY_B)),
            VGroup(MathTex("D.\\ (-2,\\ -7)"), MathTex("\\times", color=RED), Text("both signs flipped", font_size=24, color=GREY_B)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.3)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(EQ_POS + UP * 0.1)
        rows[0][0].set_color(ANSWER)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(0.5)
        self.wait(1.5)
        ban = Text("Answer: A   (2, 7)", font_size=32, color=ANSWER)
        box = SurroundingRectangle(ban, color=YELLOW, buff=0.2)
        VGroup(ban, box).move_to(RIGHT * CX + DOWN * 3.1)
        self.play(FadeIn(ban, shift=UP * 0.2), Create(box))
        self.wait(3)
