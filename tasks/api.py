import json

from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response

from tasks.models import Task
from tasks.serializers import TaskSerializer


def api_get(request, id=None):
    return api_get_by_id(request, id) if id is not None else api_get_all(request)


def api_get_by_id(request, id):
    if request.method == "GET":
        try:
            task = Task.objects.get(pk=id)
            t = {
                "title": task.title,
                "subject": task.subject.name,
                "due_date": f"{task.due_date}",
                "urgent": task.urgent,
                "priority": task.priority,
                "created": f"{task.created}",
                "updated": f"{task.updated}",
                "is_complete": task.is_complete,
            }
            response = json.dumps(t)
            return HttpResponse(response, content_type="application/json", status=200)
        except Task.DoesNotExist:
            error = {
                "status": {
                    "type": "error",
                    "code": 404,
                    "message": "The requested task could not be found",
                }
            }
            return HttpResponse(
                json.dumps(error), content_type="application/json", status=404
            )


def api_get_all(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        response = []
        for task in tasks:
            t = {
                "title": task.title,
                "subject": task.subject.name,
                "due_date": f"{task.due_date}",
                "urgent": task.urgent,
                "priority": task.priority,
                "created": f"{task.created}",
                "updated": f"{task.updated}",
                "is_complete": task.is_complete,
            }
            response.append(t)
        response = json.dumps(response)
        return HttpResponse(response, content_type="application/json", status=200)


def api_creat_task(request, pk):
    return HttpResponse(pk)


class API_Create(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        # Formato invalido
        if request.content_type != "application/json":
            error_response = {
                "status": {
                    "type": "error",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Malformed body: only valid JSON is accepted",
                }
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Tarea Existente
        task_name = serializer.validated_data.get("title")
        due_date = serializer.validated_data.get("due_date")

        if Task.objects.filter(title=task_name, due_date=due_date).exists():
            error_response = {
                "status": {
                    "type": "error",
                    "code": status.HTTP_409_CONFLICT,
                    "message": "A task with the same name and due date already exists.",
                }
            }
            return Response(error_response, status=status.HTTP_409_CONFLICT)

        # Crear Tarea
        self.perform_create(serializer)

        task_id = serializer.instance.id

        response_data = {
            "status": {
                "type": "ok",
                "code": status.HTTP_200_OK,
                "message": "Task created successfully",
            },
            "id": task_id,
        }
        return Response(response_data, status=status.HTTP_200_OK)
