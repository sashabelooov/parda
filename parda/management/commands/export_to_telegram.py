# management/commands/export_to_telegram.py
import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from parda.models import Parda, RulonKusok
import requests
from datetime import datetime

class Command(BaseCommand):
    help = 'Export DB to Excel and send to Telegram'

    def handle(self, *args, **options):
        try:
            # Prepare data for export
            data = []
            
            for parda in Parda.objects.all():
                # Get all pieces (kusoks)
                kusoks = parda.pieces.all().order_by('created_at')
                
                row = {
                    'Model': parda.model,
                    'Boyi': parda.boyi,
                }
                
                # Add ALL kusok columns (not limited to 7)
                for i, kusok in enumerate(kusoks, 1):
                    row[f'Metraj_Kusok{i}'] = kusok.length
                
                row['Vitrina'] = parda.vitrina
                row['RulonKusok_Jami'] = parda.pieces_total()
                row['Umumiy_Ostatok'] = parda.vitrina_plus_pieces()
                
                data.append(row)
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Create exports directory if it doesn't exist
            export_dir = os.path.join(settings.BASE_DIR, 'exports')
            os.makedirs(export_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
            filename = f'parda_export_{timestamp}.xlsx'
            filepath = os.path.join(export_dir, filename)
            
            # Export to Excel
            df.to_excel(filepath, index=False, engine='openpyxl')
            
            self.stdout.write(self.style.SUCCESS(f'Excel file created: {filename}'))
            
            # Send to Telegram
            self.send_to_telegram(filepath, filename)
            
            # Optional: Clean up old files (keep last 7 days)
            self.cleanup_old_files(export_dir, days=7)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
    
    def send_to_telegram(self, filepath, filename):
        """Send file to Telegram (supports single chat or multiple groups)"""
        try:
            bot_token = settings.TELEGRAM_BOT_TOKEN
            
            # Support both single chat and multiple chats
            chat_ids = []
            if hasattr(settings, 'TELEGRAM_CHAT_IDS'):
                chat_ids = settings.TELEGRAM_CHAT_IDS
            elif hasattr(settings, 'TELEGRAM_CHAT_ID'):
                chat_ids = [settings.TELEGRAM_CHAT_ID]
            else:
                raise ValueError('TELEGRAM_CHAT_ID or TELEGRAM_CHAT_IDS not configured')
            
            url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
            caption = f'📊 Parda qoldig\'i hisoboti\n📅 Sana: {datetime.now().strftime("%d.%m.%Y %H:%M")}'
            
            success_count = 0
            for chat_id in chat_ids:
                with open(filepath, 'rb') as file:
                    files = {'document': (filename, file)}
                    data = {
                        'chat_id': chat_id,
                        'caption': caption
                    }
                    
                    response = requests.post(url, files=files, data=data)
                    
                    if response.status_code == 200:
                        success_count += 1
                        self.stdout.write(self.style.SUCCESS(f'✓ Sent to chat: {chat_id}'))
                    else:
                        self.stdout.write(self.style.ERROR(f'✗ Failed for chat {chat_id}: {response.text}'))
            
            self.stdout.write(self.style.SUCCESS(f'Sent to {success_count}/{len(chat_ids)} chats'))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error sending to Telegram: {str(e)}'))
    
    def cleanup_old_files(self, directory, days=7):
        """Remove files older than specified days"""
        import time
        from pathlib import Path
        
        now = time.time()
        cutoff = now - (days * 86400)
        
        for file_path in Path(directory).glob('parda_export_*.xlsx'):
            if file_path.stat().st_mtime < cutoff:
                file_path.unlink()
                self.stdout.write(self.style.WARNING(f'Deleted old file: {file_path.name}'))