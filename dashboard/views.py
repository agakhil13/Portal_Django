from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.views import generic

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added from {request.user.username} successfully!")
        return redirect('notes')
        
    else:
        form = NotesForm()
        notes = Notes.objects.filter(user=request.user)
        context = {'notes': notes, 'form': form}
        return render(request, 'dashboard/notes.html', context)

def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

class NotesDetailView(generic.DetailView):
    model = Notes
