$ErrorActionPreference='Stop'
$taskRoot='C:/Users/User/Documents/ChatGPT/Sci_eum_AIPPT/ppt_harness'
$taskAssets=Join-Path $taskRoot 'units/AI-001_모션그래픽수업영상_무료웨비나/assets/motion-audio-20261030'
$wasRunning=@(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$app=$null;$deck=$null
try {
 $app=New-Object -ComObject PowerPoint.Application
 $app.AutomationSecurity=3
 $deck=$app.Presentations.Add(0)
 $deck.PageSetup.SlideWidth=960;$deck.PageSetup.SlideHeight=540
 $slide=$deck.Slides.Add(1,12)
 $i=0
 foreach($key in @('silent','with-sound')) {
  $x=170+510*$i
  $shape=$slide.Shapes.AddMediaObject2((Join-Path $taskAssets ($key+'.mp4')),0,-1,$x*.75,405*.75,430*.75,153.57*.75)
  $shape.Name='embedded-video-'+$key
  $shape.MediaFormat.SetDisplayPictureFromFile((Join-Path $taskAssets 'sound-poster.png'))
  $i++
 }
 $deck.SaveAs((Join-Path $taskRoot 'output/motion-audio-build/video-objects.pptx'),24)
 Write-Output 'Created two native embedded video objects with poster frames.'
} finally {
 if($null -ne $deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($null -ne $app){if(-not $wasRunning){$app.Quit()};[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
}
