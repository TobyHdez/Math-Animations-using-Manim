# Math Animations (Manim)

Algebra and geometry teaching animations made with
[Manim Community Edition](https://www.manim.community/). House-style rules are in
`CLAUDE.md`; day-to-day usage notes are in `INSTRUCTIONS.md`.

## Scenes

| File | Scene class |
|---|---|
| `point_slope_to_slope_intercept.py` | `PointSlopeToSlopeIntercept` |
| `perpendicular_road.py` | `PerpendicularRoad` |
| `glide_reflection.py` | `GlideReflection` |
| `glide_reflection_jkl.py` | `GlideReflectionJKL` |
| `domain_range_segment.py` | `DomainRangeSegment` |

Pictures the scenes use are in `images/`. Rendered videos are not committed
(`media/` and `*.mp4` are git-ignored), so regenerate them as below.

## Setup on a new machine (Windows)

1. Install Python 3 (tested with 3.14).
2. Install Manim:
   ```
   pip install -r requirements.txt
   ```
3. Install LaTeX (needed for all equations). MiKTeX works:
   ```
   winget install MiKTeX.MiKTeX
   ```
   Open a new terminal afterwards so `latex` is on PATH. The first render may
   pause while MiKTeX downloads packages.
4. Optional: install ffmpeg to make contact sheets for checking a render.

Check it works: `python -m manim --version` and `latex --version`.

## Rendering

Run from PowerShell, **in the repo's top folder** (scenes load images by relative
path such as `images/glide_problem.png`):

```
python -m manim -ql glide_reflection.py GlideReflection   # 480p preview
python -m manim -qh glide_reflection.py GlideReflection   # 1080p final
```

Videos are written to `media/videos/<file>/480p15/` (preview) and
`media/videos/<file>/1080p60/` (final). By house style, also copy the 1080p
render next to the preview as `<SceneName>_1080p.mp4`:

```
Copy-Item media\videos\glide_reflection\1080p60\GlideReflection.mp4 media\videos\glide_reflection\480p15\GlideReflection_1080p.mp4
```

If `python -m manim` can't find LaTeX, run from PowerShell (not Git Bash) in a
fresh terminal.
