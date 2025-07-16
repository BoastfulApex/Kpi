from django import forms
from .models import WorkSchedule
from datetime import datetime
from django.core.exceptions import ValidationError


class SelectTimeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        hours = [(f'{h:02}', f'{h:02}') for h in range(0, 24)]
        minutes = [(f'{m:02}', f'{m:02}') for m in range(0, 60, 5)]

        widgets = [
            forms.Select(attrs=attrs, choices=hours),
            forms.Select(attrs=attrs, choices=minutes),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.hour, value.minute]
        return [None, None]

    def format_output(self, rendered_widgets):
        return ':'.join(rendered_widgets)
