from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User

from .models import *

from .forms import *


class Home(generic.ListView):
	template_name = "home.html"
	context_object_name = "latest_games"
 
	def get_queryset(self):
		"""Return the last five published games."""
		return Game.objects.order_by("-add_date")[:10]


class GameList(generic.ListView):
	template_name = "games.html"
	context_object_name = "games"

	def get_queryset(self):
		return Game.objects.order_by("-add_date")

class PlatformList(generic.ListView):
	template_name = "platforms.html"
	context_object_name = "platforms"

	def get_queryset(self):
		return Platform.objects.order_by("-add_date")

class PublisherList(generic.ListView):
	template_name = "publishers.html"
	context_object_name = "publishers"

	def get_queryset(self):
		return Publisher.objects.order_by("-add_date")


class GameDetail(generic.DetailView):
	model = Game
	template_name = "game.html"

class PlatformDetail(generic.DetailView):
	model = Platform
	template_name = "platform.html"

class PublisherDetail(generic.DetailView):
	model = Publisher
	template_name = "publisher.html"


def add_publisher(request):
	# if this is a POST request we need to process the form data
	if request.method == "POST":
		# create a form instance and populate it with data from the request:
		form = PublisherForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			name = form.cleaned_data["name"]
			description = form.cleaned_data["description"]
			publisher = Publisher(name = name, description = description)
			publisher.save()
			# redirect to a new URL:
			return HttpResponseRedirect(reverse("game_list_app:publisher_detail", args=[publisher.id]))

	# if a GET (or any other method) we'll create a blank form
	else:
		form = PublisherForm()

	return render(request, "add_publisher_form.html", {"form": form})

def add_platform(request):
	if request.method == "POST":
		form = PlatformForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data["name"]
			release_date = form.cleaned_data.get("release_date")
			owner = form.cleaned_data.get("owner")
			description = form.cleaned_data.get("description")
			Platform(name=name, release_date=release_date, owner=owner, description = description).save()
			return HttpResponseRedirect(reverse("game_list_app:home"))
	else:
		form = PlatformForm()

	return render(request, "add_platform_form.html", {"form": form})

def add_game(request):
	if request.method == "POST":
		form = GameForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			genre = form.cleaned_data.get("genre")
			publisher = form.cleaned_data.get("publisher")
			platform = form.cleaned_data.get("platform")
			release_date = form.cleaned_data.get("release_date")
			description = form.cleaned_data.get("description")
			Game(title=title, genre=genre, publisher=publisher, platform=platform, release_date=release_date, description = description).save()
			return HttpResponseRedirect(reverse("game_list_app:home"))
	else:
		form = GameForm()

	return render(request, "add_game_form.html", {"form": form})


def edit_publisher(request, pk):
	
	publisher = get_object_or_404(Publisher, pk=pk)

	# if this is a POST request we need to process the form data
	if request.method == "POST":
		# create a form instance and populate it with data from the request:
		form = PublisherForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			publisher.name = form.cleaned_data["name"]
			publisher.description = form.cleaned_data.get("description")

			publisher.save()
			# redirect to a new URL:
			return HttpResponseRedirect(reverse("game_list_app:home"))

	# if a GET (or any other method) we'll create a blank form
	else:
		form = PublisherForm(initial={"name": publisher.name, "description": publisher.description})

	return render(request, "edit_publisher_form.html", {"form": form, "pk": pk})

def edit_platform(request, pk):
	
	platform = get_object_or_404(Platform, pk=pk)

	if request.method == "POST":

		form = PlatformForm(request.POST)

		if form.is_valid():
			platform.name = form.cleaned_data["name"]
			platform.release_date = form.cleaned_data.get("release_date")
			platform.owner = form.cleaned_data.get("owner")
			platform.description = form.cleaned_data.get("description")

			platform.save()

			return HttpResponseRedirect(reverse("game_list_app:home"))

	else:
		form = PlatformForm(initial={"name": platform.name, "release_date": platform.release_date, "owner": platform.owner, "description": platform.description})

	return render(request, "edit_platform_form.html", {"form": form, "pk": pk})

def edit_game(request, pk):
	
	game = get_object_or_404(Game, pk=pk)

	if request.method == "POST":

		form = GameForm(request.POST)

		if form.is_valid():
			game.title = form.cleaned_data["title"]
			game.genre = form.cleaned_data.get("genre")
			game.publisher = form.cleaned_data.get("publisher")
			game.platform = form.cleaned_data.get("platform")
			game.release_date = form.cleaned_data.get("release_date")
			game.description = form.cleaned_data.get("description")

			game.save()

			return HttpResponseRedirect(reverse("game_list_app:home"))

	else:
		form = GameForm(initial={
			"title": game.title, 
			"genre": game.genre, 
			"publisher": game.publisher, 
			"platform": game.platform, 
			"release_date": game.release_date,
			"description": game.description
		})

	return render(request, "edit_game_form.html", {"form": form, "pk": pk})
		

def delete_publisher(request, pk):
	Publisher.objects.get(pk=pk).delete()
	return HttpResponseRedirect(reverse("game_list_app:home"))

def delete_platform(request, pk):
	Platform.objects.get(pk=pk).delete()
	return HttpResponseRedirect(reverse("game_list_app:home"))

def delete_game(request, pk):
	get_object_or_404(Game, pk=pk).delete()
	return HttpResponseRedirect(reverse("game_list_app:home"))


def delete_db(request):
	Game.objects.all().delete()
	Platform.objects.all().delete()
	Publisher.objects.all().delete()

	return HttpResponseRedirect(reverse("game_list_app:home"))


def signup(request):
	if request.method == "POST":
		form = SignInForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			email = form.cleaned_data.get("release_date")
			password = form.cleaned_data.get("password")
			User.objects.create_user(username, email, password).save()
			return HttpResponseRedirect(reverse("login"))
	else:
		form = SignInForm()

	return render(request, "signup.html", {"form": form})


## Doing the same thing without generic views
# def index(request):
# 	latest_games = Game.objects.order_by("-release_date")[:5]
# 	template = loader.get_template("index.html")
# 	context = {
# 		"latest_games": latest_games,
# 	}
# 	return HttpResponse(template.render(context, request))

# def game_detail(request, game_id):
# 	game = get_object_or_404(Game, pk=game_id)
# 	template = loader.get_template("game.html")
# 	context = { "game": game }
# 	return HttpResponse(template.render(context, request))

# def platform_detail(request, platform_id):
# 	platform = get_object_or_404(Platform, pk=platform_id)
# 	template = loader.get_template("platform.html")
# 	context = { "platform": platform }
# 	return HttpResponse(template.render(context, request))