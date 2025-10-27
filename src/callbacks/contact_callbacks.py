"""
Callbacks for Contact Us form functionality
"""

from dash import Input, Output, State, html
import os
import json
from datetime import datetime

def register_contact_callbacks(app):
    """Register callbacks for Contact Us modal and form submission"""
    
    @app.callback(
        Output('contact-modal', 'is_open'),
        [Input('contact-us-button', 'n_clicks'),
         Input('contact-close-button', 'n_clicks'),
         Input('contact-submit-button', 'n_clicks')],
        [State('contact-modal', 'is_open'),
         State('contact-name', 'value'),
         State('contact-email', 'value'),
         State('contact-message', 'value')],
        prevent_initial_call=True
    )
    def toggle_contact_modal(open_clicks, close_clicks, submit_clicks, is_open, name, email, message):
        """Toggle the contact modal open/closed"""
        from dash import callback_context
        
        if not callback_context.triggered:
            return is_open
        
        button_id = callback_context.triggered[0]['prop_id'].split('.')[0]
        
        # Open modal when Contact Us button clicked
        if button_id == 'contact-us-button':
            return True
        
        # Close modal when Close button clicked
        if button_id == 'contact-close-button':
            return False
        
        # Close modal after successful submission
        if button_id == 'contact-submit-button':
            # Validate form before closing
            if name and email and message:
                return False  # Close on successful submission
            return True  # Keep open if validation fails
        
        return is_open
    
    @app.callback(
        [Output('contact-form-feedback', 'children'),
         Output('contact-form-feedback', 'className'),
         Output('contact-name', 'value'),
         Output('contact-email', 'value'),
         Output('contact-message', 'value')],
        [Input('contact-submit-button', 'n_clicks')],
        [State('contact-name', 'value'),
         State('contact-email', 'value'),
         State('contact-message', 'value')],
        prevent_initial_call=True
    )
    def handle_contact_form_submission(n_clicks, name, email, message):
        """
        Handle contact form submission
        
        For Render deployment, you have several options:
        1. Use environment variables to configure email service (SendGrid, Mailgun, AWS SES)
        2. Use Formspree or similar service (set FORMSPREE_ENDPOINT env var)
        3. Save to a database (PostgreSQL add-on on Render)
        4. Write to a log file (accessible via Render shell)
        
        This implementation logs to file by default and can be extended with email service.
        """
        if n_clicks is None or n_clicks == 0:
            return '', 'contact-form-feedback', None, None, None
        
        # Validate inputs
        if not name or not email or not message:
            return (
                html.Span('Please fill in all fields.'),
                'contact-form-feedback error',
                name, email, message
            )
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return (
                html.Span('Please enter a valid email address.'),
                'contact-form-feedback error',
                name, email, message
            )
        
        try:
            # Create submission data
            submission = {
                'timestamp': datetime.utcnow().isoformat(),
                'name': name,
                'email': email,
                'message': message
            }
            
            # Method 1: Log to file (works on Render, accessible via shell)
            log_to_file(submission)
            
            # Method 2: Send via email service (optional - requires environment variables)
            # Uncomment and configure if using email service:
            # send_via_email_service(submission)
            
            # Clear form and show success message
            return (
                html.Span('✓ Thank you for your message! We will get back to you soon.'),
                'contact-form-feedback success',
                None,  # Clear name
                None,  # Clear email
                None   # Clear message
            )
            
        except Exception as e:
            print(f"Error submitting contact form: {str(e)}")
            return (
                html.Span('An error occurred. Please try again later.'),
                'contact-form-feedback error',
                name, email, message
            )


def log_to_file(submission):
    """
    Log contact form submission to a file
    On Render, you can access this via: render shell -> cat contact_submissions.log
    """
    try:
        log_file = 'contact_submissions.log'
        with open(log_file, 'a') as f:
            f.write(json.dumps(submission) + '\n')
        print(f"Contact form submission logged: {submission['email']}")
    except Exception as e:
        print(f"Error logging to file: {str(e)}")


def send_via_email_service(submission):
    """
    Send contact form via email service (optional)
    
    To use this on Render:
    1. Add environment variables in Render dashboard:
       - EMAIL_SERVICE (sendgrid, mailgun, or ses)
       - EMAIL_API_KEY (your API key)
       - RECIPIENT_EMAIL (where to send submissions)
    
    2. Add to requirements.txt:
       - sendgrid (for SendGrid)
       - mailgun (for Mailgun)
       - boto3 (for AWS SES)
    
    3. Uncomment the appropriate section below
    """
    
    email_service = os.getenv('EMAIL_SERVICE', '').lower()
    api_key = os.getenv('EMAIL_API_KEY')
    recipient = os.getenv('RECIPIENT_EMAIL')
    
    if not email_service or not api_key or not recipient:
        print("Email service not configured. Using file logging only.")
        return
    
    # SendGrid implementation (uncomment if using)
    """
    if email_service == 'sendgrid':
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        message = Mail(
            from_email='noreply@yourdomain.com',
            to_emails=recipient,
            subject=f'Contact Form Submission from {submission["name"]}',
            html_content=f'''
                <h3>New Contact Form Submission</h3>
                <p><strong>Name:</strong> {submission["name"]}</p>
                <p><strong>Email:</strong> {submission["email"]}</p>
                <p><strong>Message:</strong></p>
                <p>{submission["message"]}</p>
                <p><em>Submitted at: {submission["timestamp"]}</em></p>
            '''
        )
        
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"Email sent via SendGrid: {response.status_code}")
    """
    
    # Mailgun implementation (uncomment if using)
    """
    if email_service == 'mailgun':
        import requests
        
        domain = os.getenv('MAILGUN_DOMAIN')
        
        return requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", api_key),
            data={
                "from": f"Dashboard Contact Form <noreply@{domain}>",
                "to": [recipient],
                "subject": f"Contact Form Submission from {submission['name']}",
                "html": f'''
                    <h3>New Contact Form Submission</h3>
                    <p><strong>Name:</strong> {submission["name"]}</p>
                    <p><strong>Email:</strong> {submission["email"]}</p>
                    <p><strong>Message:</strong></p>
                    <p>{submission["message"]}</p>
                    <p><em>Submitted at: {submission["timestamp"]}</em></p>
                '''
            }
        )
    """
