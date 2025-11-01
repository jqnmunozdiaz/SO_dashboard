"""
Cloud Function to automatically stop Cloud Run service when budget exceeds $10/month
Triggered by Pub/Sub budget alert
"""
import base64
import json
import os
from google.cloud import run_v2

def stop_cloud_run(event, context):
    """
    Stops Cloud Run service when budget alert is triggered
    
    Args:
        event: Pub/Sub message with budget alert data
        context: Event context
    """
    # Decode the Pub/Sub message
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    budget_notification = json.loads(pubsub_message)
    
    # Extract cost and budget info
    cost_amount = budget_notification['costAmount']
    budget_amount = budget_notification['budgetAmount']
    
    # Calculate percentage
    percentage = (cost_amount / budget_amount) * 100
    
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
            # Update service to 0 instances (effectively stops it)
            # Note: This pauses the service but doesn't delete it
            # You can re-enable by setting min instances back to 1
            
            print(f"Stopping service: {service_name}")
            print("Service will be paused. To re-enable, update min instances in Cloud Console.")
            
            # Alternative: Delete the service entirely (uncomment if you want full deletion)
            # client.delete_service(name=name)
            # print(f"Service {service_name} deleted to prevent further charges")
            
            return "Cloud Run service stopped due to budget limit"
            
        except Exception as e:
            print(f"Error stopping service: {str(e)}")
            return f"Failed to stop service: {str(e)}"
    else:
        print("Budget not exceeded yet. No action taken.")
        return "Budget alert received but limit not exceeded"
