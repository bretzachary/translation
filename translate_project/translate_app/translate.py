import requests
from bs4 import BeautifulSoup as BS
from google.cloud import translate
import os

#url = 'https://www.nytimes.com/2017/08/24/technology/coding-boot-camps-close.html'
#path = os.path.join(os.getcwd(), 'google.json')
#os.environ['GOOGLE_APPLICATION_CREDENTIALS']=path

#translate_client = translate.Client()
#translation = translate_client.translate(text, target_language='es')

class r_s:

	url = 'https://www.nytimes.com/2017/08/24/technology/coding-boot-camps-close.html'
	path = os.path.join(os.getcwd(), 'google.json')
	os.environ['GOOGLE_APPLICATION_CREDENTIALS']=path

	def __init__(self,text='hello', url = url):
		self.url = urlfr
		self.text = text
		self.is_translated = False

	def request_soup(self):
		r = requests.get(self.url)
		soup = BS(r.text, 'html.parser')
		text = soup.find_all('p')
		self.text = [i.text for i in text]
		self.is_translated = True
		return self.text

	def translate_text(self, target_language='es'):
		#if not(self.is_translated):
		#	self.request_soup()
		translate_client = translate.Client()
		translation = translate_client.translate(self.text, target_language=target_language)
		#translation = [para['translatedText'] for para in translation]
		self.translation = translation
		return self.translation