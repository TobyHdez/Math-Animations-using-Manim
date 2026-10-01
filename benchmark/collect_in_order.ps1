# Copy every finished 1080p benchmark video into one folder, numbered by the first
# question each video covers, so they play in the order of the practice test.
# Run from the repo's top folder in PowerShell:  .\benchmark\collect_in_order.ps1
$out = "benchmark_videos_in_order"
New-Item -ItemType Directory -Force $out | Out-Null
$map = @(
    @('01_Q01+Q06_Midpoints',                  'b01_midpoints',            'Midpoints'),
    @('02_Q02-05_Parallel_Lines',              'b06_parallel_lines',       'ParallelLines'),
    @('07_Q07+Q22_Angle_Sums',                 'b02_angle_sums',           'AngleSums'),
    @('08_Q08-11_Constructions',               'b07_constructions',        'Constructions'),
    @('12_Q12-15_Logic_Forms',                 'b05_logic_forms',          'LogicForms'),
    @('16_Q16-18_Transformations',             'b08_transformations_a',    'TransformationsA'),
    @('19_Q19+Q20_Segment_Ratio',              'b03_section_ratio',        'SectionRatio'),
    @('21_Q21+Q28_Proofs',                     'b09_proofs',               'Proofs'),
    @('23_Q23+Q24_Fraction_of_the_Way',        'b04_number_line_fraction', 'NumberLineFraction'),
    @('25_Q25-27+Q29_Transformation_Sequences','b10_transformation_sequences', 'TransformationSequences')
)
foreach ($m in $map) {
    $src = "media\videos\$($m[1])\480p15\$($m[2])_1080p.mp4"
    if (Test-Path $src) { Copy-Item $src "$out\$($m[0]).mp4" -Force; "ok   $($m[0])" } else { "MISSING $src" }
}
