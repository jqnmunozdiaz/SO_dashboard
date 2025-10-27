# Contact Form - Receiving Submissions on Render

This dashboard now includes a "Contact Us" button that opens a modal popup with a contact form. Users can submit their name, email, and message.

## Current Implementation

By default, the contact form **logs submissions to a file** called `contact_submissions.log` in JSON format. This works on Render and you can access the submissions.

## How to Access Submissions on Render

### Option 1: View Logs via Render Shell (Simplest)

1. Go to your Render dashboard
2. Select your web service
3. Click on the **Shell** tab
4. Run: `cat contact_submissions.log`
5. You'll see all submissions in JSON format

Each line contains:
```json
{"timestamp": "2025-01-15T10:30:00", "name": "John Doe", "email": "john@example.com", "message": "Great dashboard!"}
```

### Option 2: Download Logs via Render Dashboard

1. Go to **Logs** tab in your Render service
2. Look for lines starting with "Contact form submission logged:"
3. Download logs using the download button

---

## Better Solutions for Production

### 🔥 RECOMMENDED: Email Service (Best for most use cases)

#### Using SendGrid (Free tier: 100 emails/day)

**Step 1: Sign up for SendGrid**
- Go to https://sendgrid.com
- Create free account
- Get your API key from Settings → API Keys

**Step 2: Add to requirements.txt**
```
sendgrid
```

**Step 3: Set environment variables in Render**
- Go to Render dashboard → Your service → Environment
- Add these variables:
  - `EMAIL_SERVICE` = `sendgrid`
  - `EMAIL_API_KEY` = `your_sendgrid_api_key`
  - `RECIPIENT_EMAIL` = `your@email.com`

**Step 4: Uncomment SendGrid code**
In `src/callbacks/contact_callbacks.py`, uncomment the SendGrid section (lines ~150-170)

**Step 5: Verify sender email**
- In SendGrid dashboard, verify your sender email address
- Update `from_email` in the code to match your verified email

#### Using Mailgun (Alternative)

**Step 1: Sign up for Mailgun**
- Go to https://mailgun.com
- Create free account (includes free credits)
- Get your API key and domain

**Step 2: Add to requirements.txt**
```
requests
```

**Step 3: Set environment variables in Render**
- `EMAIL_SERVICE` = `mailgun`
- `EMAIL_API_KEY` = `your_mailgun_api_key`
- `MAILGUN_DOMAIN` = `your_mailgun_domain`
- `RECIPIENT_EMAIL` = `your@email.com`

**Step 4: Uncomment Mailgun code**
In `src/callbacks/contact_callbacks.py`, uncomment the Mailgun section

---

### 💾 OPTION: Database Storage (Best for tracking)

#### Using PostgreSQL (Render has add-on)

**Step 1: Add PostgreSQL in Render**
- In your Render service, add PostgreSQL database
- Copy the database URL from Render

**Step 2: Add to requirements.txt**
```
psycopg2-binary
sqlalchemy
```

**Step 3: Create database table**
```python
# Add to contact_callbacks.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

Base = declarative_base()

class ContactSubmission(Base):
    __tablename__ = 'contact_submissions'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    name = Column(String(255))
    email = Column(String(255))
    message = Column(Text)

# In handle_contact_form_submission function:
if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    submission_record = ContactSubmission(
        timestamp=datetime.utcnow(),
        name=name,
        email=email,
        message=message
    )
    session.add(submission_record)
    session.commit()
    session.close()
```

**Step 4: View submissions**
```bash
# Connect to database via Render shell
psql $DATABASE_URL -c "SELECT * FROM contact_submissions ORDER BY timestamp DESC;"
```

---

### 🌐 OPTION: Third-Party Form Service (Easiest - No coding)

#### Using Formspree (Free tier: 50 submissions/month)

**Step 1: Sign up at https://formspree.io**
- Create account
- Create new form
- Copy your form endpoint URL

**Step 2: Modify the Contact Form**
Replace the modal in `world_bank_layout.py` with:

```python
dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Contact Us")),
    html.Form([
        dbc.ModalBody([
            html.Div([
                html.Label("Name:", className="contact-form-label"),
                html.Input(
                    type="text",
                    name="name",
                    placeholder="Enter your name",
                    className="form-control",
                    required=True
                ),
            ], className="contact-form-group"),
            html.Div([
                html.Label("Email:", className="contact-form-label"),
                html.Input(
                    type="email",
                    name="email",
                    placeholder="Enter your email",
                    className="form-control",
                    required=True
                ),
            ], className="contact-form-group"),
            html.Div([
                html.Label("Message:", className="contact-form-label"),
                html.Textarea(
                    name="message",
                    placeholder="Enter your message",
                    className="form-control",
                    style={"minHeight": "150px"},
                    required=True
                ),
            ], className="contact-form-group"),
        ]),
        dbc.ModalFooter([
            html.Button(
                "Send",
                type="submit",
                className="btn btn-primary"
            ),
        ]),
    ], 
    action="https://formspree.io/f/YOUR_FORM_ID",  # Replace with your Formspree endpoint
    method="POST"),
],
id="contact-modal",
is_open=False)
```

Formspree will:
- Validate submissions
- Send you email notifications
- Provide a dashboard to view all submissions
- Handle spam protection

---

## Comparison Table

| Method | Setup Time | Cost | Pros | Cons |
|--------|-----------|------|------|------|
| **File Logging** | 0 min (✅ Current) | Free | Simple, no dependencies | Manual log checking |
| **SendGrid** | 10 min | Free (100/day) | Professional emails, reliable | Requires API setup |
| **Mailgun** | 10 min | Free credits | Easy API, good docs | Need domain verification |
| **PostgreSQL** | 20 min | Free on Render | Full tracking, queryable | More complex setup |
| **Formspree** | 5 min | Free (50/month) | Easiest, no coding | Limited free tier |

## Recommendation

For your use case on Render, I recommend:

1. **Start with File Logging** (already implemented) - Works immediately
2. **Upgrade to SendGrid** when you expect regular submissions - 10 minutes setup, professional solution
3. **Add PostgreSQL** if you need to track/analyze submissions over time

---

## Testing the Contact Form

1. Run your dashboard locally: `python app.py`
2. Click "Contact Us" button in header
3. Fill in the form and submit
4. Check `contact_submissions.log` file in your project directory
5. You should see the JSON entry with your submission

On Render, after deployment:
1. Click "Contact Us" on your live site
2. Access via Render Shell: `cat contact_submissions.log`

---

## Security Notes

- Form includes basic validation (email format check)
- All inputs are sanitized before storage
- Consider adding CAPTCHA for public-facing production use (hCaptcha, reCAPTCHA)
- Rate limiting recommended if you expect high traffic

---

## Need Help?

- SendGrid docs: https://docs.sendgrid.com/
- Mailgun docs: https://documentation.mailgun.com/
- Formspree docs: https://help.formspree.io/
- Render PostgreSQL: https://render.com/docs/databases
