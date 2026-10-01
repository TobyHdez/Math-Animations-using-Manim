# Manim algebra animations: house style

These animations are for teaching algebra students. Follow these rules for every
new solution scene. The reference implementation is
`point_slope_to_slope_intercept.py`; copy its structure and patterns.

## Environment
- Manim Community Edition, Windows. Render from PowerShell (LaTeX must be on PATH):
  `python -m manim -ql <file>.py <SceneName>` for previews, `-qh` for final 1080p.
- Videos land in `media/videos/<file>/480p15/`. Copy the 1080p render beside it as
  `<SceneName>_1080p.mp4`.
- After rendering, extract a contact sheet with ffmpeg and look at it before
  reporting done (overlaps and clipping are the usual bugs).

## Solution-building rules
1. **Layout:** title at top, equation at `UP * 0.7`, blue step caption at a fixed
   `STEP_POS = DOWN * 1.3`. Nothing animates into the title area. Hops, labels, and
   work written under the equation need clear space; never share a spot with the
   blue caption.
2. **One idea per step:** each step gets a blue caption ("Step 2: Add 3 to both
   sides") and the equation transforms with `TransformMatchingTex` so students
   see where each term goes.
   **Caption size:** at least 28pt, and keep each caption under about 40
   characters so it fits the column at that size. Move detail (like the point
   or slope values) into the equation or a short hint line instead of a long
   caption. Map and graph labels (rise/run, points) are at least 26pt with a
   dark semi-transparent background so they read over busy pictures.
3. **Distributing:** the multiplier (green copy) bounces in an arc over each term
   in the parentheses one at a time. Each landing flashes the term and shows a
   small product label ("2 · x = 2x") placed well above the equation, then
   fades. Then transform to the distributed form.
4. **Inverse operations go on BOTH sides:** write the operation (red, e.g. "+3")
   under the left side and under the right side, then move both into the
   equation (`y - 3 + 3 = 2x - 2 + 3`). Never show it on one side only.
5. **Cancelling:** when terms cancel (like -3 + 3), draw a red slash through each
   cancelling term, hold about a second, then fade the slashes while simplifying.
6. **Combining constants:** box the terms in orange, show a label under the box
   ("-2 + 3 = 1"), then transform to the result.
7. **Color code:** yellow = given point/values, green = slope/multiplier,
   orange = y-intercept/constants being combined, red = inverse operations and
   cancelling, blue = step captions.
8. **Final answer:** color the slope (green) and the intercept (orange) in the
   result and label them ("slope m = 2", "y-intercept b = 1").

## Graph and slope rules
9. **Graph as a check:** shrink the algebra into the top-left corner, then draw
   axes, the line, the given point, and the y-intercept with labels.
10. **Rise over run, always in this order:** show the rule text and the fraction
    m = rise/run first. Start at the y-intercept, move VERTICALLY first (rise;
    down for a negative slope), then move RIGHT (run). Pulse the numerator
    before the rise and the denominator before the run. Land on the given
    point and pulse it. Run always goes right, never left.
11. Keep labels clear of axis tick numbers (put the rise label well to the left
    of the y-axis).

## Process
- Use a fixed, hardcoded example per scene unless asked for a template.
- Teacher feedback is final; when asked to change one thing, change only that.
