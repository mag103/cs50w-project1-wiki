from django.shortcuts import render, redirect
from markdown2 import markdown
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if util.get_entry(title):
        content = markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "title": title, "content": content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })


def search(request):
    query = request.POST.get('q')

    if util.get_entry(query):
        return redirect('entry', title=query)
    else:
        entries = util.list_entries()
        search_results = []
        for single_entry in entries:
            if query.lower() in single_entry.lower():
                search_results.append(single_entry)
        return render(request, "encyclopedia/search_results.html", {
            "search_results": search_results
        })


def add(request):
    flag = "none"

    if request.method == "POST":

        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title.strip() or not content.strip():
            flag = "empty"

        else:
            if util.get_entry(title):
                flag = "exists"
            else:
                util.save_entry(title, content)
                return redirect('entry', title=title)

    return render(request, "encyclopedia/add.html", {
        "flag": flag
    })


def edit(request, title):
    if util.get_entry(title):
        flag = "none"
        content = util.get_entry(title)

        if request.method == "POST":
            new_content = request.POST.get('content')
            util.save_entry(title, new_content)
            return redirect('entry', title=title)

        return render(request, "encyclopedia/edit.html", {
            "flag": flag, "title": title, "content": content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })


def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)
