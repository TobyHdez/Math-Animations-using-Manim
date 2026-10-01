# Render every benchmark video at 480p and 1080p and copy the 1080p file beside the 480p one.
# Run from the repo's top folder in PowerShell:  .\benchmark\render_all.ps1
$jobs = @(
    @('b01_midpoints', 'Midpoints'),
    @('b02_angle_sums', 'AngleSums'),
    @('b03_section_ratio', 'SectionRatio'),
    @('b04_number_line_fraction', 'NumberLineFraction'),
    @('b05_logic_forms', 'LogicForms')
)
foreach ($j in $jobs) {
    $f, $c = $j
    $sw = [Diagnostics.Stopwatch]::StartNew()
    python -m manim -ql "benchmark/$f.py" $c 2>&1 | Select-Object -Last 1
    $lo = $sw.Elapsed.TotalSeconds
    python -m manim -qh "benchmark/$f.py" $c 2>&1 | Select-Object -Last 1
    $sw.Stop()
    Copy-Item "media\videos\$f\1080p60\$c.mp4" "media\videos\$f\480p15\${c}_1080p.mp4" -Force
    "{0}: 480p {1:N0}s, total {2:N0}s" -f $c, $lo, $sw.Elapsed.TotalSeconds
}
