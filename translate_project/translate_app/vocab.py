import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'translate_project.settings') 
import django
django.setup()

import sys
import json
from translate_app.models import ArticleWords, Article
from random import sample
from ngrams import *

def update_common_words(article):
	words_container = []

	#article = Article.objects.get(pk=article)
	#maybe should throw error if not every article has associated ArticleWords
	#or even better create that model object(row) when create article
	articlewords = ArticleWords.objects.get_or_create(article=article)[0]

	text = json.decoder.JSONDecoder().decode(article.translated_text)

	for para in text:
		words_container.append(para)
	words_container=' '.join(words_container)
	unique_words_in_article = set(find_ngrams(words_container,1))
	unique_words_in_article = ' '.join(unique_words_in_article)

	articlewords.all_words = json.dumps(unique_words_in_article)
	articlewords.save()

	return articlewords


def views_bit(article):
	#to generate word_list for context_dict
	unique_words_in_article = json.decoder.JSONDecoder().decode(article.articlewords.all_words)
	unique_words_in_article = set(find_ngrams(unique_words_in_article,1))

	with open('_800_most_common_words.txt', encoding='utf-8') as doc:
		most_common_words = set([line.strip() for line in doc]) #taking set because of a few duplicates

	#common_words(_in_article gets saved/retrieved in/from model
	#so it's precomupted (vs generated anew each time)
	common_words_in_article=set(unique_words_in_article & most_common_words)

	#this part goes in view, to be included in context_dict
	word_sample = sample(common_words_in_article, 20)

	print(word_sample)

	#in view: vocab = views_bit(article)
	#context_dict[vocab] = vocab
	return word_sample

if __name__ == "__main__":
	article_pk = sys.argv[1]
	article = Article.objects.get(pk=article_pk)
	update_common_words(article)
	print("updated vocab list for: " + str(article))

	### create command line options for one article, multiple articles, and all articles
	### 'all' articles will be part of routine?

	#update_common_words()
	#arg = sys.argv[1]
	#if not arg:
	#	raise:
	#else:
	#	if arg = 'all':
	#		update_common_words(*arg)
	#	else:
	#		update_common_words(article)