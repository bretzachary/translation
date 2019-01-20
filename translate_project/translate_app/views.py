from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from translate_app.models import Article, Image
from rango.forms import UserForm
import os
import json


from . import translate

def register(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

def index(request, link = None):
	articles = Article.objects.all()
	featured_articles = Article.objects.all()[:3]

	#get featured images
	featured_articles_list = []
	for featured in featured_articles:
		img = Image.objects.filter(article=featured)[0]
		featured.img = img.picture
		featured_articles_list.append(featured)

	#print(json.decoder.JSONDecoder().decode((articles[0].text)))
	print(featured_articles)

	context_dict = {'articles': articles, 'featured_articles_list':featured_articles_list}

	return render(request, 'translate_app/front_page.html', context=context_dict)

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

	print(paragraph_container[0].text)
	print(len(images))

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


	return render(request, 'translate_app/article2.html', context={'paragraph_container':paragraph_container, 'article':article, 'images':images, 'paragraph_count':paragraph_count})




def photo_placement(images,paragraphs):
	i = len(images)
	p = len(paragraphs)

	skip_factor = int(p/i)

	#should
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
		#print('RRRRRRRRRRRRRRRRRRRRRRRR' + last_paras)

	img_plus_paras_list.append(last_para_container)

	return img_plus_paras_list
