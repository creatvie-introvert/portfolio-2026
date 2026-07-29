from django.contrib import admin
from .models import (
    CaseStudy,
    CaseStudyMedia,
    CaseStudySection,
    Project,
    Tag,
)


class CaseStudySectionInline(admin.StackedInline):
    model = CaseStudySection
    fields = ("sort_order", "section_type", "title", "body")
    extra = 0
    ordering = ("sort_order", "pk")
    show_change_link = True


class CaseStudyMediaInline(admin.StackedInline):
    model = CaseStudyMedia
    fields = (
        "sort_order",
        "media_type",
        "image",
        "alt_text",
        "caption",
    )
    extra = 0
    ordering = ("sort_order", "pk")


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
    inlines = (CaseStudySectionInline,)


@admin.register(CaseStudySection)
class CaseStudySectionAdmin(admin.ModelAdmin):
    list_display = (
        "case_study",
        "section_type",
        "title",
        "sort_order",
    )
    list_filter = ("section_type",)
    search_fields = (
        "case_study__project__name",
        "title",
        "body",
    )
    ordering = ("case_study", "sort_order", "pk")
    autocomplete_fields = ("case_study",)
    inlines = (CaseStudyMediaInline,)
