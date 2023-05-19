from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from tasks.models import Task

PRIORITIES = [
    ("L", "Prioridad baja"),
    ("N", "Prioridad media"),
    ("H", "Prioridad alta"),
]


def max_due_date(value: timezone):
    if value and value - timezone.timedelta(days=365) > timezone.now().date():
        raise ValidationError("La fecha de entrega debe ser durante el próximo año.")


class SearchForm(forms.Form):
    query = forms.CharField(required=False, label="Buscar")
    priority = forms.MultipleChoiceField(
        label="Prioridad",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=PRIORITIES,
    )
    urgent = forms.BooleanField(required=False, label="Urgente")


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "subject", "due_date", "priority", "urgent"]
        # fields = "__all__"  # No se recomienda, puede haber campos privados


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "subject", "due_date", "priority", "urgent"]

    due_date = forms.DateField(
        validators=[
            max_date,
        ]
    )

    # def clean_due_date(self):
    #     due_date = self.cleaned_data["due_date"]
    #     max_due_date(due_date)
    #     return due_date

    # def clean(self):
    #     cleaned_data = super().clean()

    #     due_date = cleaned_data["due_date"]
    #     if due_date.year < 2024:
    #         msg = "La fecha debe ser en 2023 o posterior"
    #         self.add_error("due_date", msg)

    #     return cleaned_data
