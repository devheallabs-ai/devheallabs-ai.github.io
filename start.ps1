param(
    [int]$Port = 9000
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Prefixes.Add("http://127.0.0.1:$Port/")

function Get-ContentType {
    param([string]$Path)

    switch ([System.IO.Path]::GetExtension($Path).ToLowerInvariant()) {
        ".html" { return "text/html; charset=utf-8" }
        ".css" { return "text/css; charset=utf-8" }
        ".js" { return "application/javascript; charset=utf-8" }
        ".json" { return "application/json; charset=utf-8" }
        ".svg" { return "image/svg+xml" }
        ".png" { return "image/png" }
        ".jpg" { return "image/jpeg" }
        ".jpeg" { return "image/jpeg" }
        ".webp" { return "image/webp" }
        ".ico" { return "image/x-icon" }
        default { return "application/octet-stream" }
    }
}

try {
    $listener.Start()
    Write-Host ""
    Write-Host "  DevHeal Labs AI"
    Write-Host "  Local preview running at http://localhost:$Port"
    Write-Host "  Press Ctrl+C to stop."
    Write-Host ""

    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $relativePath = $context.Request.Url.AbsolutePath.TrimStart('/')

        if ([string]::IsNullOrWhiteSpace($relativePath)) {
            $relativePath = 'index.html'
        }

        $filePath = Join-Path $root $relativePath
        if (-not (Test-Path $filePath -PathType Leaf)) {
            $fallback404 = Join-Path $root '404.html'
            if (Test-Path $fallback404 -PathType Leaf) {
                $context.Response.StatusCode = 404
                $filePath = $fallback404
            } else {
                $context.Response.StatusCode = 404
                $buffer = [System.Text.Encoding]::UTF8.GetBytes('Not Found')
                $context.Response.OutputStream.Write($buffer, 0, $buffer.Length)
                $context.Response.Close()
                continue
            }
        }

        $bytes = [System.IO.File]::ReadAllBytes($filePath)
        $context.Response.ContentType = Get-ContentType -Path $filePath
        $context.Response.ContentLength64 = $bytes.LongLength
        $context.Response.OutputStream.Write($bytes, 0, $bytes.Length)
        $context.Response.Close()
    }
}
finally {
    if ($listener.IsListening) {
        $listener.Stop()
    }
    $listener.Close()
}