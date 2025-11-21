<#
.SYNOPSIS
    Get the size of the deployed Cloud Run container image.

.DESCRIPTION
    Queries GCR for the latest so-dashboard image digest and reports its size.

.PARAMETER ProjectId
    GCP project ID (defaults to wbso-dashboard)

.PARAMETER ImageName
    Image name (defaults to so-dashboard)

.EXAMPLE
    .\Get-CloudRunImageSize.ps1
    .\Get-CloudRunImageSize.ps1 -ProjectId my-project -ImageName my-service
#>

param(
    [string]$ProjectId = "wbso-dashboard",
    [string]$ImageName = "so-dashboard"
)

$ErrorActionPreference = "Stop"

Write-Host "Fetching image info for gcr.io/$ProjectId/$ImageName..." -ForegroundColor Cyan

# Get the latest digest
$IMAGE = "gcr.io/$ProjectId/$ImageName"
$digestJson = gcloud container images list-tags $IMAGE --limit=1 --sort-by='~TIMESTAMP' --format=json | ConvertFrom-Json

if (-not $digestJson -or $digestJson.Count -eq 0) {
    Write-Error "No images found for $IMAGE"
    exit 1
}

$digest = $digestJson[0].digest
Write-Host "Latest digest: $digest" -ForegroundColor Gray

# Get size in bytes
$sizeJson = gcloud container images describe "$IMAGE@$digest" --format=json | ConvertFrom-Json
$bytes = [long]$sizeJson.image_summary.total_size

if (-not $bytes) {
    Write-Error "Could not retrieve image size"
    exit 1
}

# Convert to human-readable
$mb = [math]::Round($bytes / 1MB, 2)
$gb = [math]::Round($bytes / 1GB, 3)

Write-Host "`nImage Size:" -ForegroundColor Green
Write-Host "  $bytes bytes"
Write-Host "  $mb MB"
Write-Host "  $gb GB"
