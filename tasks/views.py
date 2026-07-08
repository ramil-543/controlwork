from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)
        
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'uncompleted':
        tasks = tasks.filter(completed=False)
        
    context = {
        'tasks': tasks,
        'search_query': search_query,
        'status_filter': status_filter
    }
    return render(request, 'tasks/task_list.html', context)
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Создать'})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Редактировать'})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')