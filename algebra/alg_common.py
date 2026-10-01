"""Shared helpers for the Algebra 1 benchmark videos (centered layout, house style from CLAUDE.md).

Run scenes from the repo's top folder, e.g.
    python -m manim -ql algebra/a01_q01.py Q01
Question images are expected in algebra/q/qNN.png (made with benchmark/extract_questions.py).
"""
from base_common import *  # noqa: F401,F403  (op_step, slash, colors, ...; copied from the geometry helpers)

AEQ = UP * 0.9        # equation row (centered; there is no diagram on the left)
ACAP = DOWN * 1.9     # blue step caption
ABAN = DOWN * 3.1     # answer banner


def acap(text):
    return Text(text, font_size=28, color=CAP).move_to(ACAP)


def aeq(*parts, scale=1.3):
    return MathTex(*parts).scale(scale).move_to(AEQ)


def atitle(q, topic):
    return Text(f"Question {q}: {topic}", font_size=30).to_edge(UP)


def q_card(scene, q, hold=4):
    """Show the question exactly as printed on the test."""
    img = ImageMobject(f"algebra/q/q{q:02d}.png")
    img.scale_to_fit_height(min(6.2, 6.2))
    if img.width > 12.5:
        img.scale_to_fit_width(12.5)
    label = Text(f"Question {q}", font_size=30, color=CAP).to_edge(UP)
    scene.play(FadeIn(img), FadeIn(label))
    scene.wait(hold)
    scene.play(FadeOut(img), FadeOut(label))


def a_banner(scene, text):
    t = Text(text, font_size=32, color=ANSWER)
    box = SurroundingRectangle(t, color=YELLOW, buff=0.2)
    g = VGroup(t, box).move_to(ABAN)
    scene.play(FadeIn(t, shift=UP * 0.2), Create(box))
    return g


def next_cap(scene, cap, text):
    new = acap(text)
    scene.play(ReplacementTransform(cap, new))
    return new


def check_step(scene, cap, lines, colors=None):
    """'Check it' step: a few MathTex lines under the work area."""
    new = acap("Check it with numbers")
    scene.play(ReplacementTransform(cap, new))
    grp = VGroup(*[MathTex(s).scale(0.95) for s in lines]).arrange(DOWN, buff=0.55).move_to(AEQ + UP * 0.1)
    for i, m in enumerate(grp):
        scene.play(Write(m), run_time=1.0)
    scene.wait(1.5)
    return new, grp


def distribute(scene, eq, mult, targets, products, new_eq):
    """House-style distributing: the multiplier (green copy) bounces over each term
    in the parentheses one at a time, flashing it and showing the product above."""
    two = eq[mult].copy().set_color(GREEN)
    scene.add(two)
    for t, prod in zip(targets, products):
        scene.play(two.animate(path_arc=-PI * 0.8).move_to(eq[t].get_top() + UP * 0.9), run_time=0.9)
        lab = MathTex(prod, color=GREEN).scale(0.9).move_to(eq.get_center() + UP * 1.5)
        scene.play(Indicate(eq[t], color=GREEN), FadeIn(lab, shift=DOWN * 0.2))
        scene.wait(0.8)
        scene.play(FadeOut(lab))
    scene.play(FadeOut(two))
    scene.play(TransformMatchingTex(eq, new_eq))
    scene.wait(0.8)
    return new_eq


def make_frac(n, d, color=WHITE, scale=1.3):
    """Hand-built fraction so the numerator/denominator can be animated."""
    num = MathTex(n, color=color).scale(scale)
    den = MathTex(d, color=color).scale(scale)
    bar = Line(LEFT * 0.35, RIGHT * 0.35, color=color, stroke_width=3)
    num.next_to(bar, UP, buff=0.12)
    den.next_to(bar, DOWN, buff=0.12)
    return VGroup(num, bar, den)


