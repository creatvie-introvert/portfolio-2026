from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from portfolio.models import Project


def home(request):
    featured_projects = (
        Project.objects.filter(is_featured=True, is_published=True)
        .prefetch_related("tags")
        .order_by("-created_at")
    )

    success = request.GET.get("contact") == "success"

    context = {
        "featured_projects": featured_projects,
        "contact_success": success,
    }

    return render(request, "core/home.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        send_mail(
            subject=f"New contact form submission from {name}",
            message=f"{message}\n\nFrom: {email}",
            from_email=None,
            recipient_list=["lrogers1986@hotmail.com"]
        )

        return redirect("/?contact=success")

    return redirect("/")
