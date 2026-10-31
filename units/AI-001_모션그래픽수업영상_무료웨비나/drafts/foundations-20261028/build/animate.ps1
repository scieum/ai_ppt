$ErrorActionPreference='Stop'
$build=$PSScriptRoot
$source=Join-Path $build 'candidate.pptx'
$dest=Join-Path $build 'native-animation.pptx'
$spec=Get-Content -Raw -Encoding UTF8 (Join-Path $build 'animations.json') | ConvertFrom-Json
$sequence=(Get-Content -Raw -Encoding UTF8 (Join-Path $build 'preservation.json') | ConvertFrom-Json).sequence
$wasRunning=@(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$app=$null;$deck=$null;$records=@()
try {
 $app=New-Object -ComObject PowerPoint.Application
 $app.AutomationSecurity=3
 $deck=$app.Presentations.Open($source,0,0,0)
 foreach($a in $spec){
  $page=[array]::IndexOf($sequence,$a.key)+1
  if($page -lt 1){throw ('No page '+$a.key)}
  $slide=$deck.Slides.Item($page)
  $shape=$slide.Shapes.Item($a.name)
  $trigger=2;$delay=[single]$a.delay
  if($a.name -match '^demo-type-([1-3])$'){$trigger=3;$delay=[single]0.15}
  $effect=$slide.TimeLine.MainSequence.AddEffect($shape,[int]$a.effect,0,$trigger)
  $effect.Timing.Duration=[single]$a.duration
  $effect.Timing.TriggerDelayTime=$delay
  if($null -ne $a.direction){$effect.EffectParameters.Direction=[int]$a.direction}
  if($null -ne $a.decelerate){$effect.Timing.Accelerate=[single]0;$effect.Timing.Decelerate=[single]$a.decelerate}
  $records+=@{page=$page;name=$a.name;effect=[int]$a.effect;duration=$effect.Timing.Duration;delay=$effect.Timing.TriggerDelayTime;trigger=$effect.Timing.TriggerType;decelerate=$effect.Timing.Decelerate;shape_id=$shape.Id}
 }
 $deck.SaveAs($dest,24)
 $records | ConvertTo-Json -Depth 8 | Set-Content -Encoding utf8 (Join-Path $build 'native-animation-report.json')
 Write-Output ('PowerPoint created '+$records.Count+' native animation effects.')
}
finally {
 if($null -ne $deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($null -ne $app){if(-not $wasRunning){$app.Quit()};[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
}
