#!/usr/bin/env python3
"""
Run script for the Sub-Saharan Africa DRM Dashboard
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment variables
os.environ.setdefault('DASH_DEBUG', 'True')
os.environ.setdefault('DASH_HOST', '127.0.0.1')
os.environ.setdefault('DASH_PORT', '8050')

if __name__ == '__main__':
    print("Starting Sub-Saharan Africa DRM Dashboard...")
    print("Dashboard will be available at: http://localhost:8050")
    print("Press Ctrl+C to stop the server")
    
    try:
        from app import app
        app.run(
            debug=os.environ.get('DASH_DEBUG', 'True').lower() == 'true',
            host=os.environ.get('DASH_HOST', '127.0.0.1'),
            port=int(os.environ.get('DASH_PORT', 8050))
        )
    except ImportError as e:
        print(f"Error importing dashboard: {e}")
        print("Please install required dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting dashboard: {e}")
        sys.exit(1)