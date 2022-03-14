from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

# Create your views here.
from django.http import HttpResponse
from .forms import TodoForm
from .models import Todo
from django.contrib.auth.decorators import login_required

class MyClass:
  x = 5

my_obj = MyClass()

def home(request):
	return render(request, 'todo/home.html')

@login_required
def currenttodos(request):
	todos = Todo.objects.filter(user=request.user)
	return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def createtodo(request):
	bad_form_data_error = "Something went wrong with the form.  Check your entries."
	if request.method == 'GET':
		return render(request, 'todo/createtodo.html', {'form':TodoForm()})
	else:
		try:
			form = TodoForm(request.POST)
			newtodo = form.save(commit=False)
			newtodo.user = request.user
			newtodo.save()
			return redirect('currenttodos')
		except ValueError:
			return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':bad_form_data_error})

@login_required
def viewtodo(request, todo_pk):
	todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	return render(request, 'todo/viewtodo.html', {'todo':todo})

@login_required
def edittodo(request, todo_pk):
	bad_form_data_error = "Something went wrong with the form.  Check your entries."
	todo = get_object_or_404(Todo, pk=todo_pk)
	if request.method == 'GET':
		form = TodoForm(instance=todo)
		return render(request, 'todo/edittodo.html', {'todo':todo, 'form':form})
	else:
		form = TodoForm(request.POST, instance=todo)
		btn_name = request.POST.get('form-btn')
		try:
			if btn_name == 'btn_save_todo':
				form.save()
				return render(request, 'todo/viewtodo.html', {'todo':todo})
			elif btn_name == 'btn_delete_todo':
				todo.delete()
				return redirect('currenttodos')
			else:
				if btn_name == 'btn_complete_todo':
					todo.datecompleted = timezone.now()
				if btn_name == 'btn_incomplete_todo':
					todo.datecompleted = None
				todo.save()
				return render(request, 'todo/edittodo.html', {'todo':todo, 'form':form})
		except ValueError:
			return render(request, 'todo/edittodo.html', {'todo':todo, 'form':form, 'error':bad_form_data_error})





# ----
