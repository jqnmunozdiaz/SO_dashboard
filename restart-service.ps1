# Manual script to restart Cloud Run service

Write-Host "Restarting Cloud Run service: so-dashboard..." -ForegroundColor Yellow

gcloud run services update so-dashboard `
  --region us-central1 `
  --min-instances 0 `
  --max-instances 10 `
  --project wbso-dashboard

Write-Host "`n✅ Service restarted and available!" -ForegroundColor Green
Write-Host "Your dashboard is live at: https://so-dashboard-[hash]-uc.a.run.app" -ForegroundColor Cyan
Write-Host "`nTo stop the service again, run: .\stop-service.ps1" -ForegroundColor Cyan
