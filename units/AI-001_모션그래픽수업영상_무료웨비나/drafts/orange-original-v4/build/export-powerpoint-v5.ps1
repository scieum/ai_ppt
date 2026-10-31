$ErrorActionPreference = 'Stop'
$repoRoot = 'C:\Users\User\Documents\ChatGPT\Sci_eum_AIPPT\ppt_harness'
$pptxPath = Join-Path $repoRoot 'output\webinar-samples\NotionTalk_모션그래픽_주황포인트_자체사례_v5.pptx'
$pdfPath = Join-Path $repoRoot 'output\webinar-samples\NotionTalk_모션그래픽_주황포인트_자체사례_v5.pdf'
$nativeRenders = Join-Path $repoRoot 'units\AI-001_모션그래픽수업영상_무료웨비나\renders\orange-original-v4\powerpoint'
New-Item -ItemType Directory -Path $nativeRenders -Force | Out-Null
$existingPowerPoint = @(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$presentation = $null
$application = $null
try {
    $application = New-Object -ComObject PowerPoint.Application
    $application.AutomationSecurity = 3
    $presentation = $application.Presentations.Open($pptxPath, -1, 0, 0)
    $presentation.SaveAs($pdfPath, 32)
    for ($index = 1; $index -le $presentation.Slides.Count; $index++) {
        $imagePath = Join-Path $nativeRenders ('slide-{0:D2}.png' -f $index)
        $presentation.Slides.Item($index).Export($imagePath, 'PNG', 1920, 1080)
    }
    Write-Output ('PowerPoint opened {0} slides; exported PDF and native PNGs.' -f $presentation.Slides.Count)
}
finally {
    if ($null -ne $presentation) {
        $presentation.Close()
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation)
    }
    if ($null -ne $application) {
        if (-not $existingPowerPoint) { $application.Quit() }
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($application)
    }
}




