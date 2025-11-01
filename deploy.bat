@echo off
echo ========================================
echo Cloud Run Deployment
echo ========================================
echo.
echo This will take 5-10 minutes.
echo Please DO NOT close this window!
echo.

gcloud run deploy so-dashboard --source . --platform managed --region us-central1 --allow-unauthenticated --port 8080 --memory 2Gi --cpu 2 --timeout 300 --max-instances 10 --set-env-vars ENVIRONMENT=production

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
pause
