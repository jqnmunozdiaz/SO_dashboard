"""
Cloud Function to automatically stop Cloud Run service when budget exceeds $10/month
Triggered by HTTP request from budget alert via Pub/Sub push
"""
import base64
import json
import os
from google.cloud import run_v2
import functions_framework

@functions_framework.http
def stop_cloud_run(request):
    """
    Stops Cloud Run service when budget alert is triggered
    
    Args:
        request: HTTP request with Pub/Sub push notification
    """
    # Parse the Pub/Sub message from HTTP request
    envelope = request.get_json()
    if not envelope:
        return ('No Pub/Sub message received', 400)

    if 'message' not in envelope:
        return ('Invalid Pub/Sub message format', 400)

    # Decode the message data
    pubsub_message = base64.b64decode(envelope['message']['data']).decode('utf-8')
    
    # Debug: print the raw message
    print(f"Raw Pub/Sub message: {pubsub_message}")
    
    try:
        budget_notification = json.loads(pubsub_message)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        print(f"Message content: {repr(pubsub_message)}")
        # Try to handle it as plain text with simple parsing
        budget_notification = {"costAmount": 0, "budgetAmount": 10}
    
    # Extract cost and budget info
    cost_amount = budget_notification.get('costAmount', 0)
    budget_amount = budget_notification.get('budgetAmount', 10)
    
    # Calculate percentage
    percentage = (cost_amount / budget_amount) * 100 if budget_amount > 0 else 0
    
    print(f"Budget alert: ${cost_amount:.2f} / ${budget_amount:.2f} ({percentage:.1f}%)")
    
    # Only act if we've exceeded 100% of budget
    if percentage >= 100:
        print("Budget exceeded! Stopping Cloud Run service...")
        
        # Initialize Cloud Run client
        client = run_v2.ServicesClient()
        
        # Service details
        project_id = os.environ.get('GCP_PROJECT', 'wbso-dashboard')
        region = 'us-central1'
        service_name = 'so-dashboard'
        
        # Full service name
        name = f"projects/{project_id}/locations/{region}/services/{service_name}"
        
        try:
            print(f"Stopping service: {service_name}")
            
            # Use HTTP REST API to update the service directly
            import google.auth
            from google.auth.transport.requests import Request
            import requests
            
            # Get credentials
            credentials, project = google.auth.default()
            credentials.refresh(Request())
            
            # Prepare the API endpoint (using v1 for Knative annotations)
            api_url = f"https://{region}-run.googleapis.com/apis/serving.knative.dev/v1/namespaces/{project_id}/services/{service_name}"
            
            # First, get the current service
            headers = {
                'Authorization': f'Bearer {credentials.token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(api_url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to get service: {response.text}")
            
            service_data = response.json()
            
            # Update the scaling annotation
            if 'spec' not in service_data:
                service_data['spec'] = {}
            if 'template' not in service_data['spec']:
                service_data['spec']['template'] = {}
            if 'metadata' not in service_data['spec']['template']:
                service_data['spec']['template']['metadata'] = {}
            if 'annotations' not in service_data['spec']['template']['metadata']:
                service_data['spec']['template']['metadata']['annotations'] = {}
            
            # Set max scale to 1 (minimum allowed by Cloud Run)
            service_data['spec']['template']['metadata']['annotations']['autoscaling.knative.dev/maxScale'] = '1'
            
            # Update the service
            response = requests.put(api_url, headers=headers, json=service_data)
            
            if response.status_code in [200, 201]:
                print(f"Service successfully scaled down (maxScale annotation set to 1).")
                print("To re-enable full capacity, run: gcloud run services update so-dashboard --region=us-central1 --max-instances=10 --project=wbso-dashboard")
                return ('Cloud Run service scaled down to max 1 instance due to budget limit', 200)
            else:
                print(f"Failed to update service. Status: {response.status_code}, Response: {response.text}")
                return (f"Failed to stop service: {response.text}", 500)
            
        except Exception as e:
            print(f"Error stopping service: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return (f"Failed to stop service: {str(e)}", 500)
    else:
        print("Budget not exceeded yet. No action taken.")
        return ('Budget alert received but limit not exceeded', 200)
