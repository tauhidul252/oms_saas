from django.shortcuts import render, redirect
from .models import OMSSettings
from .forms import OMSSettingsForm
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def system_settings(request):
    settings_instance, created = OMSSettings.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = OMSSettingsForm(request.POST, request.FILES, instance=settings_instance)
        if form.is_valid():
            form.save()
            return redirect('system_settings')
    else:
        form = OMSSettingsForm(instance=settings_instance)
    return render(request, 'settings/system_settings.html', {'form': form})
