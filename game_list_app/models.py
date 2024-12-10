from django.db import models
from django.utils import timezone

# Create your models here.
class Publisher(models.Model):
	name = models.CharField(max_length = 100)
	description = models.TextField(blank=True, null=True)

	add_date = models.DateTimeField(editable = False, default = timezone.now)
	modified_date = models.DateTimeField(editable = False, default = timezone.now)

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.add_date = timezone.now()
		self.modified_date = timezone.now()
		return super(Publisher, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class Platform(models.Model):
	name = models.CharField(max_length = 100)
	release_date = models.IntegerField(blank=True, null=True)
	owner = models.ForeignKey(Publisher, on_delete=models.SET_NULL, blank=True, null=True)
	description = models.TextField(blank=True, null=True)

	add_date = models.DateTimeField(editable = False, default = timezone.now)
	modified_date = models.DateTimeField(editable = False, default = timezone.now)

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.add_date = timezone.now()
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

	add_date = models.DateTimeField(editable = False, default = timezone.now)
	modified_date = models.DateTimeField(editable = False, default = timezone.now)

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.add_date = timezone.now()
		self.modified_date = timezone.now()
		return super(Game, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

# class User(models.Model):
# 	username = models.CharField(max_length = 50)
# 	email = models.EmailField(max_length=254)

# 	def __str__(self):
# 		return username

# class Rating(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	game = models.ForeignKey(Game, on_delete=models.CASCADE)
# 	grade = models.IntegerField()
	
# class Review(models.Model):
# 	rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
# 	text = models.CharField(max_length = 1000)