from django.contrib import admin
from django.utils.html import format_html
from .models import Parda, RulonKusok, PardaImage

@admin.display(description="Preview")
class RulonKusokInline(admin.TabularInline):
    model = RulonKusok
    extra = 1
    fields = ("length", "created_at")
    readonly_fields = ("created_at",)

class PardaImageInline(admin.TabularInline):
    model = PardaImage
    extra = 1
    fields = ("image_preview", "image")
    readonly_fields = ("image_preview",)
    verbose_name_plural = "Parda rasmlari"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:100px; width:auto;" />', obj.image.url)
        return "Rasmsiz"
    image_preview.short_description = "Ko'rinish"

@admin.register(Parda)
class PardaAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Asosiy", {
            "fields": ("model", "boyi", "vitrina", "images_preview", "pieces_total", "vitrina_plus_pieces")
        }),
    ]
    list_display = (
        "model",
        "boyi",
        "vitrina",
        "pieces_total",
        "vitrina_plus_pieces",
        "images_preview",
    )
    readonly_fields = ("images_preview", "pieces_total", "vitrina_plus_pieces")
    search_fields = ("model",)
    inlines = [RulonKusokInline, PardaImageInline]

    def images_preview(self, obj):
        if obj.images.exists():
            return format_html(' '.join([f'<img src="{img.image.url}" style="height:60px; width:auto;" />' for img in obj.images.all()]))
        return "Rasmsiz"
    images_preview.short_description = "Barcha rasmlar"