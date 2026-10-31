$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot 'candidate.pptx'
$dest=Join-Path $PSScriptRoot 'native-animation.pptx'
$wasRunning=@(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$app=$null;$deck=$null
try {
 $app=New-Object -ComObject PowerPoint.Application
 $app.AutomationSecurity=3
 $deck=$app.Presentations.Open($source,0,0,0)
 $s=$deck.Slides.Item(9)
 for($i=$s.TimeLine.MainSequence.Count;$i -ge 1;$i--){$s.TimeLine.MainSequence.Item($i).Delete()}
 $fx=$s.TimeLine.MainSequence.AddEffect($s.Shapes.Item('demo-wipe'),22,0,2)
 $fx.EffectParameters.Direction=4;$fx.Timing.Duration=[single]1.1;$fx.Timing.TriggerDelayTime=[single]0.4
 for($i=0;$i -lt 9;$i++){
  $fx=$s.TimeLine.MainSequence.AddEffect($s.Shapes.Item('demo-type-'+$i),1,0,2)
  $fx.Timing.Duration=[single]0.05;$fx.Timing.TriggerDelayTime=[single](0.4+$i*0.2)
 }
 for($i=0;$i -lt 3;$i++){
  $fx=$s.TimeLine.MainSequence.AddEffect($s.Shapes.Item('demo-stagger-'+$i),10,0,2)
  $fx.Timing.Duration=[single]0.5;$fx.Timing.TriggerDelayTime=[single](0.4+$i*0.35)
 }
 if($s.TimeLine.MainSequence.Count -ne 13){throw 'Expected 13 effects on page 9'}
 $deck.SaveAs($dest,24)
 Write-Output 'PowerPoint created 13 native effects for the new page 9 wording.'
}
finally {
 if($null -ne $deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($null -ne $app){if(-not $wasRunning){$app.Quit()};[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
}
