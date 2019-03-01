from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from translate_app.models import Article, Image, ArticleViews, ArticleWords, RegistrationCode
from .forms import UserForm, ArticleForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
import json
from . import translate
from .vocab import views_bit
from .vocab2 import update_articlewords
import requests
from random import sample
from .registration_code_generator import generate

def add_art_and_img(request):
	if not request.user.is_superuser:
		return HttpResponse('must login as superuser')

	if request.method == "POST":
		form = ArticleForm(data=request.POST)
		if form.is_valid():
			article = form.save()
		else:
			print(form.errors)
		#article = form.save()

		text = article.text.splitlines()
		text = list(filter(None, text))
		article.text = json.dumps(text)

		translated_text = article.translated_text.splitlines()
		translated_text = list(filter(None, translated_text))
		article.translated_text = json.dumps(translated_text)
		#
		#text = text.splitlines()
		#text = list(filter(None, text))
		#article.text = json.dumps(text)


		article.save()
		
		images = []
	
		if request.POST.get('img1'):
			image1 = request.POST.get('img1')
			caption1 = request.POST.get('caption1')
			images.append((image1, caption1))

		if request.POST.get('img2'):
			image2 = request.POST.get('img2')
			caption2 = request.POST.get('caption2')
			images.append((image2, caption2))

		if request.POST.get('img3'):
			image3 = request.POST.get('img3')
			caption3 = request.POST.get('caption3')
			images.append((image3, caption3))

		if request.POST.get('img4'):
			image4 = request.POST.get('img4')
			caption4 = request.POST.get('caption4')
			images.append((image1, caption1))

		if request.POST.get('img5'):
			image5 = request.POST.get('img5')
			caption5 = request.POST.get('caption5')
			images.append((image5, caption5))

		if request.POST.get('img6'):
			image6 = request.POST.get('img6')
			caption6 = request.POST.get('caption6')
			images.append((image6, caption6))

		if request.POST.get('img7'):
			image7 = request.POST.get('img7')
			caption7 = request.POST.get('caption7')
			images.append((image7, caption7))
	
		number_of_images = len(images)
		
		print(number_of_images)
		print(images)

		os.mkdir('media/articles/{}'.format(article.slug))
		os.mkdir('media/articles/{}/images'.format(article.slug))
		
		for i in range(number_of_images):
				x = i+1 #media files seem to be unopen-able with filename 0.jpg
				with open(os.path.join(os.getcwd(), 'media/articles/{}/images/{}.jpg'.format(article.slug, str(x))), 'wb') as f:
					f.write(requests.get(images[i][0]).content)

				image = Image(article=article)
				image.picture = 'articles/{}/images/{}.jpg'.format(article.slug, str(x))
				if images[i][1]:
					image.caption = images[i][1]

				image.save()

		update_articlewords(article)
		try:
			print(article.articlewords.all_words)
		except:
			print('COULDNT DO THAT')

		return HttpResponseRedirect(reverse('article_page', args=[article.slug]))
	
	article_form = ArticleForm()

	return render(request, 'translate_app/add_art_and_img.html', {'article_form': article_form})

def template_test(request):
#	return render(request, 'translate_app/header.html')
	print(request.subdomain_language)
	return HttpResponse(request.subdomain_language)

@login_required
def user_logout(request): 
	logout(request) 
	return HttpResponseRedirect(reverse('index'))


@login_required
def restricted(request):

	return HttpResponse('something!')

def user_login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)

				return HttpResponseRedirect(reverse('index'))
		
			else:
				HttpResponse('your account has been disabled')

		else:
			return HttpResponse('invalid credentials. please try logging in again.')
			print("Invalid login details: {0}, {1}".format(username, password))
	else:

		return render(request, 'translate_app/login_template.html', {})

@login_required
def user_page(request):

	#later when using date info: must retrieve through article_views model
	#av = ArticleViews.objects.filter(article=article, user=user)
	#av.date
	#maybe instead of .filter, use .latest

	user = request.user
	articles_viewed = user.article_set.distinct()
	context_dict={'articles':articles_viewed}
	return render(request, 'translate_app/user_page_template.html',context_dict)

def register(request):
	registered = False
	registration_code = RegistrationCode.objects.get(pk=1)

	if request.method == 'POST':

		if request.POST.get('code') == registration_code.code:
			print(registration_code)
			#registration_code.code = generate()
			#registration_code.save()
			print(registration_code)
		else:
			return HttpResponse('bad code!')

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
	return render(request, 'translate_app/register_template.html', context=context_dict)

