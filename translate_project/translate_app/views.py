from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from translate_app.models import Article, Image, ArticleViews
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
import json
from . import translate

@login_required
def user_logout(request): 
	logout(request) 
	return HttpResponseRedirect(reverse('index'))


@login_required
def restricted(request):

	return HttpResponse('something!')

def user_login(request):

	print("request.user:")
	print(request.user)
	print("request.user.is_authenticated:")
	print(request.user.is_authenticated)

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)

				print("request.user:")
				print(request.user)
				print("request.user.is_authenticated:")
				print(request.user.is_authenticated)

				return HttpResponseRedirect(reverse('index'))
		
			else:
				HttpResponse('your account has been disabled')

		else:
			print("Invalid login details: {0}, {1}".format(username, password))
	else:

		return render(request, 'translate_app/login.html', {})

@login_required
def user_page(request):

	#later when using date info: must retrieve through article_views model
	#av = ArticleViews.objects.filter(article=article, user=user)
	#av.date
	#maybe instead of .filter, use .latest

	user = request.user
	articles_viewed = user.article_set.distinct()
	context_dict={'articles':articles_viewed}
	return render(request, 'translate_app/user_page.html',context_dict)

def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		if user_form.is_valid():
			user=user_form.save()
			user.set_password(user.password)
			user.save()
			registered = True
		else:
			print(user_form.errors)
	else:
		user_form = UserForm()

	context_dict = {'user_form': user_form, 'registered': registered}
	return render(request, 'translate_app/register.html', context=context_dict)

def index(request, link = None):

	articles = Article.objects.all().order_by('-date')
	featured_articles = Article.objects.all()[:3]

	#get featured images
	featured_articles_list = []
	for featured in featured_articles:
		img = Image.objects.filter(article=featured)[0]
		featured.img = img.picture
		featured_articles_list.append(featured)

	print(request.user)

	#login(request, request.user)

	print(request.user.is_authenticated)

	#print(json.decoder.JSONDecoder().decode((articles[0].text)))

	print(request.user)
	user=request.user


	#maybe make this section a custom template tag (ala rango) if including
	#section/categories section on mutliple pages (possibly on 'section_page' also)
	class Section: pass
	section_names = Article.objects.values_list('section', flat=True).distinct()
	def get_articles_by_section():
		list_of_sections = []
		for section_name in section_names:
			section = Section()
			section.name=section_name
			section.articles=[]
			articles=Article.objects.filter(section=section_name)
			for article in articles:
				section.articles.append(article)
			list_of_sections.append(section)
		return list_of_sections

	sections = get_articles_by_section()



	context_dict = {'articles': articles, 'featured_articles_list':featured_articles_list, 'sections':sections}

	return render(request, 'translate_app/front_page.html', context=context_dict)


#	def track_article_pageviews(request):
	#this is actually all unncesary. was borrowing a pattern from rango tutorial
	#but realizing now that was for redirecting to otside url
	#this can all be accomplished in article_page view, based on user login status

		#this little section is for tracking article views.
		#one question I'll need to address is whether for beta testing will login be required for
		#article page. if no, then maybe I can add another set of links to each article
		#depending on template check of user login status.
		#in that case, perhaps the non-logged-in link will send you an obscured(paywall) version
		#of the page. the logged-in link will track the page visit
		#if yes, then this can all go through regular article_page
		
#		user= request.user_page
#		article_id = request.GET['article_id']
#		article= Article.objects.get(id=article_id)
#		ArticleViews.objects.create(article=a, user=user)
#		print(len(ArticleViews.objects.filter(article=a, user=user)))

#		return HttpResponseRedirect(reverse('article_page2', args=[article.slug]))

def input_link_page(request):
	if request.method == 'POST':
		print(request.POST['link'])
		link = request.POST['link']
	
	#	return HttpResponseRedirect(reverse('index'))#, args=[link]))
		return index(request,link)
	return render(request, 'translate_app/input_link_page.html')

