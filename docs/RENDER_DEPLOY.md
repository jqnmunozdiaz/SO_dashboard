# Render Deployment Guide

## Quick Deploy to Render

### Option 1: One-Click Deploy (Recommended)

1. **Fork/Clone this repository** to your GitHub account

2. **Connect to Render:**
   - Go to [render.com](https://render.com)
   - Sign up/Login with your GitHub account
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure the service:**
   ```
   Name: drm-dashboard
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```

4. **Set Environment Variables:**
   ```
   ENVIRONMENT=production
   PORT=10000
   PYTHON_VERSION=3.11.0
   ```

5. **Deploy:** Click "Create Web Service"

### Option 2: Using render.yaml (Infrastructure as Code)

1. **Push your code** with the `render.yaml` file to GitHub

2. **Create Render service:**
   - Go to Render Dashboard
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Render will automatically read `render.yaml`

### Option 3: Manual Configuration

1. **Repository Setup:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/drm-dashboard.git
   git push -u origin main
   ```

2. **Render Configuration:**
   - **Service Type:** Web Service
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Instance Type:** Free (for testing) or Starter ($7/month)

## Configuration Files Created

### ✅ `Procfile`
```
web: python app.py
```

### ✅ `render.yaml`
```yaml
services:
  - type: web
    name: drm-dashboard
    env: python
    buildCommand: "./build.sh"
    startCommand: "python app.py"
    plan: free
```

### ✅ `runtime.txt`
```
python-3.11.0
```

### ✅ `build.sh`
```bash
#!/usr/bin/env bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Environment Variables

Set these in your Render service:

| Variable | Value | Description |
|----------|--------|-------------|
| `ENVIRONMENT` | `production` | Disables debug mode |
| `PORT` | `10000` | Port for the web service |
| `PYTHON_VERSION` | `3.11.0` | Python version |

## Post-Deployment

1. **Access your dashboard:** 
   - URL: `https://your-service-name.onrender.com`
   - Example: `https://drm-dashboard.onrender.com`

2. **Check logs:** 
   - Go to Render Dashboard → Your Service → Logs
   - Monitor for any startup issues

3. **Custom Domain (Optional):**
   - Render Dashboard → Your Service → Settings → Custom Domains
   - Add your domain and configure DNS

## Troubleshooting

### Common Issues:

1. **Build Fails:**
   ```bash
   # Check requirements.txt compatibility
   pip install -r requirements.txt --dry-run
   ```

2. **App Won't Start:**
   ```python
   # Ensure PORT environment variable is used
   port = int(os.environ.get('PORT', 8050))
   ```

3. **Memory Issues:**
   - Upgrade to Starter plan ($7/month)
   - Optimize data loading in callbacks

4. **Slow Loading:**
   - Enable caching for data processing
   - Use CDN for static assets

### Debug Steps:

1. **Check Render logs:**
   ```
   Dashboard → Service → Logs
   ```

2. **Test locally:**
   ```bash
   ENVIRONMENT=production PORT=8050 python app.py
   ```

3. **Verify dependencies:**
   ```bash
   pip list
   ```

## Performance Optimization

### For Production:

1. **Update app.py for caching:**
   ```python
   from flask_caching import Cache
   
   cache = Cache(app.server, config={
       'CACHE_TYPE': 'simple',
       'CACHE_DEFAULT_TIMEOUT': 300
   })
   ```

2. **Enable compression:**
   ```python
   app.server.config['COMPRESS_MIMETYPES'] = [
       'text/html', 'text/css', 'application/json',
       'application/javascript'
   ]
   ```

3. **Optimize data loading:**
   - Cache API responses
   - Use efficient data formats (Parquet vs CSV)
   - Implement lazy loading

## Monitoring

### Health Checks:
- Render automatically monitors your service
- Set up uptime monitoring with external services
- Monitor memory and CPU usage in dashboard

### Logging:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## Scaling

### Free Tier Limitations:
- 512MB RAM
- Sleeps after 15 minutes of inactivity
- 750 hours/month

### Paid Plans:
- **Starter ($7/month):** 1GB RAM, no sleep
- **Standard ($25/month):** 2GB RAM, better performance
- **Pro ($85/month):** 4GB RAM, priority support

## Security

### Environment Variables:
```bash
# Never commit these to git
DATABASE_URL=your_database_url
API_KEYS=your_api_keys
SECRET_KEY=your_secret_key
```

### HTTPS:
- Render provides free SSL certificates
- All traffic is automatically encrypted

## Backup Strategy

1. **Code:** Version control with Git
2. **Data:** Regular exports from data sources
3. **Configuration:** Infrastructure as Code with render.yaml

## Support

- **Render Documentation:** https://render.com/docs
- **Community:** https://community.render.com
- **Status:** https://render.com/status