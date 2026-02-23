from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
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
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            message = request.POST.get("message")

            # Validate first
            if not name or not email or not message:
                return redirect("/?contact=error")

            full_message = f"""
New enquiry from your portfolio:

Name: {name}
Email: {email}

Message:
{message}
"""

            email_message = EmailMessage(
                subject=f"New message form submission from {name}",
                body=full_message,
                from_email="hello@leannebedeaurogers.com",
                to=["hello@leannebedeaurogers.com"],  # ✅ correct
                reply_to=[email],
            )

            email_message.send(fail_silently=False)

            messages.success(request, "Message sent successfully!")
            return redirect("/")

        except Exception as e:
            print("EMAIL ERROR:", e)
            return redirect("/?contact=error")

    return redirect("/")


def privacy(request):
    context = {
        "title": "Privacy Policy",
        "intro": "This privacy policy explains what data is collected when you "
        "use this website, and how it's used.",
        "updated": "February 2026",
        "content": """
        <h3>Who I am</h3>
        <p class="text-secondary">This website is a personal portfolio operated by Leanne Bedeau-Rogers.</p>

        <h3>What data is collected</h3>
        <p class="text-secondary">If you contact me using the form, I may collect your name, email address, and message.</p>

        <h3>How your data is used</h3>
        <p class="text-secondary">Your information is only used to respond to your message and discuss potential work opportunities.</p>

        <h3>Cookies and analytics</h3>
        <p class="text-secondary">This website may use basic analytics to understand how visitors use the site. If analytics are enabled, they may collect anonymous usage information such as pages visited and device type.</p>

        <h3>Third-party services</h3>
        <p class="text-secondary">If this site uses third-party services (such as hosting providers, form handling, or analytics), those services may process limited data as part of providing their functionality.</p>

        <h3>How long data is kept</h3>
        <p class="text-secondary">Messages sent through the contact form are kept only as long as needed to respond and follow up.</p>

        <h3>Your rights</h3>
        <p class="text-secondary">You can request access to, correction of, or deletion of any personal data you have shared via the contact form.</p>

        <h3>Contact</h3>
        <p class="text-secondary">If you have questions about this privacy policy, you can contact me using the form on the Contact section of this website.</p>
        """
    }
    return render(request, "core/legal.html", context)


def accessibility(request):
    context = {
        "title": "Accessibility Statement",
        "intro": "This website is designed to be accessible and usable for as many people as possible, including users who rely on assistive technology.",
        "updated": "February 2026",
        "content": """
        <h3>Commitment</h3>
        <p class="text-secondary">I'm committed to making this website accessible, inclusive, and easy to use across devices and assistive technologies.</p>

        <h3>Standards</h3>
        <p class="text-secondary">This site aims to follow the Web Content Accessibility Guidelines (WCAG) 2.1, Level AA, where reasonably possible.</p>

        <h3>What I've done</h3>
        <p class="text-secondary">The site uses semantic HTML, clear heading structure, strong colour contrast, keyboard-friendly navigation, and accessible form labels.</p>

        <h3>Motion and animations</h3>
        <p class="text-secondary">Animations are designed to be subtle and non-essential, and the site avoids rapid flashing or distracting movement.</p>

        <h3>Known limitations</h3>
        <p class="text-secondary">Some visual content, such as project screenshots, may not include full descriptive text in every context, but I aim to improve this over time.</p>

        <h3>Feedback and contact</h3>
        <p class="text-secondary">If you experience any accessibility barriers while using this site, please contact me and I’ll do my best to fix the issue.</p>
        """
    }
    return render(request, "core/legal.html", context)


def terms(request):
    context = {
        "title": "Terms of Use",
        "intro": "These terms explain how this website and its content can be used. By browsing the site, you agree to these terms.",
        "updated": "February 2026",
        "content": """
        <h3>About this website</h3>
        <p class="text-secondary">This website is a personal portfolio operated by Leanne Bedeau-Rogers. It showcases selected work, case studies, and contact information.</p>

        <h3>Use of content</h3>
        <p class="text-secondary">Some projects may include fictional or demo content.</p>

        <h3>No professional advice</h3>
        <p class="text-secondary">All content on this website (including text, design, layout, and project case study content) is provided for viewing and evaluation purposes only.</p>
        <p class="text-secondary">You may not copy, reproduce, republish, or distribute any part of this website without permission.</p>

        <h3>Project examples</h3>
        <p class="text-secondary">Some projects shown on this site may include fictional content, placeholder data, or simplified examples created for learning, demonstration, or portfolio purposes.</p>

        <h3>No professional advice</h3>
        <p class="text-secondary">Any information presented on this website is provided for general information only.</p>
        <p class="text-secondary">Nothing on this website should be interpreted as financial, legal, medical, or professional advice.</p>

        <h3>External links</h3>
        <p class="text-secondary">This website may include links to third-party websites. I'm not responsible for the content, privacy practices, or availability of external sites.</p>

        <h3>Availability</h3>
        <p class="text-secondary">I aim to keep this website available and working, but I do not guarantee uninterrupted access or that the site will always be error-free.</p>

        <h3>Limitation of liability</h3>
        <p class="text-secondary">To the fullest extent permitted by law, I’m not liable for any loss or damage resulting from the use of this website.</p>

        <h3>Contact</h3>
        <p class="text-secondary">If you have questions about these terms, you can contact me using the form on this website.</p>
        """
    }
    return render(request, "core/legal.html", context)
