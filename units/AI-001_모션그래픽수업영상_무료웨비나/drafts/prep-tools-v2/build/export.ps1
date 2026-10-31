$ErrorActionPreference='Stop'
$root='C:\Users\User\Documents\ChatGPT\Sci_eum_AIPPT\ppt_harness'
$file=Join-Path $root 'output\webinar-part01-added\NotionTalk_대표5장유지_Part0_Part1추가_9장_v2.pptx'
$render=Join-Path $root 'units\AI-001_모션그래픽수업영상_무료웨비나\renders\prep-tools-v2\powerpoint'
New-Item -ItemType Directory -Force -Path $render | Out-Null
$wasRunning=@(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$app=$null
$deck=$null
try {
 $app=New-Object -ComObject PowerPoint.Application
 $app.AutomationSecurity=3
 $deck=$app.Presentations.Open($file,-1,0,0)
 $deck.SaveAs([IO.Path]::ChangeExtension($file,'.pdf'),32)
 for($n=1;$n -le $deck.Slides.Count;$n++) { $deck.Slides.Item($n).Export((Join-Path $render ('slide-{0:D2}.png' -f $n)),'PNG',1920,1080) }
 Write-Output 'PowerPoint exported 9 pages and revised preparation slide.'
} finally {
 if($null -ne $deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($null -ne $app){if(-not $wasRunning){$app.Quit()};[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
}
