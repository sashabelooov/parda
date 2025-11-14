# management/commands/import_excel.py
import pandas as pd
from django.core.management.base import BaseCommand
from parda.models import Parda, RulonKusok

class Command(BaseCommand):
    help = 'Import Excel to DB'

    def handle(self, *args, **options):
        # Load Excel
        excel_file = 'data/ОСТАТКИ.xlsx'
        df = pd.read_excel(excel_file, sheet_name='mix', header=0)

        # Set columns
        df.columns = ['model', 'rulon', 'metraj_rulona'] + [f'metraj_kusok{i}' for i in range(1, 8)] + ['vitrina', 'obshiy_ostatok']

        for idx, row in df.iterrows():
            if pd.isna(row['model']) or str(row['model']).strip() == '': continue
            model_name = str(row['model']).strip()

            vitrina_val = float(row['vitrina']) if not pd.isna(row['vitrina']) else 0

            parda, created = Parda.objects.get_or_create(
                model=model_name,
                defaults={'boyi': 0, 'vitrina': vitrina_val}
            )
            if not created:
                parda.vitrina = vitrina_val
                parda.save()

            # Add pieces (kusoks)
            kusok_cols = [f'metraj_kusok{i}' for i in range(1, 8)]
            for col in kusok_cols:
                length_val = float(row[col]) if not pd.isna(row[col]) else 0
                if length_val > 0:
                    RulonKusok.objects.create(curtain=parda, length=length_val)

        self.stdout.write(self.style.SUCCESS('Import complete'))