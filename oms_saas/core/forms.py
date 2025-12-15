from django import forms
from .models import OMSSettings

class OMSSettingsForm(forms.ModelForm):
    class Meta:
        model = OMSSettings
        fields = [
            'brand_name', 'logo', 'footer_text',
            'dark_mode_enabled', 'whatsapp_token', 'whatsapp_api_url',
            'rounding_enabled'  # ✅ New
        ]