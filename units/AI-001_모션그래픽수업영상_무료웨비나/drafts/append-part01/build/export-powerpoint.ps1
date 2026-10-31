$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\User\Documents\ChatGPT\Sci_eum_AIPPT\ppt_harness'
$deckPath = Join-Path $taskRoot 'output\webinar-part01-added\NotionTalk_대표5장유지_Part0_Part1추가_9장_v1.pptx'
$pdfPath = [IO.Path]::ChangeExtension($deckPath,'.pdf')
$sourcePath = Join-Path $taskRoot 'output\webinar-samples\NotionTalk_모션그래픽_주황포인트_자체사례_v5.pptx'
$renderPath = Join-Path $taskRoot 'units\AI-001_모션그래픽수업영상_무료웨비나\renders\append-part01\powerpoint'
$sourceRender = Join-Path $taskRoot 'units\AI-001_모션그래픽수업영상_무료웨비나\renders\append-part01\source'
New-Item -ItemType Directory -Force -Path $renderPath,$sourceRender | Out-Null
$wasRunning = @(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$deck = $null
$source = $null
$app = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    $app.AutomationSecurity = 3
    $deck = $app.Presentations.Open($deckPath, -1, 0, 0)
    if ($deck.Slides.Count -ne 9) { throw 'Unexpected final slide count' }
    $deck.SaveAs($pdfPath, 32)
    for ($page = 1; $page -le $deck.Slides.Count; $page++) {
        $deck.Slides.Item($page).Export((Join-Path $renderPath ('slide-{0:D2}.png' -f $page)), 'PNG', 1920, 1080)
    }
    $source = $app.Presentations.Open($sourcePath, -1, 0, 0)
    for ($page = 1; $page -le $source.Slides.Count; $page++) {
        $source.Slides.Item($page).Export((Join-Path $sourceRender ('slide-{0:D2}.png' -f $page)), 'PNG', 1920, 1080)
    }
    Write-Output 'PowerPoint: opened and exported 9-slide deck; rendered original 5 for visual comparison.'
}
finally {
    if ($null -ne $deck) { $deck.Close(); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck) }
    if ($null -ne $source) { $source.Close(); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($source) }
    if ($null -ne $app) {
        if (-not $wasRunning) { $app.Quit() }
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)
    }
}
