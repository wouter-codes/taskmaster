from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm


def index(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = TaskForm()
    
    tasks_todo = Task.objects.filter(completed=False).order_by("-created_at")
    tasks_done = Task.objects.filter(completed=True).order_by("-created_at")
    
    return render(
        request, "tasks/index.html", 
        {
            "tasks_todo": tasks_todo,
            "tasks_done": tasks_done,
            "form": form,
        }
    )

