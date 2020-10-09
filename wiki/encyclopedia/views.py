from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from . import util
from django.urls import reverse
from markdown2 import Markdown
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search(request):
    query = request.GET['q']
    if util.get_entry(query):
        return HttpResponseRedirect(reverse('encyclopedia:entry', args=(query,)))
    else:
        li = util.list_entries()
        l = []
        for e in li:
            if query.lower() in e.lower():
                l.append(e)
        flag = 0 if l == [] else 1
        return render(request, 'encyclopedia/search.html', context={'flag': flag, 'l': l})


def display_entry(request, entry):
    try:
        markdown = Markdown()
        content = util.get_entry(entry)
        html = markdown.convert(content)
        flag = True if content else False
        return render(request, 'encyclopedia/entry.html', context={'html': html, 'flag': flag, 'title': entry})
    except:
        return HttpResponse('<html><body><p><p>Page not found</body></html>')


def show_entry_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not util.get_entry(title):
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('encyclopedia:entry', args=(title,)))

        else:
            return HttpResponse('<html><body><p><p>Page Already Exists</body></html>')

    return render(request, 'encyclopedia/add_entry.html')


def random_entry(request):
    li = util.list_entries()
    random_v = random.choice(li)
    markdown = Markdown()
    content = util.get_entry(random_v)
    html = markdown.convert(content)
    return HttpResponse(html)


def edit_entry(request, title):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title):
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('encyclopedia:entry', args=(title,)))

    content = util.get_entry(title)

    if content:
        return render(request, 'encyclopedia/edit_entry.html', context={'title': title, 'content': content})
    else:
        return HttpResponse('<p>page not found</p>')
