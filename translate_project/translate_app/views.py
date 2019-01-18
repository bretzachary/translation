from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from translate_app.models import Article, Image
import os
import json


from . import translate

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
	text = json.decoder.JSONDecoder().decode(article.text)
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

	#image = Image.objects.filter(article=article)[1]
	images = Image.objects.filter(article=article)

	print(len(Image.objects.filter(article=article)))

	return render(request, 'translate_app/article.html', context={'paragraph_container':paragraph_container, 'article':article, 'images':images})


#def article_page(request, article=None):
#	text = open(os.path.join(os.getcwd(), 'translate_app/test_text.txt'), 'r').read().splitlines()
#	trans = open(os.path.join(os.getcwd(), 'translate_app/test_trans.txt'), 'r').read().splitlines()

#	tpt = list(zip(text,trans))
#	empty=[]
#	for i in tpt:
#		test = Test()
#		test.text = i[0]
#		test.trans =i[1]
#		empty.append(test)
#	print(empty[4])
#	return render(request, 'translate_app/article.html', context={'tpt':tpt, 'text':text, 'trans':trans, 'empty':empty})
#	#return HttpResponse(text)





class TextContainer(): pass
class Test(): pass


#text = open(os.path.join(os.getcwd(), 'test_text.txt'), 'r').read().splitlines()
#trans = open(os.path.join(os.getcwd(), 'test_trans.txt'), 'r').read().splitlines()

#json.dumps()