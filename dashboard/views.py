from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.views import generic
from youtubesearchpython import VideosSearch
import wikipedia
import requests

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

def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished =True
                else:
                    finished =False
            except:
                finished =False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request,f"Homework Added from {request.user.username}!!")
            return redirect('homework')

    else:
        form = HomeworkForm()
        homework = Homework.objects.filter(user=request.user)
        if len(homework) == 0:
            homework_done = True
        else:
            homework_done = False
        context = {'homeworks': homework,
            'homeworks_done': homework_done,
            'form':form,
        }
        return render(request, 'dashboard/homework.html', context)

def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    
    homework.save()
    return redirect('homework')

def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request,'dashboard/youtube.html', context)

    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request,'dashboard/youtube.html', context)

def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f"Todo Added from {request.user.username}!!")
            return redirect('todo')
    else:
        form = TodoForm()
        todo = Todo.objects.filter(user=request.user)
        if len(todo) == 0:
            todos_done = True
        else:
            todos_done = False
        context = {
            'todos': todo,
            'form': form,
            'todos_done': todos_done,
        }
        return render(request, 'dashboard/todo.html', context)

def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+ text
        r = requests.get(url)
        answer = r.json()

        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo'].get('title'),
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            if answer['items'][i]['volumeInfo'].get("imageLinks"):
                result_dict['thumbnail'] = answer['items'][i]['volumeInfo'].get("imageLinks").get("thumbnail")
            else:
                result_dict['thumbnail'] = ""
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request,'dashboard/books.html', context)

    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request,'dashboard/books.html', context)

def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+ text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
        except:
            phonetics = ''
        try:
            audio = ''
            i =0
            while audio == '':
                audio = answer[0]['phonetics'][i]['audio']
                i += 1
        except:
            audio = ''
        try:
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
        except:
            definition = ''
        try:
            example = answer[0]['meanings'][0]['definitions'][0]['example']
        except:
            example = ''
        try:
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
        except:
            synonyms= ''
        context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        return render(request,'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {'form':form}
    return render(request,'dashboard/dictionary.html', context)

def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary
        }
        return render(request,'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {'form':form}
    return render(request,'dashboard/wiki.html', context)

def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)  
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                 'form': form,
                 'm_form': measurement_form,
                 'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} Yard = {int(input)*3} Foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} Foot = {int(input)/3} Yard'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input': True,
                    'answer':answer
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()  
            context = {
                 'form': form,
                 'm_form': measurement_form,
                 'input': True
             }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} Pound = {int(input)*0.453592} Kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} Kilogram = {int(input)*2.20462} Pound'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input': True,
                    'answer':answer
                }            
    else:
        form = ConversionForm()
        context = {
        'form': form,
        'input': False
    }
    return render(request,'dashboard/conversion.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created for {username}!!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/register.html', context)