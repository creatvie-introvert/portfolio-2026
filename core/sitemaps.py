from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from portfolio.models import Project


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "privacy",
            "accessibility",
            "terms",
            "work",
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    priority = 0.9
    changefreq = "monthly"

    def items(self):
        return Project.objects.filter(is_published=True)

    def location(self, obj):
        return reverse("case_study", args=[obj.slug])
