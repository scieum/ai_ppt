$ErrorActionPreference='Stop'
$taskRoot='C:/Users/User/Documents/ChatGPT/Sci_eum_AIPPT/ppt_harness'
$taskBuild=Join-Path $taskRoot 'output/conclusion-bar-build'
$jobs=@(
 @{key='application';file='output/webinar-knowledge-only/NotionTalk_모션그래픽_결론텍스트바_43장_v32.pptx';render='units/AI-001_모션그래픽수업영상_무료웨비나/renders/conclusion-bar-20261030';count=43;pdf=$true}
)
$wasRunning=@(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$app=$null;$deck=$null
try{
 $app=New-Object -ComObject PowerPoint.Application
 $app.AutomationSecurity=3
 foreach($job in $jobs){
  $deckPath=Join-Path $taskRoot $job.file;$renderPath=Join-Path $taskRoot $job.render
  New-Item -ItemType Directory -Force -Path $renderPath|Out-Null
  $deck=$app.Presentations.Open($deckPath,-1,0,0)
  if($deck.Slides.Count -ne $job.count){throw 'Slide count mismatch'}
  if($job.pdf){$deck.SaveAs([IO.Path]::ChangeExtension($deckPath,'.pdf'),32)}
  $bounds=@()
  for($n=1;$n -le $deck.Slides.Count;$n++){
   $slide=$deck.Slides.Item($n);$slide.Export((Join-Path $renderPath ('slide-{0:D2}.png' -f $n)),'PNG',1920,1080)
   foreach($shape in $slide.Shapes){
    if($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1){
     $t=$shape.TextFrame2.TextRange
     $bounds+=@{slide=$n;name=$shape.Name;text=$t.Text;shape_left=$shape.Left;shape_top=$shape.Top;shape_width=$shape.Width;shape_height=$shape.Height;text_left=$t.BoundLeft;text_top=$t.BoundTop;text_width=$t.BoundWidth;text_height=$t.BoundHeight}
    }
   }
  }
  $bounds|ConvertTo-Json -Depth 8|Set-Content -Encoding utf8 (Join-Path $taskBuild ($job.key+'-text-bounds.json'))
  $deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck);$deck=$null
  Write-Output ('Rendered '+$job.count+' slides for '+$job.key)
 }
}finally{
 if($null -ne $deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($null -ne $app){if(-not $wasRunning){$app.Quit()};[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
}

