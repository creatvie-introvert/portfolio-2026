from django.contrib import admin
from .models import Tag, Project, CaseStudy


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "is_featured", "is_published", "created_at")
    list_filter = ("is_featured", "is_published", "created_at")
    search_fields = ("name", "slug", "short_description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("project", "created_at", "updated_at")
    search_fields = (
        "project__name",
        "intro",
        "problem",
        "role",
        "stack",
        "timeline",
    )
    autocomplete_fields = ("project",)
