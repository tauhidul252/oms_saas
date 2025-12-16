from django.db import models

class OMSSettings(models.Model):
    brand_name = models.CharField(max_length=100, default="Your Brand Name")
    logo = models.ImageField(upload_to='settings/', null=True, blank=True)
    footer_text = models.CharField(max_length=200, default="Thank you for using OMS SaaS")
    dark_mode_enabled = models.BooleanField(default=False)
    # Add to OMSSettings model
    whatsapp_token = models.CharField(max_length=255, null=True, blank=True)
    whatsapp_api_url = models.URLField(null=True, blank=True)
    rounding_enabled = models.BooleanField(default=False)  # ✅ Rounding system

    def __str__(self):
        return self.brand_name

    def logo_url(self):
        if self.logo:
            return self.logo.url
        return "/static/images/default-logo.png"
