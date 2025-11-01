# Simple Budget Monitor - Manual Check
# Run this script to check your current Google Cloud costs

Write-Host "Checking Google Cloud costs..." -ForegroundColor Cyan

# Get current month's costs
$costs = gcloud billing accounts describe 016525-3B6E8C-9D9C86 --format="value(open)"

# For a more detailed check, let's use the billing export if available
Write-Host "`nCurrent billing status:" -ForegroundColor Yellow
gcloud billing accounts describe 016525-3B6E8C-9D9C86 --format="table(name,open)"

Write-Host "`nTo check detailed costs, visit:" -ForegroundColor Green
Write-Host "https://console.cloud.google.com/billing/016525-3B6E8C-9D9C86/reports?project=wbso-dashboard"

Write-Host "`nBudget Limit: $10/month" -ForegroundColor Red
Write-Host "If you're approaching this limit, run: .\stop-service.ps1" -ForegroundColor Yellow

Write-Host "`nTo monitor costs automatically, check your email for budget alerts!" -ForegroundColor Green