def index(request, link = None):
	articles = Article.objects.all().order_by('-date')
	featured_articles = Article.objects.all()[:3]

	#get featured images
	featured_articles_list = []
	for featured in featured_articles:
		img = Image.objects.filter(article=featured)[0]
		featured.img = img.picture
		featured_articles_list.append(featured)

	main_article = Article.objects.get(id=44)
	img = Image.objects.filter(article=main_article)[0]
	main_article.img = img.picture

	first_featured_articles_column =[]
	#two_featured_articles = Article.objects.all()[:2]
	two_featured_articles = Article.objects.all().order_by('-id')[:2]
	for featured in two_featured_articles:
		img = Image.objects.filter(article=featured)[0]
		featured.img = img.picture
		first_featured_articles_column.append(featured)	

	second_featured_articles_column =[]
	two_featured_articles = Article.objects.all()[2:4]
	for featured in two_featured_articles:
		img = Image.objects.filter(article=featured)[0]
		featured.img = img.picture
		second_featured_articles_column.append(featured)	


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
			articles=Article.objects.filter(section=section_name)[:4]
			for article in articles:
				article.image = article.image_set.first().picture
				section.articles.append(article)
			list_of_sections.append(section)
		return list_of_sections

	sections = get_articles_by_section()



	context_dict = {'articles': articles, 'main_article': main_article, 'first_featured_articles_column':first_featured_articles_column, 'second_featured_articles_column':second_featured_articles_column, 'featured_articles_list':featured_articles_list, 'sections':sections}

	return render(request, 'translate_app/front_page_template.html', context=context_dict)


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
	articles = Article.objects.filter(section=section)
	for article in articles:
		article.img = article.image_set.first()
	context_dict = {'articles':articles, 'section':section}
	return render(request, 'translate_app/section_page_template.html', context=context_dict)



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

		#print(ArticleViews.objects.filter(article=article, user=request.user))

	paragraph_container[0]

	if len(images)>1:
		skip_factor = int(len(paragraph_container)/len(images))
		for i in range(len(images)):
			index_position = i*skip_factor

			paragraph_container.insert(index_position, str(images[i].picture))

	else:
		paragraph_container.insert(0, images[0].picture)

	paragraph_count = len(paragraph_container)

	context_dict={'paragraph_container':paragraph_container, 'article':article, 'images':images, 'paragraph_count':paragraph_count}
	context_dict['vocab'] = views_bit(article)

	return render(request, 'translate_app/article_page_redesign.html', context=context_dict)




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






#with the paywall
#this is basically the case study for templates
def article_paywall(request, slug):


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

	if len(images)>1:
		skip_factor = int(len(paragraph_container)/len(images))
		for i in range(len(images)):
			index_position = i*skip_factor
			

			paragraph_container.insert(index_position, str(images[i].picture))

	else:
		paragraph_container.insert(0, images[0].picture)

	title_img = paragraph_container[0]

	paragraph_container = paragraph_container[1:5]

	paragraph_count = len(paragraph_container)

	context_dict={'paragraph_container':paragraph_container, 'title_img':title_img,'article':article, 'images':images, 'paragraph_count':paragraph_count}
	context_dict['vocab'] = views_bit(article)

	return render(request, 'translate_app/article_paywall.html', context=context_dict)



#name this function
def article_page_with_paywall(request, slug):

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

	if len(images)>1:
		skip_factor = int(len(paragraph_container)/len(images))
		for i in range(len(images)):
			index_position = i*skip_factor

			visual=Test()
			visual.picture = str(images[i].picture)
			visual.caption = images[i].caption
			paragraph_container.insert(index_position, visual)
			print('LLLL' + visual.picture)
			#paragraph_container.insert(index_position, str(images[i].picture))

	else:

		visual=Test()
		visual.picture = str(images[0].picture)
		visual.caption = images[0].caption
		paragraph_container.insert(0, visual)
		#print('345345345 ' + visual.picture)

		#paragraph_container.insert(0, images[0].picture)


	context_dict={}
	
	vocab = ArticleWords.objects.get(article=article).most_common_words
	vocab = json.loads(vocab)
	vocab = sample(vocab, 20)

	paragraph_count = len(paragraph_container)

	if request.user.is_authenticated:
		ArticleViews.objects.create(article=article, user=request.user)

		context_dict={'paragraph_container':paragraph_container, 'article':article, 'images':images, 'paragraph_count':paragraph_count}
		#context_dict['vocab'] = views_bit(article)
		context_dict['vocab'] = vocab

		return render(request, 'translate_app/article_page_redesign_template.html', context=context_dict)

	else:
		#title_img = paragraph_container[0]
		title_img = paragraph_container[0].picture
		paragraph_container = paragraph_container[1:3]

		context_dict={'paragraph_container':paragraph_container, 'title_img':title_img,'article':article, 'images':images, 'paragraph_count':paragraph_count}
		#context_dict['vocab'] = views_bit(article)
		context_dict['vocab'] = vocab
		return render(request, 'translate_app/article_paywall_template.html', context=context_dict)
