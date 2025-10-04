import os
from dotenv import load_dotenv

load_dotenv()

class EmailConfig:
    # Email service configuration
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    
    # Email addresses
    FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@yoursupport.com")
    SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "support@yoursupport.com")
    
    # Templates
    COMPANY_NAME = "Customer Support Triage"
    
    @classmethod
    def is_configured(cls):
        return bool(cls.SMTP_USERNAME and cls.SMTP_PASSWORD)
