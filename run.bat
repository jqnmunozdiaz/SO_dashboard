@echo off
echo Starting Sub-Saharan Africa DRM Dashboard...
echo Activating py313 environment...
call conda activate py313
echo Dashboard will be available at: http://localhost:8050
echo Press Ctrl+C to stop the server

python run.py

pause