from celery import Celery
import os

# Create Celery app instance
celery_app = Celery(
    'support_worker',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0')
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_routes={
        'app.workers.tasks.process_ticket_ai': {'queue': 'ai_processing'},
        'app.workers.tasks.send_email_notification': {'queue': 'email_notifications'},
    },
    task_acks_late=True,
    worker_prefetch_multiplier=1
)

# Import tasks after app is created to avoid circular imports
celery_app.autodiscover_tasks(['app.workers.tasks'])

# Export the app instance
__all__ = ['celery_app']