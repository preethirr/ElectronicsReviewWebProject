# Email Setup Instructions for Contact Form

## To make contact form emails work, follow these steps:

### 1. Gmail Setup (Recommended)
1. Go to your Gmail account settings
2. Enable 2-factor authentication
3. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and your device
   - Copy the generated 16-character password

### 2. Update settings.py
Replace these values in settings.py:
```python
EMAIL_HOST_USER = 'your-actual-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-character-app-password'
CONTACT_EMAIL = 'info.electronicsreview@gmailcom'  # Where you want to receive emails
```

### 3. Alternative Email Services
- **Yahoo Mail**: EMAIL_HOST = 'smtp.mail.yahoo.com', EMAIL_PORT = 587
- **Outlook**: EMAIL_HOST = 'smtp-mail.outlook.com', EMAIL_PORT = 587
- **Custom SMTP**: Replace with your provider's SMTP settings

### 4. Testing
- Fill out the contact form on your website
- Check your email (including spam folder)
- Success/error messages will appear on the contact page

### 5. Security Note
Never commit real email credentials to version control. Consider using environment variables for production.

## Current Configuration:
- Contact form data is sent to: admin@electronicsreview.com
- Sender email: your-email@gmail.com
- All form submissions include: name, email, subject, and message
