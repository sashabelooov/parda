import os
try:
    import pandas as pd
except Exception:
    pd = None


def import_excel(file_path, apps=None, verbosity=1):
    if pd is None:
        if verbosity:
            print("pandas not available; skipping Excel import.")
        return

    if not os.path.exists(file_path):
        if verbosity:
            print(f"No Excel file at {file_path}; skipping import.")
        return

    try:
        df = pd.read_excel(file_path, sheet_name='mix', header=0)
    except Exception as e:
        if verbosity:
            print(f"Could not read sheet 'mix' from {file_path}: {e}")
        return

    expected_cols = ['model', 'rulon', 'metraj_rulona'] + [f'metraj_kusok{i}' for i in range(1, 8)] + ['vitrina', 'obshiy_ostatok']
    if len(df.columns) >= len(expected_cols):
        df.columns = expected_cols + list(df.columns[len(expected_cols):])
    else:
        df.columns = expected_cols[:len(df.columns)]

    if apps:
        Parda = apps.get_model('parda', 'Parda')
        RulonKusok = apps.get_model('parda', 'RulonKusok')
    else:
        from ...models import Parda, RulonKusok

    for _, row in df.iterrows():
        if pd.isna(row.get('model')) or str(row.get('model')).strip() == '':
            continue
        model_name = str(row['model']).strip()
        vitrina_val = float(row['vitrina']) if 'vitrina' in row and not pd.isna(row['vitrina']) else 0

        parda, created = Parda.objects.get_or_create(
            model=model_name, defaults={'boyi': 0, 'vitrina': vitrina_val}
        )
        if not created:
            parda.vitrina = vitrina_val
            parda.save()

        # deterministically replace pieces for this parda
        if apps:
            RulonKusok.objects.filter(curtain=parda).delete()
        else:
            parda.pieces.all().delete()

        kusok_cols = [f'metraj_kusok{i}' for i in range(1, 8)]
        for col in kusok_cols:
            if col in row:
                length_val = float(row[col]) if not pd.isna(row[col]) else 0
                if length_val > 0:
                    RulonKusok.objects.create(curtain=parda, length=length_val)

    if verbosity:
        print("Import complete")
