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


def privacy(request):
    context = {
        "title": "Privacy Policy",
        "intro": "add intro here",
        "updated": "February 2026",
        "content": """
        <h3>Who I am</h3>
        <p class="text-secondary">This website is a personal portfolio operated by Leanne Bedeau-Rogers.</p>

        <h3>What data is collected</h3>
        <p class="text-secondary">If you contact me using the form, I may collect your name, email address, and message.</p>

        <h3>How your data is used</h3>
        <p class="text-secondary">Your information is only used to respond to your message and discuss potential work opportunities.</p>

        <h3></h3>
        <p class="text-secondary"></p>

        <h3></h3>
        <p class="text-secondary"></p>

        <h3></h3>
        <p class="text-secondary"></p>

        <h3></h3>
        <p class="text-secondary"></p>

        <h3></h3>
        <p class="text-secondary"></p>
        """
    }
    return render(request, "core/legal.html", context)


def accessibility(request):
    context = {
        "title": "Accessibility Statement",
        "intro": "intro here",
        "updated": "February 2026",
        "content": """
        <h3>Commitment</h3>
        <p class="text-secondary">I aim to make this website accessible and usable for as many people as possible.</p>

        <h3>Standards</h3>
        <p class="text-secondary">This site follows WCAG 2.1 Level AA where reasonably possible.</p>

        <h3>What I've done</h3>
        <p class="text-secondary">Semantic HTML, keyboard navigation, and accessible form labels.</p>

        <h3></h3>
        <p class="text-secondary"></p>

        <h3></h3>
        <p class="text-secondary"></p>

        <h3></h3>
        <p class="text-secondary"></p>
        """
    }
    return render(request, "core/legal.html", context)


def terms(request):
    context = {
        "title": "Terms of Use",
        "intro": "intro",
        "updated": "February 2026",
        "content": """
        <h3>Use of content</h3>
        <p class="text-secondary">All content is for portfolio purposes only.</p>

        <h3>Project examples</h3>
        <p class="text-secondary">Some projects may include fictional or demo content.</p>

        <h3>No professional advice</h3>
        <p class="text-secondary">Nothing on this site constitutes legal or financial advice.</p>

        <h3></h3>
        <p class="text-secondary"></p>

        <h3></h3>
        <p class="text-secondary"></p>

        <h3></h3>
        <p class="text-secondary"></p>

        <h3></h3>
        <p class="text-secondary"></p>

        <h3></h3>
        <p class="text-secondary"></p>
        """
    }
    return render(request, "core/legal.html", context)
