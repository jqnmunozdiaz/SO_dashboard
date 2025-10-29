"""
Callbacks for Contact Us form functionality
"""

from dash import Input, Output, State, html
import os
import json
from datetime import datetime

def register_contact_callbacks(app):
    """Register callbacks for Contact Us modal and form submission"""
    
    # Open disclaimer once per browser session
    @app.callback(
        [Output('disclaimer-modal', 'is_open', allow_duplicate=True),
         Output('disclaimer-session-store', 'data')],
        Input('disclaimer-session-store', 'data'),
        State('disclaimer-modal', 'is_open'),
        prevent_initial_call='initial_duplicate'
    )
    def show_disclaimer_once_per_session(session_data, current_open):
        """On first load of a session, keep disclaimer open and mark as shown; otherwise keep it closed."""
        # If we've already shown it this session, ensure it's closed
        if isinstance(session_data, dict) and session_data.get('shown'):
            return False, session_data
        # First load in this session: keep whatever initial state the layout set (True) and record as shown
        return current_open, {'shown': True}
    
    @app.callback(
        Output('disclaimer-modal', 'is_open'),
        [Input('disclaimer-button', 'n_clicks'),
         Input('disclaimer-close-button', 'n_clicks')],
        [State('disclaimer-modal', 'is_open')],
        prevent_initial_call=True
    )
    def toggle_disclaimer_modal(open_clicks, close_clicks, is_open):
        """Toggle the disclaimer modal open/closed"""
        from dash import callback_context
        
        if not callback_context.triggered:
            return is_open
        
        button_id = callback_context.triggered[0]['prop_id'].split('.')[0]
        
        # Open modal when Disclaimer button clicked
        if button_id == 'disclaimer-button':
            return True
        
        # Close modal when Close button clicked
        if button_id == 'disclaimer-close-button':
            return False
        
        return is_open
    
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
            # Validate form before closing - only close if name and message are provided
            if name and message:
                # Also check email is valid if provided
                if email and ('@' not in email or '.' not in email):
                    return True  # Keep open if email is invalid
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
        Handle contact form submission via Formspree
        
        Submissions are sent to Formspree (https://formspree.io/f/xovpjdbq)
        which forwards them to your email and provides a web dashboard.
        Also logs to file as backup.
        """
        if n_clicks is None or n_clicks == 0:
            return '', 'contact-form-feedback', None, None, None
        
        # Validate required inputs (only name and message are required)
        if not name or not message:
            return (
                html.Span('Please fill in your name and message.'),
                'contact-form-feedback error',
                name, email, message
            )
        
        # Basic email validation only if email is provided
        if email and ('@' not in email or '.' not in email):
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
                'email': email if email else 'No email provided',
                'message': message
            }
            
            # Send via Formspree
            formspree_success = send_via_formspree(submission)
            
            # Also log to file as backup
            log_to_file(submission)
            
            if formspree_success:
                # Clear form and show success message
                return (
                    html.Span('✓ Thank you for your message! We will get back to you soon.'),
                    'contact-form-feedback success',
                    None,  # Clear name
                    None,  # Clear email
                    None   # Clear message
                )
            else:
                # Formspree failed but file logged
                return (
                    html.Span('✓ Message received! (Logged locally)'),
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


def send_via_formspree(submission):
    """
    Send contact form submission via Formspree
    
    Formspree endpoint: https://formspree.io/f/xovpjdbq
    - Free tier: 50 submissions/month
    - Email notifications included
    - Web dashboard to view submissions
    """
    try:
        import requests
        
        FORMSPREE_ENDPOINT = "https://formspree.io/f/xovpjdbq"
        
        # Formspree expects form data
        # Only include email field if a valid email was provided
        data = {
            'name': submission['name'],
            'message': submission['message'],
            '_subject': f"Dashboard Contact: {submission['name']}",
        }
        
        # Only add email if it was provided (not the placeholder text)
        if submission['email'] != 'No email provided':
            data['email'] = submission['email']
        
        response = requests.post(FORMSPREE_ENDPOINT, data=data)
        
        if response.status_code == 200:
            print(f"Formspree submission successful: {submission.get('name', 'Unknown')}")
            return True
        else:
            print(f"Formspree error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending via Formspree: {str(e)}")
        return False


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
