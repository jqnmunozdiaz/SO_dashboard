# Setup Custom Domain for Cloud Run Service
# Replace YOUR-DOMAIN.COM with your actual domain

param(
    [Parameter(Mandatory=$true)]
    [string]$Domain
)

Write-Host "Setting up custom domain: $Domain" -ForegroundColor Green

# Step 1: Map domain to Cloud Run service
Write-Host "`nStep 1: Creating domain mapping..." -ForegroundColor Cyan
gcloud beta run domain-mappings create `
  --service=so-dashboard `
  --domain=$Domain `
  --region=us-central1 `
  --project=wbso-dashboard

# Step 2: Get DNS records that need to be configured
Write-Host "`nStep 2: Getting DNS configuration..." -ForegroundColor Cyan
Write-Host "Copy these DNS records to your domain registrar:" -ForegroundColor Yellow

gcloud beta run domain-mappings describe $Domain `
  --region=us-central1 `
  --project=wbso-dashboard `
  --format="table(status.resourceRecords[].name,status.resourceRecords[].type,status.resourceRecords[].rrdata)"

Write-Host "`n✅ Domain mapping created!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Go to your domain registrar (Cloudflare/Namecheap/Google Domains)"
Write-Host "2. Add the DNS records shown above"
Write-Host "3. Wait 5-60 minutes for DNS propagation"
Write-Host "4. Your dashboard will be available at: https://$Domain"
Write-Host "`nSSL certificate will be automatically provisioned by Google Cloud (FREE)!" -ForegroundColor Green
