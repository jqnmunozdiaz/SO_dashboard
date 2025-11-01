# Budget Management & Auto-Shutdown

This folder contains tools to automatically stop your Cloud Run service when the monthly budget exceeds $10.

## 🚨 Quick Manual Controls

### Stop Service Immediately
```powershell
.\stop-service.ps1
```
Stops the Cloud Run service to prevent any charges.

### Restart Service
```powershell
.\restart-service.ps1
```
Restarts the Cloud Run service after it's been stopped.

## 🤖 Automatic Budget Protection

### Setup (One-time)

1. **Enable Cloud Functions API:**
```powershell
gcloud services enable cloudfunctions.googleapis.com pubsub.googleapis.com
```

2. **Deploy the auto-shutdown function:**
```powershell
cd budget-auto-shutdown
.\deploy.ps1
```

3. **Connect to your budget:**
   - Go to: https://console.cloud.google.com/billing/budgets?project=wbso-dashboard
   - Create or edit your budget
   - Set budget to **$10/month**
   - Under "Manage notifications", click "Connect a Pub/Sub topic"
   - Select: **budget-alerts**
   - Set threshold: **100%**
   - Save

### How It Works

1. Google Cloud monitors your spending
2. When you hit $10 (100% of budget), a Pub/Sub message is sent
3. The Cloud Function receives the message
4. It automatically stops your Cloud Run service
5. You receive an email notification

### Cost of Auto-Shutdown

- Cloud Function: **FREE** (2 million invocations/month free tier)
- Pub/Sub: **FREE** (10 GB messages/month free tier)
- Total cost: **$0/month**

## 📊 Monitoring Costs

View current spending:
```powershell
gcloud billing accounts get-billing-info wbso-dashboard
```

Or visit: https://console.cloud.google.com/billing?project=wbso-dashboard

## ⚠️ Important Notes

- **Budget alerts are not instant** - there can be a 1-2 day delay in billing data
- **Manual shutdown is faster** - use `.\stop-service.ps1` if you need immediate action
- **Service can be restarted** - the auto-shutdown doesn't delete anything, just pauses the service
- **You'll get email alerts** at 50%, 90%, and 100% of budget

## 🔄 Recovery After Shutdown

If the service shuts down due to budget:

1. **Check what caused the high cost:**
   - Visit: https://console.cloud.google.com/billing/reports?project=wbso-dashboard

2. **Decide if you want to restart:**
   - If it's month-end, wait for new billing cycle
   - If it's unexpected, investigate first

3. **Restart when ready:**
   ```powershell
   .\restart-service.ps1
   ```

## 💡 Tips to Stay Under Budget

1. **Set min-instances to 0** (default) - scales to zero when not in use
2. **Monitor usage weekly** - check billing reports
3. **Limit max-instances** - prevents runaway scaling
4. **Use caching** - reduces computation time
5. **Optimize Docker image** - smaller = faster deploys = lower costs
