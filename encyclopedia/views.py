import markdown

import random

from django.http import HttpResponse, HttpResponseRedirect

from django import forms 
from django.urls import reverse

from django.shortcuts import render


from . import util
class newEntryForm (forms.Form):
    title = forms.CharField(label="Enter Title")
    markdownContent = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "cols": 5}), label='')

class editForm (forms.Form):
    markdownEntry = forms.CharField(
        widget=forms.Textarea(), label='')


# to list all the entries 
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        
     
    })

# to get an entry and markdown the entry
def getEntry(request, title):
    entries = util.list_entries()
    if title not in entries:
        return render(request, "encyclopedia/error.html", {
             "warning": f"{title} page couln't be found.",
             "head": "Not found"
        })
    return render(request, "encyclopedia/entry.html", {
       "title": title,
        "content": markdown.markdown(util.get_entry(title))
    })

# To search  for an encyclopedia
def search(request):
    if request.method== "GET":
        query = request.GET['q']
        if util.get_entry(query):
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": markdown.markdown(util.get_entry(query))  
            }) 
        else: 
            entries = util.list_entries()
            likeEntries = [ entry for entry in entries if query.lower() in entry.lower()]
            
            if len(likeEntries) == 0:
                return render(request, "encyclopedia/searchResults.html",{
                    "warning": f"{query} page couldn't be found.",
                    "head": "Not found"
                })
            else:
                return render(request, "encyclopedia/searchResults.html", {
                    "likeEntries": likeEntries
                })

           
# To create a new entry
def creatNewEntry(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = newEntryForm(request.POST) 
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["markdownContent"]
            for entry in entries:
                if title.capitalize() in entries:
                    return render(request, "encyclopedia/error.html",{
                        "warning": f"The {title} page already exists"
                    })
                else:
                    util.save_entry(title, content)
                    return render(request, "encyclopedia/entry.html",{
                        "title": title,
                        "content": markdown.markdown(content)
                    })
    return render(request, "encyclopedia/newPage.html", {
            "form": newEntryForm()
    })


#to edit an entry
def edit(request, title):
    content = util.get_entry(title)
    if content is None:
         return HttpResponseRedirect(reverse("wiki:index"))
    else:
        if request.method == "POST":
            form = editForm(request.POST)
            if form.is_valid():
                newContent = form.cleaned_data["markdownEntry"]
                
                util.save_entry(title, newContent)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "content": markdown.markdown(newContent)
                })
        return render(request, "encyclopedia/EditPage.html", {   
            "editForm": editForm(initial={'markdownEntry': content}),
         "title": title
        })


#to get a random page
def random_page(request):
    entries = util.list_entries()
    num = random.randint(0, len(entries)-1)
    random_page_generated = util.get_entry(entries[num]) 
    return render(request, "encyclopedia/entry.html", {
        "content":markdown.markdown(random_page_generated),
        "title": entries[num]
    })

    
