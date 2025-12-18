from django.db import migrations
import os
from pathlib import Path
from django.conf import settings


def move_images(apps, schema_editor):
    PardaImage = apps.get_model('parda', 'PardaImage')

    media_root = Path(settings.MEDIA_ROOT)
    target_dir = media_root / 'parda_images'
    target_dir.mkdir(parents=True, exist_ok=True)

    for img in PardaImage.objects.all():
        name = img.image.name or ''
        # If image is stored at root (no folder) or still has 'curtains/' prefix, normalize to 'parda_images/<basename>'
        # Skip empty names
        if not name:
            continue
        if name.startswith('parda_images/'):
            continue

        # get basename and new relative name
        base = os.path.basename(name)
        new_rel = f'parda_images/{base}'

        old_path = media_root / name
        new_path = media_root / new_rel
        try:
            if old_path.exists() and not new_path.exists():
                old_path.replace(new_path)
        except Exception:
            # best effort move; if fail, continue
            pass

        # update DB record to new path
        img.image.name = new_rel
        img.save(update_fields=['image'])


class Migration(migrations.Migration):

    dependencies = [
        ('parda', '0002_alter_pardaimage_image'),
    ]

    operations = [
        migrations.RunPython(move_images, reverse_code=migrations.RunPython.noop),
    ]
