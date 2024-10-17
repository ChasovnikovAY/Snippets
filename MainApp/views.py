from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета',
                   'form':form,
                   }
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snipp_list")
        return render(request, 'pages/add_snippet.html', {'form': form})


def snippets_page(request, filter_type):
    # type = 1 - Все сниппеты
    # type = 2 - Мои
    snippets = Snippet.objects.all()
    if request.user.is_authenticated:
        if filter_type == 2:
            # Фильтруем Мои сниппеты
            snippets = snippets.filter(user=request.user.id)
    else:
        # Для неавторизованных тользователей только public сниппеты
        snippets = snippets.filter(is_public=True)

    context = {'pagename': 'Просмотр сниппетов',
               'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)

def snippet_detail(request, snippet_id):
    context = {'pagename':'Просмотр снипета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return render(request, "pages/error.html", context | {"error": f"Snippet with id={snippet_id} not found"})
    else:
        context["snippet"] = snippet
        return render(request, 'pages/snippet_detail.html', context)

def delete_snippet(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    snippet.delete()
    return redirect('snipp_list')

def edit_snippet(request, snippet_id):
    context = {'pagename': 'Редактирование снипета'}
    snippet = Snippet.objects.get(id=snippet_id)
    if request.method == "GET":
        form = SnippetForm(instance=snippet)
        return render(request, "pages/add_snippet.html", context | { "form":form })
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        snippet.save()
        return redirect("snipp_list")

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)
        # return HttpResponse("done")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            pass
        return redirect('home')

def logout(request):
    auth.logout(request)
    return redirect("home")

def my_snippets(request):
    pass