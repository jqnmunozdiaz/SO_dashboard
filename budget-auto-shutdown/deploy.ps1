# Deploy Budget Auto-Shutdown Cloud Function

Write-Host "Deploying Budget Auto-Shutdown Function..." -ForegroundColor Green

# Create Pub/Sub topic for budget alerts (if it doesn't exist)
Write-Host "`nStep 1: Creating Pub/Sub topic for budget alerts..." -ForegroundColor Cyan
gcloud pubsub topics create budget-alerts --project=wbso-dashboard

# Deploy Cloud Function
Write-Host "`nStep 2: Deploying Cloud Function..." -ForegroundColor Cyan
gcloud functions deploy budget-auto-shutdown `
  --gen2 `
  --runtime python311 `
  --region us-central1 `
  --source budget-auto-shutdown `
  --entry-point stop_cloud_run `
  --trigger-http `
  --allow-unauthenticated `
  --set-env-vars GCP_PROJECT=wbso-dashboard `
  --project wbso-dashboard

# Get the function URL
$functionUrl = gcloud functions describe budget-auto-shutdown --region=us-central1 --format="value(serviceConfig.uri)" --gen2
Write-Host "`nFunction URL: $functionUrl" -ForegroundColor Green

Write-Host "`n✅ Deployment complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Go to: https://console.cloud.google.com/billing/budgets?project=wbso-dashboard"
Write-Host "2. Edit your budget alert"
Write-Host "3. Under 'Manage notifications', click 'Connect a Pub/Sub topic'"
Write-Host "4. Select topic: budget-alerts"
Write-Host "5. Click 'ADD SUBSCRIPTION'"
Write-Host "6. Set Endpoint URL to: $functionUrl"
Write-Host "7. Save the budget"
Write-Host "`nYour Cloud Run service will now automatically stop when you exceed `$10/month!" -ForegroundColor Green
