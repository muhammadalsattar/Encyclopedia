from django.shortcuts import render
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random


from . import util

class searchentry(forms.Form):
    entryname = forms.CharField(label="", widget= forms.TextInput(attrs={'placeholder':'Search'}))

class create_entry(forms.Form):
    title = forms.CharField(label="Title", max_length=30)
    Content = forms.CharField(widget=forms.Textarea)

def index(request):
    if request.POST:
        form = searchentry(request.POST)
        if form.is_valid():
            entryname = form.cleaned_data['entryname']
            entry = util.get_entry(entryname)
            if entry == None:
                entries = util.list_entries()
                results = [r for r in entries if entryname in r]
                return render(request, "encyclopedia/results.html", {"results": results})
            else:
                request.session["entry"] = entryname
                return render(request, "encyclopedia/singleentry.html", {"entry": markdown2.markdown(util.get_entry(entryname)), "form": searchentry()})
        else:
            return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), "form": searchentry()})
    else:   
        entry = random.choice(util.list_entries())
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form": searchentry(), "entry": entry
        })

def title(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html")
    else:
        request.session["entry"] = title
        return render(request, "encyclopedia/singleentry.html", {"entry": markdown2.markdown(util.get_entry(title)), "entrytitle": title, "form": searchentry()})

def results(request):

    return render(request, "encyclopedia/results.html", {"form": searchentry()})


def create(request):
    if request.POST:
        form = create_entry(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['Content']
            titles = util.list_entries()
            if title in titles:
                return render(request, "encyclopedia/create.html", {"create": create_entry(), "form": searchentry(), "error": "Entery already exists!"})
            else:
                util.save_entry(title, content)
                request.session["entry"] = title
                return render(request, "encyclopedia/singleentry.html",{"entry": markdown2.markdown(util.get_entry(title)), "entrytitle": title} )
    else:
        return render(request, "encyclopedia/create.html", {"create": create_entry(), "form": searchentry()})

def edit(request):
    title = request.session.get("entry")
    if request.POST:
        content = request.POST.get("content")
        util.save_entry(title, content)
        return render(request, "encyclopedia/singleentry.html",{"entry": markdown2.markdown(util.get_entry(title)), "entrytitle": title})
    else:
        return render(request, "encyclopedia/edit.html", {"entry": util.get_entry(title)})
