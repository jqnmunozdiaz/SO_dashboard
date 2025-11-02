# Script to send a test budget alert message
# This publishes a message to the budget-alerts Pub/Sub topic

param(
    [decimal]$CostAmount = 2.5,
    [decimal]$BudgetAmount = 10.0
)

$percentage = [math]::Round(($CostAmount / $BudgetAmount) * 100, 1)

Write-Host "`n=== Sending Test Budget Alert ===" -ForegroundColor Green
Write-Host "Cost: `$$CostAmount" -ForegroundColor Cyan
Write-Host "Budget: `$$BudgetAmount" -ForegroundColor Cyan
Write-Host "Percentage: $percentage%" -ForegroundColor $(if ($percentage -ge 100) {'Red'} else {'Yellow'})
Write-Host "`nThis will trigger the budget function..." -ForegroundColor Yellow

# Create the message payload (simplified version)
$message = @{
    costAmount = $CostAmount
    budgetAmount = $BudgetAmount
} | ConvertTo-Json -Compress

Write-Host "`nMessage payload: $message" -ForegroundColor Gray

# Publish to Pub/Sub topic
gcloud pubsub topics publish budget-alerts --message=$message --project=wbso-dashboard

Write-Host "`n✓ Message published successfully!" -ForegroundColor Green
Write-Host "`nTo view function response, run:" -ForegroundColor Yellow
Write-Host "  .\view-pubsub-messages.ps1" -ForegroundColor Cyan
