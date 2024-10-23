from django import forms

from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'total_subs', 'start_date', 'end_date', 'start_time', 'end_time',]
