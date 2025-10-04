# app/services/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.email_config import EmailConfig

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
            
            print(f"✅ Email sent to: {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {str(e)}")
            return False

    @staticmethod
    def send_ticket_assigned_notification(ticket, agent, customer_email):
        """Notify customer when ticket is assigned"""
        subject = f"Your Support Ticket Has Been Assigned - #{ticket.id[:8]}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ticket Assigned</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: #f8fafc; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; text-align: center; }}
                .header h1 {{ font-size: 24px; font-weight: 600; margin-bottom: 8px; }}
                .header p {{ opacity: 0.9; font-size: 16px; }}
                .content {{ padding: 30px; }}
                .card {{ background: #f8fafc; border-radius: 12px; padding: 24px; margin: 20px 0; border-left: 4px solid #667eea; }}
                .card h3 {{ color: #2d3748; margin-bottom: 16px; font-size: 18px; }}
                .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
                .info-item {{ margin-bottom: 12px; }}
                .info-label {{ font-weight: 600; color: #4a5568; font-size: 14px; }}
                .info-value {{ color: #2d3748; font-size: 14px; }}
                .agent-card {{ background: #fff7ed; border: 1px solid #fed7aa; border-radius: 8px; padding: 16px; margin: 16px 0; }}
                .footer {{ background: #2d3748; color: #cbd5e0; padding: 24px; text-align: center; font-size: 14px; }}
                .footer a {{ color: #90cdf4; text-decoration: none; }}
                .urgency-badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
                .urgency-high {{ background: #fed7d7; color: #c53030; }}
                .urgency-medium {{ background: #feebc8; color: #dd6b20; }}
                .urgency-low {{ background: #c6f6d5; color: #276749; }}
                @media (max-width: 600px) {{
                    .info-grid {{ grid-template-columns: 1fr; }}
                    .content {{ padding: 20px; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 Ticket Assigned</h1>
                    <p>Your support ticket has been assigned to an agent</p>
                </div>
                
                <div class="content">
                    <p>Hello,</p>
                    <p>Great news! Your support ticket has been assigned to one of our expert agents who will help you shortly.</p>
                    
                    <div class="card">
                        <h3>Ticket Details</h3>
                        <div class="info-grid">
                            <div class="info-item">
                                <div class="info-label">Ticket ID</div>
                                <div class="info-value">#{ticket.id[:8]}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Subject</div>
                                <div class="info-value">{ticket.subject}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Priority</div>
                                <div class="info-value">
                                    <span class="urgency-badge {'urgency-high' if ticket.urgency >= 4 else 'urgency-medium' if ticket.urgency >= 3 else 'urgency-low'}">
                                        {ticket.urgency}/5
                                    </span>
                                </div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Status</div>
                                <div class="info-value">Assigned</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="agent-card">
                        <h3>👤 Assigned Agent</h3>
                        <p><strong>{agent.full_name}</strong> is now working on your ticket.</p>
                        <p>You can expect a response within the next few hours.</p>
                    </div>
                    
                    <p>We'll notify you when there are further updates to your ticket.</p>
                </div>
                
                <div class="footer">
                    <p><strong>{EmailConfig.COMPANY_NAME}</strong></p>
                    <p>If you have any questions, contact us at <a href="mailto:{EmailConfig.SUPPORT_EMAIL}">{EmailConfig.SUPPORT_EMAIL}</a></p>
                    <p style="margin-top: 16px; font-size: 12px; opacity: 0.7;">
                        This is an automated message. Please do not reply to this email.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        TICKET ASSIGNED NOTIFICATION
        
        Your support ticket has been assigned to an agent.
        
        TICKET DETAILS:
        - Ticket ID: #{ticket.id[:8]}
        - Subject: {ticket.subject}
        - Assigned Agent: {agent.full_name}
        - Priority: {ticket.urgency}/5
        - Status: Assigned
        
        Your ticket has been assigned to {agent.full_name}, who will help you shortly.
        You can expect a response within the next few hours.
        
        We'll notify you when there are further updates to your ticket.
        
        Thank you for choosing {EmailConfig.COMPANY_NAME}
        
        Need help? Contact us: {EmailConfig.SUPPORT_EMAIL}
        
        ---
        This is an automated message. Please do not reply.
        """
        
        return EmailService.send_email(customer_email, subject, html_content, text_content)
    
    @staticmethod
    def send_ticket_status_update(ticket, customer_email, old_status, new_status):
        """Notify customer when ticket status changes"""
        subject = f"Ticket Status Updated - #{ticket.id[:8]}"
        
        status_descriptions = {
            "in_progress": "is now being worked on",
            "resolved": "has been resolved",
            "closed": "has been closed",
            "open": "has been reopened"
        }
        
        description = status_descriptions.get(new_status, f"status changed to {new_status}")
        status_emoji = {
            "in_progress": "🔄",
            "resolved": "✅", 
            "closed": "🔒",
            "open": "📝"
        }
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Status Update</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: #f8fafc; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; }}
                .header {{ background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); color: white; padding: 30px 20px; text-align: center; }}
                .header h1 {{ font-size: 24px; font-weight: 600; margin-bottom: 8px; }}
                .content {{ padding: 30px; }}
                .status-card {{ background: #f0fff4; border: 2px solid #9ae6b4; border-radius: 12px; padding: 24px; margin: 20px 0; }}
                .status-change {{ display: flex; align-items: center; justify-content: center; gap: 16px; margin: 20px 0; }}
                .status-old, .status-new {{ padding: 12px 20px; border-radius: 8px; font-weight: 600; }}
                .status-old {{ background: #e2e8f0; color: #4a5568; }}
                .status-new {{ background: #48bb78; color: white; }}
                .arrow {{ font-size: 20px; color: #718096; }}
                .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px; }}
                .info-item {{ margin-bottom: 12px; }}
                .info-label {{ font-weight: 600; color: #4a5568; font-size: 14px; }}
                .info-value {{ color: #2d3748; font-size: 14px; }}
                .footer {{ background: #2d3748; color: #cbd5e0; padding: 24px; text-align: center; font-size: 14px; }}
                @media (max-width: 600px) {{
                    .info-grid {{ grid-template-columns: 1fr; }}
                    .content {{ padding: 20px; }}
                    .status-change {{ flex-direction: column; gap: 8px; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{status_emoji.get(new_status, '📋')} Status Updated</h1>
                    <p>Your support ticket {description}</p>
                </div>
                
                <div class="content">
                    <p>Hello,</p>
                    <p>Your support ticket {description}.</p>
                    
                    <div class="status-card">
                        <h3>Status Change</h3>
                        <div class="status-change">
                            <div class="status-old">{old_status.replace('_', ' ').title()}</div>
                            <div class="arrow">→</div>
                            <div class="status-new">{new_status.replace('_', ' ').title()}</div>
                        </div>
                        
                        <div class="info-grid">
                            <div class="info-item">
                                <div class="info-label">Ticket ID</div>
                                <div class="info-value">#{ticket.id[:8]}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Subject</div>
                                <div class="info-value">{ticket.subject}</div>
                            </div>
                        </div>
                    </div>
                    
                    {f'<p><strong>Resolution Details:</strong> Our team has completed working on your ticket. If you need further assistance, please don\'t hesitate to reach out.</p>' if new_status in ['resolved', 'closed'] else '<p>We are actively working on your ticket and will keep you updated on our progress.</p>'}
                </div>
                
                <div class="footer">
                    <p><strong>{EmailConfig.COMPANY_NAME}</strong></p>
                    <p>Contact support: {EmailConfig.SUPPORT_EMAIL}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        TICKET STATUS UPDATE
        
        Your support ticket {description}.
        
        STATUS CHANGE:
        {old_status.replace('_', ' ').title()} → {new_status.replace('_', ' ').title()}
        
        TICKET DETAILS:
        - Ticket ID: #{ticket.id[:8]}
        - Subject: {ticket.subject}
        
        {'Our team has completed working on your ticket. If you need further assistance, please reply to this email.' if new_status in ['resolved', 'closed'] else 'We are actively working on your ticket and will keep you updated.'}
        
        Thank you for choosing {EmailConfig.COMPANY_NAME}
        
        Contact: {EmailConfig.SUPPORT_EMAIL}
        """
        
        return EmailService.send_email(customer_email, subject, html_content, text_content)
    
    @staticmethod
    def send_new_ticket_notification(ticket, customer_email):
        """Notify customer when ticket is created"""
        subject = f"Support Ticket Created - #{ticket.id[:8]}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ticket Created</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: #f8fafc; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; }}
                .header {{ background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%); color: white; padding: 30px 20px; text-align: center; }}
                .header h1 {{ font-size: 24px; font-weight: 600; margin-bottom: 8px; }}
                .content {{ padding: 30px; }}
                .ticket-card {{ background: #ebf8ff; border-radius: 12px; padding: 24px; margin: 20px 0; border-left: 4px solid #4299e1; }}
                .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
                .info-item {{ margin-bottom: 12px; }}
                .info-label {{ font-weight: 600; color: #4a5568; font-size: 14px; }}
                .info-value {{ color: #2d3748; font-size: 14px; }}
                .description-box {{ background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin: 16px 0; }}
                .footer {{ background: #2d3748; color: #cbd5e0; padding: 24px; text-align: center; font-size: 14px; }}
                .urgency-badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
                .urgency-high {{ background: #fed7d7; color: #c53030; }}
                .urgency-medium {{ background: #feebc8; color: #dd6b20; }}
                .urgency-low {{ background: #c6f6d5; color: #276749; }}
                @media (max-width: 600px) {{
                    .info-grid {{ grid-template-columns: 1fr; }}
                    .content {{ padding: 20px; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📋 Ticket Received</h1>
                    <p>We've received your support ticket</p>
                </div>
                
                <div class="content">
                    <p>Hello,</p>
                    <p>Thank you for contacting support. We've received your ticket and will get back to you shortly.</p>
                    
                    <div class="ticket-card">
                        <h3>Ticket Details</h3>
                        <div class="info-grid">
                            <div class="info-item">
                                <div class="info-label">Ticket ID</div>
                                <div class="info-value">#{ticket.id[:8]}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Subject</div>
                                <div class="info-value">{ticket.subject}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Priority</div>
                                <div class="info-value">
                                    <span class="urgency-badge {'urgency-high' if ticket.urgency >= 4 else 'urgency-medium' if ticket.urgency >= 3 else 'urgency-low'}">
                                        {ticket.urgency}/5
                                    </span>
                                </div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Status</div>
                                <div class="info-value">Open</div>
                            </div>
                        </div>
                        
                        <div class="description-box">
                            <div class="info-label">Description</div>
                            <div class="info-value">{ticket.description}</div>
                        </div>
                    </div>
                    
                    <h4>What happens next?</h4>
                    <ul style="margin: 16px 0; padding-left: 20px;">
                        <li>Our team will review your ticket</li>
                        <li>We'll assign it to the best-suited agent</li>
                        <li>You'll receive updates via email</li>
                        <li>Average response time: 2-4 hours</li>
                    </ul>
                    
                    <p>We'll notify you when your ticket is assigned to an agent and when there are any updates.</p>
                </div>
                
                <div class="footer">
                    <p><strong>{EmailConfig.COMPANY_NAME}</strong></p>
                    <p>For urgent issues, contact: {EmailConfig.SUPPORT_EMAIL}</p>
                    <p style="margin-top: 16px; font-size: 12px; opacity: 0.7;">
                        This is an automated confirmation. Please do not reply to this email.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        SUPPORT TICKET CREATED
        
        Thank you for contacting support. We've received your ticket and will get back to you shortly.
        
        TICKET DETAILS:
        - Ticket ID: #{ticket.id[:8]}
        - Subject: {ticket.subject}
        - Priority: {ticket.urgency}/5
        - Status: Open
        
        DESCRIPTION:
        {ticket.description}
        
        WHAT HAPPENS NEXT?
        • Our team will review your ticket
        • We'll assign it to the best-suited agent  
        • You'll receive updates via email
        • Average response time: 2-4 hours
        
        We'll notify you when your ticket is assigned and when there are updates.
        
        Thank you for choosing {EmailConfig.COMPANY_NAME}
        
        For urgent issues: {EmailConfig.SUPPORT_EMAIL}
        
        ---
        This is an automated confirmation. Please do not reply.
        """
        
        return EmailService.send_email(customer_email, subject, html_content, text_content)