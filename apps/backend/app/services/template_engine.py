# app/services/template_engine.py - SIMPLIFIED VERSION
import os
import re
from typing import Dict, Any

class TemplateEngine:
    @staticmethod
    def render_template(template_name: str, context: Dict[str, Any]) -> str:
        """Render HTML template with context variables"""
        template_path = os.path.join(os.path.dirname(__file__), 'templates', template_name)
        
        try:
            # Read with error handling for encoding
            with open(template_path, 'r', encoding='utf-8', errors='replace') as file:
                template_content = file.read()
            
            # Use regex to replace all template variables
            def replace_match(match):
                variable_name = match.group(1).strip()
                return str(context.get(variable_name, match.group(0)))
            
            # Replace all {{ variable_name }} patterns
            template_content = re.sub(r'{{\s*([^}]+)\s*}}', replace_match, template_content)
            
            return template_content
        except FileNotFoundError:
            print(f"Template not found: {template_name}")
            return f"<h1>Template Error</h1><p>Template {template_name} not found.</p>"
        except Exception as e:
            print(f"Template rendering error: {e}")
            return f"<h1>Template Error</h1><p>{str(e)}</p>"

    @staticmethod
    def get_urgency_class(urgency: int) -> str:
        """Get CSS class for urgency level"""
        if urgency >= 4:
            return 'urgency-high'
        elif urgency >= 3:
            return 'urgency-medium'
        else:
            return 'urgency-low'

    @staticmethod
    def get_urgency_text(urgency: int) -> str:
        """Get text description for urgency level"""
        if urgency >= 4:
            return 'High'
        elif urgency >= 3:
            return 'Medium'
        else:
            return 'Low'

    @staticmethod
    def get_status_badge(status: str) -> str:
        """Get status badge HTML"""
        status_classes = {
            'open': 'status-open',
            'in_progress': 'status-in-progress', 
            'resolved': 'status-resolved',
            'closed': 'status-closed',
            'assigned': 'status-in-progress'
        }
        class_name = status_classes.get(status, 'status-open')
        display_text = status.replace('_', ' ').title()
        return f'<span class="status-badge {class_name}">{display_text}</span>'
