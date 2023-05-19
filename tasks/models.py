from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

PRIORITIES = [
    ("L", "Prioridad baja"),
    ("N", "Prioridad media"),
    ("H", "Prioridad alta"),
]


def past_date(value):
    if value and value < timezone.now().date():
        raise ValidationError("La fecha de entrega debe ser hoy o futura.")


class Subject(models.Model):
    class Meta:
        verbose_name = "asignatura"
        verbose_name_plural = "asignaturas"

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="nombre de la asignatura",
        max_length=120,
        unique=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):  # en singular
    class Meta:
        verbose_name = "tarea"
        verbose_name_plural = "tareas"

    # id = models.AutoField(primary_key=True)  # si no defino lo hace auto
    title = models.CharField("título", max_length=250, unique=True)
    subject = models.ForeignKey(
        Subject,
        verbose_name="asignatura",
        on_delete=models.PROTECT,
        related_name="tasks",  # crea un atributo en la tabla a la que se refiere
        default=1
        # null=True, blank=True
    )
    due_date = models.DateField(
        "fecha de entrega",
        null=True,
        default=None,
        blank=True,
        validators=[past_date],
    )
    urgent = models.BooleanField("urgente", default=False)
    priority = models.CharField(
        "prioridad",
        max_length=1,
        choices=PRIORITIES,
        default="N",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tarea #{self.pk}: {self.title} [{self.due_date}]"
