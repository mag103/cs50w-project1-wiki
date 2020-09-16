from django.shortcuts import render
from markdown2 import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    try:
        content = markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "title": title, "content": content
        })
    except TypeError:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

