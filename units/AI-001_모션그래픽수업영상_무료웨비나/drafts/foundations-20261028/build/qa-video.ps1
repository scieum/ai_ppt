$ErrorActionPreference='Stop'
$build=$PSScriptRoot
$app=$null;$deck=$null
$wasRunning=@(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
try {
 $app=New-Object -ComObject PowerPoint.Application
 $app.AutomationSecurity=3
 $deck=$app.Presentations.Open((Join-Path $build 'native-animation.pptx'),0,0,0)
 for($i=$deck.Slides.Count;$i -ge 1;$i--){if($i -notin @(4,6,7,8,9)){$deck.Slides.Item($i).Delete()}}
 $deck.CreateVideo((Join-Path $build 'effect-playback-check.mp4'),$true,5,720,15,80)
 $timer=[Diagnostics.Stopwatch]::StartNew()
 while($deck.CreateVideoStatus -in @(1,2)){
  if($timer.Elapsed.TotalSeconds -gt 150){throw 'Video verification export timed out'}
  Start-Sleep -Milliseconds 500
 }
 $status=$deck.CreateVideoStatus
 if($status -ne 3){throw ('Video export status '+$status)}
 $deck.Saved=-1
 Write-Output 'Exported five animated demonstration slides as a playback check MP4.'
}
finally {
 if($null -ne $deck){$deck.Saved=-1;$deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($null -ne $app){if(-not $wasRunning){$app.Quit()};[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
}
