from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import request

from MainApp.models import Snippet, Comment
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required
def add_snippet_page(request):
    if request.method == "GET":
        print("GET")
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета',
                   'form':form,
                   }
    if request.method == "POST":
        print("POST")
        form = SnippetForm(request.POST)
        #print(form)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snipp_list")

    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.filter(is_public=True)
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
        context["comments"] = Comment.objects.filter(snippet = snippet)
        return render(request, 'pages/snippet_detail.html', context)

def delete_snippet(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    snippet.delete()
    return redirect('snipp_list')

@login_required
def edit_snippet(request, snippet_id):
    context = {'pagename': 'Редактирование снипета'}
    snippet = Snippet.objects.get(id=snippet_id)
    if request.method == "GET":
        form = SnippetForm(instance=snippet)
        return render(request, "pages/add_snippet.html", context | { "form":form })
    if request.method == "POST":
        print("POST")
        data_form = request.POST
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        # snippet.is_public = data_form.get("is_public", False)
        snippet.save()
        return redirect("snipp_list")

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
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

def create_user(request):
    if request.method == "GET":
        print("Get")
        form = UserRegistrationForm()
    if request.method == "POST":
        print("Post")
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form }
    return render(request, 'pages/registration.html', context)

@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {'pagename': 'Мои сниппеты',
               'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)

@login_required
def add_snippet_comment(request, snippet_id):
    if request.method == "GET":
        comment_form = CommentForm()
        snippet = Snippet.objects.get(id=snippet_id)
        context = {'pagename': 'Добавление коментария',
                   'form': comment_form,
                   'snippet': snippet
                   }
        return render(request, 'pages/comments.html', context)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #print(request.POST)
            #print(f"request.snippet_id={request.POST.get("snippet_id")}")
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(id=request.POST.get("snippet_id"))
            comment.save()
            return redirect('snippet-detail', comment.snippet.id)

