# Deployment Guide

## Local Development

### Prerequisites
- Python 3.8 or higher
- Git (optional, for version control)

### Setup Instructions

1. **Navigate to the project directory:**
   ```bash
   cd SO_dashboard
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the dashboard:**
   ```bash
   python run.py
   ```
   Or on Windows: double-click `run.bat`

6. **Access the dashboard:**
   Open your browser and go to `http://localhost:8050`

## Production Deployment

### Option 1: Heroku Deployment

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create a Procfile:**
   ```
   web: python app.py
   ```

3. **Update app.py for production:**
   ```python
   if __name__ == '__main__':
       app.run_server(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
   ```

4. **Deploy:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   heroku create your-app-name
   git push heroku main
   ```

### Option 2: Docker Deployment

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8050
   CMD ["python", "app.py"]
   ```

2. **Build and run:**
   ```bash
   docker build -t drm-dashboard .
   docker run -p 8050:8050 drm-dashboard
   ```

### Option 3: Server Deployment (Ubuntu/CentOS)

1. **Install dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-venv nginx
   ```

2. **Set up the application:**
   ```bash
   cd /var/www/
   git clone your-repository drm-dashboard
   cd drm-dashboard
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create systemd service file** (`/etc/systemd/system/drm-dashboard.service`):
   ```ini
   [Unit]
   Description=DRM Dashboard
   After=network.target
   
   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/drm-dashboard
   ExecStart=/var/www/drm-dashboard/venv/bin/python app.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Configure Nginx** (`/etc/nginx/sites-available/drm-dashboard`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8050;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Enable and start services:**
   ```bash
   sudo systemctl enable drm-dashboard
   sudo systemctl start drm-dashboard
   sudo ln -s /etc/nginx/sites-available/drm-dashboard /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

## Environment Variables

Copy `.env.example` to `.env` and update with your configuration:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
- API keys for data sources
- Database connection strings
- Dashboard configuration

## Data Setup

1. **Download sample data:**
   ```bash
   python scripts/download_data.py
   ```

2. **Process data:**
   ```bash
   python scripts/data_processing.py
   ```

3. **Verify data files exist in:**
   - `data/processed/disasters.csv`
   - `data/processed/urbanization.csv`
   - `data/processed/flood_risk.csv`

## Troubleshooting

### Common Issues

1. **Import errors:** Make sure all dependencies are installed
2. **Data not loading:** Check that processed data files exist
3. **Port already in use:** Change the port in `app.py` or environment variables
4. **Memory issues:** Increase server memory for large datasets

### Performance Optimization

1. **Enable caching:**
   ```python
   from flask_caching import Cache
   cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})
   ```

2. **Optimize data loading:**
   - Use parquet files instead of CSV for large datasets
   - Implement data pagination
   - Add database indexing

3. **Static file serving:**
   - Use CDN for assets
   - Enable gzip compression
   - Optimize images

## Monitoring

Consider adding monitoring with:
- Application Performance Monitoring (APM) tools
- Error tracking (Sentry)
- Log aggregation (ELK stack)
- Health check endpoints

## Security

1. **HTTPS:** Always use HTTPS in production
2. **Environment variables:** Never commit sensitive data
3. **Access control:** Implement authentication if needed
4. **Input validation:** Sanitize user inputs
5. **Regular updates:** Keep dependencies updated