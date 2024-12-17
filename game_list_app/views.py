from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User

from .models import *

from .forms import *


def error(request, error):
	error_msg = ""
	for l in error:
		if l == error[0]:
			error_msg += l.upper()
		elif l == '-' or l == '_':
			error_msg += ' '
		else:
			error_msg += l
	return render(request, "error.html", {"error": error_msg})

class Home(generic.ListView):
	template_name = "home.html"
	context_object_name = "latest_games"
 
	def get_queryset(self):
		return Game.objects.order_by("-add_date")[:10]


class GameListView(generic.ListView):
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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		game = self.object
		user = self.request.user
		game_in_list = is_game_in_user_list(user, game)
		context["user_is_owner"] = game.user_owner == user
		context["game_in_list"] = game_in_list
		if game_in_list:
			context["game_state"] = get_game_state(user, game)
		return context

class PlatformDetail(generic.DetailView):
	model = Platform
	template_name = "platform.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		platform = self.object
		user = self.request.user
		context["user_is_owner"] = platform.user_owner == user 
		return context

class PublisherDetail(generic.DetailView):
	model = Publisher
	template_name = "publisher.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		publisher = self.object
		user = self.request.user
		context["user_is_owner"] = publisher.user_owner == user 
		return context


def add_publisher(user, name, description):
	publisher = Publisher(name = name, description = description)
	publisher.save(user = user)
	return publisher.id

def add_platform(user, name, release_date, owner, description):
	platform = Platform(
		name = name, 
		release_date = release_date,
		owner = owner,
		description = description
	)
	platform.save(user = user)
	return platform.id

def add_game(user, title, genre, publisher, platform, release_date, description):
	game = Game(
		title = title,
		genre = genre,
		publisher = publisher,
		platform = platform,
		release_date = release_date,
		description = description
	)
	game.save(user = user)
	return game.id


def add_item(request, item):
	form_class_map = {
		"game": GameForm,
		"platform": PlatformForm,
		"publisher": PublisherForm,
	}
	process_data_function_map = {
		"game": add_game,
		"platform": add_platform,
		"publisher": add_publisher,
	}
	response_url_map = {
		"game": "game_list_app:game_detail",
		"platform": "game_list_app:platform_detail",
		"publisher": "game_list_app:publisher_detail",
	}

	if item not in form_class_map:
		raise Http404("Invalid item type.")

	form_class = form_class_map[item]
	process_data_function = process_data_function_map[item]
	response_url = response_url_map[item]

	if request.method == "POST":
		form = form_class(request.POST)
		if form.is_valid():
			item_id = process_data_function(request.user, **form.cleaned_data)
			return HttpResponseRedirect(reverse(response_url, args=[item_id]))
	else:
		form = form_class()

	context = {
		"form": form,
		"item": item,
	}

	return render(request, "add_form.html", context)


def edit_publisher(pk, name, description):
	publisher = get_object_or_404(Publisher, pk=pk)
	publisher.name = name
	publisher.description = description
	publisher.save()

def edit_platform(pk, name, release_date, owner, description):
	platform = get_object_or_404(Platform, pk=pk)
	platform.name = name
	platform.release_date = release_date
	platform.owner = owner
	platform.description = description
	platform.save()

def edit_game(pk, title, genre, publisher, platform, release_date, description):
	game = get_object_or_404(Game, pk=pk)
	game.title = title
	game.genre = genre
	game.publisher = publisher
	game.platform = platform
	game.release_date = release_date
	game.description = description
	game.save()

def get_filled_publisher_form(pk):
	publisher = get_object_or_404(Publisher, pk=pk)
	form = PublisherForm(initial= {
			'name': publisher.name,
			'description': publisher.description
		})
	return form

def get_filled_platform_form(pk):
	platform = get_object_or_404(Platform, pk=pk)
	form = PlatformForm(initial= {
			'name': platform.name,
			'release_date': platform.release_date,
			'owner': platform.owner,
			'description': platform.description
		})
	return form

def get_filled_game_form(pk):
	game = get_object_or_404(Game, pk=pk)
	form = GameForm(initial= {
			'title': game.title,
			'genre': game.genre,
			'publisher': game.publisher,
			'platform': game.platform,
			'release_date': game.release_date,
			'description': game.description
		})
	return form

