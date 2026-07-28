# portfolio-2026

## Local email testing

SMTP remains the default email backend. To test contact-form delivery locally
without Zoho credentials, explicitly enable Django’s console email backend:

```bash
USE_CONSOLE_EMAIL_BACKEND=True .venv/bin/python manage.py runserver
```

Emails will be printed to the development terminal instead of being delivered.
Do not enable this setting in production or use real personal information while
testing. When the setting is absent or `False`, Django continues to use the
configured SMTP backend.
