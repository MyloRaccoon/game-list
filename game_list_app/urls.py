from django.urls import path

from . import views

app_name = "game_list_app"
urlpatterns = [
	path("", views.Home.as_view(), name = "home"),

	path("game/", views.GameList.as_view(), name = "game_list"),
	path("platform/", views.PlatformList.as_view(), name = "platform_list"),
	path("publisher/", views.PublisherList.as_view(), name = "publisher_list"),

	path("game/<int:pk>/", views.GameDetail.as_view(), name = "game_detail"),
	path("platform/<int:pk>/", views.PlatformDetail.as_view(), name = "platform_detail"),
	path("publisher/<int:pk>/", views.PublisherDetail.as_view(), name = "publisher_detail"),

	path("publisher/add/", views.add_publisher, name = "add_publisher"),
	path("platform/add/", views.add_platform, name = "add_platform"),
	path("game/add/", views.add_game, name = "add_game"),

	path("publisher/edit/<int:pk>/", views.edit_publisher, name = "edit_publisher"),
	path("platform/edit/<int:pk>/", views.edit_platform, name = "edit_platform"),
	path("game/edit/<int:pk>/", views.edit_game, name = "edit_game"),

	path("publisher/delete/<int:pk>/", views.delete_publisher, name = "delete_publisher"),
	path("platform/delete/<int:pk>/", views.delete_platform, name = "delete_platform"),
	path("game/delete/<int:pk>/", views.delete_game, name = "delete_game"),

	path("delete-db/", views.delete_db, name = "delete_db"),

	path("signup/", views.signup, name="signup"),
]