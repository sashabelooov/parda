# parda/tasks.py
from celery import shared_task
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

@shared_task(name='parda.tasks.export_to_telegram_task')
def export_to_telegram_task():
    """
    Celery task to export database and send to Telegram
    This runs on schedule defined in celery.py
    """
    try:
        logger.info('Starting Telegram export task...')
        call_command('export_to_telegram')
        logger.info('Telegram export task completed successfully')
        return 'Export completed successfully'
    except Exception as e:
        logger.error(f'Error in Telegram export task: {str(e)}')
        raise