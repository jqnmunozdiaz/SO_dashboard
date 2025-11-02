# Script to view Pub/Sub messages sent to budget-alerts topic
# This monitors the Cloud Function logs for budget alert processing

Write-Host "`n=== Monitoring Budget Alert Messages ===" -ForegroundColor Green
Write-Host "Topic: projects/wbso-dashboard/topics/budget-alerts" -ForegroundColor Cyan
Write-Host "Function: kill-billing-service-function" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop monitoring`n" -ForegroundColor Yellow

# Get logs from the last 10 minutes and keep refreshing
$lastTimestamp = (Get-Date).AddMinutes(-10).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

while ($true) {
    Write-Host "`n[$(Get-Date -Format 'HH:mm:ss')] Checking for new messages..." -ForegroundColor Gray
    
    # Query for function logs with budget data
    $logs = gcloud logging read @"
resource.type="cloud_run_revision" 
AND resource.labels.service_name="kill-billing-service-function" 
AND timestamp>="$lastTimestamp"
"@ --project=wbso-dashboard --format=json --limit=50 2>$null | ConvertFrom-Json
    
    if ($logs) {
        foreach ($log in $logs) {
            # Update last timestamp
            if ($log.timestamp -gt $lastTimestamp) {
                $lastTimestamp = $log.timestamp
            }
            
            # Display interesting logs
            if ($log.textPayload -or $log.jsonPayload.message) {
                Write-Host "`n----------------------------------------" -ForegroundColor Cyan
                Write-Host "Time: $($log.timestamp)" -ForegroundColor Yellow
                Write-Host "Severity: $($log.severity)" -ForegroundColor $(if ($log.severity -eq 'ERROR') {'Red'} else {'Green'})
                
                if ($log.textPayload) {
                    Write-Host "Message: $($log.textPayload)" -ForegroundColor White
                }
                
                if ($log.jsonPayload.message) {
                    Write-Host "Message: $($log.jsonPayload.message)" -ForegroundColor White
                }
                
                # Show HTTP request details if available
                if ($log.httpRequest) {
                    Write-Host "HTTP Status: $($log.httpRequest.status)" -ForegroundColor $(if ($log.httpRequest.status -eq 200) {'Green'} else {'Red'})
                    Write-Host "Request Size: $($log.httpRequest.requestSize) bytes" -ForegroundColor Gray
                }
            }
        }
    }
    
    # Wait before next check
    Start-Sleep -Seconds 30
}
