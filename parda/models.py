from django.db import models
from django.utils.html import format_html


class Parda(models.Model):
    model = models.CharField(max_length=200)
    boyi = models.FloatField(default=0, help_text="Olcham metrda (masalan: 23,4)")
    vitrina = models.FloatField(default=0)

    class Meta:
        verbose_name = "Parda"
        verbose_name_plural = "Pardalar"

    def __str__(self):
        return self.model

    def image_preview(self):
        if self.images.exists():
            return format_html('<img src="{}" style="height:150px;" />', self.images.first().image.url)
        return "No image"
    image_preview.short_description = "Preview"

    def pieces_total(self):
        return sum(piece.length for piece in self.pieces.all())
    pieces_total.short_description = "RulonKusok jami"

    def vitrina_plus_pieces(self):
        return self.pieces_total() + self.vitrina
    vitrina_plus_pieces.short_description = "Vitrina + RulonKusok jami"


class RulonKusok(models.Model):
    curtain = models.ForeignKey(Parda, related_name="pieces", on_delete=models.CASCADE)
    length = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.length} m"


class PardaImage(models.Model):
    parda = models.ForeignKey(Parda, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="curtains/", blank=True, null=True)

    def __str__(self):
        return f"Image for {self.parda}"