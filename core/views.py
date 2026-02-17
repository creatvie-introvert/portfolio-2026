from django.shortcuts import render
from portfolio.models import Project


def home(request):
    featured_projects = (
        Project.objects.filter(is_featured=True, is_published=True)
        .prefetch_related("tags")
        .order_by("-created_at")
    )

    context = {
        "featured_projects": featured_projects,
    }

    return render(request, "core/home.html", context)
