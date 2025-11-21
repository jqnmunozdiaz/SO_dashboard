<#
.SYNOPSIS
    Get the maximum memory used by Cloud Run service over the last 30 days.

.DESCRIPTION
    Queries Cloud Monitoring API for peak container memory usage.

.PARAMETER ProjectId
    GCP project ID (defaults to wbso-dashboard)

.PARAMETER ServiceName
    Cloud Run service name (defaults to so-dashboard)

.PARAMETER Region
    Cloud Run region (defaults to us-central1)

.PARAMETER Days
    Number of days to look back (defaults to 30)

.EXAMPLE
    .\Get-CloudRunMemoryMax.ps1
    .\Get-CloudRunMemoryMax.ps1 -Days 7
#>

param(
    [string]$ProjectId = "wbso-dashboard",
    [string]$ServiceName = "so-dashboard",
    [string]$Region = "us-central1",
    [int]$Days = 30
)

$ErrorActionPreference = "Stop"

Write-Host "Fetching memory metrics for $ServiceName in $Region (last $Days days)..." -ForegroundColor Cyan

# Build time range
$end = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$start = (Get-Date).AddDays(-$Days).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# Build filter (Cloud Run memory utilization metric)
$filter = "metric.type=`"run.googleapis.com/container/memory/utilizations`" AND resource.type=`"cloud_run_revision`" AND resource.label.service_name=`"$ServiceName`" AND resource.label.location=`"$Region`""

# Get auth token
$token = gcloud auth print-access-token

if (-not $token) {
    Write-Error "Failed to get auth token. Run 'gcloud auth login'"
    exit 1
}

# Query Monitoring API (using GET with query parameters)
# Note: Memory utilization is a DISTRIBUTION metric, so we query raw data
$encodedFilter = [System.Web.HttpUtility]::UrlEncode($filter)
$uri = "https://monitoring.googleapis.com/v3/projects/$ProjectId/timeSeries?filter=$encodedFilter&interval.startTime=$start&interval.endTime=$end"

Write-Host "Querying Cloud Monitoring API..." -ForegroundColor Gray

try {
    $response = Invoke-RestMethod -Uri $uri -Method Get -Headers @{
        Authorization = "Bearer $token"
    } -ErrorAction Stop

    if (-not $response.timeSeries -or $response.timeSeries.Count -eq 0) {
        Write-Warning "No memory data found for the specified period"
        exit 0
    }

    # Extract max value across all series and points
    # Memory utilization is a percentage (0.0-1.0), we need to convert to bytes using the container limit
    $maxUtilization = 0.0
    $maxRevision = $null
    $maxTime = $null
    $containerLimitBytes = 2GB  # Default 2Gi limit

    foreach ($series in $response.timeSeries) {
        $revision = $series.resource.labels.revision_name
        foreach ($point in $series.points) {
            # Distribution metrics have distributionValue with mean, count, buckets
            if ($point.value.distributionValue) {
                $utilization = $point.value.distributionValue.mean
                if ($utilization -gt $maxUtilization) {
                    $maxUtilization = $utilization
                    $maxRevision = $revision
                    $maxTime = $point.interval.endTime
                }
            } 
            # Fallback for double/int64 value types
            elseif ($point.value.doubleValue) {
                $utilization = $point.value.doubleValue
                if ($utilization -gt $maxUtilization) {
                    $maxUtilization = $utilization
                    $maxRevision = $revision
                    $maxTime = $point.interval.endTime
                }
            }
        }
    }
    
    # Convert utilization (0.0-1.0) to bytes
    $maxBytes = [long]($maxUtilization * $containerLimitBytes)

    # Convert to human-readable
    $mb = [math]::Round($maxBytes / 1MB, 2)
    $gb = [math]::Round($maxBytes / 1GB, 3)
    $utilizationPercent = [math]::Round($maxUtilization * 100, 1)

    Write-Host "`nPeak Memory Usage:" -ForegroundColor Green
    Write-Host "  Utilization: $utilizationPercent% of container limit"
    Write-Host "  Estimated: $maxBytes bytes ($mb MB / $gb GB)"
    Write-Host "  Container Limit: 2048 MB (2 Gi)"
    Write-Host "`nRevision: $maxRevision" -ForegroundColor Gray
    Write-Host "Time: $maxTime" -ForegroundColor Gray

    # Decision guidance
    Write-Host "`nMemory Sizing Guidance:" -ForegroundColor Yellow
    if ($mb -lt 900) {
        $headroom = [math]::Round((1024 - $mb) / 1024 * 100)
        Write-Host "  [OK] Safe to use 1Gi (1024 MB) with ~$headroom% headroom"
    } elseif ($mb -lt 1024) {
        Write-Host "  [WARNING] Borderline for 1Gi. Consider keeping 2Gi or reducing concurrency."
    } else {
        Write-Host "  [DANGER] Keep 2Gi. Peak usage ($mb MB) exceeds 1Gi limit."
    }

} catch {
    Write-Host "`nAPI request failed" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    
    # Try to parse error response
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $reader.DiscardBufferedData()
        $responseBody = $reader.ReadToEnd()
        Write-Host "`nAPI Response:" -ForegroundColor Yellow
        Write-Host $responseBody
    }
    
    Write-Host "`nTips:" -ForegroundColor Yellow
    Write-Host "  - Ensure Cloud Monitoring API is enabled"
    Write-Host "  - Check you have monitoring.timeSeries.list permission"
    Write-Host "  - Verify the service has been deployed and has metrics"
    exit 1
}
