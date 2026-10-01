from alg_common import *


class Q27(Scene):
    """Table x: -2 0 2 4 / y: 11 5 -1 -7 -> equation."""

    def construct(self):
        q_card(self, 27)
        self.play(Write(atitle(27, "Equation From a Table")))

        xs, ys = ["-2", "0", "2", "4"], ["11", "5", "-1", "-7"]
        cells = []
        for i in range(4):
            cx = MathTex(xs[i]).scale(1.1)
            cy = MathTex(ys[i]).scale(1.1)
            col = VGroup(cx, cy).arrange(DOWN, buff=0.45)
            cells.append(col)
        row = VGroup(*cells).arrange(RIGHT, buff=1.4)
        hdr = VGroup(MathTex("x").scale(1.1), MathTex("y").scale(1.1)).arrange(DOWN, buff=0.45)
        table = VGroup(hdr, row).arrange(RIGHT, buff=0.9).move_to(UP * 1.7)
        hdr.align_to(row, DOWN) if False else None
        hdr[0].align_to(cells[0][0], UP); hdr[1].align_to(cells[0][1], UP)
        hdr[0].set_y(cells[0][0].get_y()); hdr[1].set_y(cells[0][1].get_y())
        hline = Line(table.get_left() + LEFT * 0.2, table.get_right() + RIGHT * 0.2).set_y((cells[0][0].get_y() + cells[0][1].get_y()) / 2)
        vline = Line(UP * 0.8, DOWN * 0.8).move_to([(hdr.get_right()[0] + row.get_left()[0]) / 2, table.get_center()[1], 0])
        self.play(Write(table), Create(hline), Create(vline))

        # Step 1: rate of change
        cap = acap("Step 1: Find the rate of change")
        self.play(FadeIn(cap, shift=UP * 0.2))
        arrows = VGroup()
        for i in range(3):
            top = MathTex("+2", color=GREEN).scale(0.8)
            bot = MathTex("-6", color=RED).scale(0.8)
            mx = (cells[i][0].get_center()[0] + cells[i + 1][0].get_center()[0]) / 2
            top.move_to([mx, cells[0][0].get_y() + 0.65, 0])
            bot.move_to([mx, cells[0][1].get_y() - 0.65, 0])
            arrows.add(top, bot)
        self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.1) for a in arrows], lag_ratio=0.12))
        m_eq = aeq("m", "=", "{-6", "\\over", "2}", "=", "-3").move_to(DOWN * 0.45)
        m_eq[6].set_color(GREEN)
        self.play(Write(m_eq))
        self.wait(1.5)

        # Step 2: y-intercept
        cap = next_cap(self, cap, "Step 2: Find the y-intercept")
        self.play(FadeOut(arrows))
        box = SurroundingRectangle(cells[1], color=CONST, buff=0.15)
        b_txt = MathTex("x = 0 \\text{ gives } y = 5, \\text{ so } b = 5", color=CONST).scale(0.9).move_to(DOWN * 1.25)
        self.play(Create(box), FadeIn(b_txt, shift=UP * 0.2))
        self.wait(1.5)

        # Step 3: write the equation
        cap = next_cap(self, cap, "Step 3: Write y = mx + b")
        self.play(FadeOut(m_eq), FadeOut(b_txt))
        gen = aeq("y", "=", "m", "x", "+", "b").move_to(DOWN * 0.1)
        self.play(Write(gen))
        fin = aeq("y", "=", "-3", "x", "+", "5").move_to(DOWN * 0.1)
        fin[2].set_color(GREEN); fin[5].set_color(CONST)
        self.play(TransformMatchingTex(gen, fin))
        self.wait(1.5)

        # Step 4: check
        cap = next_cap(self, cap, "Step 4: Check another point")
        chk = MathTex("x = 4:\\quad -3(4) + 5 = -7 \\ \\checkmark", color=ANSWER).scale(0.95).move_to(DOWN * 1.1)
        self.play(Create(SurroundingRectangle(cells[3], color=ANSWER, buff=0.15)), Write(chk))
        self.wait(2)
        a_banner(self, "Answer: A   y = -3x + 5")
        self.wait(3)
