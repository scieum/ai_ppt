$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot 'candidate.pptx'
$dest=Join-Path $PSScriptRoot 'native-animation.pptx'
$spec=Get-Content -Raw -Encoding UTF8 (Join-Path $PSScriptRoot 'animations.json') | ConvertFrom-Json
$rows=Get-Content -Raw -Encoding UTF8 (Join-Path $PSScriptRoot 'additions.json') | ConvertFrom-Json
$wasRunning=@(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$app=$null;$deck=$null
try {
 $app=New-Object -ComObject PowerPoint.Application;$app.AutomationSecurity=3
 $deck=$app.Presentations.Open($source,0,0,0)
 foreach($a in $spec){
  $page=($rows | Where-Object {$_.key -eq $a.key}).page
  $slide=$deck.Slides.Item([int]$page)
  $fx=$slide.TimeLine.MainSequence.AddEffect($slide.Shapes.Item($a.name),[int]$a.effect,0,2)
  $fx.Timing.Duration=[single]$a.duration;$fx.Timing.TriggerDelayTime=[single]$a.delay
 }
 $deck.SaveAs($dest,24)
 Write-Output ('PowerPoint authored '+$spec.Count+' new native effects.')
}
finally {
 if($null -ne $deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($null -ne $app){if(-not $wasRunning){$app.Quit()};[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
}
