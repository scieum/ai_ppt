$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\User\Documents\ChatGPT\Sci_eum_AIPPT\ppt_harness'
$deckPath = Join-Path $taskRoot 'output\webinar-ui-guide\NotionTalk_Part1_실제앱_단계별캡처_v1.pptx'
$pdfPath = Join-Path $taskRoot 'output\webinar-ui-guide\NotionTalk_Part1_실제앱_단계별캡처_v1.pdf'
$renderPath = Join-Path $taskRoot 'units\AI-001_모션그래픽수업영상_무료웨비나\renders\ui-guide\powerpoint'
New-Item -ItemType Directory -Force -Path $renderPath | Out-Null
$wasRunning = @(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$deck = $null
$app = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    $app.AutomationSecurity = 3
    $deck = $app.Presentations.Open($deckPath, -1, 0, 0)
    $deck.SaveAs($pdfPath, 32)
    for ($page = 1; $page -le $deck.Slides.Count; $page++) {
        $deck.Slides.Item($page).Export((Join-Path $renderPath ('slide-{0:D2}.png' -f $page)), 'PNG', 1920, 1080)
    }
    Write-Output ('Opened {0} slides in PowerPoint; exported PDF and PNGs.' -f $deck.Slides.Count)
}
finally {
    if ($null -ne $deck) { $deck.Close(); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck) }
    if ($null -ne $app) {
        if (-not $wasRunning) { $app.Quit() }
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)
    }
}
