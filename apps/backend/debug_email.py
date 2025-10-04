# debug_email.py
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.email_config import EmailConfig

print("🔧 DEBUG Email Test")
print("=" * 50)

def test_smtp_connection():
    print("1. Testing SMTP connection...")
    try:
        server = smtplib.SMTP(EmailConfig.SMTP_SERVER, EmailConfig.SMTP_PORT, timeout=10)
        print("   ✅ Connected to SMTP server")
        
        print("2. Starting TLS...")
        server.starttls()
        print("   ✅ TLS started")
        
        print("3. Attempting login...")
        server.login(EmailConfig.SMTP_USERNAME, EmailConfig.SMTP_PASSWORD)
        print("   ✅ Login successful")
        
        print("4. Testing email creation...")
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Debug Test Email"
        msg['From'] = EmailConfig.FROM_EMAIL
        msg['To'] = "songoklee26@gmail.com"
        
        text_part = MIMEText("This is a test email.", 'plain')
        html_part = MIMEText("<h1>Test Email</h1><p>This is a test email.</p>", 'html')
        
        msg.attach(text_part)
        msg.attach(html_part)
        print("   ✅ Email message created")
        
        print("5. Sending email...")
        server.send_message(msg)
        print("   ✅ Email sent successfully!")
        
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"   ❌ Authentication failed: {e}")
        print("   💡 Check your App Password - make sure it's 16 characters, no spaces")
    except smtplib.SMTPException as e:
        print(f"   ❌ SMTP error: {e}")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
    
    return False

if __name__ == "__main__":
    if not EmailConfig.is_configured():
        print("❌ Email not configured")
    else:
        print("✅ Configuration loaded")
        print(f"   Server: {EmailConfig.SMTP_SERVER}:{EmailConfig.SMTP_PORT}")
        print(f"   Username: {EmailConfig.SMTP_USERNAME}")
        
        success = test_smtp_connection()
        if success:
            print("\n🎉 SUCCESS! Check your email inbox and spam folder.")
        else:
            print("\n💥 FAILED! See errors above.")
