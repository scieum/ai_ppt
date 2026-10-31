$ErrorActionPreference='Stop'
$taskBuild='C:/Users/User/Documents/ChatGPT/Sci_eum_AIPPT/ppt_harness/units/AI-001_모션그래픽수업영상_무료웨비나/drafts/reflow-mascots-20261028/build'
$wasRunning=@(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$app=$null;$deck=$null
try {
 $app=New-Object -ComObject PowerPoint.Application
 $app.AutomationSecurity=3
 $deck=$app.Presentations.Open((Join-Path $taskBuild 'playback-reflow.pptx'),-1,0,0)
 $deck.CreateVideo((Join-Path $taskBuild 'playback-reflow.mp4'),$false,4,720,25,80)
 $taskDeadline=(Get-Date).AddMinutes(4)
 do {
  Start-Sleep -Seconds 2
  $taskStatus=$deck.CreateVideoStatus
 } while($taskStatus -in @(1,2) -and (Get-Date) -lt $taskDeadline)
 Write-Output ('PowerPoint video export status: '+$taskStatus)
 if($taskStatus -ne 3){throw 'Playback QA video export did not complete'}
}
finally {
 if($null -ne $deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($null -ne $app){if(-not $wasRunning){$app.Quit()};[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
}
