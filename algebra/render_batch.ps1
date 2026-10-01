# Render Algebra benchmark videos at 1080p and copy them into "Algebra Benchmark Practice Videos".
# Run from the repo's top folder in PowerShell, with the question numbers to do:
#     .\algebra\render_batch.ps1 -Questions 1,2,3,4,5
param([int[]]$Questions)
$names = @{
    1 = 'Rearrange_for_P'; 2 = 'Rearrange_for_h'; 3 = 'Solve_for_a'; 4 = 'Solve_for_q'; 5 = 'Solve_Decimal_Equation'
}
$out = "Algebra Benchmark Practice Videos"
New-Item -ItemType Directory -Force $out | Out-Null
foreach ($q in $Questions) {
    $n = "{0:D2}" -f $q
    $file = (Get-ChildItem algebra -Filter "a${n}_q${n}.py").BaseName
    $cls = "Q$n"
    $sw = [Diagnostics.Stopwatch]::StartNew()
    python -m manim -qh "algebra/$file.py" $cls 2>&1 | Select-Object -Last 1
    $label = if ($names.ContainsKey($q)) { $names[$q] } else { 'Video' }
    Copy-Item "media\videos\$file\1080p60\$cls.mp4" "$out\Q${n}_$label.mp4" -Force
    "{0}: {1:N0}s" -f $cls, $sw.Elapsed.TotalSeconds
}
