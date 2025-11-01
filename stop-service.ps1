# Manual script to stop Cloud Run service

Write-Host "Stopping Cloud Run service: so-dashboard..." -ForegroundColor Yellow

gcloud run services update so-dashboard `
  --region us-central1 `
  --min-instances 0 `
  --max-instances 0 `
  --project wbso-dashboard

Write-Host "`n✅ Service stopped! No more charges will accrue." -ForegroundColor Green
Write-Host "`nTo restart the service, run: .\restart-service.ps1" -ForegroundColor Cyan
