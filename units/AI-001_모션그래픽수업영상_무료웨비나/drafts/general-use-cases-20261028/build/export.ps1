$ErrorActionPreference='Stop'
$taskRoot='C:/Users/User/Documents/ChatGPT/Sci_eum_AIPPT/ppt_harness'
$deckPath=Join-Path $taskRoot 'output/webinar-part1-developed/NotionTalk_Part1_내용디자인고도화_21장_v4.pptx'
$renderPath=Join-Path $taskRoot 'units/AI-001_모션그래픽수업영상_무료웨비나/renders/general-use-cases-20261028'
New-Item -ItemType Directory -Force -Path $renderPath | Out-Null
$wasRunning=@(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$app=$null;$deck=$null
try {
 $app=New-Object -ComObject PowerPoint.Application
 $app.AutomationSecurity=3
 $deck=$app.Presentations.Open($deckPath,-1,0,0)
 if($deck.Slides.Count -ne 21){throw 'Expected 21 slides'}
 $deck.SaveAs([IO.Path]::ChangeExtension($deckPath,'.pdf'),32)
 $bounds=@()
 for($n=1;$n -le $deck.Slides.Count;$n++){
  $slide=$deck.Slides.Item($n)
  $slide.Export((Join-Path $renderPath ('slide-{0:D2}.png' -f $n)),'PNG',1920,1080)
  foreach($shape in $slide.Shapes){
   if($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1){
    $t=$shape.TextFrame2.TextRange
    $bounds+=@{slide=$n;name=$shape.Name;text=$t.Text;shape_left=$shape.Left;shape_top=$shape.Top;shape_width=$shape.Width;shape_height=$shape.Height;text_left=$t.BoundLeft;text_top=$t.BoundTop;text_width=$t.BoundWidth;text_height=$t.BoundHeight}
   }
  }
 }
 $bounds | ConvertTo-Json -Depth 8 | Set-Content -Encoding utf8 (Join-Path $renderPath 'text-bounds.json')
 Write-Output 'PowerPoint opened 21 slides, exported PDF and all slide PNGs.'
}
finally {
 if($null -ne $deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($null -ne $app){if(-not $wasRunning){$app.Quit()};[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
}
