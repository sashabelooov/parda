from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Parda, RulonKusok, PardaImage
from django.contrib.admin import SimpleListFilter
from django.contrib import admin
from django.db.models import Q



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




class BoyiSearchFilter(admin.SimpleListFilter):
    title = "Boyi bo'yicha izlash"
    parameter_name = "boyi_search"
    template = "admin/boyi_input_filter.html"

    def lookups(self, request, model_admin):
        return ()  # Keep empty

    def has_output(self):
        return True  # Optional: force show even if no choices

    def queryset(self, request, queryset):
        value = request.GET.get("boyi_search")
        if value:
            try:
                boyi_val = float(value.replace(",", "."))
                return queryset.filter(boyi=boyi_val)
            except ValueError:
                return queryset.none()
        return queryset
    
    
class ModelSearchFilter(admin.SimpleListFilter):
    title = "Model bo'yicha izlash"
    parameter_name = "model_search"
    template = "admin/boyi_input_filter.html"

    def lookups(self, request, model_admin):
        return ()

    def has_output(self):
        return True

    def queryset(self, request, queryset):
        value = request.GET.get("model_search")
        if value:
            return queryset.filter(model__icontains=value)
        return queryset
    
    

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
    # search_fields = ("model",)
    
    list_filter = (BoyiSearchFilter, ModelSearchFilter)

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
