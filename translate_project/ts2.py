import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'translate_project.settings')

import django
django.setup()

import requests
from bs4 import BeautifulSoup as BS
from google.cloud import translate
import os
from django.template.defaultfilters import slugify
from translate_app.models import Article, Image
import json


class r_s:

	url = 'https://www.nytimes.com/2017/08/24/technology/coding-boot-camps-close.html'
	path = os.path.join(os.getcwd(), 'google.json')
	os.environ['GOOGLE_APPLICATION_CREDENTIALS']=path

	def __init__(self, url = url, title=None, text=None):
		self.url = url
		self.title = title
		self.text = text
		self.is_translated = False
		self.section=None
		self.publisher=None

	def request_soup(self):
		r = requests.get(self.url)
		self.soup = BS(r.text, features='html.parser')
		text = self.soup.find_all('p')
		self.text = [i.text for i in text]
		return self.text

	def translate_text(self, filetype='html', target_language='es'):
		if filetype == 'html':
			self.request_soup()
		translate_client = translate.Client()
		translation = translate_client.translate(self.text, target_language=target_language)
		translation = [para['translatedText'] for para in translation]
		self.translation = translation
		self.is_translated = True
		return self.translation

	def save_to_file(self, includes_images=True):

		self.slug = slugify(self.title)
		os.mkdir('media/articles/{}'.format(self.slug))
		os.mkdir('media/articles/{}/images'.format(self.slug))
		os.mkdir('articles/{}'.format(self.slug))
		os.mkdir('articles/{}/images'.format(self.slug))

		translation = json.dumps(self.translation)
		text = json.dumps(self.text)

		article = Article(url = self.url, title = self.title, slug = self.slug, text=text, translated_text=translation)
		if not(self.section == None):
			article.section = self.section

		if self.publisher:
			article.publisher = self.publisher

		article.save()

		for i in self.translation:
			with open(os.path.join(os.getcwd(), 'articles/{}/original.txt'.format(self.slug)), "a+", encoding='utf-8') as t:
				t.write(i + "\r\n")

		for i in self.text:
			with open(os.path.join(os.getcwd(), 'articles/{}/translation.txt'.format(self.slug)), "a+", encoding='utf-8') as t:
				t.write(i + "\r\n")

		if includes_images == True:
			imgs = self.soup.find_all('img')
			for i in range(len(imgs)):
				x = i+1 #media files seem to be unopen-able with filename 0.jpg
				with open(os.path.join(os.getcwd(), 'media/articles/{}/images/{}.jpg'.format(self.slug, str(x))), 'wb') as f:
					f.write(requests.get(imgs[i]['src']).content)

				image = Image(article=article)
				image.picture = 'articles/{}/images/{}.jpg'.format(self.slug, str(x))

				image.save()
		


#img = soup.find_all('img')['src']
#req = requests.get(img)
#with open(os.path.join(os.getcwd(), 'test.jpg'), 'wb') as f:
#	f.write(req.content)

#for i in range(len(imgs)):
#    with open(os.path.join(os.getcwd(), 'test{}.jpg'.format(str(i))), 'wb') as f:
#            f.write(requests.get(imgs[i]['src']).content)

#for i in text.translation:
#	with open)os.path.join(os.getcwd(), 'test_trans.txt'), "a+") as t:
#		t.write(i + "\r\n")

#for i in text.text[:5]:
#	with open)os.path.join(os.getcwd(), 'test_text.txt'), "a+") as t:
#		t.write(i + "\r\n")