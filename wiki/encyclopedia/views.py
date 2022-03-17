import re
from typing import Text
from django.http.response import HttpResponse
from django.shortcuts import render
import markdown
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def converttohtml(entry_name):
    mark = markdown.Markdown()
    entry = util.get_entry(entry_name)
    html = mark.convert(entry) if entry else None
    return html

def entry(request, entry_name):
    entrypage = converttohtml(entry_name)

    if entrypage is None:
        return HttpResponse("does not exist, Check out another page")
    return render(request, "encyclopedia/entry.html", {
        "entry" : entrypage,
        "entryTitle" : entry_name
    })     


def search(request):

	if request.method == 'POST':

		input = request.POST.get('q')
		html = converttohtml(input)
		entries = util.list_entries()
		search_pages = []

		for entry in entries:
			if input.upper() in entry.upper():
				search_pages.append(entry)

		for entry in entries:
			if input.upper() == entry.upper():
				return render(request, "encyclopedia/entry.html",{
					"entry": html,
					"entryTitle": input
				})

			elif search_pages != []:
				return render(request, "encyclopedia/search.html",{
					"entries": search_pages
					})

			else:
				return HttpResponse("Not Found!")

def newpage(request):	
	return render(request, "encyclopedia/newpage.html")

def savepage(request):
	if request.method == "POST":
		title = request.POST.get("title")
		text = request.POST.get("text")
		entries = util.list_entries()

		if title in entries:
			return HttpResponse("This Title Is Already Exist!")
		else:
			util.save_entry(title, text)
			html = converttohtml(title)
			return render(request, "encyclopedia/entry.html", {
				"entry" : html ,
				"entryTitle" : title ,
			})	

def editpage(request):
	if request.method == "POST":
		title = request.POST.get("title")
		text = util.get_entry(title)

		return render(request, "encyclopedia/edit.html", {
			"entryTitle" : title ,
			"entry" : text,
		})

def saveeditpage(request):
	if request.method  == "POST":

		title = request.POST.get("title")
		text = request.POST.get("text")
		util.save_entry(title, text)
		html = converttohtml(title)
		return render(request, "encyclopedia/entry.html", {
			"entryTitle" : title ,
			"entry" : html ,
		})		

def randompage(request):
	entries = util.list_entries()
	randompage	= random.choice(entries)
	html = converttohtml(randompage)

	return render(request, "encyclopedia/entry.html", {
		"entryTitle" : randompage , 
		"entry" : html ,
	})