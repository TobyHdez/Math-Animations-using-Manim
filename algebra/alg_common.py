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