def flip_slope(scene, n, d, pos=None, hint_pos=None, result_sign="-"):
    """m = n/d  ->  flip it, then change the sign  ->  m_perp = -d/n.
    Returns a group holding everything on screen so the caller can fade it out."""
    pos = AEQ if pos is None else pos
    hint_pos = (pos + DOWN * 1.5) if hint_pos is None else hint_pos
    lhs = MathTex("m", "=").scale(1.3)
    fr = make_frac(str(n), str(d), color=GREEN)
    row = VGroup(lhs, fr).arrange(RIGHT, buff=0.3).move_to(pos)
    scene.play(Write(lhs), FadeIn(fr))
    scene.wait(1)
    hint = Text("Flip it, then change the sign", font_size=28, color=YELLOW).move_to(hint_pos)
    scene.play(FadeIn(hint, shift=UP * 0.2))
    num, bar, den = fr
    num_pos, den_pos = num.get_center(), den.get_center()
    scene.play(num.animate(path_arc=PI).move_to(den_pos), den.animate(path_arc=PI).move_to(num_pos), run_time=1.4)
    scene.wait(0.8)
    new_lhs0 = MathTex("m_{\perp}").scale(1.3).move_to(lhs[0])
    minus = MathTex(result_sign, color=GREEN).scale(1.5).next_to(fr, LEFT, buff=0.12).shift(RIGHT * 0.3)
    scene.play(ReplacementTransform(lhs[0], new_lhs0), fr.animate.shift(RIGHT * 0.3), Write(minus))
    scene.wait(1.5)
    return VGroup(new_lhs0, lhs[1], fr, minus, hint)


def op_step_n(scene, eq, ops, under, mid, result, mapping, op_idx, cancel=(), combine=()):
    """Like op_step but for any number of parts (e.g. -3 < x - 4 <= 5: do it to all three).
    ops: list of op tex; under: list of index-lists of eq; op_idx: where each op lands in mid;
    combine: list of (indices, label_tex) boxed in orange."""
    centre = eq.get_center()
    labels = [MathTex(o, color=CANCEL).scale(0.9).next_to(VGroup(*[eq[i] for i in u]), DOWN, buff=0.4)
              for o, u in zip(ops, under)]
    scene.play(*[FadeIn(l, shift=UP * 0.15) for l in labels])
    scene.wait(0.8)
    mid.move_to(centre)
    for i in op_idx:
        mid[i].set_color(CANCEL)
    anims = [ReplacementTransform(eq[o], mid[n]) for o, n in mapping]
    anims += [ReplacementTransform(l, mid[i]) for l, i in zip(labels, op_idx)]
    scene.play(*anims, run_time=1.4)
    scene.remove(*mid.submobjects)
    scene.add(mid)
    scene.wait(0.6)
    extras = VGroup()
    if cancel:
        extras.add(*[slash(mid[i]) for i in cancel])
        scene.add(extras)
        scene.play(Create(extras), run_time=0.6)
        scene.wait(1)
    for idxs, label_tex in combine:
        consecutive = all(y - x == 1 for x, y in zip(idxs, idxs[1:]))
        groups = [idxs] if consecutive else [[i] for i in idxs]
        boxes = [SurroundingRectangle(VGroup(*[mid[i] for i in g]), color=CONST, buff=0.08) for g in groups]
        lab = MathTex(label_tex, color=CONST).scale(0.8).next_to(VGroup(*boxes), DOWN, buff=0.3)
        extras.add(*boxes, lab)
        scene.add(extras)
        scene.play(*[Create(b) for b in boxes], FadeIn(lab))
    scene.wait(1.2)
    result.move_to(centre)
    scene.play(FadeOut(extras), TransformMatchingTex(mid, result), run_time=1.2)
    scene.wait(1)
    return result


def open_circle(pos, color=YELLOW, r=0.14):
    return Circle(radius=r, color=color, stroke_width=5, fill_color=BLACK, fill_opacity=1).move_to(pos)


def closed_circle(pos, color=YELLOW, r=0.14):
    return Dot(pos, color=color, radius=r)
