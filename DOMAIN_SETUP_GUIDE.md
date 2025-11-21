# Custom Domain Setup Guide (Render)
## Sub-Saharan Africa DRM Dashboard

---

## 🎯 Recommended Domain Names

### **Top Picks (Scalable to Other Regions)**
1. **global-drm-dashboard.org** - Scalable worldwide, professional
2. **disaster-risk-monitor.org** - Clear purpose, memorable
3. **resilience-data.org** - Broad appeal, future-proof
4. **drm-platform.org** - Platform focus, expandable
5. **risk-insights.io** - Modern, analytics-focused

---

## 🚀 Setup Instructions for Render.com

Since your application is deployed on Render, setting up a custom domain is straightforward and includes free SSL.

### **Step 1: Purchase Domain**

You can purchase a domain from any registrar. Recommended options:
- **Cloudflare** (Best value, at-cost pricing)
- **Namecheap** (User-friendly)
- **Google Domains** (Integrated)

### **Step 2: Add Domain to Render**

1. Go to your **Render Dashboard**.
2. Select your Web Service (`drm-dashboard`).
3. Click on **Settings** in the left sidebar.
4. Scroll down to the **Custom Domains** section.
5. Click **Add Custom Domain**.
6. Enter your domain name (e.g., `www.your-domain.org` or `your-domain.org`).
7. Click **Save**.

### **Step 3: Configure DNS Records**

Render will provide you with the necessary DNS records. You need to add these to your domain registrar's DNS settings.

#### If using a root domain (e.g., `your-domain.org`):
- **Type:** `A`
- **Name:** `@` (or blank)
- **Value:** `216.24.57.1` (Render's IP - verify in dashboard)

#### If using a subdomain (e.g., `www.your-domain.org`):
- **Type:** `CNAME`
- **Name:** `www`
- **Value:** `drm-dashboard.onrender.com` (Your Render URL)

**Note:** Render recommends using a `CNAME` for `www` and an `A` record for the root domain if your registrar supports it (or CNAME flattening if using Cloudflare).

### **Step 4: Verify SSL Certificate**

Render automatically provisions a Let's Encrypt SSL certificate for your custom domain.
- This process usually takes a few minutes after DNS propagation.
- You can check the status in the **Custom Domains** section of your Render service settings.
- Status will change to "Verified" and "Certificate Issued".

---

## 🔧 Troubleshooting

### Domain not working?
- **Check DNS Propagation:** Use [DNS Checker](https://dnschecker.org) to see if your records have updated globally.
- **Cloudflare Users:** Ensure the "Proxy status" is set to **DNS Only** (gray cloud) initially to allow Render to verify the domain and issue the certificate. You can enable the proxy (orange cloud) later if you configure Full (Strict) SSL in Cloudflare.

### "Certificate provisioning failed"?
- Ensure your DNS records match exactly what Render provided.
- Remove any conflicting A or AAAA records from your DNS settings.

---

## 📞 Support Resources

- **Render Custom Domains Docs:** https://render.com/docs/custom-domains
- **Cloudflare DNS:** https://developers.cloudflare.com/dns/

