from django.shortcuts import render, redirect
from markdown2 import markdown
import random
from . import util


# List all entries on the index page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Display entry page
def entry(request, title):
    if util.get_entry(title):
        content = markdown(util.get_entry(title))  # Convert markdown to HTML
        return render(request, "encyclopedia/entry.html", {
            "title": title, "content": content
        })
    # Go to error page if entry with provided title does not exist
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })


# Search for entries matching the query from the search box
def search(request):
    query = request.POST.get('q')  # Get query from search box

    # If there is an exact match, go to entry page
    if util.get_entry(query):
        return redirect('entry', title=query)

    # Else search for matching substrings
    else:
        entries = util.list_entries()
        search_results = []
        for single_entry in entries:
            if query.lower() in single_entry.lower():
                search_results.append(single_entry)
        # Display search_results as a list
        # If there are no search_results, message is displayed (covered by html template)
        return render(request, "encyclopedia/search_results.html", {
            "search_results": search_results
        })


# Add new entry
def add(request):
    flag = "none"

    # When form is submitted, create new entry
    if request.method == "POST":

        title = request.POST.get('title')
        content = request.POST.get('content')

        # If title or content is empty
        if not title.strip() or not content.strip():
            flag = "empty"

        else:
            # If entry with this title already exists
            if util.get_entry(title):
                flag = "exists"
            else:
                # Save new entry
                util.save_entry(title, content)
                return redirect('entry', title=title)

    # Display "add" page
    return render(request, "encyclopedia/add.html", {
        "flag": flag
    })


# Edit entry
def edit(request, title):

    # Check if entry with this title exists
    if util.get_entry(title):
        content = util.get_entry(title)

        # When form is submitted, update entry with new content and redirect to entry page
        if request.method == "POST":
            new_content = request.POST.get('content')
            util.save_entry(title, new_content)
            return redirect('entry', title=title)

        # Load entry title and content
        return render(request, "encyclopedia/edit.html", {
            "title": title, "content": content
        })
    else:
        # Go to error page if entry with provided title does not exist
        return render(request, "encyclopedia/error.html", {
            "title": title
        })


# Go to random entry page
def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)
