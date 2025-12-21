from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Parda, RulonKusok, PardaImage


class RulonKusokInline(admin.TabularInline):
    model = RulonKusok
    extra = 1
    readonly_fields = ("created_at",)


class PardaImageInline(admin.TabularInline):
    model = PardaImage
    extra = 1
    readonly_fields = ("image_preview",)
    fields = ("image_preview", "image")

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px; width:auto;" />',
                obj.image.url
            )
        return "Rasmsiz"

    image_preview.short_description = "Ko‘rinish"


@admin.register(Parda)
class PardaAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Asosiy", {
            "fields": (
                "model",
                "boyi",
                "vitrina",
                "images_preview",
                "pieces_total",
                "vitrina_plus_pieces",
            )
        }),
    )

    readonly_fields = (
        "images_preview",
        "pieces_total",
        "vitrina_plus_pieces",
    )
    search_fields = ("model",)

    list_display = (
        "model",
        "boyi",
        "vitrina",
        "pieces_total",
        "vitrina_plus_pieces",
        "image_preview",
    )

    inlines = [RulonKusokInline, PardaImageInline]

    def images_preview(self, obj):
        images = [
            format_html(
                '<img src="{}" style="height:60px; width:auto; margin-right:5px;" />',
                img.image.url
            )
            for img in obj.images.all() if img.image
        ]
        return mark_safe(" ".join(images)) if images else "Rasmsiz"

    images_preview.short_description = "Barcha rasmlar"
