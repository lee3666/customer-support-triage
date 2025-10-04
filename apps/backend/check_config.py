# check_config.py
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.email_config import EmailConfig

print("🔍 Checking Email Configuration")
print("=" * 40)

print("Current environment variables:")
print(f"SMTP_SERVER: {os.getenv('SMTP_SERVER', 'Not set')}")
print(f"SMTP_PORT: {os.getenv('SMTP_PORT', 'Not set')}")
print(f"SMTP_USERNAME: {os.getenv('SMTP_USERNAME', 'Not set')}")
print(f"SMTP_PASSWORD: {'***' + os.getenv('SMTP_PASSWORD', 'Not set')[-4:] if os.getenv('SMTP_PASSWORD') else 'Not set'}")
print(f"FROM_EMAIL: {os.getenv('FROM_EMAIL', 'Not set')}")
print(f"COMPANY_NAME: {os.getenv('COMPANY_NAME', 'Not set')}")
print(f"SUPPORT_EMAIL: {os.getenv('SUPPORT_EMAIL', 'Not set')}")

print("\n" + "=" * 40)
print("EmailConfig class values:")
print(f"SMTP_SERVER: {EmailConfig.SMTP_SERVER}")
print(f"SMTP_PORT: {EmailConfig.SMTP_PORT}")
print(f"SMTP_USERNAME: {EmailConfig.SMTP_USERNAME}")
print(f"SMTP_PASSWORD: {'***' + EmailConfig.SMTP_PASSWORD[-4:] if EmailConfig.SMTP_PASSWORD else 'Not set'}")
print(f"FROM_EMAIL: {EmailConfig.FROM_EMAIL}")
print(f"COMPANY_NAME: {EmailConfig.COMPANY_NAME}")
print(f"SUPPORT_EMAIL: {EmailConfig.SUPPORT_EMAIL}")

print("\n" + "=" * 40)
print(f"Configuration status: {'✅ CONFIGURED' if EmailConfig.is_configured() else '❌ NOT CONFIGURED'}")
