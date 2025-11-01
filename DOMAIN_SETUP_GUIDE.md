# Custom Domain Setup Guide
## Sub-Saharan Africa DRM Dashboard

---

## 🎯 Recommended Domain Names

### **Top Picks (Scalable to Other Regions)**
1. **global-drm-dashboard.org** - Scalable worldwide, professional
2. **disaster-risk-monitor.org** - Clear purpose, memorable
3. **resilience-data.org** - Broad appeal, future-proof
4. **drm-platform.org** - Platform focus, expandable
5. **risk-insights.io** - Modern, analytics-focused

### **By Category**

#### Global/Scalable (.org - Professional)
- `global-drm-dashboard.org` - Worldwide scope
- `disaster-risk-monitor.org` - Clear monitoring focus
- `resilience-data.org` - Data platform emphasis
- `drm-platform.org` - Platform-oriented
- `disaster-risk-data.org` - Descriptive, professional
- `drm-insights.org` - Analytics angle
- `resilience-monitor.org` - Resilience focus
- `risk-dashboard.org` - Simple, direct
- `disaster-analytics.org` - Data science focus
- `climate-risk-data.org` - Climate + disaster intersection

#### Regional Focus (Currently Africa, Expandable)
- `africa-drm.org` - Start with Africa, add subdomains later
- `africa-resilience.org` - Resilience emphasis
- `drm-africa.org` - DRM-first approach
- `africadrm.org` - Compact
- `africa-risk-platform.org` - Platform approach

#### Tech/Modern (.io/.dev)
- `drm.io` - Ultra short (if available, premium price)
- `risk-insights.io` - Analytics focus
- `disaster-data.io` - Data platform
- `resilience-hub.io` - Community/hub concept
- `drm-platform.dev` - Developer-friendly
- `disaster-risk.dev` - Tech-forward
- `risk-monitor.io` - Monitoring emphasis

#### Commercial/Brandable (.com)
- `disaster-insights.com` - Insights focus
- `resilience-platform.com` - Platform brand
- `drm-global.com` - Global scope
- `risk-analytics.com` - Analytics brand
- `disaster-monitor.com` - Monitoring service

#### Data/Analytics Focus
- `drm-analytics.org` - Analytics platform
- `disaster-risk-insights.org` - Insights emphasis
- `resilience-metrics.org` - Metrics/measurement
- `risk-intelligence.org` - Intelligence focus
- `disaster-data-platform.org` - Full description

#### World Bank Branded (if official)
- `wb-drm.org` - Short, institutional
- `worldbank-drm.org` - Full institutional
- `wb-risk-platform.org` - Platform approach
- `worldbank-resilience.org` - Resilience focus

#### Short/Memorable (Premium if available)
- `drm.io` - Two-letter premium
- `resilience.io` - Single word
- `risk-data.org` - Hyphenated, clear
- `disaster-hub.org` - Hub concept

---

## 💰 Cost Comparison

| Registrar | .com | .org | .io | .dev | Notes |
|-----------|------|------|-----|------|-------|
| **Cloudflare** | $8.57/yr | $9.77/yr | $32.57/yr | $12.03/yr | **Cheapest** - At-cost pricing |
| **Namecheap** | $8.98/yr | $12.98/yr | $32.88/yr | $9.98/yr | User-friendly, frequent sales |
| **Google Domains** | $12/yr | $12/yr | $40/yr | $12/yr | Integrated with GCP |
| **GoDaddy** | $9.99/yr* | $11.99/yr* | $49.99/yr* | $14.99/yr* | *Watch renewal prices! |

**Recommendation**: Use **Cloudflare** or **Namecheap** for best value.

---

## 📦 What's Included (FREE with Cloud Run)

✅ **SSL/HTTPS Certificate** - Automatic, managed by Google  
✅ **Global CDN** - Fast worldwide access  
✅ **DDoS Protection** - Built-in security  
✅ **Auto-scaling** - Pay only for what you use  

**Total Monthly Cost**: Domain (~$1/month) + Cloud Run usage (covered by your $10 budget)

---

## 🚀 Setup Instructions

### **Step 1: Purchase Domain**

#### Option A: Cloudflare (Cheapest)
```
1. Go to: https://www.cloudflare.com/products/registrar/
2. Create free account
3. Search for your domain
4. Purchase (at-cost pricing)
5. DNS automatically configured
```

#### Option B: Namecheap (User-Friendly)
```
1. Go to: https://www.namecheap.com
2. Search domain → Add to cart
3. Purchase (use coupon codes for first year)
4. Access domain dashboard
```

#### Option C: Google Domains (Integrated)
```
1. Go to: https://domains.google.com
2. Search and purchase
3. Linked to your Google account
```

---

### **Step 2: Verify Domain Ownership**

**IMPORTANT**: Before mapping the domain to Cloud Run, you must verify ownership.

#### Option A: Google Search Console (Recommended - Works for any registrar)

```
1. Go to: https://search.google.com/search-console
2. Click "Add Property" → Select "Domain" (not "URL prefix")
3. Enter your domain (e.g., your-domain.org)
4. Google will show a TXT record like:
   google-site-verification=abcdefg123456789
5. Add this TXT record to your domain's DNS:
   - Go to your registrar (Cloudflare/Namecheap/Google Domains)
   - Navigate to DNS settings
   - Add new TXT record:
     * Name/Host: @ (or leave blank)
     * Type: TXT
     * Value: google-site-verification=abcdefg123456789
     * TTL: 3600 (or automatic)
6. Wait 5-10 minutes for DNS propagation
7. Return to Search Console and click "Verify"
8. Once verified, you can proceed to Step 3
```

