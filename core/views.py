import datetime

from django.shortcuts import render, redirect
from core.forms import CallRequestForm
from core.models import ManagerCallRequest
from django.contrib.admin.models import LogEntry


def index(request):
    form = CallRequestForm()
    if request.method == 'POST':
        form = CallRequestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ManagerCallRequest.objects.create(full_name=data.get('name'),
                                              phone_number=data.get('phone'))
            return redirect('/')
    return render(request, 'core/index.html', {'form': form})

