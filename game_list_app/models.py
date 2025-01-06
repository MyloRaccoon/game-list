from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Publisher(models.Model):
	name = models.CharField(max_length = 100)
	description = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to="uploads/", blank=True, null=True)

	add_date = models.DateTimeField(editable = False, default = timezone.now)
	modified_date = models.DateTimeField(editable = False, default = timezone.now)
	user_owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

	def save(self, *args, **kwargs):
		if not self.id:
			self.add_date = timezone.now()
			if 'user' in kwargs:
				self.user_owner = kwargs.pop('user')
		self.modified_date = timezone.now()
		return super(Publisher, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class Platform(models.Model):
	name = models.CharField(max_length = 100)
	release_date = models.IntegerField(blank=True, null=True)
	owner = models.ForeignKey(Publisher, on_delete=models.SET_NULL, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to="uploads/", blank=True, null=True)

	add_date = models.DateTimeField(editable = False, default = timezone.now)
	modified_date = models.DateTimeField(editable = False, default = timezone.now)
	user_owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

	def save(self, *args, **kwargs):
		if not self.id:
			self.add_date = timezone.now()
			if 'user' in kwargs:
				self.user_owner = kwargs.pop('user')
		self.modified_date = timezone.now()
		return super(Platform, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class Game(models.Model):
	title = models.CharField(max_length = 200)
	genre = models.CharField(max_length = 200, blank=True, null=True)
	publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, blank=True, null=True)
	platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, blank=True, null=True)
	release_date = models.IntegerField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to="uploads/", blank=True, null=True)

	add_date = models.DateTimeField(editable = False, default = timezone.now)
	modified_date = models.DateTimeField(editable = False, default = timezone.now)
	user_owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

	def save(self, *args, **kwargs):
		if not self.id:
			self.add_date = timezone.now()
			if 'user' in kwargs:
				self.user_owner = kwargs.pop('user')
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
		choices=State.choices,
		default=State.PLAYING,
		max_length=10
	)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['user', 'game'], name='unique_user_game')
		]

def is_game_in_user_list(user, game):
	return GameList.objects.filter(user=user, game=game).exists()

def get_game_state(user, game):
	game_list = GameList.objects.get(user=user, game=game)
	return game_list.get_state_display()

# class Rating(models.Model):
# 	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
# 	game = models.ForeignKey(Game, on_delete=models.CASCADE)
# 	grade = models.IntegerField()
	
# class Review(models.Model):
# 	rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
# 	text = models.CharField(max_length = 1000)