#### Option B: Cloud Console (Alternative)

```
1. Go to: https://console.cloud.google.com/run/domains/verify?project=wbso-dashboard
2. Enter your domain
3. Follow the verification instructions shown
4. Add the verification record to your DNS
5. Click verify
```

**Verification only needs to be done once per domain!**

---

### **Step 3: Map Domain to Cloud Run**

Once you have the domain, run this PowerShell script:

```powershell
# Replace with your actual domain
.\setup-custom-domain.ps1 -Domain "your-domain.org"
```

This script will:
1. Create domain mapping in Cloud Run
2. Display DNS records you need to configure
3. Guide you through next steps

---

### **Step 4: Configure DNS Records**

After running the script, you'll get output like:

```
NAME                           TYPE    RRDATA
your-domain.org                A       216.239.32.21
your-domain.org                AAAA    2001:db8::1
www.your-domain.org            CNAME   ghs.googlehosted.com
```

**Add these records to your domain registrar:**

#### For Cloudflare:
```
1. Go to Cloudflare Dashboard → DNS
2. Click "Add record"
3. Copy each record from the output
4. Set Proxy status to "DNS only" (gray cloud)
5. Save
```

#### For Namecheap:
```
1. Go to Dashboard → Manage → Advanced DNS
2. Click "Add New Record"
3. Copy each record from the output
4. Save
```

#### For Google Domains:
```
1. Go to DNS → Custom records
2. Click "Manage custom records"
3. Add each record
4. Save
```

---

### **Step 5: Wait for DNS Propagation**

- **Typical time**: 5-30 minutes
- **Maximum**: Up to 48 hours (rare)
- **Check status**: https://dnschecker.org

---

### **Step 6: Verify SSL Certificate**

Google automatically provisions SSL certificate (may take 15-60 minutes):

```powershell
# Check domain mapping status
gcloud run domain-mappings describe YOUR-DOMAIN.org `
  --region=us-central1 `
  --project=wbso-dashboard
```

Look for: `certificateStatus: ACTIVE`

---

## 🔧 Additional Configuration (Optional)

### **Redirect www to root (or vice versa)**

```powershell
# Map www subdomain
.\setup-custom-domain.ps1 -Domain "www.your-domain.org"
```

Then add a Page Rule in Cloudflare to redirect.

### **Add Subdomain for API/Services**

```powershell
# Example: api.your-domain.org
gcloud run domain-mappings create `
  --service=so-dashboard `
  --domain=api.your-domain.org `
  --region=us-central1 `
  --project=wbso-dashboard
```

---

## 🔄 Switching Cloud Providers Later

Your domain is **completely portable**:

1. **Keep the domain** at your registrar (Cloudflare/Namecheap/etc.)
2. **Update DNS records** to point to new service
3. **No downtime** if planned properly

**Example**: Moving from Google Cloud Run → AWS:
```
1. Deploy to AWS
2. Get new DNS records from AWS
3. Update DNS at registrar
4. Wait 5-30 minutes
5. Done! Domain now points to AWS
```

---

## 📊 Cost Estimate Summary

**One-Time Costs:**
- Domain registration: $8-$13 first year
- Renewal: $8-$13/year

**Ongoing Costs:**
- Domain: ~$1/month ($12/year)
- Cloud Run: Already budgeted in your $10/month
- SSL Certificate: $0 (FREE with Cloud Run)
- DNS: $0 (included with registrar)

**Total Additional Cost: ~$1/month**

---

## ✅ Final Checklist

- [ ] Choose domain name
- [ ] Purchase from registrar
- [ ] Run `setup-custom-domain.ps1`
- [ ] Configure DNS records at registrar
- [ ] Wait for DNS propagation (15-60 min)
- [ ] Verify SSL certificate is active
- [ ] Test: https://your-domain.org
- [ ] Update documentation/links

---

## 🆘 Troubleshooting

### Domain not working after 1 hour?
```powershell
# Check DNS propagation
nslookup your-domain.org

# Check domain mapping status
gcloud run domain-mappings describe your-domain.org `
  --region=us-central1 --project=wbso-dashboard
```

### SSL Certificate not provisioning?
- Ensure DNS records are correct (no typos)
- Check that proxy is disabled (Cloudflare: gray cloud, not orange)
- Wait up to 24 hours for Google to verify domain ownership

### "Certificate provisioning failed"?
- Verify all DNS records match exactly
- Remove any conflicting records (old A/AAAA records)
- Delete mapping and recreate:
```powershell
gcloud run domain-mappings delete your-domain.org --region=us-central1
.\setup-custom-domain.ps1 -Domain "your-domain.org"
```

---

## 📞 Support Resources

- **Google Cloud Run Domains**: https://cloud.google.com/run/docs/mapping-custom-domains
- **Cloudflare DNS**: https://developers.cloudflare.com/dns/
- **DNS Checker**: https://dnschecker.org
- **SSL Checker**: https://www.sslshopper.com/ssl-checker.html

---

**Your current service**: https://so-dashboard-3zqmparfua-uc.a.run.app

**Future service**: https://your-chosen-domain.org
