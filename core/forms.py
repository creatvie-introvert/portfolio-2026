from django import forms
from django.core.exceptions import ValidationError


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "name",
                "class": "form-control",
                "id": "contact-name",
                "placeholder": "Your name",
            }
        ),
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "form-control",
                "id": "contact-email",
                "placeholder": "you@example.com",
            }
        ),
    )
    message = forms.CharField(
        min_length=5,
        max_length=3000,
        strip=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "contact-message",
                "placeholder": "Write your message...",
                "rows": 5,
            }
        ),
    )
    privacy = forms.BooleanField(
        required=True,
        error_messages={
            "required": "You must agree to the privacy policy.",
        },
        widget=forms.CheckboxInput(
            attrs={
                "id": "contact-privacy",
            }
        ),
    )
    contact_reference = forms.CharField(
        required=False,
        label="Contact reference",
        widget=forms.TextInput(
            attrs={
                "aria-hidden": "true",
                "autocomplete": "one-time-code",
                "data-1p-ignore": "true",
                "data-bwignore": "true",
                "data-lpignore": "true",
                "tabindex": "-1",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("contact_reference"):
            raise ValidationError(
                "Your message could not be submitted. Please try again."
            )

        return cleaned_data