def article_page(request, slug):
	article = Article.objects.get(slug=slug)
	#text = open(os.path.join(os.getcwd(), 'test_text.txt'), 'r').read().splitlines()
	text = json.decoder.JSONDecoder().decode(article.text)
	#trans = open(os.path.join(os.getcwd(), 'test_trans.txt'), 'r').read().splitlines()
	translated_text = json.decoder.JSONDecoder().decode(article.translated_text)
	print(translated_text)
	text_plus_translation = list(zip(text,translated_text))
	paragraph_container=[]
	for i in text_plus_translation:
		test = Test()
		test.text = i[0]
		test.trans =i[1]
		paragraph_container.append(test)
	print(len(paragraph_container))

	paragraph_count = len(paragraph_container)

	#image = Image.objects.filter(article=article)[1]
	images = Image.objects.filter(article=article)

	print(len(Image.objects.filter(article=article)))

	return render(request, 'translate_app/article.html', context={'paragraph_container':paragraph_container, 'article':article, 'images':images, 'paragraph_count':paragraph_count})


def section_page(request, section):
	articles = Article.obejcts.filter(section=section)
	context_dict = {'articles':articles}
	return render(request, 'translate_app/section_page.html', context=context_dict)



class TextContainer(): pass
class Test(): pass
class StoryUnit(): pass


def article_page2(request, slug):


	article = Article.objects.get(slug=slug)
	images = Image.objects.filter(article=article)
	#text = open(os.path.join(os.getcwd(), 'test_text.txt'), 'r').read().splitlines()
	text = json.decoder.JSONDecoder().decode(article.text)
	#trans = open(os.path.join(os.getcwd(), 'test_trans.txt'), 'r').read().splitlines()
	translated_text = json.decoder.JSONDecoder().decode(article.translated_text)
	text_plus_translation = list(zip(text,translated_text))
	paragraph_container=[]
	for i in text_plus_translation:
		test = Test()
		test.text = i[0]
		test.trans =i[1]
		paragraph_container.append(test)


	if request.user.is_authenticated:
		ArticleViews.objects.create(article=article, user=request.user)

		print(ArticleViews.objects.filter(article=article, user=request.user))
	

	#container_with_images =[]
	#for img in imgs:
	#index_position = 0
	#paragraph_container[index_position] = images[0]
	paragraph_container[0]

	if len(images)>1:
		skip_factor = int(len(paragraph_container)/len(images))
		for i in range(len(images)):
			#index_position += skip_factor
			index_position = i*skip_factor
			print(i)
			print(skip_factor)

			paragraph_container.insert(index_position, str(images[i].picture))
			#paragraph_container[index_position] = str(images[i].picture)

#			paragraph_container[index_position:index_position] = str(images[i].picture)
	else:
		#paragraph_container[:0]=images[0].picture
		paragraph_container.insert(0, images[0].picture)
		#paragraph_container[0]=images[0].picture


	print(images)	
	print(paragraph_container[0])
	print(paragraph_container[1])
	print(paragraph_container[2])
	print(paragraph_container[3])
	print(paragraph_container[4])

	paragraph_count = len(paragraph_container)

	context_dict={'paragraph_container':paragraph_container, 'article':article, 'images':images, 'paragraph_count':paragraph_count}

	return render(request, 'translate_app/article2.html', context=context_dict)




def photo_placement(images,paragraphs):
	i = len(images)
	p = len(paragraphs)

	skip_factor = int(p/i)

	img_plus_paras_list = []
	counter = 0
	for img in images:

		img_plus_paras = Test()
		img_plus_paras.img = img
		img_plus_paras.para_container = []

		for sf in range(skip_factor):
			para = paragraphs[counter:counter+1]
			img_plus_paras.para_container.append(para)
			counter+=1
	
		img_plus_paras_list.append(img_plus_paras)

	last_para_container = []
	last_paragraphs = p%i
	last_para_counter = -(last_paragraphs)
	for each in range(last_paragraphs):
		last_paras = (paragraphs[last_para_counter])
		last_para_container.append(last_paras)
		last_para_counter +=1

	img_plus_paras_list.append(last_para_container)

	return img_plus_paras_list
