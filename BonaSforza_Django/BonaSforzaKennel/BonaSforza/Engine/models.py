from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify

from .utils import *



# Create your models here.

class Dog(models.Model):
	category=models.SlugField(null=True)

	slug=models.SlugField(null=False, unique=True)

	name=models.CharField(unique=True, max_length=200)
	born_date=models.DateField(auto_now=False, auto_now_add=False)
	parents=models.TextField()
	breeder_or_kennel=models.CharField(null=True, max_length=200)
	titles=models.TextField(null=True)
	working_titles=models.TextField(null=True)
	tests=models.TextField(null=True)
	facebook=models.CharField(null=True, max_length=200)

	main_image=models.ImageField(upload_to='dogs', null=True, blank=True)

	
	def get_absolute_url(self):
		return reverse('dog_page_url', kwargs={'category': self.category, 'slug': self.slug})

	def save(self, *args, **kwargs):
		if is_ascii(self.name):
			self.slug=slugify(self.name)
		else:
			translit=transliterate(self.name)
			self.slug=slugify(translit)	
		return super().save(*args, **kwargs)	


	def delete(self, *args, **kwargs):
		self.main_image.delete()
		super().delete(*args, **kwargs)




class Gallery(models.Model):
	parent=models.ForeignKey(Dog, on_delete=models.CASCADE, null=True, blank=True, related_name='gallery')

	item=models.ImageField(upload_to='dogs/gallery', null=True, blank=True)

	def delete(self, *args, **kwargs):
		self.item.delete()
		super().delete(*args, **kwargs)	





						





