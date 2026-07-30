# PDFito Build Script
param()

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$outFile = Join-Path $root "js\app.bundle.js"

Write-Host "Generando js/app.bundle.js ..." -ForegroundColor Cyan

$files = @(
  "js\utils\helpers.js",
  "js\utils\favorites.js",
  "js\utils\history.js",
  "js\core\imageProcessor.js",
  "js\core\pdfProcessor.js",
  "js\ui\components.js",
  "js\ui\dashboard.js",
  "js\ui\imageTools.js",
  "js\ui\pdfTools.js",
  "js\app.js"
)

$bundle = [System.Collections.Generic.List[string]]::new()
$bundle.Add("/* PDFito Static Bundle */")
$bundle.Add("(function(window) { 'use strict';")

foreach ($f in $files) {
  $path = Join-Path $root $f
  if (Test-Path $path) {
    $content = Get-Content $path -Raw -Encoding UTF8

    # Remove import lines
    $content = [System.Text.RegularExpressions.Regex]::Replace($content, '(?m)^import\s+.*$', '')
    # Remove export keyword before const/let/var/function/class
    $content = [System.Text.RegularExpressions.Regex]::Replace($content, '\bexport\s+(const|let|var|function|class|async)\b', '$1')
    # Remove export default
    $content = [System.Text.RegularExpressions.Regex]::Replace($content, '\bexport\s+default\b', '')
    # Remove export { ... } blocks
    $content = [System.Text.RegularExpressions.Regex]::Replace($content, '(?s)export\s*\{[^}]*\}\s*;?', '')

    $bundle.Add("/* --- $f --- */")
    $bundle.Add($content)
    $bundle.Add("")
    Write-Host "  OK: $f" -ForegroundColor Green
  } else {
    Write-Host "  MISSING: $f" -ForegroundColor Red
  }
}

$bundle.Add("})(window);")

[System.IO.File]::WriteAllText($outFile, ($bundle -join "`n"), [System.Text.Encoding]::UTF8)

$sizeKB = [math]::Round((Get-Item $outFile).Length / 1KB, 1)
Write-Host ""
Write-Host "Bundle listo: js/app.bundle.js ($sizeKB KB)" -ForegroundColor Green