def edit_item(request, item_type, pk):
	
	item_class_map = {
		"game": Game,
		"platform": Platform,
		"publisher": Publisher
	}
	form_class_map = {
		"game": GameForm,
		"platform": PlatformForm,
		"publisher": PublisherForm,
	}
	process_data_function_map = {
		"game": edit_game,
		"platform": edit_platform,
		"publisher": edit_publisher,
	}
	filled_form_function_map = {
		"game": get_filled_game_form,
		"platform": get_filled_platform_form,
		"publisher": get_filled_publisher_form
	}
	response_url_map = {
		"game": "game_list_app:game_detail",
		"platform": "game_list_app:platform_detail",
		"publisher": "game_list_app:publisher_detail",
	}

	if item_type not in item_class_map:
		raise Http404("Invalid item type.")

	form_class = form_class_map[item_type]
	
	process_data_function = process_data_function_map[item_type]
	response_url = response_url_map[item_type]
	filled_form_function = filled_form_function_map[item_type]

	item = get_object_or_404(item_class_map[item_type], pk=pk)

	if request.method == "POST":
		form = form_class(request.POST)
		if form.is_valid():
			if request.user == item.user_owner or request.user.is_staff:
				process_data_function(pk, **form.cleaned_data)
				return HttpResponseRedirect(reverse(response_url, args=[pk]))
			else:
				return HttpResponseRedirect(reverse("game_list_app:error", args=["You don't have the autorisation to edit this item"]))
			
	else:
		form = filled_form_function(pk)

	context = {
		'form': form,
		'item': item_type,
		'pk': pk
	}

	return render(request, "edit_form.html", context)		

def delete_publisher(request, pk):
	publiser = get_object_or_404(Publisher, pk=pk)

	if request.user == publisher.user_owner or request.user.is_staff:
		publisher.delete()
		return HttpResponseRedirect(reverse("game_list_app:home"))
	else:
		return HttpResponseRedirect(reverse("game_list_app:error", args=["You don't have the autorisation to delete this item"]))

def delete_platform(request, pk):
	platform = get_object_or_404(Platform, pk=pk)

	if request.user == platform.user_owner or request.user.is_staff:
		platform.delete()
		return HttpResponseRedirect(reverse("game_list_app:home"))
	else:
		return HttpResponseRedirect(reverse("game_list_app:error", args=["You don't have the autorisation to delete this item"]))

def delete_game(request, pk):
	game = get_object_or_404(Game, pk=pk)

	if request.user == game.user_owner or request.user.is_staff:
		game.delete()
		return HttpResponseRedirect(reverse("game_list_app:home"))
	else:
		return HttpResponseRedirect(reverse("game_list_app:error", args=["You don't have the autorisation to delete this item"]))


def delete_db(request):
	if request.user.is_staff:
		Game.objects.all().delete()
		Platform.objects.all().delete()
		Publisher.objects.all().delete()

		return HttpResponseRedirect(reverse("game_list_app:home"))
	else:
		return HttpResponseRedirect(reverse("game_list_app:error", args=["You don't have the autorisation to access this page"]))

def signup(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			email = form.cleaned_data.get("email")
			password = form.cleaned_data.get("password")

			if User.objects.filter(username=username).exists():
				form.add_error('username', 'This username is not avaible.')
			elif User.objects.filter(email=email).exists():
				form.add_error('email', 'This email is already used.')
			else:
				User.objects.create_user(username, email, password).save()
				return HttpResponseRedirect(reverse("login"))
	else:
		form = SignUpForm()

	return render(request, "signup.html", {"form": form})

def add_to_list(request, game_id):
	game = get_object_or_404(Game, pk=game_id)

	if request.method == "POST":
		form = GameListForm(request.POST)
		if form.is_valid():
			game_list = form.save(commit=False)
			game_list.user = request.user
			game_list.game = game  
			game_list.save()
			return HttpResponseRedirect(reverse('game_list_app:game_detail', args=[game_id]))
	else:
		form = GameListForm()

	return render(request, 'list_add.html', {'form': form, 'game': game})

def edit_from_list(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	game_list = GameList.objects.get(game=game, user=request.user)

	if request.method == "POST":
		form = GameListForm(request.POST, instance=game_list)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('game_list_app:game_detail', args=[game_id]))
	else:
		form = GameListForm(instance=game_list)

	return render(request, 'list_edit.html', {'form': form, 'game': game})

def delete_from_list(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	try:
		game_list = GameList.objects.get(user=request.user, game=game)
		game_list.delete()
		return HttpResponseRedirect(reverse("game_list_app:home"))
	except GameList.DoesNotExist:
		raise Http404("This game is not in this user's list.")

def profil_general(request):
	return render(request, 'profil_general_information.html', {})

class ProfilGameList(generic.ListView):
	template_name = "profil_list.html"
	context_object_name = "games"

	def get_queryset(self):
		gameListObject = GameList.objects.filter(user=self.request.user).select_related('game')
		return [game_list.game for game_list in gameListObject]