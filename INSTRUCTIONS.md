# How to use this Manim project

## 1. Where everything lives

```
C:\Users\tob31\Desktop\Manim\
  CLAUDE.md                  <- house-style rules (auto-loaded by Claude Code)
  INSTRUCTIONS.md            <- this file
  images\                    <- put pictures for word problems here
  point_slope_to_slope_intercept.py   <- the reference scene
  media\videos\<scene>\480p15\        <- finished videos (480p + _1080p copy)
```

## 2. Make sure the rules get used

The rules in `CLAUDE.md` are only loaded when Claude Code is **opened in this
folder**.

1. In the Claude desktop app, open the **Code** tab.
2. Choose `C:\Users\tob31\Desktop\Manim` as the working folder.
3. Start a new session there. The rules load automatically.

To check, ask: "What are the house-style rules for this project?" It should
list the both-sides, cancel-slash, bounce, and rise-then-run rules. If it
doesn't, you're in the wrong folder.

When you request a new scene, you can also say "follow the house style in
CLAUDE.md and use point_slope_to_slope_intercept.py as the model."

To add or change a rule, edit `CLAUDE.md` directly, or tell Claude "add a rule
that...". Keep each rule short and specific. Rules that name colors, positions,
and order work best.

## 3. Skills: what they are and where they're saved

A **skill** is a packaged set of instructions Claude loads when a task matches.
They are different from `CLAUDE.md`: `CLAUDE.md` is always loaded for this
folder, while a skill loads only when it's relevant or you call it by name.

| Where | Path | Applies to |
|---|---|---|
| This project only | `C:\Users\tob31\Desktop\Manim\.claude\skills\<skill-name>\SKILL.md` | Sessions opened in this folder |
| All your projects | `C:\Users\tob31\.claude\skills\<skill-name>\SKILL.md` | Everywhere |

Each skill is a folder with one `SKILL.md` file. It starts with a short header
giving the skill's `name` and a `description` of when to use it, followed by the
instructions.

**Skills already available in your setup** (no installation needed) include:
- `k12-education:k12-lesson-plan-creation`, `k12-lesson-prep`,
  `k12-check-for-understanding`, and `k12-lesson-differentiation`
- `anthropic-skills:docx`, `pptx`, `pdf`, and `xlsx` for making handouts, slides,
  and worksheets
- `skill-creator` for building your own skills

To use one, name it in your request, e.g. "Use the check-for-understanding
skill to write an exit ticket for this video," or type `/` followed by the
skill name.

Note: some K-12 connectors (ASSISTments, Canva, MagicSchool, etc.) need to be
authorized in your claude.ai connector settings before their tools work.

**Turning your Manim rules into a skill:** if you want the style to follow you
into other folders, ask: "Use skill-creator to make a skill from the rules in
CLAUDE.md." It will save it under `.claude\skills\` (project) or
`C:\Users\tob31\.claude\skills\` (all projects), whichever you choose.

## 4. Word problems and pictures

Manim can show pictures next to or inside a solution.

- **Your own images:** drop `.png`, `.jpg`, or `.svg` files in the `images\`
  folder and tell Claude the file names and what each one is. PNG with a
  transparent background looks best. Claude places them with `ImageMobject`
  (png/jpg) or `SVGMobject` (svg).
- **Drawn pictures:** Claude can build simple illustrations from Manim shapes:
  a number line, a rectangle for area problems, bars or blocks for
  quantities, coins, a ladder against a wall, a simple graph. These are crisp
  and animate well.
- **Pictures from the word problem:** if the problem is in a PDF or image you
  have, save the picture into `images\` and Claude can use it (or recreate it
  with shapes). Photos or art found online need your OK first, and check that
  you have the right to use them in class.
- **Not available:** Manim can't generate photographs. For a photo, you
  provide the file.

**Word-problem scene pattern**
1. Show the problem text and the picture.
2. Highlight the key numbers in the text and pull them into variables
   (yellow = given values, as in the house style).
3. Write the equation, then solve using the same house-style steps
   (both sides, cancel-slash, bounce for distributing).
4. Show the answer back on the picture and state it in a sentence with units.

**Example request:** "Make a scene for this word problem: a gym charges a $20
sign-up fee plus $15 per month. Use gym.png from the images folder. Follow
the house style."

## 5. Rendering and finding your video

Claude renders for you. To render yourself, open PowerShell in the Manim
folder:

```
python -m manim -ql my_scene.py MySceneName    (quick 480p preview)
python -m manim -qh my_scene.py MySceneName    (1080p final)
```

Videos are saved in `media\videos\my_scene\`. The 1080p copy is also placed next
to the 480p file with `_1080p` added to the name.

## 6. Troubleshooting
- **Overlapping text:** tell Claude the timestamp. It adjusts positions.
- **Old video playing:** close your video player and reopen the file.
- **LaTeX error:** Manim needs MiKTeX. Run from PowerShell, not Git Bash, so it
  finds LaTeX.
- **Rules ignored:** confirm the session was opened in the Manim folder.
