from django.core.exceptions import ValidationError
from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:
		return self.name


class Task(models.Model):
	title = models.CharField(max_length=255)
	due_date = models.DateTimeField(null=True, blank=True)
	completed = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tasks")

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:
		return self.title
	
	def save(self, *args, **kwargs):
		if len(self.title) > 100:
			raise ValidationError("title can't be longer than 100 chars")
		super().save(*args, **kwargs)
