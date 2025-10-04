# app/services/email_service.py - UPDATED VERSION WITH TEMPLATES
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.email_config import EmailConfig
from app.services.template_engine import TemplateEngine

class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, html_content: str, text_content: str = None):
        """Send email using SMTP"""
        if not EmailConfig.is_configured():
            print(f"EMAIL NOT SENT (no config): To: {to_email}, Subject: {subject}")
            return False

        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = EmailConfig.FROM_EMAIL
            msg['To'] = to_email

            # Create text version
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)

            # Create HTML version
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Send email
            with smtplib.SMTP(EmailConfig.SMTP_SERVER, EmailConfig.SMTP_PORT) as server:
                server.starttls()
                server.login(EmailConfig.SMTP_USERNAME, EmailConfig.SMTP_PASSWORD)
                server.send_message(msg)

            print(f"Email sent to: {to_email}")
            return True

        except Exception as e:
            print(f"Failed to send email to {to_email}: {str(e)}")
            return False

    @staticmethod
    def send_new_ticket_notification(ticket, customer_email):
        """Send enhanced new ticket notification using templates"""
        subject = f"Support Ticket Created - #{ticket.id[:8]}"
        
        # Prepare context for template
        context = {
            'customer_name': 'Customer',
            'ticket_id': ticket.id[:8],
            'ticket_subject': ticket.subject,
            'ticket_description': ticket.description,
            'created_date': ticket.created_at.strftime('%B %d, %Y at %H:%M'),
            'urgency_class': TemplateEngine.get_urgency_class(ticket.urgency),
            'urgency_text': TemplateEngine.get_urgency_text(ticket.urgency),
            'category': ticket.category or 'General',
            'status_badge': TemplateEngine.get_status_badge('open'),
            'expected_response_time': EmailService.get_expected_response_time(ticket.urgency),
            'ticket_url': f"https://yoursupportportal.com/tickets/{ticket.id}",
            'emergency_contact_url': f"mailto:{EmailConfig.SUPPORT_EMAIL}"
        }
        
        # Render email content
        email_content = TemplateEngine.render_template('new_ticket_notification.html', context)
        full_html = TemplateEngine.render_template('base_template.html', {
            'email_content': email_content,
            'email_subject': subject,
            'support_url': "https://yoursupportportal.com/support",
            'knowledge_base_url': "https://yoursupportportal.com/knowledge-base", 
            'contact_url': f"mailto:{EmailConfig.SUPPORT_EMAIL}"
        })
        
        # Create text version
        text_content = f"""
SUPPORT TICKET CREATED - AI ANALYSIS COMPLETE

Hello {context['customer_name']},

Thank you for contacting support! We've received your ticket and our AI system has already analyzed it for faster resolution.

TICKET DETAILS:
- Ticket ID: #{context['ticket_id']}
- Subject: {ticket.subject}
- Priority: {context['urgency_text']} (AI Analyzed)
- Category: {context['category']}
- Created: {context['created_date']}

AI ANALYSIS:
Our AI has identified your ticket as {context['urgency_text']} priority.
Estimated response time: {context['expected_response_time']}

WHAT HAPPENS NEXT?
- Your ticket is in our queue with {context['urgency_text']} priority
- Our team will review it within {context['expected_response_time']}
- You'll be assigned a dedicated support agent
- We'll send you regular updates

View your ticket: {context['ticket_url']}

For urgent issues: {EmailConfig.SUPPORT_EMAIL}

Thank you for choosing {EmailConfig.COMPANY_NAME}
"""

        return EmailService.send_email(customer_email, subject, full_html, text_content)

    @staticmethod
    def get_expected_response_time(urgency: int) -> str:
        """Get expected response time based on urgency"""
        if urgency >= 4:
            return "1-2 hours"
        elif urgency >= 3:
            return "2-4 hours" 
        else:
            return "4-8 hours"

    # Keep your existing methods
    @staticmethod
    def send_ticket_assigned_notification(ticket, agent, customer_email):
        """Notify customer when ticket is assigned"""
        from app.services.email_service_original import EmailService as OriginalEmailService
        return OriginalEmailService.send_ticket_assigned_notification(ticket, agent, customer_email)

    @staticmethod
    def send_ticket_status_update(ticket, customer_email, old_status, new_status):
        """Notify customer when ticket status changes"""
        from app.services.email_service_original import EmailService as OriginalEmailService
        return OriginalEmailService.send_ticket_status_update(ticket, customer_email, old_status, new_status)