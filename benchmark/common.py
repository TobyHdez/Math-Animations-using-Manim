"""Shared helpers for the benchmark review videos (house style from CLAUDE.md).

Run scenes from the repo's top folder, e.g.
    python -m manim -ql benchmark/b01_midpoints.py Midpoints
"""
from manim import *

CX = 3.4                          # centre of the right-hand work column
EQ_POS = UP * 0.9 + RIGHT * CX    # equation / work area
STEP_POS = DOWN * 1.8 + RIGHT * CX
EQ_SCALE = 1.0

GIVEN = YELLOW      # given values
ANSWER = GREEN
CONST = ORANGE      # constants being combined
CANCEL = RED        # inverse operations / cancelling
CAP = BLUE          # step captions


def caption(text):
    return Text(text, font_size=28, color=CAP).move_to(STEP_POS)


def make_title(text):
    return Text(text, font_size=30).to_edge(UP)


def eq_tex(*parts):
    """Equation in the work area, split into parts so pieces can be animated."""
    return MathTex(*parts).scale(EQ_SCALE).move_to(EQ_POS)


def question_card(scene, q, hold=4):
    """Show a question exactly as printed on the test (benchmark/q/qNN.png)."""
    img = ImageMobject(f"benchmark/q/q{q:02d}.png")
    img.scale_to_fit_height(6.4)
    if img.width > 12.5:
        img.scale_to_fit_width(12.5)
    label = Text(f"Question {q}", font_size=30, color=BLUE).to_edge(UP)
    scene.play(FadeIn(img), FadeIn(label))
    scene.wait(hold)
    scene.play(FadeOut(img), FadeOut(label))


def answer_banner(scene, text):
    t = Text(text, font_size=32, color=ANSWER)
    box = SurroundingRectangle(t, color=YELLOW, buff=0.2)
    g = VGroup(t, box).move_to(RIGHT * CX + DOWN * 2.9)
    scene.play(FadeIn(t, shift=UP * 0.2), Create(box))
    return g


def slash(m):
    return Line(m.get_corner(DL) + DL * 0.05, m.get_corner(UR) + UR * 0.05,
                color=CANCEL, stroke_width=6)


def op_step(scene, eq, ops, under, mid, result, mapping=None, op_idx=None,
            cancel=(), combine=None):
    """One 'do the same thing to both sides' step, in house style.

    eq       current MathTex on screen
    ops      (left_op_tex, right_op_tex) written in red under each side
    under    (parts_left, parts_right): indices of eq parts to write the ops under
    mid      equation with the operation written in (red parts at op_idx)
    result   simplified equation
    mapping  [(old_index, new_index)] carrying eq parts into mid (None = morph all)
    op_idx   (left, right) indices of the operation parts inside mid
    cancel   indices in mid to slash in red (terms that cancel)
    combine  (indices in mid, label_tex): box in orange with a label, then combine
    """
    centre = eq.get_center()
    op_l = MathTex(ops[0], color=CANCEL).scale(0.9)
    op_r = MathTex(ops[1], color=CANCEL).scale(0.9)
    op_l.next_to(VGroup(*[eq[i] for i in under[0]]), DOWN, buff=0.4)
    op_r.next_to(VGroup(*[eq[i] for i in under[1]]), DOWN, buff=0.4)
    scene.play(FadeIn(op_l, shift=UP * 0.15), FadeIn(op_r, shift=UP * 0.15))
    scene.wait(0.8)

    mid.move_to(centre)
    if op_idx is not None:
        mid[op_idx[0]].set_color(CANCEL)
        mid[op_idx[1]].set_color(CANCEL)
        anims = [ReplacementTransform(eq[o], mid[n]) for o, n in mapping]
        anims += [ReplacementTransform(op_l, mid[op_idx[0]]),
                  ReplacementTransform(op_r, mid[op_idx[1]])]
        scene.play(*anims, run_time=1.4)
        scene.remove(*mid.submobjects)
        scene.add(mid)
    else:
        scene.play(ReplacementTransform(eq, mid), FadeOut(op_l), FadeOut(op_r), run_time=1.4)
    scene.wait(0.6)

    extras = VGroup()
    if cancel:
        extras.add(*[slash(mid[i]) for i in cancel])
        scene.add(extras)
        scene.play(Create(extras), run_time=0.6)
        scene.wait(1)
    if combine:
        idxs, label_tex = combine
        consecutive = all(y - x == 1 for x, y in zip(idxs, idxs[1:]))
        groups = [idxs] if consecutive else [[i] for i in idxs]
        boxes = [SurroundingRectangle(VGroup(*[mid[i] for i in g]), color=CONST, buff=0.08) for g in groups]
        lab = MathTex(label_tex, color=CONST).scale(0.9).next_to(VGroup(*boxes), DOWN, buff=0.3)
        extras.add(*boxes, lab)
        scene.add(extras)
        scene.play(*[Create(bx) for bx in boxes], FadeIn(lab))
        scene.wait(1.2)

    result.move_to(centre)
    scene.play(FadeOut(extras), TransformMatchingTex(mid, result), run_time=1.2)
    scene.wait(1)
    return result
