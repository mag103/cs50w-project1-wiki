from django.shortcuts import render
from markdown2 import markdown
from . import util


def index(request):
    if request.method == "POST":
        query = request.POST.get('q')

        if util.get_entry(query):
            return entry(request, query)
        else:
            entries = util.list_entries()
            search_results = []
            for single_entry in entries:
                if query.lower() in single_entry.lower():
                    search_results.append(single_entry)
            return render(request, "encyclopedia/search_results.html", {
                "search_results": search_results
            })

    else:
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





