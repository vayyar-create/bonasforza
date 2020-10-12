from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.forms import inlineformset_factory
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import send_mail
import codecs

from .models import *
from .forms import *

# Create your views here.

def index(request):
    return render(request, 'Engine/index.html')  

def contact(request):
	if request.method == 'POST':
		form=MailForm(request.POST)

		if form.is_valid():
			slug=form.cleaned_data.get('slug')
			email=form.cleaned_data.get('email')
			subject='Bona Sforza - Новое собщение. {}'.format(form.cleaned_data.get('subject'))
			message='От: {}\nEmail: {}\n\n\t{}'.format(slug, email, form.cleaned_data.get('message'))

			recipient=[settings.EMAIL_HOST_USER]

			send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=False)

	else:
		form=MailForm()	
	return render(request, 'Engine/contacts.html', context={'form': form })


class Login(View):	
	def get(self, request):
		form=LoginForm()
		return render(request, 'Engine/login.html', context={'form': form})
	def post(self, request):
		loginform=LoginForm(request.POST)

		if loginform.is_valid():

			username=loginform.cleaned_data.get('username')
			password=loginform.cleaned_data.get('password')

			user=auth.authenticate(username=username, password=password)

			if user is not None:
				auth.login(request, user)
				return redirect('/')

		return render(request, 'Engine/login.html', context={'form': loginform})	


def logout(request):
	auth.logout(request)

	return redirect('/')		




def dog_list(request, category):
	dogs=Dog.objects.filter(category=category)

	return render(request, 'Engine/dog/dog_list.html', context={'category': category, 'dogs': dogs})	



def dog_page(request, category, slug):
	dog=Dog.objects.get(slug=slug)

	return render(request, 'Engine/dog/dog_page.html', context={'category': category, 'slug': slug, 'dog': dog})


# CRUD
class AddDog(LoginRequiredMixin, View):

	raise_exception=True

	dog=Dog()
	bound_form=DogForm(instance=dog)
	GalleryFormset=inlineformset_factory(Dog, Gallery, fields=('item',), extra=1)

	def get(self, request, category):
		form=DogForm(instance=self.dog)
		formset=self.GalleryFormset()

		return render(request, 'Engine/dog/add_new_dog.html', context={
			'category': category,
			'form': form,
			'formset': formset
			})

	def post(self, request, category):
		bound_form=DogForm(request.POST, request.FILES)

		formset=self.GalleryFormset(request.POST, request.FILES)

		if bound_form.is_valid():
			new_dog=bound_form.save(commit=False)
			new_dog.category=category

			formset=self.GalleryFormset(request.POST, request.FILES, instance=new_dog)

			if formset.is_valid():
				new_dog.save()
				formset.save()

				return redirect(new_dog)

		return render(request, 'Engine/dog/add_new_dog.html', context={
			'category': category,
			'form': bound_form,
			'formset': formset
			})


class UpdateDog(LoginRequiredMixin, View):
	GalleryFormset=inlineformset_factory(Dog, Gallery, fields=('item',), extra=1, max_num=1)

	def get(self, request, category, slug):
		dog=Dog.objects.get(slug=slug)

		bound_form=DogForm(instance=dog)
		formset=self.GalleryFormset(instance=dog)


		return render(request, 'Engine/dog/update_dog.html', context={
			'category': category,
			'slug': slug,
			'form': bound_form,
			'dog': dog,
			'formset': formset
			})

	def post(self, request, category, slug):

		dog=Dog.objects.get(slug=slug)
		bound_form=DogForm(request.POST, request.FILES, instance=dog)

		formset=self.GalleryFormset(request.POST, request.FILES)


		if bound_form.is_valid():

			new_dog=bound_form.save(commit=False)

			formset=self.GalleryFormset(request.POST, request.FILES, instance=new_dog)

			if formset.is_valid():

				new_dog.save()

				formset.save()

				return redirect(new_dog)


		return render(request, 'Engine/dog/update_dog.html', context={
			'category': category,
			'slug': slug,
			'form': bound_form,
			'dog': dog,
			'formset': formset
			})
		


class DeleteDog(LoginRequiredMixin, View):
	def get(self, request, category, slug):
		dog=Dog.objects.get(slug=slug)
		return render(request, 'Engine/dog/delete_dog.html', context={'category': category, 'slug': slug, 'dog': dog})

	def post(self, request, category, slug):
		dog=Dog.objects.get(slug=slug)
		gallery=Gallery.objects.filter(parent=dog)
		for g in gallery:
			g.delete()
		dog.delete()
		return redirect(reverse('dog_list_url', kwargs={'category': category}))













	
 





