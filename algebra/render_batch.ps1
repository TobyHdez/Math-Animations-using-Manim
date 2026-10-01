# Render Algebra benchmark videos at 1080p and copy them into "Algebra Benchmark Practice Videos".
# Run from the repo's top folder in PowerShell, with the question numbers to do:
#     .\algebra\render_batch.ps1 -Questions 1,2,3,4,5
param([int[]]$Questions)
$names = @{
    1 = 'Rearrange_for_P'; 2 = 'Rearrange_for_h'; 3 = 'Solve_for_a'; 4 = 'Solve_for_q'; 5 = 'Solve_Decimal_Equation'
    6 = 'Distribute_Both_Sides'; 7 = 'Distribute_and_Solve'; 8 = 'Decimals_and_Distributing'; 9 = 'First_Step_Distribute'; 10 = 'Parallel_Line_Equation'
    11 = 'Perpendicular_Line_Equation'; 12 = 'Perpendicular_to_a_Graph'; 13 = 'Compound_Inequality_Or'; 14 = 'Graph_to_Compound_Inequality'; 15 = 'Buses_Inequality'
    16 = 'Three_Part_Inequality'; 17 = 'Solve_and_Graph_Inequality'; 18 = 'Sodium_Inequality'; 19 = 'Absolute_Value_Basics'; 20 = 'Absolute_Value_Equation'
    21 = 'Absolute_Value_Two_Cases'; 22 = 'Absolute_Value_Subtract_First'; 23 = 'Absolute_Value_Fractions'; 24 = 'Point_on_a_Line'; 25 = 'Slope_and_Intercept'
    26 = 'Match_Lines_to_Equations'; 27 = 'Equation_From_a_Table'; 28 = 'Graph_to_Equation'; 29 = 'Vertex_of_Absolute_Value'; 30 = 'Vertex_From_a_Table'
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
