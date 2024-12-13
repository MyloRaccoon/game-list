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

	path("<str:item>/add/", views.add_item, name = "add_item"),

	path("<str:item_type>/edit/<int:pk>", views.edit_item, name = "edit_item"),

	path("publisher/delete/<int:pk>/", views.delete_publisher, name = "delete_publisher"),
	path("platform/delete/<int:pk>/", views.delete_platform, name = "delete_platform"),
	path("game/delete/<int:pk>/", views.delete_game, name = "delete_game"),

	path("delete-db/", views.delete_db, name = "delete_db"),

	path("signup/", views.signup, name="signup"),

	path('error/<str:error>/', views.error, name = "error"),
]