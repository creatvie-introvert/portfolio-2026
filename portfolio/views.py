from django.shortcuts import render
from .models import Project, Tag


def work(request):
    # 1) Read the active tag slug from the querystring
    active_tag_slug = request.GET.get("tag")

    # 2) Base queryset: all published projects
    projects = (
        Project.objects
        .filter(is_published=True)
        .prefetch_related("tags")
    )

    # 3) Tags for the filter UI (only tags linked to published projects)
    tags = (
        Tag.objects
        .filter(projects__is_published=True)
        .distinct()
        .order_by("name")
    )

    # 4) Filtering logic + invalid slug fallback
    active_tag = None
    if active_tag_slug:
        active_tag = tags.filter(slug=active_tag_slug).first()

        if active_tag:
            projects = projects.filter(tags=active_tag)

        # If invalid slug: fallback to show all projects

    context = {
        "projects": projects,
        "tags": tags,
        "active_tag": active_tag,
    }

    return render(request, "portfolio/work.html", context)
