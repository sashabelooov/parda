# management/commands/import_excel.py
import pandas as pd
from django.core.management.base import BaseCommand
from parda.models import Parda, RulonKusok  # Adjust import

class Command(BaseCommand):
    help = 'Import Excel to DB'

    def handle(self, *args, **options):
        # Load Excel
        excel_file = 'data/ОСТАТКИ.xlsx'
        sheets = pd.read_excel(excel_file, sheet_name=None)

        # Process Sheet 0 (Общийе остатки)
        df = sheets['Общийе остатки']
        df.columns = ['brand', 'model', 'rulon', 'metrazh_rulon', 'vitrina_metrazh', 'metrazh_kusok1', 'metrazh_kusok2', 'metrazh_kusok3', 'metrazh_kusok4', 'obshiy_ostatok']
        
        for idx, row in df.iterrows():
            if pd.isna(row['model']) or str(row['model']).strip() == '': continue
            model_name = str(row['model']).strip()
            
            vitrina_val = 0 if pd.isna(row.get('vitrina_metrazh')) else float(row.get('vitrina_metrazh'))
            
            parda, created = Parda.objects.get_or_create(
                model=model_name,
                defaults={'boyi': 0, 'vitrina': vitrina_val}
            )
            if not created:
                parda.vitrina = vitrina_val
                parda.save()
            
            # Add pieces (kusoks)
            kusok_cols = [col for col in df.columns if 'metrazh_kusok' in str(col)]
            for col in kusok_cols:
                length_val = 0 if pd.isna(row.get(col)) else float(row.get(col))
                if length_val > 0:
                    RulonKusok.objects.create(curtain=parda, length=length_val)
        
        # TODO: Adapt and add processing for other sheets like 'mix', 'BLACKOUT', etc.

        self.stdout.write(self.style.SUCCESS('Import complete'))