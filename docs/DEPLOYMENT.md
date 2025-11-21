# Deployment Guide

## Local Development

### Prerequisites
- Python 3.10 or higher
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
   python app.py
   ```
   Or on Windows: double-click `run.bat`

6. **Access the dashboard:**
   Open your browser and go to `http://localhost:8050`

## Production Deployment

### Render.com (Recommended)

See [RENDER_DEPLOY.md](RENDER_DEPLOY.md) for detailed instructions.

### Generic Server Deployment (Ubuntu/CentOS)

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
   Environment="PORT=8050"
   Environment="ENVIRONMENT=production"
   
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

Create a `.env` file or set these in your deployment environment:

- `ENVIRONMENT`: Set to `production` to disable debug mode.
- `PORT`: The port the app should listen on (default: 8050).
- `PYTHON_VERSION`: 3.10.0 or higher.

## Data Setup

The dashboard relies on processed data in the `data/processed/` directory. Ensure these files are present in your deployment.

1. **EM-DAT Data:** `data/processed/african_disasters_emdat.csv`
2. **WDI Data:** `data/processed/wdi/*.csv`
3. **Urban Projections:** `data/processed/UNDESA_Country/*.csv`
4. **Flood Data:** `data/processed/flood/*.csv`

## Troubleshooting

### Common Issues

1. **Import errors:** Make sure all dependencies are installed (`pip install -r requirements.txt`).
2. **Data not loading:** Check that processed data files exist in the correct paths.
3. **Port already in use:** Change the port in `app.py` or environment variables.
