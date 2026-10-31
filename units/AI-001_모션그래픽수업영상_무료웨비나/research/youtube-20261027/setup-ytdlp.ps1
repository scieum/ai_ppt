$ErrorActionPreference='Stop'
$research=Split-Path -Parent $MyInvocation.MyCommand.Path
$toolDir=Join-Path $research 'toolchain/yt-dlp-2026.10.26'
$keyring=Join-Path $toolDir 'gpg-home'
New-Item -ItemType Directory -Force -Path $toolDir,$keyring | Out-Null
$gpg='C:/Program Files/Git/usr/bin/gpg.exe'
$release='https://github.com/yt-dlp/yt-dlp/releases/download/2026.10.26'
foreach($name in @('SHA2-256SUMS','SHA2-256SUMS.sig','SHA2-512SUMS','SHA2-512SUMS.sig','yt-dlp.exe')) {
 $file=Join-Path $toolDir $name
 if(-not (Test-Path -LiteralPath $file)) {
  & curl.exe -fL --silent --show-error --connect-timeout 15 --max-time 180 --output $file "$release/$name"
  if($LASTEXITCODE -ne 0){throw "Download failed: $name"}
 }
}
$publicKey=Join-Path $toolDir 'public.key'
$keyResponse=Join-Path $toolDir 'public-key-response.json'
& curl.exe -fL --silent --show-error --connect-timeout 15 --max-time 60 --output $keyResponse 'https://api.github.com/repos/yt-dlp/yt-dlp/contents/public.key'
if($LASTEXITCODE -ne 0){throw 'Public key download failed'}
$keyObject=Get-Content -Raw -LiteralPath $keyResponse | ConvertFrom-Json
if($keyObject.encoding -ne 'base64'){throw 'Unexpected official key encoding'}
[IO.File]::WriteAllBytes($publicKey,[Convert]::FromBase64String($keyObject.content))
Set-Location -LiteralPath $toolDir
& $gpg --homedir './gpg-home' --batch --import './public.key' 2>&1 | Out-File -LiteralPath (Join-Path $toolDir 'key-import.log') -Encoding utf8
if($LASTEXITCODE -ne 0){throw 'Public key import failed'}
$checks=@()
foreach($bits in @(256,512)) {
 $manifest=Join-Path $toolDir "SHA2-${bits}SUMS"
 $signature=$manifest+'.sig'
 $status= & $gpg --homedir './gpg-home' --batch --status-fd 1 --verify "SHA2-${bits}SUMS.sig" "SHA2-${bits}SUMS" 2>&1
 $exit=$LASTEXITCODE
 $status | Out-File -LiteralPath (Join-Path $toolDir "verify-$bits.log") -Encoding utf8
 if($exit -ne 0 -or -not ($status -match '\[GNUPG:\] VALIDSIG ')){throw "OpenPGP signature verification failed: SHA$bits"}
 $line=Get-Content -LiteralPath $manifest | Where-Object { $_ -match '^([a-fA-F0-9]+)\s+\*?yt-dlp\.exe$' }
 if(@($line).Count -ne 1){throw "Missing unique executable checksum: SHA$bits"}
 $expected=([regex]::Match($line,'^([a-fA-F0-9]+)')).Groups[1].Value
 $actual=(Get-FileHash -LiteralPath (Join-Path $toolDir 'yt-dlp.exe') -Algorithm "SHA$bits").Hash
 if($expected -ine $actual){throw "Executable checksum mismatch: SHA$bits"}
 $checks += @{algorithm="SHA$bits";signature_valid=$true;expected=$expected;actual=$actual;matched=$true}
 Write-Output "SHA$bits manifest: valid OpenPGP signature; yt-dlp.exe checksum matched."
}
$version= & (Join-Path $toolDir 'yt-dlp.exe') --version
if($LASTEXITCODE -ne 0){throw 'Verified yt-dlp could not run'}
@{version=$version;download_url="$release/yt-dlp.exe";public_key_url='https://api.github.com/repos/yt-dlp/yt-dlp/contents/public.key';key_transport_note='The official raw endpoint failed a Windows Schannel revocation availability check. Retrieved the identical repository file through the official GitHub contents API with normal TLS verification.';gpg_executable=$gpg;keyring=$keyring;checks=$checks} | ConvertTo-Json -Depth 6 | Out-File -LiteralPath (Join-Path $toolDir 'verification.json') -Encoding utf8
Write-Output "Verified yt-dlp version: $version"
