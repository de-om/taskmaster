from django.shortcuts import redirect, render

from tasks import forms
from tasks.models import Subject, Task


def homepage(request):
    tasks = Task.objects.all().order_by("-created")[:4]
    return render(
        request,
        "tasks/homepage.html",
        {
            "title": "TaskMaster homepage",
            "tasks": tasks,
        },
    )


def examples(request):
    return render(
        request,
        "tasks/examples.html",
        {
            "title": "TaskMaster Examples",
        },
    )


def list_tasks(request):
    tasks = Task.objects.all()
    return render(
        request,
        "tasks/list_tasks.html",
        {
            "title": "Tareas activas",
            "tasks": tasks,
        },
    )


def task_detail(request, pk):  # Improve this!
    if task := Task.objects.filter(pk=pk):
        return render(
            request,
            "tasks/list_tasks.html",
            {
                "title": f"Tarea número {pk}",
                "tasks": task,
                "task_detail": True,
            },
        )
    else:
        return  # Error, no existe la tarea


def list_tasks_per_year(request, year):
    tasks = Task.objects.filter(created__year=year)
    return render(
        request,
        "tasks/list_tasks.html",
        {
            "title": f"Tareas creadas el año {year}",
            "tasks": tasks,
        },
    )


def search_task(request):
    if request.method == "POST":
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            tasks = Task.objects.filter(title__icontains=query)
            if priority := form.cleaned_data.get("priority"):
                tasks = tasks.filter(priority__in=priority)
            if form.cleaned_data.get("urgent"):
                tasks = tasks.filter(urgent=True)
    else:
        form = forms.SearchForm()
        tasks = []
        query = ""

    # query = request.POST.get("query")
    # if not query:
    #     query = request.GET.get("query", "")
    # tasks = Task.objects.filter(title__icontains=query)
    # priorities = request.POST.getlist("priority")
    # if priorities:
    #     tasks = tasks.filter(priority__in=priorities)

    return render(
        request,
        "tasks/search.html",
        {
            "title": "Buscar tareas",
            "form": form,
            "query": query,
            "tasks": tasks,
            # "priorities": priorities,
        },
    )


# Otros ejemplos:
# Model.objects.filter(num__gt=23) que num > 23
# Model.objects.filter(num__gte=23) que num ≥ 23
# Model.objects.filter(num__lt=23) que num < 23
# Model.objects.filter(num__lte=23) que num ≤ 23
# Model.objects.exclude(num=23) que num != 23
# Model.objects.filter(fecha=datetime.datetime.today())
# Model.objects.filter(fecha__gt=datetime.datetime.today())
# Model.objects.filter(fecha__year=2023)
# Model.objects.filter(fecha__year__gte=2022)
# Model.objects.filter(fecha__month=5).filter(fecha__year=2023)
# Model.objects.filter(fecha__year=2023)
# Model.objects.filter(texto__contains=txt)  # case sensitive
# Model.objects.filter(texto__icontains=txt)  # case insensitive
# Model.objects.filter(texto__contains=txt)  # case sensitive
# Model.objects.filter(texto__startwith=txt)  # case sensitive
# Model.objects.filter(texto__istartwith=txt)  # case insensitive
# Model.objects.filter(priority__in=['L', 'N'])
# Task.objects.filter(subject__name='core')


def list_tasks_by_priority(request, priority: str):
    priority = priority[0].upper()
    tasks = Task.objects.filter(priority=priority)
    if priority == "H":
        priority = "alta"
    elif priority == "N":
        priority = "media"
    elif priority == "L":
        priority = "baja"
    return render(
        request,
        "tasks/list_tasks.html",
        {
            "title": f"Tareas de prioridad {priority}",
            "tasks": tasks,
        },
    )


def add_task(request):
    if request.method == "POST":
        form = forms.CreateTaskForm(request.POST)
        if form.is_valid():
            form.save()  # new_task =
            return redirect("/")
    else:  # is GET, or other
        form = forms.CreateTaskForm()
    return render(
        request,
        "tasks/add_task.html",
        {
            "title": "Añadir una tarea",
            "form": form,
        },
    )


def edit_task(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        form = forms.EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("list_tasks")
    else:
        form = forms.EditTaskForm(instance=task)
    return render(
        request,
        "tasks/edit_task.html",
        {
            "title": f"Editar la tarea #{task.pk}",
            "form": form,
        },
    )


def complete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.is_complete = not task.is_complete
    task.save()
    return redirect("list_tasks")


def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect("list_tasks")


def list_subjects(request):
    subjects = Subject.objects.all()
    return render(
        request, "tasks/list_subjects.html", {"title": "Temas", "subjects": subjects}
    )


def subject_detail(request, pk):
    subject = Subject.objects.get(pk=pk)
    return render(
        request,
        "tasks/subject_detail.html",
        {
            "title": f"Tema {subject.name}",
            "subject": subject,
            "tasks": subject.tasks.all(),
        },
    )


def lab_view(request):
    return render(request, "tasks/lab.html", {"title": "Labs page"})
