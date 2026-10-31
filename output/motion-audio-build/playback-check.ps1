$ErrorActionPreference='Stop'
$taskBuild='C:/Users/User/Documents/ChatGPT/Sci_eum_AIPPT/ppt_harness/output/motion-audio-build'
$wasRunning=@(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$app=$null;$deck=$null
try {
 $app=New-Object -ComObject PowerPoint.Application;$app.AutomationSecurity=3
 $deck=$app.Presentations.Open((Join-Path $taskBuild 'candidate.pptx'),-1,0,0)
 $deck.SaveCopyAs((Join-Path $taskBuild 'playback-check.pptx'),24)
 $deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)
 $deck=$app.Presentations.Open((Join-Path $taskBuild 'playback-check.pptx'),0,0,0)
 for($i=$deck.Slides.Count;$i -ge 1;$i--){if($i -notin @(14,15,16,19)){$deck.Slides.Item($i).Delete()}}
 foreach($slide in $deck.Slides){
  $slide.SlideShowTransition.AdvanceOnTime=-1;$slide.SlideShowTransition.AdvanceTime=5
  foreach($shape in $slide.Shapes){if($shape.Name -like 'embedded-video-*'){$shape.AnimationSettings.PlaySettings.PlayOnEntry=-1}}
 }
 $deck.Save()
 $deck.CreateVideo((Join-Path $taskBuild 'playback-check.mp4'),-1,5,720,20,80)
 $timer=[Diagnostics.Stopwatch]::StartNew()
 do {Start-Sleep -Milliseconds 500;$status=$deck.CreateVideoStatus} while($status -in @(1,2) -and $timer.Elapsed.TotalSeconds -lt 180)
 if($status -ne 3){throw ('Video export status '+$status)}
 Write-Output 'PowerPoint rendered the four motion/video test slides to MP4.'
} finally {
 if($null -ne $deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($null -ne $app){if(-not $wasRunning){$app.Quit()};[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
}
