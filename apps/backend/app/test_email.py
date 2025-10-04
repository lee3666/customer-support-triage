# test_email.py
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.email_service import EmailService
from app.core.email_config import EmailConfig

def test_email_service():
    print("🔧 Testing email service configuration...")
    print("=" * 50)
    
    # Check if email is configured
    if not EmailConfig.is_configured():
        print("❌ Email not configured - check your environment variables")
        print("\nRequired environment variables:")
        print(f"  SMTP_SERVER: {EmailConfig.SMTP_SERVER}")
        print(f"  SMTP_USERNAME: {'✅ Set' if EmailConfig.SMTP_USERNAME else '❌ Missing'}")
        print(f"  SMTP_PASSWORD: {'✅ Set' if EmailConfig.SMTP_PASSWORD else '❌ Missing'}")
        print(f"  FROM_EMAIL: {'✅ Set' if EmailConfig.FROM_EMAIL else '❌ Missing'}")
        return False
    
    print("✅ Email configuration loaded successfully!")
    print(f"  SMTP Server: {EmailConfig.SMTP_SERVER}:{EmailConfig.SMTP_PORT}")
    print(f"  From Email: {EmailConfig.FROM_EMAIL}")
    print(f"  Company: {EmailConfig.COMPANY_NAME}")
    
    # Test data - REPLACE WITH YOUR ACTUAL EMAIL FOR TESTING
    test_email = "songoklee26@gmail.com"  # ⚠️ CHANGE THIS TO YOUR EMAIL
    test_subject = "Test Email from Customer Support System"
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: #2563eb; color: white; padding: 20px; text-align: center; }
            .content { background: #f9fafb; padding: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Customer Support Test</h1>
            </div>
            <div class="content">
                <h2>Test Email Successful! 🎉</h2>
                <p>This is a test email from the customer support system.</p>
                <p>If you received this, the email service is working correctly!</p>
                <p><strong>Timestamp:</strong> This email was sent to test the system configuration.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    test_text = """
    TEST EMAIL FROM CUSTOMER SUPPORT SYSTEM
    
    This is a test email from the customer support system.
    If you received this, the email service is working correctly!
    
    Timestamp: This email was sent to test the system configuration.
    
    Thank you for testing!
    """
    
    print(f"\n📧 Sending test email to: {test_email}")
    print("Please wait...")
    
    try:
        # Send test email
        success = EmailService.send_email(
            to_email=test_email,
            subject=test_subject,
            html_content=test_html,
            text_content=test_text
        )
        
        if success:
            print("✅ Test email sent successfully!")
            print("📬 Please check your inbox (and spam folder) for the test email.")
        else:
            print("❌ Failed to send test email")
            print("   Check your SMTP settings and credentials.")
        
        return success
        
    except Exception as e:
        print(f"💥 Error during email test: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Email Service Test")
    print("=" * 50)
    test_email_service()