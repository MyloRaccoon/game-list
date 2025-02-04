from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)

    add_date = models.DateTimeField(editable=False, default=timezone.now)
    modified_date = models.DateTimeField(editable=False, default=timezone.now)
    user_owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.add_date = timezone.now()
            if "user" in kwargs:
                self.user_owner = kwargs.pop("user")
        self.modified_date = timezone.now()
        return super(Publisher, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)

    add_date = models.DateTimeField(editable=False, default=timezone.now)
    modified_date = models.DateTimeField(editable=False, default=timezone.now)
    user_owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.add_date = timezone.now()
            if "user" in kwargs:
                self.user_owner = kwargs.pop("user")
        self.modified_date = timezone.now()
        return super(Platform, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200, blank=True, null=True)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, blank=True, null=True
    )
    platform = models.ForeignKey(
        Platform, on_delete=models.SET_NULL, blank=True, null=True
    )
    release_date = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)

    add_date = models.DateTimeField(editable=False, default=timezone.now)
    modified_date = models.DateTimeField(editable=False, default=timezone.now)
    user_owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.add_date = timezone.now()
            if "user" in kwargs:
                self.user_owner = kwargs.pop("user")
        self.modified_date = timezone.now()
        return super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class GameList(models.Model):
    class State(models.TextChoices):
        WANT = "want", "Want to play"
        PLAYING = "playing", "Playing"
        FINISHED = "finished", "Finished"
        HUNDRED = "hundred", "100%"
        DROPPED = "dropped", "Dropped"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    state = models.CharField(
        choices=State.choices, default=State.PLAYING, max_length=10
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "game"], name="unique_user_game")
        ]


class Review(models.Model):
    class Rating(models.TextChoices):
        ONE = "1/5"
        TWO = "2/5"
        THREE = "3/5"
        FOUR = "4/5"
        FIVE = "5/5"

    game_list = models.ForeignKey(GameList, on_delete=models.CASCADE)
    rate = models.CharField(choices=Rating.choices, default=Rating.FIVE, max_length=10)
    review = models.TextField(blank=True, null=True)


def is_game_in_user_list(user, game):
    return GameList.objects.filter(user=user, game=game).exists()

def is_game_reviewed(game_list):
	return Review.objects.filter(game_list=game_list).exists()


def get_game_state(user, game):
    game_list = GameList.objects.get(user=user, game=game)
    return game_list.get_state_display()


def add_publisher(user, name, description, image):
    publisher = Publisher(name=name, description=description, image=image)
    publisher.save(user=user)
    return publisher.id


def add_platform(user, name, release_date, owner, description, image):
    platform = Platform(
        name=name,
        release_date=release_date,
        owner=owner,
        description=description,
        image=image,
    )
    platform.save(user=user)
    return platform.id


def add_game(user, title, genre, publisher, platform, release_date, description, image):
    game = Game(
        title=title,
        genre=genre,
        publisher=publisher,
        platform=platform,
        release_date=release_date,
        description=description,
        image=image,
    )
    game.save(user=user)
    return game.id


def edit_publisher(pk, name, description, image):
    publisher = get_object_or_404(Publisher, pk=pk)
    publisher.name = name
    publisher.description = description
    if image:
        publisher.image = image
    publisher.save()


def edit_platform(pk, name, release_date, owner, description, image):
    platform = get_object_or_404(Platform, pk=pk)
    platform.name = name
    platform.release_date = release_date
    platform.owner = owner
    platform.description = description
    if image:
        platform.image = image
    platform.save()


def edit_game(pk, title, genre, publisher, platform, release_date, description, image):
    game = get_object_or_404(Game, pk=pk)
    game.title = title
    game.genre = genre
    game.publisher = publisher
    game.platform = platform
    game.release_date = release_date
    game.description = description
    if image:
        game.image = image
    game.save()
