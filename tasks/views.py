from django.shortcuts import render
from django.http import HttpRequest
from django.http.response import HttpResponse
from .models import Task


def index(request: HttpRequest) -> HttpResponse:
    tasks_todo = Task.objects.filter(completed=False).order_by("-created_at")
    tasks_done = Task.objects.filter(completed=True).order_by("-created_at")
    
    return render(
        request, "index.html", 
        {"tasks_todo": tasks_todo,
         "tasks_done": tasks_done,
        }
    )

